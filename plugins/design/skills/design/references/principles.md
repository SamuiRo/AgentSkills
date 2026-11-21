# Principles

The reasoning behind the procedure. Read when a situation has no written rule
— derive from here rather than inventing a motif.

## 1. The role test

Almost nothing is an anti-pattern by category. Things become anti-patterns
**without a role**. A gradient is bad with arbitrary saturation and no
compositional purpose, not because it is a gradient. A shadow is a normal
elevation primitive, and bad as decoration with no logic of light. Neon,
pastel, purple, rounded corners, a popular typeface, hover feedback — none of
these is a defect on its own.

This matters more than it sounds. A long list of "no X" rules teaches one
strategy — avoidance — and avoidance produces cautious design. **Cautious
design is exactly the inoffensive default Rule zero exists to prevent.** That
is why this skill has few bans and many tests.

Before adding any visible treatment:

1. What does it communicate?
2. Is that already clear without it?
3. Is it an established element of this direction, and does its meaning match
   here?
4. What intensity tier is this element?
5. Is there a quieter solution — content, hierarchy, spacing, type, contrast,
   geometry — not yet tried?
6. Is the same treatment already used elsewhere in the view?
7. Will it compete with a more important signal?
8. Does it improve understanding or interaction, or only make the thing look
   more designed?

Communicates nothing and is not established identity → do not add it.
Communicates something already communicated → stop. Otherwise use the
lowest-intensity solution that works.

### Escalation ladder

Content → typography → spacing → contrast → geometry → surface → colour →
motion → signature motif.

Not a mechanical sequence — a rule against reaching for high-intensity
decoration to solve a structural problem. The first two steps plus mass solve
most screens.

## 2. Attention and intensity

Classify every element and event before designing it.

| Tier | Role | Frequency | Examples | Intensity |
|---|---|---|---|---|
| T0 | Ambient | Persistent | background, shell, structural rules | very low |
| T1 | Utility | Very frequent | buttons, inputs, navigation, tabs | low |
| T2 | Interactive | Regular | cards, panels, selection, routine dialogs | moderate |
| T3 | Signal | Occasional | toasts, meaningful status change | high |
| T4 | Interruption | Rare | security prompt, blocked flow | very high |
| T5 | Critical | Exceptional | irreversible or severe event | maximum |

- **Only one element claims dominant attention at a time.** When a T4/T5
  surface is present, everything else stays alive but restrained.
- A prominent primary CTA is T2 at most. An action does not become an alarm
  because it matters commercially.
- A signature motif's loudest form belongs to the rarest tier. The more often
  something appears, the less it may shout.

## 3. Mass, silhouette and lines

> An object is recognised by its mass and silhouette, not by its outline.

**How mass is built**
- a filled surface that **is** the object, not a background behind a border;
- a real silhouette — the direction's corner treatment, a stepped or offset
  edge, a strong crop;
- enough size and contrast that the shape registers before the content;
- depth from layering and occlusion.

An object without mass has no identity of its own, so identity gets printed on
top of it as notation — labels, stripes, badges, icons, prefixes. Most motif
saturation is a symptom of empty objects. **The fix is not to remove the
stripe (that is avoidance again); it is to give the object a form.**

**Where lines are legitimate**
- **Seam between plates.** A grid with `gap: 1px` over a border-coloured
  background, each cell painting its own surface. The line is negative space
  between masses, not an outline around each box. Hover changes the plate's
  fill rather than lighting a border.
- **Structural rule.** A divider under a heading; a table's row boundary.
- **Data boundary.** Cell edges where the grid is the information.

A line drawn around something to make it feel finished is decoration.

**Frame the thing a person acts on, not the area it sits in.** A sidebar, a
hero, a section, a shell — these hold objects. Framing the holder as well is
containment for its own sake, and it stacks: a bordered sidebar holding a
bordered list holding bordered chips. One level of nesting is normal — a badge
inside a card. Three is a habit.

**Before adding a divider, count the separators already there.** Vertical
space, a change of type size and a heading are three; a line is a fourth.

**A divider lives in the coordinate system of what it divides.** A full-width
rule on a page whose content holds a measure makes two claims about the page's
width at once.

## 4. Composition

**Hierarchy first.** Visual weight follows semantic weight. Equal visual
treatment is correct only for genuine peers: five tools of one product are
peers; three products with two, one and zero shipped features are not — that
is a hierarchy problem wearing a grid.

**Typography and placement before containers.** Strong type against solid
surfaces needs very little else.

**Width follows the content's job.** The test: would more width show more, or
only stretch the same thing?
- *Working surfaces* — grids, tables, editors, dashboards, lists — use the
  width. Capping them at a "safe" 1120px wastes half a large monitor and makes
  people scroll through a grid that would have fit. That cap is the same reflex
  as the inoffensive default: chosen to be harmless, not useful.
- *Reading surfaces* — prose, forms, statements — hold a measure of ~60–75
  characters.
- A full-bleed shell still bounds its own prose.

**Density is a decision, not a risk.** Dense is fine when hierarchy is clear,
targets are usable and information can be scanned. Generous whitespace is not
automatically "considered".

**Asymmetry needs two edges.** A block pinned at a small fixed inset with no
right-hand boundary does not read as deliberately off-centre; it reads as
pinned. Give the page a measure and a margin that scales with it, then place
content off-centre inside that.

**Layouts outlive their content.** When a column or block is removed, the grid
track reserved for it often is not. Emptiness that looks like a design problem
is often a structural leftover — measure the boxes before restyling them.

**Grids follow content, not the other way round.** Bento, three cards in a
row, a 2×2 — right when the content has that shape, wrong when content was
bent to fit.

**Background changes with context, not for rhythm.** Alternating section
backgrounds to "create rhythm" makes a page read as a stack of components.
Change the surface when the role of the content changes.

**Responsive is a rehierarchy, not a compression.** On a narrow screen,
reconsider what comes first, what collapses, what navigation becomes. Use the
project's breakpoint ladder; no ad hoc values.

**A shared layout is a component.** When two screens share a layout, extract
it **including its breakpoints**, and verify by rendering both at every
breakpoint — a jump nobody sees at desktop width is still a jump.

## 5. States

States mean different things and must not share one treatment.

- **Rest** — the quietest valid intensity.
- **Hover** — *this can be acted on.* Must not look like selection.
- **Pressed** — immediate, perceptible acknowledgement.
- **Selected** — persistent, still distinguishable after the pointer leaves;
  stable contrast, not continuous animation. It belongs in the object (a
  tinted fill), not beside it (a stripe).
- **Focus** — visible and unambiguous on every surface, ≥ 3:1 against what is
  around it. Style it; never remove it.
- **Disabled** — loses affordance, stays legible. Not opacity alone if that
  hurts reading.
- **Loading** — match what the system knows. Known structure → a skeleton may
  fit. App start → a loader. A concrete operation → that operation's progress.
  Skeletons are not a universal answer.
- **Empty** — say what would be here and how it gets here.
- **Error** — human, concrete, actionable, next to the thing that failed.

Test with real content: long names, the longest translation, missing images,
huge and zero numbers, wrapping, no data, partial data, no permission.

## 6. Motion

> Every animation answers a question the user is asking right now.

The object the user is acting on stays spatially stable by default; the
system responds around it — a fill, a reveal, a state. Lift and scale on
hover answer no question in business and product design; in a playful
direction they can be part of the voice (see the strong defaults in
`SKILL.md`).

- Entrance animations on every block on scroll are a generated-site signature,
  not a direction.
- Continuous ambient motion stays quiet — its value is being present without
  demanding attention.
- Durations come from a small token set; easing is consistent.
- Every motion has a reduced-motion behaviour that preserves meaning.

## 7. Imagery

- **Real material beats illustration of it.** A real screenshot, product photo
  or work sample is proof; an abstract 3D blob is filler.
- Show each image once per page. A teaser and a reveal show different
  material — a crop, a state, a motion clip — not the same screenshot twice.
- Where imagery should establish presence without competing with information,
  use restraint — silhouette, a tight crop, desaturation. Full-colour artwork
  belongs where the artwork is the subject.
- The frame adapts to the material. Dense UI needs almost no framing; a quiet
  image may take more.
- Placeholders for absent art read as "nothing here yet" — low contrast, not
  decoration.

## 8. External references

References inform principles; they never supply a template. Take *why* a
reference works — its restraint, its information layering, how it handles
type — never its layout, colour system, typography, iconography or ornament.
