---
title: "Decision 0010: A project Pages site"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_project_pages_site]
requires: []
---

# Decision 0010: A project Pages site

## Context

GitHub Pages serves a project site at `<owner>.github.io/<repository>/`, with the account
lowercased in the host. Only a user site, or a site with a custom domain, is served from
the root of a domain.

Poodl's record on its address chose a domain of its own, with a landing page in front of
the game and a step that assembled the domain around the build. Its own reopening clause
was a second Biscuit Games game, because that shape put an address larger than the
repository inside it.

A rendered game has to publish on its first push, with no domain, no DNS records and
nothing to stage.

## Decision

This game is a project Pages site at `https://steven-cutting.github.io/pawdoku/`.

`.github/workflows/pages.yml` builds with `BASE_PATH=/<repository name>`, reading the name
from the workflow event as `github.event.repository.name`, and uploads `build/`. The file
is therefore identical in every game and never carries a name. `svelte.config.js` reads
`BASE_PATH` into `paths.base`, and it is empty locally. `static/.nojekyll` rides along so
that Pages serves `_app/`.

There is no custom domain. Adding one later is a change for this game alone, to the
repository settings and to `BASE_PATH` in the workflow, and it survives every update from
the template because the game changed those lines and the template did not.

## Consequences

**Two settings come before the first push.** The Pages source is set to GitHub Actions in
the repository settings; until it is, the build job succeeds and uploads its artefact but
the deploy job fails with `Failed to create deployment (status: 404)`. And the hub package
grants this repository read access, so that the build job's own token can install it.

**The address in this handbook is prose.** It is decided by the `repository` answer given
when the game was rendered, so a mismatch with the repository's real name is invisible to
every gate, while `pages.yml` stays correct because it reads the event. `uvx copier update`
asks the question again, with the recorded answer as its default, and that is how the
address is corrected.

**Every path the app builds goes through `paths.base`.** A link or an asset written from
the root works locally, where the base is empty, and breaks only once it is published
beneath the repository's name.

**Nothing outside `build/` is published.** There is no landing page, no second copy of a
stylesheet and no staging script to keep true.

## What would reopen this

A custom domain for this game. The platform serving its games beneath a domain of its own.

## Related pages

- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Configuration](../reference/configuration.md)
- [Decision 0001: A static site with no backend](0001-static-site-no-backend.md)
- [Decision 0009: Rendered from the template](0009-rendered-from-the-template.md)
