---
name: design
description: Base design procedure for any visual output, so the result carries a deliberate direction instead of reading as AI-generated. Covers websites and landing pages, web and desktop app UI, components and stylesheets, dashboards, HTML artifacts, presentations and slides, posters, social and marketing graphics. Use whenever creating, changing, restyling or reviewing anything visual — choosing colour, type, spacing, layout, shape or motion; building a screen, component, deck or graphic; or when asked to make something look better, less generic, less "AI", more on-brand. A project's own design skill or design docs always take precedence; this skill is the base underneath them.
---

# Design

Left to defaults, generated design converges on one look: large rounded
buttons, soft cards, diffuse shadows, a purple gradient, generous empty space,
a centred hero, three feature cards, a fade-up on everything. Each choice is
individually defensible. Together they are the signature of nobody having
decided anything.

This skill is the procedure for deciding. The reasoning lives in
`references/`; read the file you need, not all of them by reflex.

## Precedence

1. **A project design skill** (`.claude/skills/*design*` or similar) — it is
   tuned to one product and always wins. Use this skill only for what it does
   not cover, and never to "correct" it.
2. **The project's own system** — tokens, theme files, design docs, brand
   guidelines, component library, screens the owner has approved.
3. **This skill.**

Never move an approved system toward this skill's defaults. A different look
is not an improvement.

## Rule zero

> The design must not read as the inoffensive default — oversized rounded
> controls, soft cards, diffuse shadows, generous empty space and neutral
> proportions, chosen so as not to offend anyone, afraid to show character.

Character comes from **geometry, density, contrast, asymmetry and typographic
confidence**. It never comes from adding a motif. If something feels weak and
the fix you reach for is a glow, a gradient, a coloured stripe, a badge or an
extra border, the fix is wrong. Go back to hierarchy.

> **Swap test:** could this belong to any other product if the colours were
> swapped? If yes, it has no character yet.

Soft, round and playful are legitimate **directions** — for children, for
cartoon or toy-like brands, for some consumer products. The defect is the
default nobody chose, not the shape.

## Two load-bearing laws

When a situation has no written rule, derive from these rather than inventing
a motif.

**1. Visual intensity is inversely proportional to interaction frequency.**
What the user sees constantly stays quiet; what is rare may be loud. Only one
element claims dominant attention at a time. A persistent element that
demands attention is a defect however good it looks alone.

**2. An object is recognised by its mass and silhouette, not by its outline.**
A rectangle with a 1px border is a rectangle with a line around it. Give an
object a filled surface, a real edge and weight, and it needs no frame. A
coloured side stripe is a degenerate silhouette — two pixels of mass, added
because the object was never given a form.

Lines are legitimate when they separate, align or bound data. A line that is
there to "finish" something is decoration.

## Procedure

Steps 1–4 solve most screens, slides and layouts. If it is right after step 4,
do not proceed to add anything.

**0. Establish the direction.** Find the project's system and follow it. If
the user has their own ideas, take them as given and fill only the gaps. If
there is nothing, do **not** offer a menu of styles: study the product, ask for
references only if the analysis cannot ground a direction, then propose one
direction with its reasoning. → `references/discovery.md`

**1. State the hierarchy in words before drawing.** Primary task, primary
information, supporting information, metadata. Visual weight follows this and
nothing else. Equal treatment only for genuine peers.

**2. Solve it with typography and placement first.** Size, weight, position
and spacing remove most lines and most containers outright. Do not open a
container until a heading and spacing have been tried.

**3. Decide the format by the content's job.** Where people *work*, use the
space — full width, density, more columns. Where people *read*, hold a measure
(~60–75 characters). Slides and graphics: decide what is seen first, from how
far and at what size.

**4. Give objects mass, not outlines.** If something must read as a discrete
object, give it a filled surface and a real edge. Frame the thing a person acts
on, not the area it sits in. Butt neighbours together with a seam instead of
framing each one.

**5. Classify the intensity.** Ambient → utility → interactive → signal →
interruption → critical. Only one element is dominant. A commercially
important CTA is not an alarm.

**6. Use only primitives that carry meaning here.** Each signature element
(an accent, a motif, a shape, a notation) has one meaning. Used outside it, it
spends the meaning it had. Never stack motifs to make something feel on-brand.

**7. Design the states and the real content.** Loading, empty, error,
disabled, focus, selected, partial data, no permission. Then test with real
content: long names, translations, missing images, large numbers, wrapping.

**8. Verify.** Render and look at it; run the gate; run the review.
→ "Verify" below.

## Hard bans

Wrong regardless of direction:

| Ban | Why |
|---|---|
| Fabricated proof — testimonials, metrics, logos, client lists, awards, team, screenshots, statuses | A trust problem, not a style problem |
| Technical theatre — invented codes, telemetry, logs, hex, coordinates, `SYS.024` as atmosphere | A technical-looking string must be a real value the system knows |
| Emoji or ✨ as a substitute for designed iconography | Emoji in user content is fine; as interface icons it replaces a decision |
| The design system's principles as on-screen copy ("Not another template", "Signal > noise") | A product announcing it is not generic is making the most generic move available |
| A status that never varies within its list, or that contradicts its affordance | "Soon" on a working link is a lie the component tells; the reader believes the link |
| One colour with two contradictory meanings (brand accent *and* danger) | The reader cannot learn either |
| Invisible focus, or motion with no reduced-motion behaviour | Accessibility is not a style choice |
| Text or controls below legible contrast (4.5:1 body, 3:1 large text, UI parts and focus) | Unreadable is not a direction |

## Strong defaults

Depart from these only when the agreed direction says so, and say why in it.

- **Interaction feedback through fill, colour, state or reveal — not lift or
  scale.** In business, product and editorial design, a card that jumps on
  hover answers no question. Playful directions (children, cartoon, games,
  toy-like brands) may move objects; then motion is part of the direction:
  consistent across the product, still tied to an interaction, and still
  honouring reduced motion.
- **Depth from layering, contrast and occlusion, not glow, blur or diffuse
  shadow.** A direction may define an elevation scale with a consistent light
  logic; a shadow added "to make it pop" has none.
- **Shape is a token, not a reflex.** One shape language — radius, chamfer or
  square — chosen and applied by role. A 16px radius on everything is not a
  shape language.
- **No coloured side stripe** to mark emphasis, selection or kind. Tint the
  object's own surface or give it a shape.
- **Containers only for objects.** No frame around a region that already
  groups by fill and spacing; no frame inside a frame inside a frame.
- **Human text in a human voice** — sentence case, interface type.
  Uppercase-mono micro labels are a scarce system voice, not the default
  texture of "secondary".

## Budgets

Countable, per screen, slide or composition at rest. Count them.

| | Budget |
|---|---|
| Dominant element | **1** |
| Each signature motif | set in the direction; default **1** |
| Repeated per-item decoration (an index or mark on every card) | hover/focus only, or none |
| Pulsing or continuously animated attention element | **1** |
| Fabricated technical strings | **0** |
| The same information twice in one view, or in two notations | **0** |

## Motion

> Every animation answers a question the user is asking right now. No
> question, no animation.

| Question | Response |
|---|---|
| Can I interact with this? | hover / focus state |
| Did it register my input? | press feedback |
| Is something happening? | progress, loading |
| Where did it go, where did it come from? | transition |
| Is the system alive? | restrained ambient motion |

A fade-up on every section on scroll answers none of these. Every motion has a
`prefers-reduced-motion` behaviour that keeps meaning and navigation intact.

## Verify

**Render and look.** Never declare design verified from code: hierarchy, crop,
line breaks and density only exist in a render.

- Web: 390 and 1440 px, plus 320 and 2560 when relevant; long strings in every
  language; focus on every surface; reduced motion; no horizontal overflow.
- Desktop app: minimum window size, a large window, system light and dark,
  keyboard-only, high DPI.
- Slides: at presentation size and as a thumbnail grid — is the hierarchy
  visible from the back of the room, and do slides vary by role?
- Graphics: at real display size and as a feed thumbnail.

**Run the gate** on code changes:

```bash
python <this-skill-dir>/scripts/design_gate.py <project-root>
```

It counts the patterns that make UI code read as generated (hover lift, side
stripes, diffuse shadows, glow, gradient text, glass, colour and size
literals, machine-label density, removed focus outlines, missing
reduced-motion…). Most are not bans — they are numbers that must not grow
unnoticed.

- **First run on a project:** the report shows where each count comes from.
  Exclude what is not the product (static mockups, labs, galleries) in
  `.design-gate.json` with the reason, disable checks the agreed direction
  makes meaningless (hover motion in a playful direction), then ask the user
  before writing `--update-baseline` into their repo.
- **After that, your change must not raise a number.** If it must, say why —
  in the direction, or as `design-gate: ignore[check-id] reason` on the line.
- `--list` explains every check; `-v` prints every hit. Read the hits; a count
  is a prompt to look, not a verdict.

**Then the judgement tests no script can make:**

- **Boring screen test.** Take a settings page, a form, a table, a plain text
  slide. Remove artwork and effects. Does it still read as this product? If
  not, fix type, proportion, hierarchy and density — not decoration.
- **Removal test.** Strip every decorative motif from a component. If it
  becomes generic, its structure was never designed; the motifs were carrying
  it.
- **Swap test** (Rule zero).

→ `references/review.md` for the checklist and how to report findings.

## References

| File | Read it when |
|---|---|
| `references/discovery.md` | Starting work in a project, or no direction exists yet |
| `references/principles.md` | Composition, mass, lines, width, density, states, motion — the reasoning behind the procedure |
| `references/fingerprints.md` | What reads as generated in each medium, the role test for each pattern, Bad / Good / Why |
| `references/system.md` | Setting up or extending tokens: colour roles, type roles and font choice, scales, shape, voices |
| `references/media.md` | Medium-specific rules: marketing sites, product UI, desktop apps, presentations, graphics |
| `references/review.md` | Final pass, reviewing someone else's design, classifying feedback |
