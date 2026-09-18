---
title: "Architecture"
kind: "explanation"
audience: [contributor, maintainer, operator, agent]
canonical_for: [system_architecture]
requires: []
---

# Architecture

This game is a static site. The build produces a directory of files; a host serves them
unchanged; everything after that happens in the browser. There is no request the
application can make to itself, no session, and no origin it trusts.

That constraint is not a limitation working around a missing backend — it is the
architecture. See
[Decision 0001](../decisions/0001-static-site-no-backend.md).

## Build

SvelteKit with `@sveltejs/adapter-static`, prerendering every route. `+layout.ts` sets
`prerender = true` for the whole tree, so a route that could not be rendered at build
time fails the build rather than shipping broken.

Prerendering has one consequence worth stating plainly: **module-scope work runs twice,
once at build time in Node and again in each visitor's browser as the page hydrates.** The
build's run decides what the generated page holds. Anything that must differ per visitor —
drawing a random value, reading device storage, looking at the clock — would give the page
one answer and the browser another, and a browser object is not there to read in Node at
all, so it happens in the browser after hydration, not while the page is being generated.

The build is portable across base paths. SvelteKit emits relative asset URLs, and
`paths.base` is read from `BASE_PATH` at build time, which `pages.yml` sets from the
repository name, so a local build and the deployed build differ in that value alone.

## Runtime shape

```text
routes/           assembles the page, and is the only place a port is built
  └── components/ renders and handles interaction
        └── ports/   every side effect, behind an interface
```

`src/lib/config.ts` and `src/lib/brand.ts` sit beneath all three and import nothing.

The direction is one way and is described in
[Layering and dependency direction](layering.md).

There is no rules layer yet: the seed tree is a route, a lockup component and three
ports. When this game has rules, they belong in pure modules under `src/lib/` between the
components and the ports, fed their clock and randomness as arguments rather than
imports, so that the whole of the behaviour is testable without a browser.

## State

There is no server, so every piece of durable state lives in the browser. All of it is one
value, saved under one key with a schema version inside it, and read back defensively —
storage is somewhere other software can write, and somewhere an older release of this game
may already have written, so nothing found there is believed without being checked.

| State | Where it lives | Lost when |
| --- | --- | --- |
| Whatever this game keeps between visits, such as a game in progress or its settings | Device storage, through the storage port, under one key with a schema version inside it | Browser data is cleared |
| Whatever the game is saying at the moment | Nowhere at all | The page is reloaded |

## Side effects

Five things reach outside the pure core: storage, randomness, the clock, the device's
colour-scheme and reduced-motion preferences, and the device's keyboard. Each sits
behind a port with a real adapter and an in-memory fake, so the entire application
above them is testable without a browser. The first three are in `src/lib/ports/`; the
last two are the platform's and arrive from `@steven-cutting/biscuit-games`. A side
effect this game adds gets a port there in the same shape. The reasoning is in
[Decision 0002](../decisions/0002-ports-and-fakes.md).

## What is not here

No API, no database, no authentication, no background jobs, no telemetry. Those are not
deferred; they are out of scope, as this game's purpose-and-scope page records.

## Related pages

- [Layering and dependency direction](layering.md)
- [Security model](security-model.md)
- [Repository map](../project/repository-map.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
