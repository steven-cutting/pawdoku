---
title: "Troubleshooting"
kind: "operations"
audience: [contributor, maintainer, operator, agent]
canonical_for: [troubleshooting]
requires: []
---

# Troubleshooting

Symptoms as headings, causes and fixes as bodies.

## `just check` reports that a recipe changed the worktree

The recipe is the defect, not your change. Checks are read-only; anything that writes
belongs in `.pre-commit-fix.yaml` and runs from `just fix`. The report names which paths
moved. Move the offending hook, or add the generated path to the ignore rules.

## `docs validation: frontmatter <field> disagrees with the manifest`

Almost always list order. The comparison between `docs/manifest.yml` and a page's
frontmatter is order-sensitive, so `[maintainer, contributor]` fails against
`["contributor", "maintainer"]`. Copy the order from the manifest.

If the field is `title`, check for a stray difference in punctuation — the level-one
heading must match it byte for byte as well.

## `docs validation: not reachable from docs/README.md`

The page exists and is registered, but nothing links to it. Add it to
[the documentation map](../README.md), or to a page that is already reachable.

## `agent validation: unexpected managed file`

Something appeared under `.agents/`, `.claude/` or `.codex/` that is neither a declared
skill nor `.claude/settings.json`. If it is local tool state, add it to `.gitignore` —
the inventory reads Git, so an ignored file is invisible to it. If it is real content, it
belongs in `.agents/skills/` with bridges, or somewhere else entirely.

## `agent validation: must stay a thin pointer to the canonical skill`

A bridge under `.claude/` or `.codex/` has grown content, or its frontmatter has drifted
from the canonical skill. Regenerate it: the canonical frontmatter verbatim, one blank
line, then the fixed pointer sentence and nothing else. The body is compared against a
template rather than measured, so a clause of your own fails however short it is —
[Agent contract](../reference/agent-contract.md#what-a-bridge-must-be) carries the text.

## Coverage fails but everything is tested

Distinguish two cases. If a real path is untested, add the test. If the uncovered branch
cannot be reached by any input — a bounds check after a modulo, a fallback after an
exhaustive assignment — delete the branch. Do not lower the threshold.

Svelte compiles text interpolation into update branches that only run on re-render, so a
component tested only with fresh renders shows uncovered branches. A test that updates
props covers them, and is worth having on its own merits.

## `npm` reports `401 Unauthorized` for `@steven-cutting/biscuit-games`

GitHub Packages authenticates every request, including a read of a public package, and
refuses an unauthenticated one by naming the credential: `401 Unauthorized … authentication
token not provided`. That is the string to search a log for, and it is the common fault by
some distance.

On a laptop, `~/.npmrc` has no `//npm.pkg.github.com/:_authToken=` line, its placeholder was
never replaced, or its token has expired. [Develop locally](../how-to/develop-locally.md) has the line; a token that is
present but stale fails the same way, so re-issue it before looking anywhere else.

A `404 Not Found` for the same package is a different fault, and the order matters: the
request authenticated and then found nothing it was allowed to see. On a laptop that is a
token without `read:packages`. In continuous integration it is the package having stopped
granting this repository read access — a setting on the package, not on either repository.
A `401` or a `404` from a CI step that installs nothing is a third fault again. Only the
steps that install carry a token, so that step reached the registry without one: the
question is what in it made the request, not which credential it lacks.

## `just check` stops because Playwright cannot start Chromium

The story gate renders in a real browser, and the browser is in neither lockfile, so
`just sync` does not install it — `just sync` installs exactly what the lockfiles say. Run
`just storybook-browsers` once per machine, and again after the `playwright` pin moves. On
Linux, run `just storybook-browsers-deps` first. On a fresh clone `just initialize`
downloads the browser for you, but on Linux it only names `just storybook-browsers-deps`,
because that recipe asks for sudo, so that one is still yours to run.

## Tests fail on `localStorage`

It is not available. Node ships its own experimental `localStorage` that shadows the one
jsdom would provide and stays undefined.

This is not something to work around with a stub. Every adapter takes its platform object
as a defaulted argument — pass one in. See [Testing](../reference/testing.md).

## The site works locally but assets 404 once deployed

The base path. This game is a project site, served beneath the repository name rather
than at the root of its host, so serve it from there before concluding anything:

```console
BASE_PATH=/<repository name> just frontend-build
BASE_PATH=/<repository name> just preview
```

The second command matters as much as the first. A reproduction mounted at `/` cannot show
this fault at all: an asset referenced by an absolute path — the usual cause — resolves
there and returns 200. It has to sit on the base path. See
[Configuration](../reference/configuration.md).

## A deployed change is not visible, or an old URL still serves the old body

The CDN, not the deployment. GitHub Pages serves HTML with `cache-control: max-age=600`, so
for ten minutes a page can keep answering with what it held before the deploy — with the
`age` header climbing towards 600 to say so.

**The cache key ignores the query string**, so appending `?cachebust=1` proves nothing: it
returns the same cached body. To read the current behaviour, request a path that has never
been requested before and check that the response says `age: 0`.

## The Pages deployment fails with a 404

`Failed to create deployment (status: 404)`, with the build job green and its artefact
uploaded. Pages has not been switched to the GitHub Actions source in the repository
settings. The workflow cannot do that for itself; see
[Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md).

## Something works under `just dev` but not in the build

Prerendering. Module-scope work runs in Node at build time as well as in the browser, and
the build's run is what the generated page holds — so a value computed there is the same
for every visitor until hydration computes it again, and a browser object read there does
not exist while the page is generated. Anything that must vary per visitor has to happen
in the browser, after hydration.

## Related pages

- [Test and debug](../how-to/test-and-debug.md)
- [Quality gates](../reference/quality-gates.md)
- [Maintenance](maintenance.md)
