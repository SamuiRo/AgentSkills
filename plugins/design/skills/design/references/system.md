# The system: tokens, roles, scales

How to set up or extend a design system so that decisions are made once and
reused, instead of re-made by eye in every component. Read when a project has
no tokens yet, or when a value you need does not exist.

The one rule underneath everything here:

> **Every colour, size, spacing, font, radius, shadow and duration resolves to
> a named step. No ad hoc values.**

Sixty-nine distinct font sizes in a codebase, sixteen of them between 9 and
13px, is what happens without a scale — nobody can see the difference between
0.64rem and 0.66rem, but everybody can see that nothing lines up.

Applies beyond CSS: a slide master's theme colours and text styles, a design
tool's styles and variables, a desktop framework's resource dictionaries.

## Colour

### Name by role, not by hue

```
--ground        page background
--surface       panel, card, row
--surface-2     nested, hovered, selected base
--border        seams and structural rules
--text          primary text on ground
--text-muted    secondary text
--primary       primary action, selection, brand identity
--accent        controlled secondary emphasis
--on-primary    text or glyph on a primary/accent/state fill
--danger  --warning  --success  --info
```

A role name says what the colour is *for*, so a component never has to decide
which purple. `--on-primary` is a role, not "white": text on a saturated fill
usually needs a different value from text on the page ground.

### One colour, one meaning

- **Brand colours carry no semantic state.** If the accent is coral and
  danger is red, the accent never appears on a destructive control, and the
  primary never stands in for success. A product where one colour means both
  "main action" and "danger" teaches the reader neither.
- **Danger is not communicated by hue alone.** A destructive action is
  recognised by three things together: the danger colour, an explicit
  confirmation, and never being the visually dominant button. Swapping a hex
  without the other two changes nothing.
- An alias is fine where two roles genuinely coincide (`--info: var(--primary)`).
  Do not invent a colour for table symmetry.
- Each fill colour that takes hover and press states has its darker/lighter
  step as a token too, or raw hex will creep into states.

### Contrast is checked per pair

List the text/background pairs the design actually uses and check each:
4.5:1 for body text, 3:1 for large text, UI components and focus indicators.
Some brand pairs will fail for small text (a warm accent on a light ground can
sit near 1.5:1) — write down where that pair is forbidden.

### Surfaces and alpha

If panels sit over a background (an image, a canvas, an ambient field), their
translucency is a token too — a handful of steps (`--surface-over`,
`--surface-quiet`, `--scrim`, `--scrim-strong`), not nineteen hand-mixed
`rgba()` values picked by eye.

## Typography

### Roles, not families

Family tokens (`--font-sans`, `--font-mono`) offer exactly one axis — normal
versus technical — so every time text needs to read as secondary, the only
lever is "make it technical". That is how products end up with monospace
uppercase labels as their default texture. Use role tokens:

| Role | Carries |
|---|---|
| Display | large page titles, statements, identity moments |
| Interface | navigation, buttons, inputs, headings in UI, forms — the core layer |
| Reading | longer descriptions and prose |
| System | IDs, timestamps, compact status labels — needs tabular figures |
| Code | real code, secrets, IDs where character alignment matters |

Components name roles only. Which family answers a role is decided once, in
the token layer; changing it later is a handful of lines, not hundreds.

The system role does not have to be monospace. It needs tabular figures,
unambiguous `0 O 1 I l`, and compactness — not fixed advance width. Keep real
monospace for the few places character alignment matters.

> Text becoming technical in tone is not a reason to switch it to monospace.
> System type is not a synonym for "secondary".

### Choosing a typeface

Measure, do not assume:

- **Script coverage for every language the product ships.** Many popular
  families have zero Cyrillic, Greek or Vietnamese glyphs; the interface then
  silently renders in the OS fallback, and in exported images the fallback is
  baked in. Check the actual font files.
- **Tabular figures** (`tnum`) if the product shows numbers in tables, prices,
  timers or stats.
- **Distinguishable `I l 1 | 0 O`** in interface and system roles.
- **The weights you actually need**, and their cost if served as static files.
- **Pairing** — two families should agree in x-height and proportions, or
  differ decisively. A family with separate display and text cuts avoids the
  problem.
- **Licence** for the use (web, app embedding, print).

Test candidates on real components in every script, not on a specimen page.
Record rejected candidates with the reason, so nobody re-opens them.

Expressive faces belong where type is content the user is designing with
(a card editor, a poster tool), not in interface chrome.

### Scale

A named ladder, by size, not by element:

```
--text-xs  --text-sm  --text-base  --text-md  --text-lg  --text-xl ...
```

Heading sizes are roles that point at ladder steps
(`--text-h1: var(--text-3xl)`), and usually only two distinctions are real:
a routine page heading and a feature/area heading. Nine different H1 sizes
across a product is drift, not hierarchy.

`clamp()` and viewport units generate every intermediate size, which is what a
ladder exists to prevent. Use them only for display type whose job is to be a
shape filling a band; both bounds should be ladder steps. A `clamp()` that
rests on its bounds through most real widths is two steps and a breakpoint,
said less honestly.

Tracking: one token for uppercase labels is usually enough. Negative tracking
on large display type is size-dependent and stays next to its size.

## Spacing

A base unit (4 or 8px) and a ladder. Spacing between groups larger than
spacing within them — proximity is a grouping tool before any container is.

## Shape

One shape language, chosen in the direction: radius, chamfer, or square.

- As a scale of steps, applied **by role** — controls, panels, signal
  objects, media — not one value on everything.
- Avatars and genuinely circular objects are circles; that is not a radius
  decision.
- Whatever the shape, it must not become the new reflex. If every object has
  the signature corner, the corner stops meaning anything.

## Elevation

If the direction uses shadows, define a small elevation scale with one light
source and consistent offsets, tied to what is actually above what (menu over
page, dialog over scrim). Otherwise build depth from surface steps, contrast
and occlusion.

## Motion

Two or three duration tokens and one or two easings. Signature motion
mechanics are components, not copy-pasted keyframes. Reduced-motion behaviour
is part of each token's definition, not an afterthought.

## Breakpoints and layers

A named breakpoint ladder; no ad hoc media queries. A named z-index ladder
(base, raised, overlay, modal, nav, toast); no `z-index: 9999`. Fixed
dimensions that several places depend on (header height, rail width) are
tokens.

## Voices

Interface text speaks in distinct voices that do not mix arbitrarily:

| Voice | Use | Form |
|---|---|---|
| Human | the default: headings, labels, buttons, errors, empty states | interface type, sentence case |
| System | system context and instrumentation, scarce | system type, often uppercase |
| Metadata | real identifiers — IDs, receipts, timestamps | system or code type, **case preserved** |
| Interruption | a blocked flow addressing the user directly | human, direct, short |

> Keep human language human. Machine language may look machine-made. The
> distinction must be visible.

A label above a heading that reads "Account security" is human text — not
mono, not uppercase, not prefixed. An ordinary form does not speak like
instrumentation to gain character.

Whether buttons and badges are uppercase is a direction decision; record it
so it is not "fixed" later.

## Shared voice definitions

When a role repeats — a small label, a metadata line — define it once (a
mixin, a utility, a text style) and include it. A hundred local
`__eyebrow`, `__tag`, `__kicker`, `__meta` classes each re-deciding the same
font, size, case and tracking is how a voice drifts 0.66px at a time.

## Deprecations

Name what was removed and why, in the system docs, so it is not reintroduced:
a removed utility, a banned pattern, a rejected typeface. A rule that loses
its reason gets undone by the next session.
