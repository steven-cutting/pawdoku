---
title: "Layering and dependency direction"
kind: "explanation"
audience: [contributor, maintainer, agent]
canonical_for: [dependency_boundaries]
requires: []
---

# Layering and dependency direction

Three layers, and imports only ever run downwards.

| Layer | May import | Must not |
| --- | --- | --- |
| `src/routes/` | components, ports, brand, config, the platform package | be imported by anything below it |
| `src/lib/components/` | components, brand, config, platform components and types | import a port adapter or reach for a browser global |
| `src/lib/ports/` | config | import a component or a route |
| `@steven-cutting/biscuit-games` | nothing here | be copied back into `src/` |

`src/lib/config.ts` and `src/lib/brand.ts` sit below everything and import nothing. The
package is below every layer: it is a dependency, so anything may name it and it names
nothing here.

There is no rules layer yet. When this game has rules, they go in pure modules under
`src/lib/` between the components and the ports, and the components row already says what
a component may do with them: name a type, render a value, and call the callback it was
handed. A component may not construct a port, reach for a browser global, or keep a fact
the rules own as view state of its own.

## Why the direction matters

The rule is not tidiness. It is what makes the claim below true, and that claim is
load-bearing:

**Components are testable without the platform.** A component that read `localStorage`
directly could only be tested where `localStorage` exists. Under Node 26 and jsdom it does
not — Node's own experimental global shadows jsdom's and stays undefined. Because the
storage adapter takes its backing store as an argument, that costs nothing: the test
passes a store in, and the real code path still runs.

## Where a side effect goes

If something new needs the outside world, it needs a port. A port is three things in one
file:

1. An interface naming what the application needs, in the application's vocabulary.
2. A real adapter, with the platform object as a defaulted argument rather than a global
   read.
3. An in-memory fake with the same interface.

There are five, and three of them are here: storage, randomness and the clock. The
device's preferences and the device's keyboard are the platform's, taken from
`@steven-cutting/biscuit-games` with the fakes it ships, because what a surface reads
from a device is not one game's question.

Both of those take their platform object as an argument for the usual reason — jsdom
supplies a `window` without `matchMedia`, so the adapter has to answer for its absence
itself rather than being stubbed around — and a game's route is where all five are
constructed, because that is where a window exists.

The rule that follows: **tests inject fakes, they never stub globals.** A stubbed global
leaks between tests and hides the fact that the code reached outside its layer.

## Enforcement

There is no import-boundary checker here: a three-directory frontend does not earn the
machinery. The direction is enforced by review, by the `svelte-change` and `code-review`
skills, and by the shape of the tests: code in the wrong layer is usually code that is
hard to test.

## Related pages

- [Architecture](architecture.md)
- [Testing](../reference/testing.md)
- [Decision 0002](../decisions/0002-ports-and-fakes.md)
