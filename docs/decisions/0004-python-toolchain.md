---
title: "Decision 0004: A Python toolchain in a frontend repository"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_python_toolchain]
requires: []
---

# Decision 0004: A Python toolchain in a frontend repository

*Carried from Poodl's decision 0004 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

This game ships no Python. The hook gate it inherits runs on `prek` under `uv`, and the
documentation and agent contracts are enforced by two Python checkers. A frontend
repository could avoid Python entirely by moving the hook runner to a Node equivalent and
rewriting both validators in TypeScript.

## Decision

Keep the Python toolchain. `pyproject.toml` declares a virtual project — `package = false`
— whose dependencies are `prek`, `ruff` and `biscuit-games-tooling`, each pinned exactly
and locked in `uv.lock`. The first two are tools; the third is the package whose console
scripts are the checkers themselves, pinned to a release tag of
`steven-cutting/biscuit_games_tooling`.

Ruff is added on top of the inherited gate list so that Python this game adds is linted in
a repository that gates everything else. None ships today: the checkers moved into the
package, and `scripts/` holds the first-run script and the browser preflight.

## Consequences

Contributors need `uv` as well as Node, and both have to be installed before
`just initialize`, which runs each of them to lock and install its own dependencies.
Neither the application nor the published site contains any Python.

The two contracts stay as they are, rather than being rewritten and re-debugged. That is
most of the value: `bg-validate-docs` and `bg-validate-agents` come from a working
implementation, so their behaviour is known rather than newly invented. Every game runs
the same release of them, and a fix arrives as a moved pin rather than as an edit merged
into each copy.

`prek` brings pinned third-party hooks with it — `typos`, `lychee`, `shellcheck`,
`actionlint`, `ripsecrets`, `editorconfig-checker` — each locked to a commit SHA. Assembling
an equivalent set on Node would be a project in itself.

The cost is an extra toolchain to install, keep current, and explain. It is accepted
deliberately rather than by drift.

## What would reopen this

A Node-native hook runner with the same pinned-hook ecosystem, or the two validators
becoming so simple that rewriting them is cheaper than keeping Python around. Either would
have to replace the whole package, not only the two validators, because the allium
installer and runner and the gate runner are in it as well.

## Related pages

- [Quality gates](../reference/quality-gates.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
