#!/bin/sh
set -eu

project_root=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd -P)
cd "$project_root"

git rev-parse --is-inside-work-tree >/dev/null

uv lock
uv sync --frozen

npm install --package-lock-only --ignore-scripts --no-audit
npm ci --no-audit

# `just check` runs the story tests, so a first run has to leave the workspace
# able to reach a green gate. The browser lands in a per-user cache outside the
# repository. This is one of the two network downloads in the first-run path
# that no lockfile accounts for.
npm run storybook:browsers

# On Linux those binaries also need system libraries, which
# `just storybook-browsers-deps` installs through apt. It is named here rather
# than run: `playwright install-deps` says of itself that it "will ask for sudo
# permissions", and a first-run script that escalates without being asked is
# what the authorization rule in AGENTS.md exists to prevent. CI runs the recipe
# unconditionally; macOS has nothing to add.
if [ "$(uname -s)" = 'Linux' ]; then
    printf '%s\n' 'Linux: Chromium also needs system libraries.' >&2
    printf '%s\n' 'Run just storybook-browsers-deps once; it asks for sudo.' >&2
fi

# The other one. The Allium checker for docs/specs/, pinned and checksummed in
# the biscuit-games-tooling package that pyproject.toml pins, landing in the
# gitignored .tools/bin. `just check-specs` and `just analyse-specs` run it, and
# both the hook gate and `just check` run those, so a worktree without it cannot
# reach a green gate.
uv run --frozen bg-install-allium

# Formatting is normalised once here rather than leaving the first `just check`
# to fail on it.
uv run --frozen ruff check --fix-only .
uv run --frozen ruff format .
npm run lint:fix

# Hooks are installed only from the primary checkout. Every worktree of this
# repository shares one .git/hooks directory, and `prek install` writes a shim
# naming an absolute path into whichever worktree ran it — so a hook installed
# from a secondary worktree runs that worktree's virtual environment for commits
# made anywhere, and keeps doing so after the worktree is deleted, at which point
# every commit fails on a `prek` that is not on PATH. The comparison is the test
# git itself uses: in a secondary worktree the common directory and the git
# directory differ.
if [ "$(git rev-parse --git-common-dir)" = "$(git rev-parse --git-dir)" ]; then
    just install-hooks
else
    printf '%s\n' 'Secondary worktree: skipping install-hooks.' >&2
    printf '%s\n' 'Run just install-hooks once from the primary checkout.' >&2
fi

printf '\n%s\n' 'Ready. Next: just check.'
printf '%s\n' 'Nothing has been staged, committed, tagged, or pushed.'
