# Pawdoku

A sudoku puzzle game for Biscuit Games.

**Play it at <https://steven-cutting.github.io/pawdoku/>.**

Pawdoku is a Biscuit Games game: a single-page static site with no backend, no
accounts and no telemetry. It runs entirely in the browser and is published to GitHub
Pages as a project site beneath `/pawdoku/`. Every rule comes from the
specifications in `docs/specs/`.

## Quick start

```console
just initialize
just dev
```

`just initialize` creates both lockfiles, installs both toolchains, downloads the browser
the story gate needs, normalises formatting and installs the pre-commit hook. It never
stages, commits, tags or pushes.

It also installs the design system from GitHub Packages, which needs a token carrying
`read:packages` in `~/.npmrc` first — [Develop locally](docs/how-to/develop-locally.md) has
the line.

## Check your work

```console
just fix      # the safe automatic repairs; unlike any check, it modifies files
just check    # every gate, read-only, proving the worktree is unchanged
```

`just --list` prints every recipe. Each one is described in
[Commands](docs/reference/commands.md).

## Layout

```text
src/lib/brand.ts     The one place this game's name is written
src/lib/ports/       Every side effect, each with an in-memory fake
src/lib/components/  Svelte 5 components, runes only
src/routes/          Prerendered routes
tests/               Vitest suites, never colocated
stories/             Svelte CSF stories, one per component
docs/                The handbook
docs/specs/          Allium specifications — the source of truth for behaviour
```

## Documentation

Start at [the documentation map](docs/README.md).

- [Purpose and scope](docs/project/purpose-and-scope.md) — what Pawdoku is, and is not
- [Make your first change](docs/tutorials/first-change.md) — clone to green gate
- [Architecture](docs/explanation/architecture.md) — how a site with no server fits together
- [Specifications](docs/explanation/specifications.md) — why behaviour is written down first

Engineering conventions and the agent working agreement are in [AGENTS.md](AGENTS.md).

## Boundaries

Behaviour is decided in `docs/specs/`, not in code. When the two disagree, the
specification is right and the code is a defect. Changing what the game does means
changing a specification first.

Whatever this game remembers lives in one browser on one device and is never uploaded.
Clearing browser data destroys it. See
[Security model](docs/explanation/security-model.md).

This repository was rendered from the Biscuit Games template. The toolchain, the
handbook's managed pages and the agent contract arrive from it by `copier update`, and
[Update from the template](docs/how-to/update-from-template.md) says which files are this
game's alone.
