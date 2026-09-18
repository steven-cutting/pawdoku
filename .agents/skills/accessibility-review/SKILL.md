---
name: accessibility-review
description: Review a change against the accessibility guarantees the specifications state for every surface.
---

# Review a change for accessibility

The `@guarantee` clauses in `docs/specs/` are the acceptance criteria, not aspirations. Each one names an obligation that a change can break silently.

1. Read `AGENTS.md` and `docs/explanation/accessibility.md`. Identify which surface in `docs/specs/` the change touches, and read that surface's guarantees.
2. Check the colour obligation. Every state the surface distinguishes by colour also carries a non-colour indication and an accessible name, in the words the surface's `@guarantee` clauses use, so it is readable without colour vision.
3. Check keyboard operation. Every control the surface `provides` is reachable and invocable from the keyboard alone, with visible focus, whatever the physical-keyboard setting says.
4. Check what is announced. Every outcome the surface's `@guarantee` clauses say is announced reaches assistive technology through the platform's `Announcer`, carrying the detail the clause names.
5. Check what is not exposed. Whatever a surface's specification withholds from the player stays out of the DOM as well, attributes included.
6. Check motion. Animation runs only when the setting allows it and the operating system expresses no reduced-motion preference; the operating system wins.
7. Report findings by severity with `file:line` references, then run `just frontend-static` and `just check`.
