---
title: "Decision 0008: The design system arrives as a package"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_design_system_as_a_package]
requires: []
---

# Decision 0008: The design system arrives as a package

*Carried from Poodl's decision 0013 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

The hub, `steven-cutting/biscuit_games`, decides how Biscuit Games looks and publishes it as
`@steven-cutting/biscuit-games`. The package carries the stylesheet and the typefaces; the
chrome every game wears — `HeaderBar`, `Wordmark`, `Monogram`, `Announcer`, `Modal`,
`Notice`, `Button`, `IconButton`, `Tile`, `Key`, `Keyboard`, `PhysicalKeyboard` and the
rest of the components it exports; the preferences and keys ports with their fakes; and
the three specification modules `appearance.allium`, `operation.allium` and
`play-surfaces.allium`.

Poodl ported a copy of the design system in first and replaced it with the package once
the hub existed. Its record explains what the copy cost: every copy was correct on the day
it was made and unverifiable from the next, and by then its specifications restated ten of
the platform's clauses, one of which the platform had reworded three times since the port.
Nothing anywhere compared the two, and nothing would have.

This game starts with the package and has nothing to delete.

## Decision

Install the package at an exact version, and restate only what this game has a surface for.

- **Installed exactly.** The version `package.json` pins, no caret, matching invariant 4.
  GitHub Packages authenticates every read, so a committed `.npmrc` names the registry for
  the scope and holds no token; the token is a contributor's own in `~/.npmrc`, and in CI
  it is `github.token`, the one GitHub mints for the run, granted `packages: read`.
- **The platform's figures are restated by name.** The six figures the platform's modules
  state live in `src/lib/config.ts`, this game's root module states them by name, and
  `tests/platformSpecs.test.ts` holds both equal to the text the package ships.
- **The restated clauses take the platform's words**, and the same test holds them there. A
  clause this game restates word for word is listed in `tests/restated.ts` and compared
  with the platform's text on every run.
- **The workshop composes the platform's**, which costs gate 6 a network request; see
  [Quality gates](../reference/quality-gates.md).
- **One page points outward.** [The platform upstream](../project/platform.md) is where
  this handbook hands a reader to the hub, and it is the only page here that does.

## Consequences

**A first run needs a credential.** There is no anonymous install, and the registry answers
an unauthenticated read by naming the package rather than the missing token — a 404 that
sends a reader to look for the wrong fault. That is the honest price of the mechanism, and
it is written down where a first run meets it, including the troubleshooting page.

**A build here can fail because of something that happened there.** That is the point:
drift becomes a version number in a lockfile rather than a difference nobody can see. What
it costs is that a platform release nobody has read can break this repository's gate, and
the gate is the only thing that will ever say this game is behind.

**The platform's clauses are not this game's to word.** Amending one means a change
upstream and a version bump here. That is a real loss of local authority, taken
deliberately: the alternative is two specifications with the same clause names and
different meanings, which is what Poodl had before it took the package.

**The cross-repository links rot silently.** Nothing offline checks them, and
`just check-links-online` is monthly and manual.

## What would reopen this

A contributor the token scheme cannot serve. A component, a token or a clause this game
needs and the platform will not take. The platform publishing its handbook, which would
turn the citations into something a package carries.

## Related pages

- [The platform upstream](../project/platform.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Quality gates](../reference/quality-gates.md)
- [Testing](../reference/testing.md)
