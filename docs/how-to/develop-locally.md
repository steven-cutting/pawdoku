---
title: "Develop locally"
kind: "how-to"
audience: [contributor, maintainer, agent]
canonical_for: [local_development]
requires: []
---

# Develop locally

## Prerequisites

| Tool | Why |
| --- | --- |
| Node 26 | Runs the application, Vite and Vitest. |
| npm 11 | The package manager. Nothing else is supported. |
| `uv` | Provides the pinned Python tooling the hook gate runs on. |
| `just` | The task runner, and the only supported interface to the checks. |
| A GitHub token with `read:packages` | The design system is installed from GitHub Packages, which authenticates every request. |

`package.json` states the supported ranges in `engines` and the exact Node and npm in
`volta`, so a Volta user gets the right Node automatically. `.python-version` names the
Python that `uv` runs the tooling on.

## First run

This game takes its design system from `@steven-cutting/biscuit-games`, published to GitHub
Packages. That registry authenticates every request, including a read of a public package,
so the token comes before anything else. Put one line in `~/.npmrc` — the user
configuration, never this repository's `.npmrc`, which names the registry for the scope and
holds no credential:

```text
//npm.pkg.github.com/:_authToken=<your token>
```

Replace the placeholder, angle brackets and all. It is bracketed rather than spelled
`YOUR_TOKEN` because `ripsecrets` reads this repository as part of the gate and takes a
bare word after `_authToken=` for a token whether or not it is one — so a plainer
placeholder here would fail the commit that documented it. The token is a personal access
token carrying `read:packages`, and it lives in `~/.npmrc` and nowhere in this repository.

Without the line npm answers `401 Unauthorized` and says the authentication token was not
provided — the registry refusing the request, rather than a broken install.

```console
just initialize
```

This creates `uv.lock` and `package-lock.json`, installs both toolchains and the Chromium
build the story tests need, normalises formatting, and installs the pre-commit hook. Run it
once per clone. It never stages, commits, tags or pushes.

## Every day

```console
just dev
```

Vite serves the app with hot module replacement. There is no backend to start, no
database to bring up and no proxy to configure; the browser talks to Vite and to nothing
else.

To build a component on its own, rather than by playing until the game produces the state
you want, run the workshop instead:

```console
just storybook
```

See [Work in the component workshop](work-in-the-component-workshop.md).

To see what a deployment would actually serve, build first and then preview:

```console
just frontend-build
just preview
```

To reproduce the published site exactly, set the base path the project site is served
under — the repository's name, which `pages.yml` reads from the event — on both commands,
for the reason [Configuration](../reference/configuration.md) gives:

```console
BASE_PATH=/<repository name> just frontend-build
BASE_PATH=/<repository name> just preview
```

## Before handing work back

```console
just fix       # formats and applies the safe automatic repairs
just check     # the whole gate, read-only
```

Of the two, only `just fix` modifies files. Every check is read-only, and `just check`
proves it by comparing the worktree before and after each recipe.

## Keeping the workspace current

After pulling, re-sync so the installed dependencies match the lockfiles:

```console
just sync
```

## Related pages

- [Commands](../reference/commands.md)
- [Test and debug](test-and-debug.md)
- [Work in the component workshop](work-in-the-component-workshop.md)
- [Troubleshooting](../operations/troubleshooting.md)
