---
title: "Deploy to GitHub Pages"
kind: "how-to"
audience: [maintainer, operator, agent]
canonical_for: [deployment_procedure]
requires: []
---

# Deploy to GitHub Pages

This game publishes to GitHub Pages from `.github/workflows/pages.yml` on every push to
`main`. Its one job calls `game-pages.yml` in `steven-cutting/biscuit_games_tooling`, at a
pinned release, which builds the static site and hands `build/` to the Pages deployment
action; nothing is committed to a branch.

The site is a project site, served at <https://steven-cutting.github.io/pawdoku/>: the repository
`steven-cutting/pawdoku`, beneath `/pawdoku/` on its owner's Pages host.

## One-time setup

A rendered repository starts from nothing, so both steps are done once, before the first
push that should deploy.

1. In the repository settings, under Pages, set the source to **GitHub Actions**. The
   workflow cannot do this for itself.
2. Grant this repository read access on the `@steven-cutting/biscuit-games` package, so
   that the build job's own token can install it. It is a setting on the package, not on
   either repository: on the package's page, open **Package settings**, choose
   **Add repository** under **Manage Actions access**, search for this repository,
   `steven-cutting/pawdoku`, and give it the **Read** role.

The template repository's `scripts/bootstrap_repo.sh` applies step 1 with `gh`, together
with the branch protection and the vulnerability-reporting setting the rest of this
handbook assumes. Run it from a checkout of the template before the first push; it also
prints step 2, which it cannot make, because no REST endpoint for that setting exists.

The deploy job names a `github-pages` environment, which needs no setup: GitHub creates it
on the first run that reaches that job.

Until step 2 is done, the build job fails at `npm ci` with `404 Not Found` for the package
and the deploy job never starts. Until step 1 is done, the build job succeeds and uploads
its artefact but the deploy job fails with `Failed to create deployment (status: 404)`,
even though the workflow itself is correct.

## Where the site is served from

A project site lives beneath the repository's name on the owner's Pages host, so the app is
built to live under `/pawdoku`. The workflow reads that name from the event that
triggered it rather than carrying it in the file, which keeps `pages.yml` the same in every
game and keeps `paths.base` in `svelte.config.js` from drifting away from the address Pages
serves. A custom domain is a later change to the repository settings and to nothing here;
[decision 0010](../decisions/0010-a-project-pages-site.md) records why the project site is
the starting point.

## What the workflow does

- Passes a slash and the repository name, read from the event, to the shared workflow as
  its `base_path` input, and the shared workflow sets `BASE_PATH` from it, so the build
  cannot drift from where Pages serves it.
- Builds with `npm run build`, which is `just frontend-build`.
- Uploads `build/` as the Pages artefact. `static/.nojekyll` rides along so Pages serves
  the underscore-prefixed `_app/` directory rather than treating it as a Jekyll internal.
- Deploys it in a second job that holds the `pages: write` and `id-token: write` scopes.
  The job that builds holds `contents: read` and `packages: read` and neither publishing
  scope, so the credential that installs and the credential that deploys never meet.

Deployments are serialised by a concurrency group and are never cancelled mid-flight: a
half-published site is worse than a slightly stale one.

## Reproduce a deployment locally

```console
BASE_PATH=/pawdoku just frontend-build
BASE_PATH=/pawdoku just preview
```

The base path goes on both commands, so the preview sits where Pages serves. See
[Configuration](../reference/configuration.md).

## Rolling back

Re-run the last good deployment from the Actions tab, or revert the commit and let the push
trigger a fresh build. There is no state to migrate and no cache to clear beyond the
browser's.

## Related pages

- [Decision 0010: A project Pages site](../decisions/0010-a-project-pages-site.md)
- [Architecture](../explanation/architecture.md)
- [Configuration](../reference/configuration.md)
- [Maintenance](../operations/maintenance.md)
