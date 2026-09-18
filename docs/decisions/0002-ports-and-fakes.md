---
title: "Decision 0002: Side effects behind ports"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_ports_and_fakes]
requires: []
---

# Decision 0002: Side effects behind ports

*Carried from Poodl's decision 0002 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

The template this game's conventions descend from isolates its one side effect — the HTTP
API — behind a port with an in-memory fake, so components can be tested without a running
backend. This game has no API, but it has boundaries of its own. Three are here: device
storage, randomness and the clock. Two more — the device's preferences and its keyboard —
arrive as ports the platform package exports, each with the fake it ships.

Two of those are awkward to test directly. A specification that draws with
`uniform_choice` calls it the one deliberately non-deterministic step. A specification that
arms a countdown asks a test to wait real seconds, and a test that waits is not a test
worth having.

## Decision

Every side effect sits behind a port in `src/lib/ports/`. Each port is one file exporting
three things: an interface in the application's vocabulary, a real adapter, and an
in-memory fake. Real adapters take their platform object as a defaulted argument rather
than reading a global.

Tests inject fakes. Stubbing a global is banned.

## Consequences

The domain and the components are testable without a browser, and time and randomness
become ordinary values a test controls.

The defaulted-argument rule turned out to be load-bearing rather than stylistic. Under
Node 26 with jsdom there is no `localStorage` — Node's own experimental global shadows
jsdom's and stays undefined — and no `navigator.clipboard` at all. Code that read either
global directly would be untestable here. Because the adapters take theirs as arguments,
both real code paths still run under test.

There is a cost: three small indirections here and two in the package, for boundaries some
projects would touch directly, and a rule that has to be enforced by review because no
tool checks it.

## What would reopen this

Nothing foreseeable. The alternative — reaching for globals and stubbing them in tests —
was already unavailable in this environment before it was rejected on principle.

## Related pages

- [Layering and dependency direction](../explanation/layering.md)
- [Testing](../reference/testing.md)
