---
title: "Maintain dependencies"
kind: "how-to"
audience: [maintainer, agent]
canonical_for: [dependency_maintenance]
requires: []
---

# Maintain dependencies

Every dependency is pinned to an exact version, in `package.json` and in
`pyproject.toml`. No `^`, no `~`. Both lockfiles are committed and marked
`linguist-generated`. Nothing updates them for you.

One of them comes from a second registry: `@steven-cutting/biscuit-games` is read from
GitHub Packages through the committed `.npmrc`, which scopes `@steven-cutting` there and
holds no token. Moving it is its own section below, because what it carries is not only
code.

## Check that the lockfiles still match

```console
just lock-check
```

This runs `uv lock --check` and an npm install dry run. It is part of `just check`, so a
manifest edited without relocking fails the gate rather than drifting.

## Update deliberately

```console
just lock            # relock at the versions the manifests already state
just lock-upgrade    # move to newer versions within the manifests' constraints
```

Because the manifests pin exact versions, `just lock-upgrade` on its own changes very
little. Moving a dependency forward means editing the version in the manifest and then
relocking.

## Upgrading a package

1. Check what it is compatible with before choosing a version. This bites: the current
   TypeScript major is ahead of what `typescript-eslint` supports, so the repository
   pins the 6.x line deliberately, not by neglect.

   ```console
   npm view typescript-eslint peerDependencies
   ```

2. Edit the exact version in `package.json` or `pyproject.toml`.
3. Run `just lock`, then read the lockfile diff before accepting it.
4. Run `just sync`. `just lock` rewrites the lockfiles and installs nothing, and no check
   installs `node_modules` for itself, so without this the gate runs the old versions.
5. Run `just check`. A type-checker or linter upgrade usually surfaces new findings; fix
   them rather than pinning back, unless the finding is wrong for this project.
6. If the change moved `playwright`, reinstall the browser with `just storybook-browsers`.
   The binary is versioned by that pin and is in neither lockfile — see
   [Work in the component workshop](work-in-the-component-workshop.md).

## Moving the design system package

`@steven-cutting/biscuit-games` carries the stylesheet this game wears, the components it
renders and the specifications it restates, so a bump is read before it is taken.

1. See what is published, which needs the token
   [Develop locally](develop-locally.md) describes:

   ```console
   npm view @steven-cutting/biscuit-games versions
   ```

2. Read what moved. The package ships its own changelog, so after installing it is at
   `node_modules/@steven-cutting/biscuit-games/CHANGELOG.md`; before installing, the
   platform's repository has both that and a handover page naming every consumer-visible
   change — [The platform upstream](../project/platform.md) links them.
3. Edit the exact version, run `just lock`, and read the lockfile diff: one dependency line
   and one entry, and anything else is a stop-and-read. Then run `just sync`, because
   `just lock` installs nothing and every step below reads the installed package.
4. Run `just frontend-coverage` before anything else. One gate fails by design here:
   `tests/platformSpecs.test.ts`, on a figure whose value moved or a restated clause whose
   wording did. Each failure is the moment somebody decides whether the platform's meaning
   moved — a reworded clause is amended upstream and taken, never reworded here.
5. Add a `CHANGELOG.md` entry naming what a reader would see; `package.json` is the one
   place the installed version is stated.
6. Run `just check`, then review the workshop in Chromatic: a rendered change upstream
   arrives as a diff in this game's own stories.

Nothing proposes this bump for you. There is no Dependabot here, and one would need the
registry credential as a stored secret of its own.

## Moving the tooling package

The documentation, agent and specification gates, the allium installer and the runner
behind `just check` are console scripts of `biscuit-games-tooling`, which the `dev` group in
`pyproject.toml` pins to a release tag of `steven-cutting/biscuit_games_tooling`. `uv.lock`
records the commit behind the tag, and `just lock-check` fails when the tag moves without a
relock.

1. Read the package's `CHANGELOG.md` in that repository for the release you are taking, and
   the level its README gives the change. A Major release can fail a tree that passed.
2. Edit the tag in the `biscuit-games-tooling` line of `pyproject.toml`, then relock that
   one package and read the lockfile diff:

   ```console
   uv lock --upgrade-package biscuit-games-tooling
   ```

3. Run `just sync`, because the lock installs nothing, and `just install-allium`, which
   replaces the binary if the release moved its pin.
4. On a Major release, run `just check` before committing. Otherwise the hooks that read
   `pyproject.toml` re-run the contracts and the specifications on the commit.

A tag the package has released is never moved, so relocking without editing the tag
changes nothing.

## Moving the Allium binary

`allium` is a checksummed binary, not a package, so no lockfile accounts for it and
`just lock-check` cannot speak for it. The `biscuit-games-tooling` package holds the
version and the SHA-256 of each supported artefact; see
[decision 0007](../decisions/0007-project-managed-allium-cli.md). Moving the allium pin is
a release of that package, and this game takes it by moving the package pin, as the section
above describes. The package's README carries the recomputation of the checksums, because
upstream publishes none for these files.

After taking a release that moves it, reinstall and confirm:

```console
just install-allium
just check-specs
```

Reinstalling is always safe to retry. The download lands beside the installed copy under a
temporary name and is asked for both its checksum and its version there, so a failed
download, a mismatched checksum or a binary that will not run leaves the working
installation exactly where it was. `just install-allium` also replaces a binary that no
longer runs, so an installation damaged by other means repairs itself rather than needing
`.tools/` cleared by hand.

A version change can move what the checker reports, in both directions. After moving the
pin, run `just check-specs` and `just analyse-specs`: a new version can report something
the modules were clean of, and it can also stop needing a waiver they carry. The modules
carry none at present, but the directive leans on behaviour upstream documents nowhere and
was verified against 3.6.1 only, so any waiver added later must be re-verified on the
commit that moves the pin, dropped where the new version no longer needs it, and its count
and shape updated in [Work with the specifications](work-with-the-specs.md) in that same
commit. Moving the package pin in `pyproject.toml` is itself a trigger for both
specification hooks, so the gate re-reads the modules against the new version on the
commit that moves the pin — but only after `just install-allium` has actually installed it.

## Take a template update

The pins above move through the template too. `copier update` carries a changed pin into
`package.json` or `pyproject.toml` as an ordinary hunk, which is why the game commits its
lockfiles and relocks after an update;
[Update from the template](update-from-template.md) is the procedure.

## Actions in the workflows

The three workflows hold one pin each, and it is the same one: the shared workflow they
call in `steven-cutting/biscuit_games_tooling`, pinned to a commit SHA with its release tag
as a comment, not to the tag. The actions those jobs run and the toolchain versions they
install are pinned inside that repository and move there. A new release reaches this game
when a template release moves the pin and this game takes the update.

To move the pin ahead of the template, resolve the release's commit and replace both the
SHA and the comment in all three files. Its tags are annotated, so ask for the commit: the
SHA a tag reference answers with names the tag object, which no `uses:` line accepts.

```console
gh api repos/steven-cutting/biscuit_games_tooling/commits/v0.1.0 --jq .sha
```

The three files are managed. An update that moves the pin to the same commit merges
silently, and one that moves it anywhere else writes markers. An action in a workflow of
this game's own is pinned the same way, and the same command resolves its tag.

`actionlint` runs inside `just lint`, so a malformed workflow fails locally.

## Related pages

- [Configuration](../reference/configuration.md)
- [Quality gates](../reference/quality-gates.md)
- [Maintenance](../operations/maintenance.md)
