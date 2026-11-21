#!/usr/bin/env python3
"""
design_gate.py — count the patterns that make UI code read as generated.

Most of what this counts is not forbidden. A gradient, a shadow, a radius or
an uppercase label can all have a role. What the gate does is make the
numbers visible and stop them from growing unnoticed:

  1. Run it once on a project with --update-baseline. The counts are stored
     in .design-gate.json at the project root.
  2. After that, every run compares against the baseline. A change must not
     raise a number. If it must, move the baseline and say why — or disable
     the check in .design-gate.json when the project's direction makes it
     meaningless (a playful direction that chose hover motion, say).

A number nobody can reproduce is worse than no number, so the gate scans the
whole project, not a hand-picked folder, and skips only build output and
dependencies.

    python design_gate.py [root] [-v] [--update-baseline] [--only ids]
                          [--disable ids] [--list] [--json] [--strict]

Silencing one line, with the reason next to it:

    transform: scale(1.1); /* design-gate: ignore[hover-motion] mascot wiggle */

`design-gate: ignore` without a list silences every check on that line; on
its own line it applies to the next line.

.design-gate.json:

    {
      "disable": { "hover-motion": "playful direction, see DESIGN.md" },
      "exclude": { "docs/mockups/**": "static prototypes, not the product",
                   "**/*.stories.*": "component gallery" },
      "baseline": { "side-stripe": 3, ... }
    }

Standard library only; Python 3.8+.
"""

from __future__ import annotations

import argparse
import bisect
import fnmatch
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Iterable

# ─────────────────────────────────────────────
# Scope
# ─────────────────────────────────────────────

STYLE = {".css", ".scss", ".sass", ".less", ".styl", ".pcss", ".postcss"}
# Markup that can hold a <style> block, so CSS checks apply to it too.
STYLED_MARKUP = {".html", ".htm", ".vue", ".svelte", ".astro"}
COMPONENT = {".jsx", ".tsx"}
SCRIPT = {".js", ".mjs", ".cjs", ".ts"}

CSS_FILES = STYLE | STYLED_MARKUP
MARKUP_FILES = STYLED_MARKUP | COMPONENT
# Where utility classes (Tailwind and friends) and inline motion props live.
CLASS_FILES = STYLED_MARKUP | COMPONENT | SCRIPT

ALL_FILES = CSS_FILES | MARKUP_FILES | CLASS_FILES

SKIP_DIRS = {
    "node_modules", ".git", ".hg", ".svn", "dist", "build", "out", ".next",
    ".nuxt", ".svelte-kit", ".astro", ".angular", ".turbo", ".vercel",
    ".output", ".cache", ".parcel-cache", "coverage", "vendor", "venv",
    ".venv", "__pycache__", "target", "bin", "obj", "storybook-static",
    "_archive",
}

MAX_BYTES = 1_000_000  # anything larger is generated or vendored

CONFIG_NAME = ".design-gate.json"

# ─────────────────────────────────────────────
# Files
# ─────────────────────────────────────────────


@dataclass
class Source:
    path: str          # relative, forward slashes
    ext: str
    text: str
    line_starts: list = field(default_factory=list)
    lines: list = field(default_factory=list)

    def __post_init__(self):
        self.lines = self.text.split("\n")
        starts, pos = [], 0
        for line in self.lines:
            starts.append(pos)
            pos += len(line) + 1
        self.line_starts = starts

    def line_of(self, offset: int) -> int:
        """1-based line number of a character offset."""
        return bisect.bisect_right(self.line_starts, offset)


def walk(root: str, exclude: list[str]) -> list[Source]:
    sources = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            ext = os.path.splitext(name)[1].lower()
            if ext not in ALL_FILES or ".min." in name:
                continue
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root).replace("\\", "/")
            if any(fnmatch.fnmatch(rel, pat) for pat in exclude):
                continue
            try:
                if os.path.getsize(full) > MAX_BYTES:
                    continue
                with open(full, encoding="utf-8", errors="replace") as fh:
                    sources.append(Source(rel, ext, fh.read()))
            except OSError:
                continue
    sources.sort(key=lambda s: s.path)
    return sources


# ─────────────────────────────────────────────
# Matching
# ─────────────────────────────────────────────

# `*` opens a comment continuation line, but `* {` and `*::-webkit-scrollbar`
# are selectors — the universal selector is where global overrides live.
COMMENT_LINE = re.compile(r"^\s*(//|/\*|\*/|\*(?=\s|$)(?![^\n]*\{)|<!--|\{/\*)")
IGNORE = re.compile(r"design-gate:\s*ignore(?:\[([^\]]*)\])?")


def ignored(src: Source, line_no: int, check_id: str) -> bool:
    """A comment line is prose about code, not code; an ignore marker is a
    reason written where the exception lives."""
    line = src.lines[line_no - 1]
    if COMMENT_LINE.match(line) and not IGNORE.search(line):
        return True
    candidates = [line]
    if line_no >= 2:
        prev = src.lines[line_no - 2]
        if IGNORE.search(prev) and COMMENT_LINE.match(prev):
            candidates.append(prev)
    for text in candidates:
        m = IGNORE.search(text)
        if m:
            ids = m.group(1)
            if ids is None or check_id in [i.strip() for i in ids.split(",")]:
                return True
    return False


@dataclass
class Hit:
    path: str
    line: int
    text: str
    col: int = 0

    def __str__(self):
        """The line, or on a long (minified) line a window around the hit."""
        text, width = self.text, 140
        if len(text.strip()) <= width:
            return f"{self.path}:{self.line}  {text.strip()}"
        start = max(0, self.col - 40)
        snippet = text[start:start + width].strip()
        prefix = "..." if start > 0 else ""
        suffix = "..." if start + width < len(text) else ""
        return f"{self.path}:{self.line}:{self.col + 1}  {prefix}{snippet}{suffix}"


# A rule is (file extensions, regex, optional predicate on the match).
Rule = tuple  # (set[str], re.Pattern, Callable[[re.Match, Source], bool] | None)


def tw(pattern: str) -> re.Pattern:
    """A utility class, bounded so `hover:scale-105` matches inside
    `md:hover:scale-105` but not inside `myhover:scale-105x`."""
    return re.compile(r"(?<![\w-])" + pattern + r"(?![\w-])")


def css(pattern: str, flags: int = re.IGNORECASE) -> re.Pattern:
    return re.compile(pattern, flags)


# ─────────────────────────────────────────────
# Predicates
# ─────────────────────────────────────────────


def not_custom_property(m: re.Match, src: Source) -> bool:
    """A literal inside a token definition is the token layer doing its job.
    Judged by the declaration the literal sits in, not by the line, so a
    one-line `:root { --brand: #7b5cf0; }` is still a token."""
    pos = m.start("lit") if "lit" in m.re.groupindex else m.start()
    start = max(src.text.rfind(ch, 0, pos) for ch in ";{}\n") + 1
    decl = src.text[start:pos].lstrip()
    return not re.match(r"(--[\w-]+|\$[\w-]+|@[\w-]+)\s*:", decl)


def blur_at_least(n: int):
    """Offset shadows only; a zero-offset shadow is a glow and counted there."""
    def pred(m: re.Match, src: Source) -> bool:
        offset = float(m.group("x")) != 0 or float(m.group("y")) != 0
        return offset and float(m.group("blur")) >= n
    return pred


def moves(func: str, args: str) -> bool:
    """Whether one transform function moves or resizes the object. Not
    counted: scale(1) and translate(0), which return a revealed element to
    rest, and ±50%, which centres an absolutely positioned element."""
    values = [a.strip().lower() for a in re.split(r"[,\s]+", args) if a.strip()]
    if func.startswith("scale"):
        return any(re.sub(r"[^\d.]", "", v) not in ("1", "1.0", "") for v in values)
    return any(not re.fullmatch(r"-?0(px|rem|em|%)?|-?50%", v) for v in values)


def hover_block_moves(m: re.Match, src: Source) -> bool:
    body = m.group("body")
    for decl in re.finditer(r"(?<![\w-])(transform|scale|translate)\s*:\s*([^;]*)", body, re.I):
        prop, value = decl.group(1).lower(), decl.group(2)
        if prop == "transform":
            for fn in re.finditer(r"(scale[XYZ3d]*|translate[XYZ3d]*)\(([^)]*)\)", value, re.I):
                if moves(fn.group(1).lower(), fn.group(2)):
                    return True
        elif moves(prop, value):
            return True
    return False


def large_radius(m: re.Match, src: Source) -> bool:
    value = float(m.group("r"))
    unit = m.group("u").lower()
    px = value * 16 if unit == "rem" else value
    return 16 <= px < 999


def not_in_font_face(m: re.Match, src: Source) -> bool:
    start = m.start()
    for ff in re.finditer(r"@font-face\s*\{[^}]*\}", src.text, re.IGNORECASE):
        if ff.start() <= start < ff.end():
            return False
    return not_custom_property(m, src)


PAGE_SELECTOR = re.compile(r"^(html|body|:root)(::?-webkit-scrollbar[\w-]*)?$", re.I)


def not_page_level(m: re.Match, src: Source) -> bool:
    """The page's own scrollbar is a direction choice; an inner area's is an
    affordance. Judged by the selector of the rule the match sits in."""
    # The `{` that opens the rule: after the match when the match is the
    # selector (`html::-webkit-scrollbar {`), before it when it is a
    # declaration inside the rule (`scrollbar-width: none`).
    if "webkit-scrollbar" in m.group(0):
        brace = src.text.find("{", m.start())
    else:
        brace = src.text.rfind("{", 0, m.start())
    head = src.text[:brace]
    start = max(head.rfind("}"), head.rfind(";"), head.rfind("{")) + 1
    selector = re.sub(r"/\*.*?\*/|//[^\n]*", "", head[start:], flags=re.S)
    selectors = [s.strip() for s in selector.split(",") if s.strip()]
    return not selectors or not all(PAGE_SELECTOR.match(s) for s in selectors)


def not_page_tag(m: re.Match, src: Source) -> bool:
    tag_start = src.text.rfind("<", 0, m.start())
    return not re.match(r"<(html|body)\b", src.text[tag_start:m.start()], re.I)


def file_lacks_focus_visible(m: re.Match, src: Source) -> bool:
    return not re.search(r"focus-visible", src.text)


def uppercase_and_tracked_block(m: re.Match, src: Source) -> bool:
    body = m.group("body")
    # Negative tracking on uppercase is display type, not a label voice.
    return bool(re.search(r"text-transform\s*:\s*uppercase", body, re.I)
                and re.search(r"letter-spacing\s*:\s*(?!-|0[;\s}]|normal)", body, re.I))


def uppercase_and_tracked_classes(m: re.Match, src: Source) -> bool:
    classes = m.group("cls")
    return bool(re.search(r"(?<![\w-])uppercase(?![\w-])", classes)
                and re.search(r"(?<![\w-])tracking-(wide|wider|widest|\[)", classes))


# Emoji used as icons: pictographs, dingbats, sparkles, check marks. The plain
# stars ★ ☆ are left out — "5★" is rating notation, which is content.
EMOJI = re.compile(
    "[\U0001F300-\U0001F5FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF"
    "\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF☀-☄☇-⛿"
    "✀-➿⭐⬆⬇⬅➡]"
)

# ─────────────────────────────────────────────
# Checks
# ─────────────────────────────────────────────


@dataclass
class Check:
    id: str
    kind: str          # tell | drift | a11y
    name: str
    test: str          # the question to ask about each hit
    rules: list
    project: Callable[[list[Source]], list[Hit]] | None = None


CHECKS: list[Check] = [
    Check(
        "hover-motion", "tell", "hover lift or scale",
        "Does moving the object answer a question? Strong default against in "
        "business/product design; disable for a playful direction that chose it.",
        [
            (CSS_FILES, css(r":hover[^{};]*\{(?P<body>[^{}]*)\}"), hover_block_moves),
            (CLASS_FILES, tw(r"(group-)?hover:-?(scale|translate-[xy])-(?!100\b|0\b)[\w\[\].%-]+"), None),
            (CLASS_FILES, css(r"whileHover\s*=\s*\{\{[^}]*\b(scale|y|x)\s*:", 0), None),
        ],
    ),
    Check(
        "side-stripe", "tell", "coloured side stripe",
        "Is a 2px+ edge standing in for a shape? Tint the object's surface or "
        "give it a form. Tab underlines and corner brackets are legitimate.",
        [
            (CSS_FILES, css(r"border-(left|inline-start)(-width)?\s*:\s*[2-9](\.\d+)?px"), None),
            (CSS_FILES, css(r"box-shadow\s*:\s*inset\s+[2-9]px\s+0"), None),
            (CLASS_FILES, tw(r"border-(l|s)-(2|4|8|\[\d+px\])"), None),
        ],
    ),
    Check(
        "diffuse-shadow", "tell", "large diffuse shadow",
        "Is there a light logic and an elevation scale, or is it 'to make it pop'?",
        [
            (CSS_FILES, css(r"box-shadow\s*:\s*(?!inset)[^;{}]*?(?P<x>-?\d+(\.\d+)?)(px)?\s+(?P<y>-?\d+(\.\d+)?)(px)?\s+(?P<blur>\d+(\.\d+)?)px"),
             blur_at_least(16)),
            (CLASS_FILES, tw(r"shadow-(lg|xl|2xl)"), None),
            (CLASS_FILES, tw(r"drop-shadow-(lg|xl|2xl)"), None),
        ],
    ),
    Check(
        "glow", "tell", "glow / coloured shadow",
        "What is emitting light, and why?",
        [
            # Blur of 4px or more; `0 0 0 3px` is a focus ring's spread, not a glow.
            (CSS_FILES, css(r"(box|text)-shadow\s*:\s*0(px)?\s+0(px)?\s+([4-9]|[1-9]\d+)(\.\d+)?(px|rem)"), None),
            (CSS_FILES, css(r"drop-shadow\(\s*0(px)?\s+0(px)?\s+([4-9]|[1-9]\d+)(\.\d+)?(px|rem)"), None),
            (CLASS_FILES, tw(r"shadow-(red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}(/\d+)?"), None),
        ],
    ),
    Check(
        "gradient-text", "tell", "gradient text",
        "Is the gradient on the headline a brand decision, or the generated hero?",
        [
            (CSS_FILES, css(r"background-clip\s*:\s*text"), None),
            (CLASS_FILES, tw(r"bg-clip-text"), None),
        ],
    ),
    Check(
        "gradient", "tell", "gradient",
        "Compositional, brand, state or atmospheric role? Purple/blue/pink "
        "defaults are the generated signature.",
        [
            (CSS_FILES, css(r"(repeating-)?(linear|radial|conic)-gradient\("), not_custom_property),
            (CLASS_FILES, tw(r"bg-(gradient-to-\w+|linear-\w+|radial|conic)"), None),
        ],
    ),
    Check(
        "glass-blur", "tell", "glass / blurred orb",
        "Is there something meaningful behind the glass? Is the blurred shape "
        "carrying information?",
        [
            (CSS_FILES, css(r"backdrop-filter\s*:\s*[^;]*blur"), None),
            (CSS_FILES, css(r"(?<![\w-])filter\s*:\s*[^;]*blur\(\s*([4-9]\d|\d{3,})px"), None),
            (CLASS_FILES, tw(r"backdrop-blur(-\w+)?"), None),
            (CLASS_FILES, tw(r"blur-(2xl|3xl|\[\d{2,}px\])"), None),
        ],
    ),
    Check(
        "soft-radius", "tell", "large radius on objects",
        "Is 16px+ rounding the direction's shape language, or the reflex? "
        "Circles (50%, 9999px) are not counted.",
        [
            (CSS_FILES, css(r"border-radius\s*:\s*(?P<r>\d+(\.\d+)?)(?P<u>px|rem)"), large_radius),
            (CLASS_FILES, tw(r"rounded(-[trblse]{1,2})?-(2xl|3xl|4xl)"), None),
        ],
    ),
    Check(
        "machine-label", "tell", "uppercase tracked label",
        "Machine-voice density. Is each one system context, or human text "
        "dressed as instrumentation (eyebrows, section tags)?",
        [
            (CSS_FILES, css(r"\{(?P<body>[^{}]*)\}"), uppercase_and_tracked_block),
            (CLASS_FILES, css(r"class(Name)?\s*=\s*[\"'{`](?P<cls>[^\"'`]*)", 0), uppercase_and_tracked_classes),
        ],
    ),
    Check(
        "section-number", "tell", "numbered section label",
        "Are sections addressed by number anywhere? If not, the number carries "
        "nothing.",
        [
            (MARKUP_FILES, css(r">\s*(//\s*|#\s*)?0[1-9]\s*(<|[./:—–-]\s)", 0), None),
        ],
    ),
    Check(
        "entrance-stagger", "tell", "fade-up / stagger entrance",
        "What question does the entrance answer? On every block it answers none.",
        [
            (CLASS_FILES | CSS_FILES, css(r"fade-?in-?up|fade-up|fadeUp|stagger-\d|animate-fade|\bstagger\b"), None),
            (CLASS_FILES, css(r"initial\s*=\s*\{\{\s*opacity\s*:\s*0\s*,\s*y\s*:", 0), None),
            (CLASS_FILES, css(r"\bdata-aos\s*=", 0), None),
        ],
    ),
    Check(
        "emoji-icon", "tell", "emoji in markup",
        "Is it user content, or standing in for designed iconography?",
        [
            (MARKUP_FILES, EMOJI, None),
        ],
    ),
    Check(
        "transition-all", "drift", "transition: all",
        "Animate the properties that change, nothing else.",
        [
            (CSS_FILES, css(r"transition(-property)?\s*:\s*all\b"), None),
            (CLASS_FILES, tw(r"transition-all"), None),
        ],
    ),
    Check(
        "colour-literal", "drift", "colour literal outside a token",
        "Does it belong in the token layer with a role name?",
        [
            (CSS_FILES, css(r":\s*[^;{}\n]*?(?P<lit>#[0-9a-fA-F]{3,8}\b|(rgba?|hsla?)\(\s*\d)"), not_custom_property),
            (CLASS_FILES, tw(r"[\w-]+-\[(#[0-9a-fA-F]{3,8}|rgba?\([^\]]*\))\]"), None),
        ],
    ),
    Check(
        "size-literal", "drift", "font size outside the scale",
        "Does it resolve to a step of the type scale? (em and % ratios are "
        "not counted; clamp() is, except on declared display type.)",
        [
            (CSS_FILES, css(r"font-size\s*:\s*(clamp\(|-?[\d.]+\s*(px|rem|pt|vw|vh)\b)"), not_custom_property),
            (CSS_FILES, css(r"(?<![\w-])font\s*:\s*[^;{}]*?\b[\d.]+(px|rem|pt)\b"), not_custom_property),
            (CLASS_FILES, tw(r"text-\[[\d.]+(px|rem|pt)\]"), None),
        ],
    ),
    Check(
        "font-literal", "drift", "font family named outside a token",
        "Components name a type role; the family is decided once.",
        [
            (CSS_FILES, css(r"font-family\s*:\s*(?!\s*(var\(|inherit|initial|unset))"), not_in_font_face),
            (CLASS_FILES, tw(r"font-\['[^\]]+\]"), None),
        ],
    ),
    Check(
        "outline-removed", "a11y", "focus outline removed",
        "Counted only in files with no focus-visible style. Style focus; never "
        "remove it.",
        [
            (CSS_FILES, css(r"outline\s*:\s*(none|0)\b"), file_lacks_focus_visible),
            (CLASS_FILES, tw(r"(focus:)?outline-none"), file_lacks_focus_visible),
        ],
    ),
    Check(
        "hidden-scrollbar", "a11y", "hidden scrollbar on inner areas",
        "Hiding the page scrollbar (html, body, :root) is a direction choice "
        "and is not counted. An inner scroll area — or `*`, which hides them "
        "all — must still show there is more: a cut-off item or an edge fade.",
        [
            (CSS_FILES, css(r"::-webkit-scrollbar[^{]*\{[^}]*display\s*:\s*none"), not_page_level),
            (CSS_FILES, css(r"scrollbar-width\s*:\s*none"), not_page_level),
            (CLASS_FILES, tw(r"(scrollbar-hide|no-scrollbar|scrollbar-none)"), not_page_tag),
        ],
    ),
]

# Movement, not every colour fade: a 150ms colour transition is not what
# vestibular sensitivity is about.
ANIMATION = re.compile(r"@keyframes|animation(-name)?\s*:|(?<![\w-])animate-(?!none)[\w-]+|"
                       r"whileHover|whileInView|gsap\.|scroll-behavior\s*:\s*smooth|"
                       r"transition[^;{}\n]*transform", re.I)
REDUCED = re.compile(r"prefers-reduced-motion|motion-reduce:|motion-safe:|"
                     r"useReducedMotion|reducedMotion", re.I)


def reduced_motion_project(sources: list[Source]) -> list[Hit]:
    """One project-level hit if anything animates and nothing anywhere
    answers prefers-reduced-motion."""
    if any(REDUCED.search(s.text) for s in sources):
        return []
    for s in sources:
        m = ANIMATION.search(s.text)
        if m:
            line = s.line_of(m.start())
            return [Hit(s.path, line,
                        "motion here, and no prefers-reduced-motion handling anywhere in the project")]
    return []


CHECKS.append(Check(
    "reduced-motion", "a11y", "no reduced-motion handling",
    "Every motion needs a prefers-reduced-motion behaviour.",
    [], project=reduced_motion_project,
))

CHECK_BY_ID = {c.id: c for c in CHECKS}

# ─────────────────────────────────────────────
# Running
# ─────────────────────────────────────────────


def run_check(check: Check, sources: list[Source]) -> list[Hit]:
    if check.project:
        return check.project(sources)
    hits, seen = [], set()
    for src in sources:
        for exts, pattern, pred in check.rules:
            if src.ext not in exts:
                continue
            for m in pattern.finditer(src.text):
                if pred and not pred(m, src):
                    continue
                # Point at the decisive declaration, not at the selector.
                anchor = m.start()
                if "body" in pattern.groupindex and m.group("body") is not None:
                    decisive = re.search(r"transform|scale|translate", m.group("body"), re.I)
                    anchor = m.start("body") + (decisive.start() if decisive else 0)
                # Keyed by position, not by line: a minified stylesheet is one
                # line, and every hit on it is still a hit.
                key = (src.path, anchor)
                line = src.line_of(anchor)
                if key in seen or ignored(src, line, check.id):
                    continue
                seen.add(key)
                col = anchor - src.line_starts[line - 1]
                hits.append(Hit(src.path, line, src.lines[line - 1], col))
    hits.sort(key=lambda h: (h.path, h.line, h.col))
    return hits


def where(hits: list[Hit], top: int = 3) -> str:
    """Where the hits are, by their first two path segments. On a first run
    this is what shows that a number belongs to mockups or labs, which
    should be excluded, rather than to the product."""
    counts: dict[str, int] = {}
    for h in hits:
        key = "/".join(h.path.split("/")[:2])
        counts[key] = counts.get(key, 0) + 1
    ranked = sorted(counts.items(), key=lambda kv: -kv[1])
    text = " · ".join(f"{k} {v}" for k, v in ranked[:top])
    if len(ranked) > top:
        text += f" · +{len(ranked) - top} more"
    return text


def load_config(root: str) -> dict:
    path = os.path.join(root, CONFIG_NAME)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save_config(root: str, config: dict) -> None:
    path = os.path.join(root, CONFIG_NAME)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(config, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def ids(value: str | None) -> list[str]:
    if not value:
        return []
    out = [v.strip() for v in value.split(",") if v.strip()]
    unknown = [v for v in out if v not in CHECK_BY_ID]
    if unknown:
        sys.exit(f"unknown check id(s): {', '.join(unknown)} — see --list")
    return out


def list_checks() -> None:
    for c in CHECKS:
        print(f"{c.id:<18} {c.kind:<6} {c.name}")
        print(f"{'':<25} {c.test}\n")


def main(argv: Iterable[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except AttributeError:
            pass

    ap = argparse.ArgumentParser(description="Count the patterns that make UI code read as generated.")
    ap.add_argument("root", nargs="?", default=".", help="project root (default: current directory)")
    ap.add_argument("-v", "--verbose", action="store_true", help="print every hit, not only those over baseline")
    ap.add_argument("--update-baseline", action="store_true", help=f"store current counts in {CONFIG_NAME}")
    ap.add_argument("--only", help="comma-separated check ids to run")
    ap.add_argument("--disable", help="comma-separated check ids to skip (in addition to the config)")
    ap.add_argument("--strict", action="store_true", help="without a baseline, fail on any 'tell' or 'a11y' hit")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--list", action="store_true", help="list checks and the question each one asks")
    args = ap.parse_args(argv)

    if args.list:
        list_checks()
        return 0

    root = os.path.abspath(args.root)
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    config = load_config(root)
    disabled = dict(config.get("disable", {}) or {})
    if isinstance(config.get("disable"), list):
        disabled = {k: "" for k in config["disable"]}
    for d in ids(args.disable):
        disabled.setdefault(d, "--disable")
    only = ids(args.only)
    baseline = config.get("baseline", {}) or {}

    # A list of globs, or {glob: reason} so the reason travels with the rule.
    exclude = config.get("exclude", []) or []
    sources = walk(root, list(exclude))
    active = [c for c in CHECKS if c.id not in disabled and (not only or c.id in only)]
    results = {c.id: run_check(c, sources) for c in active}

    if args.update_baseline:
        new = dict(baseline)
        for cid, hits in results.items():
            new[cid] = len(hits)
        config["baseline"] = dict(sorted(new.items()))
        save_config(root, config)

    has_baseline = bool(baseline) and not args.update_baseline
    over = []
    rows = []
    for c in active:
        n = len(results[c.id])
        base = baseline.get(c.id) if has_baseline else None
        if base is not None and n > base:
            status = f"OVER by {n - base}"
            over.append(c.id)
        elif base is not None:
            status = f"{n}/{base}" if n else "clean"
        else:
            status = str(n) if n else "clean"
            if args.strict and n and c.kind in ("tell", "a11y") and not has_baseline:
                over.append(c.id)
        rows.append((c, n, base, status))

    if args.json:
        print(json.dumps({
            "root": root,
            "files": len(sources),
            "checks": [
                {"id": c.id, "kind": c.kind, "name": c.name, "count": n, "baseline": base,
                 "over": c.id in over, "hits": [str(h) for h in results[c.id]]}
                for c, n, base, _ in rows
            ],
            "disabled": disabled,
        }, indent=2, ensure_ascii=False))
        return 1 if over else 0

    print(f"design gate — {len(sources)} files under {root}\n")
    for kind, title in (("tell", "Generated-look tells"), ("drift", "System drift"), ("a11y", "Accessibility")):
        group = [r for r in rows if r[0].kind == kind]
        if not group:
            continue
        print(f"  {title}")
        for c, n, base, status in group:
            mark = "x" if c.id in over else ("." if n == 0 else "-")
            print(f"   {mark} {c.id:<18} {c.name:<34} {status}")
            hits = results[c.id]
            if hits and (args.verbose or c.id in over):
                for h in hits:
                    print(f"        {h}")
                print(f"        ? {c.test}")
            elif hits:
                print(f"        in {where(hits)}")
        print()

    if disabled:
        print("  Disabled")
        for cid, why in disabled.items():
            print(f"     {cid:<18} {why}")
        print()

    if args.update_baseline:
        print(f"  baseline written to {CONFIG_NAME} — from now on a change must not raise a number")
    elif over:
        print(f"  {len(over)} check(s) above baseline — fix, or move the baseline and say why")
    elif not has_baseline:
        print("  no baseline yet: counts are informational. Review the hits with -v,")
        print("  then run --update-baseline so future changes cannot raise them.")
    else:
        print("  gate clean against baseline")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
