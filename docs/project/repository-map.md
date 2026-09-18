---
title: "Repository map"
kind: "project"
audience: [contributor, maintainer, agent]
canonical_for: [repository_layout]
requires: []
---

# Repository map

The application sits at the repository root. There is no `frontend/` directory because
there is no backend to be a sibling of.

```text
.
├── AGENTS.md            Engineering conventions and the agent working agreement
├── Justfile             Every supported command
├── package.json         The application: Svelte, SvelteKit, Vite, Vitest
├── pyproject.toml       Repository tooling only: prek, ruff and the checkers
├── .npmrc               Scopes @steven-cutting to GitHub Packages; holds no token
├── .copier-answers.yml  What the template was told; read by copier update
├── src/
│   ├── app.html         The page shell
│   ├── lib/
│   │   ├── brand.ts     The one place this game's name is written
│   │   ├── components/  PascalCase Svelte components
│   │   ├── config.ts    The values the specifications declare
│   │   └── ports/       Every side effect, each with an in-memory fake
│   └── routes/          SvelteKit routes, prerendered
├── tests/               Vitest suites, never colocated with src/
├── stories/             Svelte CSF stories, one per component
├── static/              Copied verbatim into the build
├── scripts/             The first-run script and the browser preflight
├── docs/                This handbook, plus specs/
├── .agents/skills/      Canonical agent procedures
└── .storybook/          The component workshop, served and built locally
```

## What each part is responsible for

| Directory | Responsibility |
| --- | --- |
| `src/lib/ports/` | The only place a browser global is touched. Each port exports an interface, a real adapter, and a fake. |
| `src/lib/brand.ts` | The one place this game's name is written; every component, story and test reads it from here. |
| `src/lib/` (the rest) | Pure behaviour this game adds, in directories of its own beside these. Given the same input it returns the same output, always. |
| `src/lib/components/` | Rendering and interaction. Components take callbacks as props and hold no application state of their own. |
| `src/routes/` | Assembling components into pages, and the only place a store is built. Prerendered, so nothing here may assume a request. |
| `tests/` | Vitest suites named for what they cover, not for the file they mirror. |
| `stories/` | Every state of a component, as something that can be looked at. Rendered in Chromium with axe over each. |
| `scripts/` | `initialize.sh` and `check_playwright_browsers.js`. The two validators, the allium installer and runner, the gate runner and the ripsecrets wrapper are console scripts of `biscuit-games-tooling`, pinned in `pyproject.toml`. |
| `docs/specs/` | The Allium specifications. Behaviour is decided here, not in code. |
| `.storybook/` | The workshop's configuration. Served locally, and built both by the gate, which discards it, and by `just chromatic`, which publishes it. |

Which of these may import which is not a matter of taste; see
[Layering and dependency direction](../explanation/layering.md).

## Related pages

- [Architecture](../explanation/architecture.md)
- [Commands](../reference/commands.md)
