---
title: "Decision 0006: Visual review in Chromatic"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_visual_review]
requires: []
---

# Decision 0006: Visual review in Chromatic

*Carried from Poodl's decision 0008 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*

## Context

[Decision 0005](0005-component-workshop.md) built the workshop and gates it. What the
gate answers is a question about rules: axe says whether a rule is met. A rendered
pixel answers a different question, whether the thing looks right, and that question
has no local answer that survives being forgotten. Headless Chromium reports a light
preference, so a dark-theme defect can stay green in the gate and be caught only by
a person flipping a toolbar control, which is how Poodl found one. A workshop of many
stories is also more than anyone re-opens by hand after a change to a stylesheet.

## Decision

Publish the workshop to Chromatic for visual review.

`chromatic` is a pinned devDependency, `chromatic.config.json` names the build script and
the two behaviours below, and `just chromatic` is the only way it is ever run — locally or
in CI, which is what keeps
[the rule that nothing in CI runs a command you cannot run yourself](../reference/quality-gates.md)
true. The Chromatic GitHub Action was not used: it would be a second, separately versioned
copy of logic the pinned dependency already holds, and its documented `@latest` reference
cannot satisfy this repository's SHA pinning.

The recipe sits outside `just check`, beside `check-links-online`, because it needs a
token. Gate 6 composes the platform's published workshop through a `refs` entry and
fetches its address while it builds, so `just check` does reach the network — but it
needs no token and cannot fail on the request. [Quality gates](../reference/quality-gates.md)
owns the list of gates.

`.github/workflows/chromatic.yml` has two entry points, and they do different jobs:

- **A push to `main` sets the baseline.** `autoAcceptChanges` is scoped to that branch, so
  what merges becomes what later builds are measured against. Without it the baseline would
  be the last *accepted* build, nothing would ever be accepted, and every build would
  accumulate the same growing diff against a frozen ancestor.
- **A `/chromatic` comment on a pull request publishes that branch for review.** This is
  where a change is actually looked at. It is deliberately a thing you ask for: most pushes
  do not touch a component, and every snapshot is a real cost. It publishes for a commenter
  whose effective repository permission is write or better, and only a head branch in this
  repository; a fork's pull request is refused rather than published.

A detected change reports and passes. Chromatic is not a required check. A missing token
is not a failure either. When `CHROMATIC_PROJECT_TOKEN` is not set on the repository, a
step notes its absence, the publish step is skipped, and the reply on a pull request says
that no build was published; the run passes. A rendered game therefore does not fail its
first push for a secret it has not created, and creating one is the whole of switching
visual review on.

## Consequences

The question no local tool can answer now has somewhere to be answered, and the answer is a
link on the pull request rather than an intention to look later.

**A third party now holds renders of the interface.** This game collects nothing and stores
nothing remotely, and that is still true of the product; it is no longer true of the
development toolchain. The renders contain no data about anyone — they are the components,
in states a story pins — but the claim in
[the security model](../explanation/security-model.md) had to be narrowed from *there are
no credentials* to *there are none in the product*, which is a smaller claim honestly
stated.

**The repository has its first secret.** `CHROMATIC_PROJECT_TOKEN` lives as a GitHub
Actions secret and is read from the environment. It is written into no file here, which is
why `just chromatic` fails rather than publishing when it is missing, and why a contributor
has to set it up rather than finding it already working.

**A regression that reaches `main` is accepted silently.** That is the direct cost of
auto-accepting there. The review gate is the pull request comment and there is no other, so
a change nobody asked to see becomes the baseline it should have been compared against. The
alternative — a human accepting every `main` build in Chromatic's own interface — was
rejected as a step that would be skipped, leaving a baseline that quietly stopped moving.

**The comment trigger is a manual step someone has to remember**, and it does nothing until
this file's workflow is on the default branch, because GitHub runs `issue_comment` from
there. The pull request that introduces it cannot trigger itself.

**`issue_comment` is a known privilege-escalation shape, so a fork's pull request gets no
visual review.** Two questions have to be answered before the token is in reach, and only
one of them is about the person. Who asked is settled by querying the commenter's effective
repository permission and requiring write or better. `author_association` decides nothing,
because it reports a relationship rather than a permission and an organization member or a
triage-level collaborator would pass a check on it; it survives as a prefilter on the job
only because it is a superset of write access, so a stranger cannot start a runner. Whose
code runs is settled by refusing a cross-repository head, because `just sync` runs the
head's `package.json` lifecycle scripts, and a maintainer deciding after reading the diff
is judgement, not isolation. Both are settled in a job that checks nothing out and holds no
secret.

The workflow holds `pull-requests: write` as well as `issues: write`, because a comment on
a pull request sits on `issues/*` endpoints but is weighed against the pull request. The
acknowledging reaction and the closing reply are best-effort: neither is the build, and a
note about a published build must not colour it red.

The cost is that a contributor without write access cannot see their own change rendered,
and neither can anyone reviewing it. On a repository with one author that is a cost nobody
pays. It is the first thing to revisit if that changes: publishing a fork under Chromatic's
`owner:branch` form would fix the baseline half of the problem, but the token half needs
the build to stop being the thing that holds the token.

**The workshop is built twice on a push to `main`** — once by the `stories` job, which
proves it and throws it away, and once by Chromatic, which publishes it. That is a minute
of duplicated work kept on purpose, so that a red gate and a published baseline stay
independent of each other.

**The branch name is resolved by hand in the workflow, and the resolution has to hold.** An
`issue_comment` run reports `GITHUB_REF` as the default branch, so without `--branch-name`
a review build would file itself under `main` and be auto-accepted as the baseline it was
meant to be compared against. The step asserts a non-empty name rather than falling back,
and refuses one that is `main` outright — with cross-repository heads already refused there
is no legitimate way for that name to arrive, and the check costs a line.

TurboSnap (`--only-changed`) is not enabled. It would cut the snapshot count sharply, but
it depends on the builder's dependency graph and adds a way for the comparison to be wrong
rather than merely slow. It is the obvious thing to reach for when the count starts to
matter.

## What would reopen this

The snapshot count outgrowing what the plan allows, which would make TurboSnap the next
decision rather than a deferred one. Chromatic's pricing or ownership changing. Or the same
thing that would reopen 0005: the surfaces getting built and the workshop being deleted,
which takes its visual review with it.

## Related pages

- [Decision 0005: A component workshop](0005-component-workshop.md)
- [Work in the component workshop](../how-to/work-in-the-component-workshop.md)
- [Quality gates](../reference/quality-gates.md)
- [Security model](../explanation/security-model.md)
