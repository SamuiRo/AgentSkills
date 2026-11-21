# Review

The final pass on your own work, and the method for reviewing someone else's.
Anything that fails is fixed or named explicitly in the report with a reason.

## Checklist

### Direction
- [ ] The project's design skill / system was found and followed; this skill
      only filled gaps
- [ ] Every decision traces to the direction, the content or the user's
      intent — not to a default
- [ ] A small change stayed small; nothing was redesigned that was not asked
- [ ] Any departure from a strong default is recorded in the direction with a
      reason

### Structure
- [ ] The hierarchy can be stated in words, and visual weight matches it
- [ ] Type and placement were tried before any container was opened
- [ ] Every container is an object boundary, not a wrapper around a region
- [ ] Objects read as mass, not as a rectangle with a line around it
- [ ] Every line separates, aligns or bounds data — none finishes a shape
- [ ] Equal treatment only for genuine peers
- [ ] Width/format follows the job: working surfaces wide, prose on a measure
- [ ] No leftover grid tracks, empty columns or dividers drawn against nothing
- [ ] Responsive rehierarchises; shared layouts share their breakpoints too

### Intensity and budgets
- [ ] Exactly one dominant element
- [ ] Nothing persistent demands attention
- [ ] Each signature motif within budget and used only in its meaning
- [ ] No motifs stacked to make something feel on-brand
- [ ] No status that never varies; no status contradicting its affordance
- [ ] The same information does not appear twice or in two notations
- [ ] Machine-signal density is deliberate (mono, uppercase micro labels,
      prefixes, codes)

### System
- [ ] Every value resolves to a token / style; new values were added to the
      token layer with a role name
- [ ] Colours by role; no brand colour carrying a semantic state
- [ ] Destructive actions: danger colour + confirmation + not dominant
- [ ] Type by role; fonts cover every shipped script; tabular figures where
      numbers align
- [ ] One shape language, applied by role

### Honesty
- [ ] No fabricated proof, metrics, statuses or technical strings
- [ ] No design-system principles as on-screen copy; no invented vocabulary
- [ ] No emoji as interface iconography

### States, content, access
- [ ] Loading, empty, error, disabled, focus, selected designed — not inherited
- [ ] Tested with long strings, every language, missing images, extreme
      numbers, no data
- [ ] Contrast checked per pair; focus visible on every surface (≥ 3:1)
- [ ] Keyboard-complete; every inner scroll area shows there is more (bar,
      cut-off item or edge fade) — hiding the page scrollbar is a direction
      choice
- [ ] Every animation answers a question; reduced motion honoured

### Verification
- [ ] Rendered and looked at, at the sizes in `SKILL.md` → Verify
- [ ] `design_gate.py` run; no number raised without a recorded reason
- [ ] Boring screen test, removal test, swap test

## Classifying feedback

Separate findings so taste is not presented as a defect:

1. **Blocker** — the purpose is unclear, the main action unreachable, proof
   untrue, layout broken at a real size, contrast unreadable, a form or
   control not working.
2. **System deviation** — a value outside the system, a surface or motif
   without a role, generated-template structure, fabricated detail, broken
   voice, untranslated text.
3. **Contextual risk** — real content competes with the heading, a
   translation changes the rhythm, new material needs a different frame.
4. **Polish** — a crop, a line break, optical spacing, a timing — does not
   change the direction.

## Reporting

For each finding: where (what a person sees, not a selector), what is wrong in
one line, the consequence, and the **minimal sufficient change**. Offer
removal whenever it is an option — it usually is.

Do not launch a new style because of one crop or one line break. When
reviewing an approved system, judge against that system, not against this
skill's defaults.
