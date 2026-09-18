---
title: "Configuration"
kind: "reference"
audience: [contributor, maintainer, operator, agent]
canonical_for: [configuration_reference]
requires: []
---

# Configuration

There is no runtime configuration. A static site has no process to configure, so
everything below is read at build time or is a fixed part of the source.

## Build-time environment

| Variable | Default | Effect |
| --- | --- | --- |
| `BASE_PATH` | empty | Where this game sits beneath its host, read into `paths.base`. The Pages workflow sets it to a slash followed by the repository name, from the workflow event, because a project site is served beneath that name; left empty for local builds. |

That is the whole list for the site. SvelteKit's `PUBLIC_` convention is available but
unused: a value baked into a public static bundle is not configuration, it is a constant,
and constants belong in source where they can be reviewed.

### The base path

`BASE_PATH` is read twice, not once. `svelte.config.js` reads it into `paths.base` for
the build, and the preview server reads it to decide where it mounts the output. So it
belongs on both commands that touch the deployment:

```console
BASE_PATH=/<repository name> just frontend-build
BASE_PATH=/<repository name> just preview
```

Build with it and preview without it and the site comes up at `/` rather than beneath the
repository name, which is not the path Pages serves, so the preview is not the
deployment.

Nothing announces the mistake. A prerendered page references its own assets relatively
(`./_app/…`), so it loads at either mount and no request 404s. Only a path written
absolutely by hand gives the fault away, and only when the preview sits on the
subdirectory. That is why the value has to be set deliberately rather than noticed.

## Tooling environment

One variable is read by a tool rather than by the build, and it never reaches the bundle.

| Variable | Read by | Effect |
| --- | --- | --- |
| `CHROMATIC_PROJECT_TOKEN` | `just chromatic` | Which Chromatic project the workshop publishes to. Export it locally; CI supplies it from the repository secret of the same name. Without it the recipe fails rather than publishing somewhere unexpected. |
| `NODE_AUTH_TOKEN` | npm, through the `.npmrc` `actions/setup-node` writes outside the checkout | The credential GitHub Packages demands for every read of `@steven-cutting/biscuit-games`. CI sets it from the run's own token on each step that installs, and on no other. Not read on a laptop, where the token is an `_authToken` line in `~/.npmrc`. |

It is the only secret this repository *stores*, and it is deliberately not written into a
file. The registry credential above is not stored either: per run in CI, and the
contributor's own on a laptop — see
[Security model](../explanation/security-model.md).

## Configuration files

| File | Governs |
| --- | --- |
| `svelte.config.js` | The static adapter, preprocessing, and the base path. |
| `vite.config.ts` | The dev server, the jsdom unit suite, and the coverage thresholds. |
| `vitest.config.ts` | Names both suites as projects and nothing else. It exists so the Storybook UI's test runner, which finds its configuration by filename, resolves the story project instead of failing on the unit one. |
| `tsconfig.json` | Strict TypeScript, plus `noUncheckedIndexedAccess`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `isolatedModules` and `checkJs`. |
| `eslint.config.js` | Flat config on `strictTypeChecked`, the Svelte and Storybook presets, and no rule overrides yet. |
| `.storybook/main.ts` | Where stories are found, which addons load, the SvelteKit framework, telemetry off, and the dev server's permission to serve `stories/`. |
| `.storybook/preview.ts` | The design tokens, the theme, contrast and motion toolbar globals, and the axe run applied to every story. |
| `vitest.storybook.config.ts` | The story run: browser mode, Chromium, axe. It declares no coverage block, and the run that measures the floor pins `vite.config.ts`, so a story cannot affect the number. |
| `chromatic.config.json` | Visual review: the build script to call, that a change reports rather than fails, and that `main` accepts its own changes as the new baseline. It holds no token. |
| `.prettierrc.json` | 100 columns, single quotes, no trailing commas, Svelte block order. |
| `.prettierignore` | Notably excludes Markdown, which markdownlint owns, and `.copier-answers.yml`, which Copier rewrites on every update. |
| `.markdownlint-cli2.jsonc` | Markdown rules, including the exemptions the documentation contract needs. |
| `.editorconfig` | Whitespace. LF, UTF-8, two spaces, four for the `Justfile` and the specifications. |
| `pyproject.toml` | The pinned Python tooling, Ruff's rules, and the `typos` exclusions. |
| `lychee.toml` | Link checking. |
| `.pre-commit-config.yaml` | The read-only gate. Installed as the hook. |
| `.pre-commit-fix.yaml` | The mutating counterpart. Run only by `just fix`. |

### Storybook appearance globals

Set from the workshop toolbar, or pinned by a story with a `globals` prop. The attributes
go on the preview document's root element, because the design system's stylesheet keys
every palette on `:root`.

| Global | Values | Effect |
| --- | --- | --- |
| `theme` | `system`, `light`, `dark` | `system` removes `data-theme` so the device preference decides; the other two set it. |
| `highContrast` | `off`, `on` | `on` sets `data-high-contrast="true"`, which swaps in the high-contrast palette. |
| `animations` | `on`, `off` | The animations setting. `on` sets `data-animations="on"` unless `reducedMotion` is `reduce`, because the device's preference wins over the setting; `off` removes the attribute. |
| `reducedMotion` | `follow`, `reduce` | `reduce` injects a stylesheet that freezes declarative motion. A simulation: nothing inside the page can change what `prefers-reduced-motion` reports. |

## Values the specifications decide

`src/lib/config.ts` mirrors the `config` blocks in `docs/specs/`. These are not tunables:
changing one here without changing it in the specification is drift. All six are the
platform's, stated in the modules `@steven-cutting/biscuit-games` ships and restated by
name in this game's root module; `tests/platformSpecs.test.ts` holds this file, that
module and the shipped text equal. A figure this game alone states belongs below these,
mirrored from the module that states it, and a constant that appears here without a
`config` entry to name is drift in the other direction.

| Constant | Value | Specification |
| --- | --- | --- |
| `MINIMUM_TEXT_CONTRAST` | 4.5 | `appearance.allium`, `config.minimum_text_contrast`, a contrast ratio |
| `MINIMUM_BOUNDARY_CONTRAST` | 3.0 | `appearance.allium`, `config.minimum_boundary_contrast`, a contrast ratio |
| `MINIMUM_TOUCH_TARGET` | 44 | `operation.allium`, `config.minimum_touch_target`, in CSS pixels |
| `NARROWEST_SUPPORTED_WIDTH` | 320 | `operation.allium`, `config.narrowest_supported_width`, in CSS pixels |
| `MINIMUM_STATE_SEPARATION` | 3.0 | `play-surfaces.allium`, `config.minimum_state_separation`, a contrast ratio |
| `MINIMUM_MARK_SEPARATION` | 2.0 | `play-surfaces.allium`, `config.minimum_mark_separation`, a contrast ratio |

`MINIMUM_TOUCH_TARGET` and `NARROWEST_SUPPORTED_WIDTH` are the two whose real consumer
is a stylesheet, and CSS cannot import a TypeScript constant. Both figures are written
out in the platform's stylesheet, so the story run is what holds this repository's
constants to them: it frames the header at `NARROWEST_SUPPORTED_WIDTH` and measures
every control there against `MINIMUM_TOUCH_TARGET`. The specification is held to the
platform's separately, by `tests/platformSpecs.test.ts`, so a figure that moved upstream
fails on the number rather than on the paint.

## Version pins

Exact versions, no ranges. Node and npm are additionally constrained by `engines` and
recorded in `volta` in `package.json`; Python by `.python-version`. See
[Maintain dependencies](../how-to/maintain-dependencies.md).

One dependency is outside that scheme. The browser the story run drives is a binary
Playwright downloads into a cache outside the repository; its version follows the
`playwright` pin and appears in neither lockfile.

## Related pages

- [Commands](commands.md)
- [Deploy to GitHub Pages](../how-to/deploy-to-github-pages.md)
- [Quality gates](quality-gates.md)
