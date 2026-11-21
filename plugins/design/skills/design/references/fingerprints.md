# What reads as generated

Generated design is recognisable not by any single choice but by a cluster of
defaults appearing together, each of them unchosen. This file catalogues the
cluster per medium, gives the test for each pattern, and shows Bad / Good /
Why pairs. The explanation is the point: the goal is transferable reasoning,
not swapping one pattern for another.

Remember the principle from `principles.md`: almost everything here is a
**test**, not a ban. The hard bans are in `SKILL.md`.

## Patterns and their tests

| Pattern | Verdict | The actual test |
|---|---|---|
| Gradients | contextual | Compositional, brand, state or atmospheric role? No banding, text readable? |
| Purple → blue / pink gradient, gradient headline text | strong cliché | Is purple a brand decision, or the model's default "tech" colour? |
| Drop shadows | neutral | Is there a consistent light logic and an elevation scale? Or "to make it pop"? |
| Glow, coloured shadow, neon edge | strong cliché | What is glowing, and why would it emit light? |
| Glassmorphism, backdrop blur everywhere | strong cliché | Is something meaningful behind the glass? Usually it is a blurred blob |
| Blurred radial orbs, gradient mesh, dot or grid backgrounds | strong cliché | Decorative filler with no information |
| Rounded corners | neutral | One chosen radius scale by role, or 16–24px on everything by reflex? |
| Pill buttons, pill badges everywhere | cliché | Is the pill the direction's shape, or the default? |
| Coloured left stripe on cards, alerts, nav items | cliché, and a symptom | A cheap substitute for shape — see `principles.md` §3 |
| A border **and** a shadow **and** a radius on one card | cliché | Three edge treatments for one edge; pick the one with a role |
| Popular typefaces (Inter, Geist, Space Grotesk, Poppins) | neutral | The defect is absence of typographic direction, not the family. Check script coverage |
| Small uppercase tracked label above every heading ("eyebrow") | strong cliché | Does it carry information the heading does not? Usually it repeats it |
| Section numbering 01 / 02 / 03 | strong cliché | Are the sections addressed by number anywhere? If not, the number says nothing |
| Monospace as the texture of "secondary" | cliché | Is the text a code, ID or number that needs fixed width? |
| Icon library icon on every item | cliché | Does the icon say something the word does not? |
| Icon in a tinted rounded square / circle | strong cliché | Same test, plus: is the container doing anything? |
| Checkmark bullets | cliché | Fine for a genuine benefit list, reflexive everywhere else |
| Emoji / ✨ as icons | **banned** as interface iconography | — |
| Three feature cards in a row | strong cliché | Genuinely three peers, or forced to fit? |
| Bento grid | strong cliché | Do content relationships fit it, or was content bent to the grid? |
| Three pricing tiers, middle one "Most popular" | strong cliché | Pricing comes from the business model, not a template |
| Logo strip "Trusted by" | contextual | Real customers with permission? Otherwise **banned** (fabricated proof) |
| Testimonial carousel, avatar stack "Join 2,000+" | contextual | Real people, real quotes? Otherwise **banned** |
| Stats row "10k+ users · 99.9% uptime · 24/7" | contextual | Real, current, sourced? Otherwise **banned** |
| Fake terminal / code window / boot log | cliché | Defensible for a developer product showing real output; otherwise theatre |
| Hover lift / scale | strong default against | See `SKILL.md`. Fine in a playful direction that chose it |
| `transition: all` | drift | Animate the properties that change, nothing else |
| Fade-up / stagger on every block | strong cliché | What question does this answer? |
| Skeleton loaders everywhere | over-generalised | Does the system know the structure of what is loading? |
| Hidden scrollbars | contextual | Hiding the page scrollbar is a direction choice. An inner scroll area (carousel, table, panel, code block) must still show there is more — a visible bar, a cut-off item or an edge fade |
| Everything centred | cliché | Is symmetry a decision, or the absence of one? |
| Same section rhythm repeated (same padding, same heading block, same grid) | strong cliché | Does each section's form follow its content? |
| Alternating section backgrounds | cliché | Did the context change, or only the colour? |
| Dark mode with neon accents as "tech" | cliché | Palette is not identity. Execution is |
| No real product shown | **major problem** | A page that sells an abstraction instead of the product |
| Em dashes, "It's not X, it's Y", "Unlock the power of…" | copy tells | Not a visual pattern, but they travel together — see the copywriting skill |

## The stamped templates

These are the full clusters. If a draft matches one, the structure was filled
in, not designed.

### Landing page

Pill badge "✨ New" → huge centred H1 with one gradient word → grey subtitle →
primary button + ghost button → logo strip → three feature cards with icons in
tinted squares → bento grid → stats row → testimonial carousel → three pricing
tiers → FAQ accordion → gradient CTA band → four-column footer. Every block
fades up on scroll. Blurred purple orb behind the hero.

**What to do instead:** start from the business scenario (`media.md`):
category, value, proof and a path to action in the first view; real work
before self-promotion; every section's form follows its content; sections that
carry nothing are removed, not filled.

### App / dashboard

Left sidebar with an icon on every item and the active item marked with a
coloured stripe → top bar with search, bell and avatar → greeting "Welcome
back, Alex 👋" → row of four KPI cards each with an icon, a big number and a
green "+12%" → a chart card → a "Recent activity" list → every block a
rounded card with a border and a shadow, at max-width 1280px, centred.

**What to do instead:** decide what the user comes here to *do*, and give that
the space and the first position. KPIs only if they vary and drive a decision.
Selection as a filled row. Working surfaces full-width. Trends only when
sourced.

### Page skeleton, repeated

Eyebrow → H1 → paragraph → `01` heading → block → `02` heading → block → `03`
heading. Identical on every page of the product, including the settings page.
This is a form being filled in. Numbered section headers carry no information
when sections are not addressed by number.

### Presentation

Title slide with a gradient and a stock photo → "Agenda" → a title and five
bullets on every slide → three icons in circles with a word under each → the
same layout forty times → a "Thank you! Questions?" slide. Decorative shapes
in two corners of every slide.

### Graphic / social post

Centred headline on a purple-to-blue gradient → glow → floating 3D shapes →
sparkles → three lines of text all at similar size → a drop shadow on the
text → logo bottom-right.

## What makes a surface read as "cyberpunk" or "terminal"

Not the palette. The **density of machine signals per view**: monospace,
uppercase micro labels, `//` or `>` prefixes, invented codes, status lights. At
a dozen of these on one screen, any palette reads as a terminal. Technical
character that works is small, real and peripheral — a genuine ID at the edge
of the screen, not a fake readout in the middle.

## Bad / Good / Why

### Hover on a card

**Bad**
```css
.card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 16px 40px rgba(0, 0, 0, .4);
}
```
**Good**
```css
.card:hover { background: var(--surface-2); }
```
**Why** — the card was already visible; lifting it communicates nothing but
itself. The object stays stable and the system responds around it. (In a
playful direction that chose motion, the lift may be the voice — then it is
consistent everywhere and honours reduced motion.)

### Section emphasis

**Bad** — a section with a violet left border because it "needed emphasis".
```
│ SECURITY
│ Manage your account security.
```
**Good**
```
Account security
────────────────────────────
Manage your account security.
```
**Why** — emphasis comes from hierarchy and type. The stripe stood in for a
structure that was never built. "Account security" is human text, so it takes
the interface voice in sentence case.

### A status that never varies

**Bad**
```
Studio             LIVE        Profile   LIVE     Archive  LIVE
Database           LIVE        Planner   SOON     Index    SOON
```
**Good**
```
Studio                         Profile            Archive
Database                       Planner   SOON     Index    SOON
```
**Why** — when every row is live, `LIVE` distinguishes nothing. Marking only
the exceptions makes `SOON` mean something. A count is the opposite case and
always earns its place, because a count varies by definition.

### A status that disagrees with its affordance

**Bad** — a card labelled "Soon" that is still a link and still says
"Open →".
**Good** — the "Soon" card is not a link and has no arrow; it keeps its place
in the grid.
**Why** — when label and affordance disagree, the reader believes the
affordance. The label becomes a lie the component tells about itself.

### The design system talking to the user

**Bad**
```
SYSTEM ONLINE
NOT A TEMPLATE WITH A DARK COAT OF PAINT
```
**Good** — nothing; or one concrete sentence about what the product does.
**Why** — the system's vocabulary, aimed at a reader who does not know there
is a system. It reads as placeholder text someone forgot to delete.

### Invented vocabulary

**Bad** — one concept, four words across the product: *Channels*, *Worlds*,
*Spaces*, *Hubs*.
**Good** — the plain noun the user already uses.
**Why** — a fabricated code one level up. The reader must learn a private
vocabulary that buys them nothing, and the product cannot keep it straight
either. One concept, one word; one function, one name.

### Technical character on an ordinary screen

**Bad**
```
// INITIALIZING PROFILE
> USER AUTHORIZED
ID: 0x3F9A
```
**Good**
```
Profile
Username    Alex
Avatar      [Change]
```
**Why** — technological character comes from how the system behaves, not from
decorating surfaces with invented code.

### A signal object

**Bad** — a dark rectangle, 1px border, coloured left stripe, mono uppercase
kind label, an icon, and a title.
**Good** — a filled plate with a real shape whose surface carries the kind
(tint, colour plate, edge geometry); title and body in human voice.
**Why** — identity carried by mass needs no notation. Notation appears when
the object has no shape.

### A feature section

**Bad** — three equal cards, each an icon in a tinted circle, a two-word
title, and a sentence, regardless of what the three features are.
**Good** — the most important capability shown large, with real product
material; the others as a compact list or woven into it — or three cards,
**if** they genuinely are three peers of equal weight.
**Why** — equal treatment is correct only for genuine peers. The template
decides the shape before the content does.

### A slide

**Bad** — title "Our Results", five bullets, three icons in circles in the
corner.
**Good** — the title states the finding ("Churn halved after onboarding
change"), one chart with the relevant series highlighted and labelled
directly, one line of source.
**Why** — a slide makes one point. The title carries it; the visual proves
it; everything else is removed.
