---
title: "Accessibility"
kind: "explanation"
audience: [user, contributor, maintainer, agent]
canonical_for: [accessibility_model]
requires: []
---

# Accessibility

Accessibility is specified, not retrofitted. The platform package
`@steven-cutting/biscuit-games` ships three Allium modules, and their clauses are
acceptance criteria for any change that touches a surface here. `appearance.allium`
carries six `@guarantee` clauses on its `Appearance` surface; `operation.allium` states
keyboard operability, visible focus, announcement, and the figures every control has to
meet; `play-surfaces.allium` states that a mark is never only a colour. None of the
three imports anything, so this game inherits the obligations whole rather than
restating them, and owes an account of whatever it adds on top.

## What the platform decides

**Colour never carries meaning alone.** Every state a colour helps to show also carries
a shape, a word, or both, and has an accessible name that says it in words. This holds
in every theme and in both palettes.

**The legibility floor holds in all four combinations of theme and high contrast.**
Text reaches `config.minimum_text_contrast` (4.5) against what is behind it; a control's
boundary reaches `config.minimum_boundary_contrast` (3.0) against the page. High
contrast is a second palette that clears the same bar, not the place legibility is
finally attended to.

**Everything is keyboard operable, and every control is big enough to hit.** 44 CSS
pixels in both directions, down to the 320-pixel viewport that is the narrowest
supported width. `src/lib/config.ts` mirrors those figures from the module that states
them, and `tests/platformSpecs.test.ts` holds the mirror to the shipped text.

**The device wins.** More contrast asked of the operating system turns high contrast
on, and a reduced-motion preference stops every animation whatever the setting says.

## What this game owes

- A non-colour indication and an accessible name for every state it adds beyond the
  platform's marks, in the words its own specification uses.
- A stated distance between two of its own states that sit side by side. No standard
  supplies one, so the game states the figure and measures it.
- The sentence each mark is read out as, arriving at the call site rather than being
  inferred.
- Proof of what only it renders. The platform measures its palette and its primitives
  in its own workshop; this game's stories measure its arrangements, framed at the
  narrowest width, with axe over every render.

## How this is checked

By test, not by audit. Component tests query by accessible role and name, never by
class or test id, with one bounded exception for an element that is `aria-hidden`
because the words beside it already say the same thing. `.storybook/preview.ts` sets
the accessibility addon's test mode to `error`, so a violation fails
`just storybook-test` rather than being reported. A gate's silence is not a pass: axe
never checks contrast behind `aria-hidden`, downgrades any single-character text to
*incomplete*, and answers `target-size` at 24 pixels rather than 44. Focus order,
announcement timing and a palette on a phone at minimum backlight still need a person.
The `accessibility-review` skill in `.agents/skills/` is the procedure.

## Related pages

- [Specifications](specifications.md)
- [Testing](../reference/testing.md)
- [Work in the component workshop](../how-to/work-in-the-component-workshop.md)
- [Work with the specifications](../how-to/work-with-the-specs.md)
- [Decision 0005](../decisions/0005-component-workshop.md)
