# Establishing the direction

Step 0 of the procedure. Its job is to make sure every later decision traces
back to something real — the project's system, the user's intent, or the
product itself — rather than to the model's defaults.

## 1. Find what already exists

Look before deciding anything. In order of authority:

1. **A project design skill** — `.claude/skills/*design*`, or any skill that
   describes this product's visual language. Follow it. This skill fills only
   what it leaves open.
2. **Tokens and theme** — `:root` custom properties, `variables.scss`,
   `tailwind.config.*` / `@theme`, `theme.ts`, `design-tokens.json`, a
   component library's theme, XAML/QML resource dictionaries, slide masters
   and theme colours in an existing deck.
3. **Design docs** — `DESIGN.md`, `docs/design*`, brand guidelines, a
   brandbook PDF, a style guide, a decisions log.
4. **Approved work** — live screens, published decks, existing graphics the
   owner signed off on. They show the system in use, including what the docs
   forgot.
5. **Brand assets** — logo, brand colours, the typefaces actually in use.

**Find, don't invent.** If a token exists, use it. If a value you need does
not exist, add it to the token layer with a role name — never inline it in a
component.

**Small task in a project with a system:** read the parts of the system the
task touches and go. Do not run full discovery for a button, and do not turn a
local fix into a redesign.

## 2. When the user already has ideas

Take them as given. Do not reinterpret them toward your own taste or toward
this skill's defaults.

- Fill only the gaps, and say which gaps you filled and how.
- If an idea is underspecified ("make it modern"), ask what they mean by
  pointing at something concrete — a product they consider modern — rather
  than guessing.
- If an idea collides with a hard ban (fake testimonials, an unreadable
  contrast pair), say so once, plainly, with the reason.
- If an idea departs from a strong default (hover lift in a children's app),
  that is a direction, not a violation. Record it.

## 3. When there is nothing

### Do not offer a menu

Never answer "no direction" with options like *minimal / bold / playful —
which do you prefer?* A menu pushes the analysis onto the user, and its
options are generic by construction: they are the three defaults, renamed.

### Study the product first

The direction is derived from what the product is, not picked from a list.
Find out:

- **What it is and does**, in one sentence, without marketing words.
- **Who it is for**, and their context — on what device, in what moment, in
  what state of mind, how often.
- **What content actually exists** — real screens, products, photos, data,
  work samples. Design for that content, not for placeholders.
- **The job of this surface** — sell, explain, let someone work, report,
  persuade a room.
- **The category's conventions** — what users of this kind of product expect,
  and what every competitor looks like. That second part tells you what
  "generic" means here.
- **Existing brand assets**, however small: a logo, a colour someone already
  uses, a name with a character.

Sources, in order of usefulness: the product itself (run it, open it), the
codebase and its README, existing materials, the user's description, and, if
available, the live site or app.

### Ask for references only when analysis cannot ground a direction

If there is no product to look at, no assets, and the audience is ambiguous,
ask once, compactly:

- two or three products, sites, apps, decks or brands they like — **and what
  specifically** they like in each;
- anything they explicitly dislike;
- any hard constraints (brand colours, mandatory fonts, platform, accessibility
  requirements).

References inform principles. They never supply a template: take *why* a
reference works (its density, its restraint, how it uses type), never its
layout, palette, typeface or ornament.

### Then propose one direction

After the analysis, if the user has not decided, propose **one** direction
with its reasoning. Every line must trace back to something found above.

```
Direction — <product>

Character    one sentence on what it should feel like, and one on what it must not
Structure    the sequence of screens / sections / slides, and why in that order
Colour       roles, not swatches: ground, surface, text, primary action,
             accent, states — and which colour must never do which job
Type         roles (display / interface / reading / system / code), the
             families proposed, and why they fit (script coverage checked)
Shape        radius, chamfer or square — and where it applies
Density      dense / balanced / spacious, and why for this audience
Motion       the vocabulary (calm / responsive / playful) and what moves
Signatures   each signature element with its single meaning and its budget
             (zero signatures is a valid answer)
Departures   any strong default this direction deliberately breaks, and why
```

Wait for agreement before building more than a small sample. A small sample —
one key screen, one slide, one section — is often the best way to make the
proposal concrete.

## 4. Record the agreed direction

Write the direction down where the project keeps documentation — `DESIGN.md`,
`docs/design/`, or as a project design skill — so the next session follows it
instead of re-deriving it. Offer this; do not assume it.

When a later decision changes the direction, record the change with its
reason. Decisions that lose their reason get re-opened.
