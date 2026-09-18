---
title: "Update from the template"
kind: "how-to"
audience: [maintainer, agent]
canonical_for: [template_update_procedure]
requires: []
---

# Update from the template

This game was rendered by Copier from the Biscuit Games template,
<https://github.com/steven-cutting/biscuit_games_template>, at template version
`v2.0.0`. The answers the
questionnaire took are recorded in `.copier-answers.yml`, and that file is what makes a
later update possible: `copier update` reads it, renders the template again at a newer
version, and merges what changed between the two renders into this repository. In the
template's own tree a file carries a `.jinja` suffix where an answer is substituted into
it; the files rendered here carry no such syntax.

## What an update touches, and what it never does

Every file the template renders is one of three kinds.

**Seed files are this game's.** The template writes them once, on the first render, and an
update never merges, recreates or deletes one: rewrite them freely, and one you delete
stays deleted. `copier.yml` lists them, and the list is frozen — after the template's first
release it never adds, renames or retitles a seed page or a numbered decision, because
`docs/manifest.yml` and `docs/README.md` re-render on every update while seeds do not.

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

**Managed files are the template's**, and an update is a three-way merge onto each: a
change the template made arrives as a hunk, an edit this game made is kept where the
template left that hunk alone, and where both sides changed the same lines Copier writes
markers. A managed file this game deleted stays deleted. A managed file the template stops
rendering is removed from this game even where it was edited; the template's changelog
announces every such removal under "Update notes".

Some managed files are expected to be edited here, and a convention keeps the two sides in
different hunks: the template inserts into the upper blocks, and this game appends at the
end. `docs/manifest.yml` takes game pages after the last decision entry; `docs/README.md`
takes them under "This game"; `AGENTS.md` takes deviations at the end of Provenance; the
`Justfile`, `package.json`, `eslint.config.js`, `.gitignore` and `src/lib/config.ts` take
additions at the end of the relevant block. Reordering any of these is what brings the
markers back.

**`.copier-answers.yml` is Copier's.** It is neither merged like a managed file nor left
alone like a seed: every update rewrites it whole, from the answers and the template
version that update rendered, and the next update reads it.

## Take an update

1. Commit everything. Copier refuses a dirty worktree.
2. Run the update. The template declares no tasks, so no trust flag is passed:

   ```console
   uvx copier update --skip-answered
   ```

   That takes the template's latest release tag. Add `--vcs-ref=vX.Y.Z` to pick one, or
   `--vcs-ref=HEAD` for the tip; a prerelease tag is skipped unless `--prereleases` is
   given. Add `--conflict rej` to have conflicts written as `.rej` files beside the
   originals instead of inline markers.
3. Resolve every marker. They read `<<<<<<< before updating` and `>>>>>>> after updating`;
   the template's side is a suggestion, and this game's behaviour wins where the two
   genuinely disagree. The hook gate refuses a commit that still carries one.
4. Regenerate what is generated, install it, repair formatting, and run the whole gate:

   ```console
   just lock
   just sync
   just fix
   just check
   ```

   `just lock` relocks both lockfiles against the manifests the update may have moved;
   read the lockfile diff before accepting it. It installs nothing, so `just sync` installs
   what the lockfiles now say before `just fix` and `just check` read it.
5. Commit the result as one change, `.copier-answers.yml` included: the next update reads
   it.

Never edit `.copier-answers.yml` by hand, with one exception: `_src_path`, when a game
rendered from a local clone moves to the template's GitHub address.

## Change an answer

Run `uvx copier update` without `--skip-answered`. Copier asks the questionnaire again with
the recorded answers as defaults, and the change lands as an update. Only the four
questions are asked; everything else is computed from them.

## Reset a managed file

`uvx copier recopy --skip-answered` renders the template again over this repository with
no merge. Seed files are skipped; every other file is overwritten, so commit first and
read the diff.

## When this game and the template disagree

A departure that suits only this game is recorded under "Deliberate deviations" in
`AGENTS.md`, and the file that carries it is edited here. A departure that would suit
every game is made in the template instead, and arrives by the next update.

## Steps by version

A template release that asks something of a game beyond resolving markers records it
here, newest first.

### 2.0.0

The six checkers left `scripts/`, and the update removed them: `validate_docs.py`,
`validate_agents.py`, `install_allium.py`, `run_allium.py`, `run_project_check.py` and
`run_ripsecrets_redacted.py`. They are console scripts of the `biscuit-games-tooling`
package now, which `pyproject.toml` pins and the hooks and recipes call. A file the update
removes is removed even where this game edited it, so move an edit you want to keep into a
script of this game's own before updating.

Run `just lock` before `just fix && just check`, so `uv.lock` learns the package pin; until
it does, every recipe that calls the package fails on a stale lockfile. A gate this game
added to `just check` goes into the `recipes` list at the end of `pyproject.toml`.

### 1.0.0

The three workflows call shared workflows in `steven-cutting/biscuit_games_tooling`, and
the checks they report are renamed: `frontend`, `documents` and `stories` become
`ci / frontend`, `ci / documents` and `ci / stories`. Once the update is committed, change
the branch protection on `main` to require the new names, in the repository's branch
settings or with `gh api`. Until then the old names never report, and every pull request
waits on checks that will not arrive.

A step this game added to one of the old jobs has no place in a caller, because a job that
calls a workflow holds no steps, and the update moves nothing for you. While resolving the
markers, move the step by hand into a workflow file of this game's own under
`.github/workflows/`, which no update touches.

## Related pages

- [Maintain dependencies](maintain-dependencies.md)
- [Documentation contract](../reference/documentation-contract.md)
- [Decision 0009: Rendered from the template](../decisions/0009-rendered-from-the-template.md)
