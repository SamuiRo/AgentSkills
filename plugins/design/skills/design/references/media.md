# Medium-specific rules

The procedure and principles apply everywhere. This file adds what each medium
needs on top. Read the section for the medium you are working in.

## Marketing site, landing page, portfolio

**Clarity, then experience.** A visitor decides in seconds whether this is
relevant. The first view gives, in this order of importance:

- the **category** — what kind of thing this is;
- the **value** — a heading about what it does for the visitor;
- one short line of introduction, readable in a second;
- **proof** — real product, real work;
- a **path to action**, reachable without opening a menu on mobile.

A cinematic or mystery sequence before the visitor learns what this is costs
the visitors who leave first.

**Structure follows the business scenario, not a landing template.** Each
section has a distinct role — promise, proof, method, scope, action — and the
order lets each one answer the question the previous one raised. A section
with no role is removed, not filled.

**Work before self-promotion.** Show the product or the work early and large.
A teaser and a full reveal use different material; the same screenshot never
appears twice on a page.

**CTA discipline.** One function, one name — the header CTA and the
contextual CTA after proof say the same words. Not a button every 500px. The
primary action may be persistent, but quiet (law 1).

**Forms ask only for what the first reply needs.** Every extra field is
friction. No qualification interrogations, no fake CRM.

**Scope honesty.** List what is actually offered and proven. Adding services
"for completeness" creates a credibility gap.

**Proof is real or absent.** No invented metrics, logos, testimonials,
awards, team or client lists — see hard bans.

## Product UI (web app, dashboard, tool)

**The user's task owns the space.** Decide what people come here to do, and
give that the first position and most of the area. Navigation, greetings and
summary cards are support.

- Working surfaces use the full width (`principles.md` §4).
- KPI and stat cards earn their place only if they vary and drive a decision.
  A trend arrow needs a real source and period.
- Selection is a filled row or tile, not a side stripe.
- A navigation marks the active item only if it locates you among siblings;
  a launcher that opens other places marks nothing.
- Exactly one H1 per route. If the location is already stated (breadcrumb,
  header), the page heading says *what is here*, not *where you are*.
- A page header earns its space only if it carries something the content
  below does not already show.
- Tables: density is fine; cell borders are a legitimate data boundary;
  a table that scrolls sideways shows it does (a visible bar, a cut-off
  column or an edge fade); numbers in tabular figures, right-aligned.
- Empty, loading and error states are designed for each surface, not
  inherited.

## Desktop app

Everything for product UI, plus the platform.

**Respect the platform's conventions** unless the direction deliberately
replaces them, and then replace them completely — a half-native,
half-web app feels broken on both counts.

- **Window chrome.** Native title bar, or a custom one that keeps every
  native behaviour: drag, double-click to maximise, snap layouts, system
  menu, traffic lights / caption buttons where the OS puts them.
- **Menus and shortcuts.** Standard shortcuts work (copy, paste, undo, find,
  settings, close, quit). Right-click context menus where users expect them.
  Shortcuts are discoverable — in menus, in tooltips.
- **Keyboard-complete.** Tab order is logical, focus is always visible, every
  action is reachable without a mouse.
- **Control sizing.** Desktop controls are compact relative to touch — a web
  landing page's 48–56px buttons inside a tool are the inoffensive default
  again. Follow the platform's density, and the direction's.
- **Resizing.** The layout works from the minimum window size to a large
  monitor; it reflows rather than letterboxing a fixed canvas. Decide what
  collapses first.
- **System settings.** Follow system light/dark, accent colour if
  appropriate, text scaling, high contrast, reduced motion; render crisply at
  every DPI scale.
- **Modality.** Prefer inline and non-blocking UI; dialogs for decisions that
  must block. Do not open a modal for something a panel can show.
- **State persistence.** Window size, position, panel layout and last
  location survive a restart.
- **No web marketing inside the tool** — no hero, no gradient banners, no
  "Welcome back 👋" card. The app is a working surface.

## Presentations and slides

First decide which kind of deck it is — the rules differ:

- **Presented** (a speaker in front of it): very little text, large, one point
  per slide; the speaker carries the explanation.
- **Read** (sent, read alone): more text is fine, but structured — each slide
  still makes one point, and the title states it.

**Rules for both**

- **One slide, one point. The title states the point** as a sentence ("Churn
  halved after the onboarding change"), not a topic ("Results"). Read the
  titles alone in order: they should tell the story.
- **Hierarchy visible from the back of the room / at thumbnail size.** If the
  thumbnail grid looks uniform, the slides have no roles.
- **Slides vary by role.** Section opener, statement, evidence, data,
  comparison, quote, image — each role has its layout. The same title +
  bullets layout forty times is the template, not a deck.
- **A grid and margins shared across all slides** — the eye notices a title
  that moves 8px between slides.
- **Type size:** presented decks ~24pt minimum for body, read decks ~14pt; a
  type scale with few steps, as everywhere.
- **Charts:** one message per chart; highlight the series that matters and
  grey the rest; label directly instead of a legend where possible; honest
  axes (no truncated baselines that exaggerate); source line; no 3D, no
  exploded pies.
- **Images:** real, large, cropped with intent, full-bleed or on the grid. A
  stock photo with a dark overlay behind every title is filler.
- **Projector contrast.** Light-grey text and thin weights disappear on a
  projector. Check contrast for the worst room, not the laptop.
- **Agenda, "Thank you", "Questions?" slides earn their place** like anything
  else — usually a closing slide with the one action or contact works better.
- **No icon triads** (three icons in circles with a word under each) unless
  three things genuinely are peers and the icons say something.
- **Data is real.** No invented numbers, quotes or logos — hard bans apply.

## Graphics: social, posters, banners, print

- **One focal point.** Decide what is seen first, second, third; size and
  contrast enforce that order. Three lines of text at similar size have no
  order.
- **Check at real size and as a thumbnail.** Social graphics are first seen at
  a fraction of their size in a feed; if the message does not survive the
  thumbnail, it does not survive.
- **Text on image** needs a deliberate contrast solution — a calm area of the
  image, a solid plate, a scrim with a role — not a drop shadow on the
  letters.
- **Platform specs and safe zones.** Aspect ratio, pixel size, UI overlays
  that cover corners (profile badges, buttons, captions), bleed and CMYK for
  print, minimum type size at print distance.
- **Brand applied by system, not by stamping.** The logo has a fixed position
  and clear space; colours and type come from the brand roles; a series of
  graphics shares a grid.
- **Real material.** Product, people, work. Floating abstract 3D shapes,
  lens flares, sparkles, glow and gradient meshes are the generated-graphic
  signature.
- **Restraint in a series.** One template with variable content beats twelve
  differently styled posts.

## HTML artifacts and one-off pages

They are small products: the same rules apply. Choose a direction even for a
one-page tool, respect light and dark mode, work at phone width, and do not
fill the page with the landing template because there was space.
