---
title: "Decision 0009: Rendered from the template"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_rendered_from_template]
requires: []
---

# Decision 0009: Rendered from the template

## Context

Every Biscuit Games game shares a great deal that is not the game itself: a toolchain, a
handbook, an agent contract and a quality gate. A change to any of those should be made
once and reach every game, rather than being made by hand in each and drifting in all of
them.

A GitHub repository template was the obvious alternative, and it does less than it
appears to. It copies a tree once and substitutes nothing, so every name in it is found
and replaced by hand; it offers no way to carry a later change into a repository created
from it; and it must itself be a valid project, so a template that names no game still has
to build, test and pass its gate as though it were one.

## Decision

This game was rendered by Copier from `biscuit_games_template`. The answers it was
rendered with, and the template commit it was rendered from, are recorded in
`.copier-answers.yml`. That file is committed and never edited by hand, with one
exception: `_src_path` changes when a game rendered from a local checkout moves to the
template's address on GitHub.

Every file the template renders is one of two kinds.

A managed file is rendered again on every `copier update` and merged three ways with
whatever this game has done to it. Where the template changed a hunk and the game did not,
the new render is taken. Where the game changed a hunk and the template did not, the
game's version is kept. Where both changed different hunks, the two merge cleanly. Where
both changed the same hunk, the update leaves inline `<<<<<<< before updating` and
`>>>>>>> after updating` markers around the two sides, and where they genuinely disagree
the template's side is a suggestion rather than an instruction.

A seed file is rendered once and is this game's from the first commit. An update never
merges, recreates or deletes one, and a seed this game deletes stays deleted. The seeds
are exactly these fourteen patterns:

```text
/README.md
/CHANGELOG.md
/SECURITY.md
/docs/project/purpose-and-scope.md
/docs/project/terminology.md
/docs/decisions/
/docs/specs/
/src/lib/brand.ts
/src/lib/components/
/src/routes/+page.svelte
/stories/
/tests/restated.ts
/tests/lockup.test.ts
/tests/route.test.ts
```

Some managed files are ones this game is expected to edit: `docs/manifest.yml`,
`docs/README.md`, `AGENTS.md`, `Justfile`, `package.json`, `pyproject.toml`,
`eslint.config.js`, `.gitignore`, `.prettierignore`, `lychee.toml`, the two hook
configurations, `src/lib/config.ts` and `tests/ports.test.ts`. They follow one
convention: the template inserts inside the upper blocks and the game appends at the end,
so a template change and a game addition land in different hunks.

The seed inventory is frozen. `docs/manifest.yml` and `docs/README.md` are managed and
re-render on every update, while the seed pages they register never do, so after its
first release the template never adds, renames or retitles a seed page or a numbered
decision. Anything it later hands to games is a managed page, and a decision the template
takes about itself is recorded in the template's own changelog rather than here. This
game's own decisions start at 0011 and can never collide with one the template ships.

## Consequences

**Managed pages say "this game" rather than its name.** `AGENTS.md` and `docs/README.md`
are the only managed pages that name it. Elsewhere in the handbook the name arrives
through the seeds, so no other managed page carries a merge point for it.

**Taking an update is a procedure, not a command.** Commit everything first, because an
update refuses a dirty worktree. Run `uvx copier update --skip-answered`, resolve every
marker it leaves, run `just lock && just fix && just check`, and commit the result
together with `.copier-answers.yml`.

**A managed file the template stops rendering is removed from this game**, even where this
game edited it. The template announces every such removal in its changelog under "Update
notes", as a MAJOR release.

**Same-hunk appends still conflict.** The append-at-the-end convention narrows the
conflicts rather than removing them: two additions at the very end of the same block still
meet, and an agent that tidies the ordering of a managed file recreates exactly the
conflicts the convention exists to avoid.

**A departure has two homes.** One that would suit every game belongs in the template,
where it reaches all of them. One that is this game's alone is recorded in `AGENTS.md`
under "Deliberate deviations" and in a decision here.

## What would reopen this

The template ceasing to be maintained: this game keeps everything it has, and updates stop
arriving. Copier changing what `_exclude` sees during an update, which is what keeps every
seed out of it; `_min_copier_version` refuses an older Copier, not a newer one. Or this
game needing to rewrite a managed file wholesale, which the frozen inventory cannot turn
into a seed.

## Related pages

- [Update from the template](../how-to/update-from-template.md)
- [Documentation contract](../reference/documentation-contract.md)
- [Decision 0010: A project Pages site](0010-a-project-pages-site.md)
