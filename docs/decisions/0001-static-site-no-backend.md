---
title: "Decision 0001: A static site with no backend"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_no_backend]
requires: []
---

# Decision 0001: A static site with no backend

*Carried from Poodl's decision 0001 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

This game is a single-player game with no accounts, no leaderboard and no shared state.
The conventions it inherits arrive by way of Poodl, and Poodl's came from a full-stack
template with a Python backend, a PostgreSQL database and a generated API client.

## Decision

Build a static site. SvelteKit with `@sveltejs/adapter-static`, every route prerendered,
published to GitHub Pages. Drop the backend half of the template entirely: no server, no
database, no API, no generated client, and no `frontend/` subdirectory to be a sibling of
something that does not exist.

## Consequences

Deployment is a directory of files. There is nothing to operate, nothing to scale,
nothing to patch between releases, and no secret to rotate. Hosting is free.

Whatever the game keeps in the browser — settings, statistics, a game in progress —
belongs to one browser on one device. Clearing browser data destroys it and nothing can
restore it. That is a real cost borne by the player.

Prerendering has teeth. Module-scope work runs once, at build time, in Node — so anything
per-visitor must happen in the browser after hydration, and a route that cannot be
rendered at build time fails the build rather than shipping.

The base path becomes configuration. A project site is served from a subdirectory,
so `BASE_PATH` is read at build time into `paths.base`. Where the value comes from,
and why no domain sits in front of it, is [Decision 0010](0010-a-project-pages-site.md).

## What would reopen this

Anything requiring shared state between players: accounts, a synchronised daily puzzle,
leaderboards, or statistics that follow a player between devices. Each of those needs a
server, and none is in scope — see
[Purpose and scope](../project/purpose-and-scope.md).

## Related pages

- [Architecture](../explanation/architecture.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
