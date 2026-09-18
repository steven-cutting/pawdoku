import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve, sep } from 'node:path';

/**
 * The files `@steven-cutting/biscuit-games` ships, resolved the way a consumer
 * resolves them.
 *
 * Through the package's own `exports` subpaths rather than a path into
 * `node_modules`, so a file the package renames fails here rather than reading
 * as nothing. And through `createRequire` anchored at the project root rather
 * than at `import.meta.url`: under Vitest's SSR transform `import.meta.url` is
 * a served path rooted at `/`, and a resolver anchored there walks a
 * `node_modules` that does not exist.
 *
 * The `node_modules` assertion is the point of the file. A resolve that fell
 * back to a copy inside this repository would stay green while proving nothing
 * about the package this game actually installs, which is the one failure that
 * would make every test below meaningless without saying so.
 */
const PACKAGE = '@steven-cutting/biscuit-games';
const resolver = createRequire(resolve(process.cwd(), 'package.json'));

/** Where the package ships `subpath`, refusing anything outside `node_modules`. */
export function platformPath(subpath: string): string {
  const path = resolver.resolve(`${PACKAGE}/${subpath}`);

  if (!path.split(sep).includes('node_modules')) {
    throw new Error(`${PACKAGE}/${subpath} resolved outside node_modules: ${path}`);
  }

  return path;
}

/** What the package ships at `subpath`, as text. */
export function platformFile(subpath: string): string {
  return readFileSync(platformPath(subpath), 'utf8');
}

/** The three modules the package ships under `specs/`. */
export type PlatformModule = 'appearance.allium' | 'operation.allium' | 'play-surfaces.allium';

/**
 * A run of clauses this game restates from one platform module, word for word.
 *
 * `alias` is the `use` alias `file` reaches its config through when it reaches
 * another module's rather than its own — Poodl's `settings.allium` wrote
 * `game/config.` where the platform wrote `config.` — or null when no
 * normalisation is needed. `tests/restated.ts` holds the game's table.
 */
export interface Restatement {
  module: PlatformModule;
  theirs: string;
  file: string;
  ours: string;
  alias: string | null;
  clauses: readonly string[];
}
