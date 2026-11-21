---
name: docs-and-versioning
description: >-
  Sets up and maintains a role-based docs/ directory (HANDOFF, ROADMAP,
  CHANGELOG, ARCHITECTURE, decisions, guides, features, archive) plus a
  client-observability-driven versioning discipline (patch/minor/major,
  keeping manifests and the changelog in sync, updating the contract doc in
  the same commit as a breaking or additive change) for any software
  project, any language or framework. Use whenever the user sets up or
  reorganizes project documentation, writes or fixes a CLAUDE.md/onboarding
  doc, decides where information belongs, writes a HANDOFF/session-log or
  CHANGELOG entry, decides if a change is patch/minor/major or "counts as
  breaking", records an architecture decision, or starts a new repo wanting
  doc conventions from day one — even without saying "documentation" or
  "versioning". Also check this skill, unprompted, before finalizing any
  commit that bumps a version or changes a public contract in a repo already
  using this structure.
---

# Docs and versioning

A codebase's documentation decays for a boring reason: nobody knows where new
information belongs, so it goes into whichever file is already open. Six
months later there's one 1500-line file that is somehow both the onboarding
doc, the architecture reference, and the backlog, and nobody trusts it enough
to read it or update it. This skill exists to prevent that by giving every
piece of project knowledge exactly one legitimate home, and by tying version
numbers to something concrete — what a consumer of this code can observe —
instead of to a feeling.

This is a **behavioral** skill: there is no script that produces good
documentation for you. Read the structure below, apply it to the project
you're actually in (scaling it down for a small project, see
[Scaling to project size](#scaling-to-project-size)), and hold to it as you
work rather than treating it as a one-time setup task.

## The docs/ structure

Every document has exactly **one** role, and the directory name says what it
is:

```
docs/
├── README.md              — index: lists every doc below with a one-line hook
├── project/
│   ├── HANDOFF.md          — current state + next steps, read in full every session
│   ├── ROADMAP.md          — backlog: open items, planned work, known debt
│   ├── CHANGELOG.md        — per-version record of what changed and why
│   └── ARCHITECTURE.md     — design, schema, trade-offs, "what not to break"
├── decisions/              — one file per significant decision, with reasoning
├── guides/                 — how to do a recurring task in this repo
├── features/               — the contract, as an external consumer sees it
└── archive/                — finished initiatives, kept for their reasoning
```

**Why split it this way, specifically:** each role answers a different
question, and mixing them is what causes bloat.

- **`HANDOFF.md`** answers "where were we, what's next" — it's the file a
  session starts by reading whole, so it must stay short (cap it around
  100 lines; when it's tempted to grow past that, something in it has become
  a decision, an architecture note, or a backlog item and belongs in one of
  those files instead, with just a pointer left behind). It also carries a
  brief session log so the *sequence* of recent work is visible without
  `git log` archaeology.
- **`ROADMAP.md`** answers "what's left to do" — it does not need current
  status or reasoning, just the list and enough context to pick an item up.
- **`CHANGELOG.md`** answers "what shipped and why" — one entry per version,
  written for someone deciding whether upgrading affects them.
- **`ARCHITECTURE.md`** answers "how does this work and what would break if I
  changed it" — schema, data flow, invariants. This is where "why is it built
  this way" lives when the reasoning is still load-bearing for how the whole
  system holds together, as opposed to one bounded choice (see `decisions/`).
- **`decisions/`** answers "why did we choose X over Y" for one bounded
  decision — one file per decision (a lightweight ADR: context, decision,
  consequences, date). This is what stops a decision from being re-litigated
  by someone who wasn't there and doesn't know it was already tried and
  rejected. Written once, rarely edited again.
- **`guides/`** answers "how do I do task X in this repo" — adding a new
  module, running a migration, the code-style contract. Task-shaped, not
  status-shaped.
- **`features/`** answers "how does an external consumer use this" — the
  contract as seen from outside: API shape, request/response, client-visible
  behavior. If this project is a library, service, or backend with any
  caller, this is the file that caller's documentation should point at.
- **`archive/`** holds finished, dated write-ups — a completed migration, a
  resolved incident, a plan that was executed. Keep it; a decision's reasoning
  has real value later when someone claims "we never considered X" and the
  archive shows otherwise. It is deliberately out of the newcomer's reading
  path — nobody should have to read archive/ to understand current state.

Every file under `docs/` (except `docs/README.md` itself) opens with a role
banner as one of its first few lines:

```
> **Role:** <what question this file answers> · **Audience:** <who reads it>
```

The banner isn't decoration — it's what lets you (or a lint check, see
[Structural self-checks](#structural-self-checks)) catch a file that has
drifted from its stated role before it turns into the next 1500-line
grab-bag. `docs/README.md` must list every file under `docs/` with a
one-line description; a file that exists but isn't indexed is exactly how
docs go stale unnoticed — nobody finds it, so nobody updates it, so it starts
lying.

Reference templates for each file type are in `templates/` next to this
skill: `docs-README.md`, `HANDOFF.md`, `ARCHITECTURE.md`, `CHANGELOG.md`,
`ROADMAP.md`, `decision.md`, `guide.md`, `feature.md`. Copy the one you need
rather than writing a role's file from scratch.

## Scaling to project size

Don't cargo-cult the full tree onto a 200-line script. A project earns a
directory when it would actually hold something:

- **Small / early project:** `docs/README.md` + `docs/project/HANDOFF.md` +
  `docs/project/ARCHITECTURE.md` is enough. Skip `decisions/`, `guides/`,
  `features/`, `archive/` until there's a real decision worth recording, a
  task worth documenting, an external consumer, or a finished initiative
  worth keeping.
- **Growing project:** add `decisions/` the first time someone would
  otherwise ask "wait, didn't we already decide this?" Add `guides/` the
  first time the same "how do I..." gets explained twice. Add `features/`
  the moment another codebase (a frontend, another service, an SDK) starts
  depending on this one's contract.
- **Multi-repo project:** see
  [Cross-repo contract awareness](#cross-repo-contract-awareness) below.

The one rule that doesn't scale down: even a two-file setup keeps `HANDOFF.md`
short and keeps the role split. A tiny project with one bloated file has the
exact same failure mode as a big one, just sooner.

## Reading order and context budget

When you (or the next session) start work on a project using this structure,
read `docs/project/HANDOFF.md` in full first — it's short by design and
tells you where things stand. Then route further reading by *question type*
using the table in `docs/README.md`, rather than grepping across everything.
Going straight to the file that owns the answer is faster and more reliable
than search, because search surfaces whichever file happens to mention a
keyword, not the file whose actual job is to answer the question.

Large generated or historical files — a long changelog, archived docs, a big
data file, a lockfile — should be grepped or queried for the specific term
you need, never read in full. Read the whole file only for `HANDOFF.md`,
where its short length is the point.

## Versioning discipline

Define patch/minor/major by what a **consumer can observe**, not by which
files changed:

| Bump | When | The test |
|---|---|---|
| patch | docs, tests, refactors, internal tooling, logging | a consumer of this code cannot tell the difference from outside |
| minor | new capability that doesn't change existing behavior (new endpoint/field/export/error code, an additive/expand-only migration) | existing callers keep working exactly as before |
| major | anything an existing caller could break on (removed/renamed field or endpoint, changed response shape or status, changed auth/session semantics, a non-expand migration) | an existing integration could break without changing its own code |

A schema migration is **never** a patch — even one that "just" adds a
nullable column touches how the system evolves under concurrent
deployments, which is squarely something a careful consumer needs to know
about.

**One change = one commit**, and that one commit carries all of:
1. the version bump, in **every** manifest that declares it (an app's
   package manifest *and* its lockfile if the ecosystem has one — a language
   package manager, a lockfile, a `VERSION` file, whatever this project
   actually uses; check for drift between them, since a bump that only
   touches one is a common and easy-to-miss mistake),
2. a regression test that would have failed before the fix (write it, then
   verify it actually fails on the pre-fix code — a test that would have
   passed either way proves nothing),
3. the documentation update the bump implies (see next paragraph).

A version bump is, by the definition above, something a consumer can
observe — so **a minor or major bump must update whatever file is this
project's contract-facing doc** (its `docs/features/` file, an OpenAPI spec,
a public README, whatever plays that role here) in the *same* commit as the
bump. Treat "I'll update the docs after" as a signal the bump and the doc
update should just be one commit, because they're one change. A patch, by
definition, can't be observed by a consumer, so it needs no contract-doc
edit — don't manufacture doc churn for internal-only changes.

## Match the check to what changed

A change-set where every touched file is under `docs/` (or is a root-level
doc like a top-level README) does not need this project's full test/lint/type
suite before committing. Running and compiling code nobody edited proves
nothing about a wording fix, and paying the full suite's cost — which is
often the majority of a session's time on a large project — for a change
that couldn't have broken any of it just trains everyone, human or AI, to
start skipping checks altogether.

That does **not** mean a docs-only change gets no check at all — it means it
gets the *right* one:

- If this project already has a lighter check path for docs-only changes
  (a `docs`-flavored script, a subset of its CI, a `--docs-only` flag),
  use that instead of the full suite.
- If it doesn't yet, that's exactly what the
  [structural self-checks](#structural-self-checks) below are for — wire
  them in as this project's docs-only check rather than reaching for the
  full suite by default.
- The structural checks still have to actually run. "Docs-only" is a reason
  to skip compiling and testing source code, not a reason to skip verifying
  the docs themselves — a docs-only change-set is precisely the kind of
  change that produces a dangling relative link or an unindexed file, and
  skipping the check because "it's just docs" is how that ships unnoticed.

Decide "docs-only" from what the change-set actually touches, not from what
it was intended to do: if anything under a source, test, config, or tooling
directory changed — even one line, even something that looks trivial like a
one-line script addition — treat it as a code change and run the full suite.
A change that touches both code and docs also takes the full suite; the
docs-only path is only for change-sets where code genuinely could not have
been affected.

## Cross-repo contract awareness

When a project has a sibling that consumes it — a frontend calling this
backend's API, a downstream service importing this library — the
**producing** repo's `docs/features/` is the source of truth for that
contract, and the consuming repo should hold only a pointer to it, never a
copy. Copying documentation across repos drifts silently: nothing fails
loudly when the copy goes stale, so it just quietly becomes wrong until
someone is misled by it. If you're working in the consumer and need to
describe the contract, point at the producer's doc by reference (a link, a
version pin) instead of restating it.

## Structural self-checks

Discipline alone doesn't hold over months and multiple contributors — the
same way tests exist because "I'll remember to check" doesn't scale, doc rot
needs something mechanical catching it. Two starting scripts are bundled
with this skill in `scripts/`:

- **`check_docs_structure.py`** — walks `docs/`, and flags: a file missing
  its role banner, a file that exists but isn't linked from
  `docs/README.md`, a relative markdown link that doesn't resolve, and
  `docs/project/HANDOFF.md` going over its line cap.
- **`check_version_bump.py`** — looks for this project's version
  manifest(s) (autodetects common ones: `package.json`, `pyproject.toml`,
  `Cargo.toml`, `composer.json`, `go.mod`, a bare `VERSION` file) and checks
  whether the current version has a matching `docs/project/CHANGELOG.md`
  entry, and whether a manifest/lockfile pair moved together in the current
  git diff.

Run them with `python scripts/check_docs_structure.py [docs_dir]` and
`python scripts/check_version_bump.py [--base <git-ref>]`. Both are
deliberately simple and dependency-free — adapt them into whatever this
project already uses for CI (a test file, a lint step, a pre-commit hook)
rather than treating them as a separate tool to remember to run. The point
isn't these exact scripts; it's that a bump missing a changelog entry, or a
doc no one links to, should fail something automatically instead of waiting
to be noticed by a human months later.

## Bootstrapping a project that has none of this yet

1. **Look before you scaffold.** Check for existing scattered docs (a big
   README, a NOTES.md, wiki pages, comments-as-documentation) — don't
   silently create parallel structure. Read what's there so nothing gets
   lost.
2. **Create the skeleton sized to the project** (see
   [Scaling to project size](#scaling-to-project-size)), using the templates
   in `templates/`.
3. **Sort existing content by the question it answers**, not by which file
   it currently lives in: current status and next steps → `HANDOFF.md`;
   backlog items → `ROADMAP.md`; design rationale that's still load-bearing
   → `ARCHITECTURE.md`; a decision that was made and argued about → a new
   file in `decisions/`; a finished write-up (a completed migration plan, a
   past incident report) → `archive/`, dated.
4. **Write `docs/README.md` last**, once you know what actually exists, and
   list every file with a one-line hook.
5. **Point the project's entry-point instructions at it** — if this project
   has (or should have) a root instruction file for an AI collaborator (a
   `CLAUDE.md`, `AGENTS.md`, or equivalent), it should say "read
   `docs/project/HANDOFF.md` first" and give the routing table from
   `docs/README.md`, not restate the docs themselves.
6. Don't retro-write a changelog history you don't actually know — start
   `CHANGELOG.md` from the current version forward, and note in it that
   earlier history predates the changelog if that matters to a reader.

## Before you commit, in a project using this structure

A short checklist worth actually running through, not just knowing about:

- Is every touched file under `docs/` (or a root-level doc)? If so, this is
  a docs-only change-set — run the docs-only check path (see
  [Match the check to what changed](#match-the-check-to-what-changed)), not
  the full suite.
- Does this change move a version? If yes: which bump, and does every
  manifest agree?
- If it's a minor/major bump, did the contract-facing doc change in this
  same commit?
- Did new project knowledge land in the file whose *role* it matches, or
  in whichever file was already open?
- Did anything get long enough, or drift far enough from its banner, that it
  should split instead of grow?
- Would `docs/README.md` still be an accurate map after this commit?
