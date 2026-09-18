---
title: "Security model"
kind: "explanation"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [security_model]
requires: []
---

# Security model

This game has no server, no accounts and no data about anyone. That removes most of the
attack surface a web application usually has, and it is worth being precise about what
remains rather than claiming the problem away.

## What there is to protect

Very little, and that is the point.

- **Nothing is collected.** No analytics, no telemetry, no error reporting, no cookies.
  Nothing leaves the browser.
- **Nothing is stored remotely.** Whatever the game keeps, its settings and a game in
  progress, lives in device storage and is never uploaded. There is nowhere to upload them
  to.
- **There are no credentials in the product.** No sign-in, no tokens, nothing secret in
  the build or the bundle. The `ripsecrets` gate exists to keep it that way. The
  repository *stores* exactly one secret and it belongs to the toolchain, not to the game: a
  Chromatic project token, held as a GitHub Actions secret and read from the environment,
  written into no file here. A second credential is needed and stored nowhere: reading the
  design system from GitHub Packages takes a token carrying `read:packages`, which lives
  in each contributor's own `~/.npmrc` and, in continuous integration, is the token GitHub
  mints for the run and discards with it. The committed `.npmrc` names the registry for
  the `@steven-cutting` scope and holds nothing.

The practical consequence for a player is that clearing browser data destroys whatever
this game kept for them, irrecoverably. That is a real cost of the design, and the game's
own purpose-and-scope page is where it is stated.

## What is deliberately not secure

**Nothing prevents a player cheating themselves.** Whatever this game holds in memory or
in device storage, a player with developer tools can read. There is no opponent and no
leaderboard, so there is nobody to cheat but themselves.

## What the build defends

- **Supply chain.** Every dependency is pinned exactly and locked; `just lock-check`
  fails if a manifest and its lockfile disagree. GitHub Actions are pinned to commit
  SHAs, not to mutable tags. One dependency comes from GitHub Packages rather than the
  public registry, pinned and locked like the rest; the scope line in `.npmrc` is what
  keeps every other package on npmjs.
- **Workflow permissions.** CI runs with `contents: read` and `packages: read`, the second
  so the install can read the design system with the run's own token. Only the Pages
  deployment holds `pages: write` and `id-token: write`, and only Chromatic holds
  `issues: write` and `pull-requests: write`, which it needs to react to and answer the
  comment that summoned it: the endpoints are issue ones, but the comment sits on a pull
  request, and a token without the second was refused the reaction. Each lives in its own
  file so the scopes are visible rather than inherited.
- **The comment trigger.** `/chromatic` on a pull request starts a job holding the
  Chromatic token, and an `issue_comment` workflow always runs against the base
  repository with its secrets — including when the comment sits on a fork's pull request.
  Two checks stand between the comment and the token, and they answer different questions.
  *Who asked* is the commenter's effective repository permission, queried and required to
  be write or better. `author_association` is a prefilter and never the authority: it
  reports a relationship, so an organization member or a triage-level collaborator reports
  a value that sounds like authority and is not. It is worth keeping only because it is a
  superset of write access, which stops a stranger starting a runner at all.
  *Whose code runs* is the head repository: a
  cross-repository head is refused outright, because `just sync` would otherwise run that
  fork's install scripts beside the token, and a person deciding to type the word is not
  isolation. Both are settled in a job that checks nothing out and holds no Chromatic
  token, only the run's own, which it needs to read the commenter's permission and the
  pull request and to add the reaction; the publishing job does not start until they pass.
  What neither check does is make the head trustworthy. A head in this repository was
  pushed by someone holding write access, so the token sits inside that boundary and
  behind no narrower one; while `main` requires no review, the same person could land the
  same code and let the push run it beside the same token, and `/chromatic` is no
  escalation over that. What the word does mean is that typing it runs a branch's code,
  and a branch nobody has read is not one to type it on.
- **Credential leakage.** `ripsecrets` scans every commit, and its output is suppressed so
  a match never copies the matched value into a log.
- **Third-party content at runtime.** There is none. The site loads no external script,
  font, or image, so there is nothing to subvert between the host and the browser.

## What is out of scope

Denial of service against the host, GitHub's own infrastructure, and anything an attacker
can do to their own browser. There is no shared state, so nothing one visitor does can
affect another.

## Reporting

See `SECURITY.md` at the repository root.

## Related pages

- [Architecture](architecture.md)
- [Maintain dependencies](../how-to/maintain-dependencies.md)
- [Quality gates](../reference/quality-gates.md)
