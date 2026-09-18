import { readdirSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';

import { platformFile, platformPath } from './platform';
import { RESTATED } from './restated';
import {
  MINIMUM_BOUNDARY_CONTRAST,
  MINIMUM_MARK_SEPARATION,
  MINIMUM_STATE_SEPARATION,
  MINIMUM_TEXT_CONTRAST,
  MINIMUM_TOUCH_TARGET,
  NARROWEST_SUPPORTED_WIDTH
} from '../src/lib/config';

/*
 * The clauses this game restates from the platform's specifications, held
 * equal to the text the platform ships, and the figures the platform states,
 * held equal to `src/lib/config.ts` and to every module under `docs/specs/`
 * that states one.
 *
 * Nothing else anywhere compares the two. Allium has no cross-repository
 * import, and putting a module inside `node_modules` does not give it one:
 * `just check-specs` reads this game's modules alone and the hub's gate reads
 * its three, and both stay green while the clauses drift apart. Only a person
 * diffing the texts side by side would notice, which is to say nobody would.
 *
 * It is meant to be over-sensitive. A reworded comma fails it, and that failure
 * is the one moment somebody is required to say whether the platform's meaning
 * moved. When it did, the clause is amended in the hub and taken here as a
 * version — never reworded here, which is what the failure is for.
 *
 * It compares clauses by the surface or contract that states them, not by name.
 * `FullyKeyboardOperable` is stated once by the platform, for its own
 * `Operation` surface, and a game may state it under several surfaces of its
 * own, each with the wording that surface needs. A register keyed by bare name
 * would compare one of those to the platform's and demand the rest be reworded.
 *
 * Which clauses are restated is the game's to say, in `tests/restated.ts`. A
 * fresh game restates none, and this file still holds the figures.
 */

/** How a clause body reads once the shape of the comment is taken off it. */
function flatten(body: readonly string[]): string {
  return body
    .map((line) => line.trim().replace(/^--[ ]?/u, ''))
    .join(' ')
    .replace(/\s+/gu, ' ')
    .trim();
}

/**
 * Every clause in a module, by the surface or contract stating it and its name.
 *
 * A body runs to the first line that is not a comment. The platform separates
 * the paragraphs of its longer clauses with lines that are exactly `--`, which
 * are part of the body and not the end of it.
 */
function clauses(text: string): Map<string, string> {
  const found = new Map<string, string>();
  const lines = text.split('\n');
  let scope = '';

  for (const [index, line] of lines.entries()) {
    const opens = /^[ \t]*(?:surface|contract)[ \t]+(?<name>\w+)[ \t]*\{/u.exec(line);

    if (opens?.groups?.['name'] !== undefined) {
      scope = opens.groups['name'];
      continue;
    }

    const clause = /^[ \t]*@(?:guarantee|invariant)[ \t]+(?<name>\w+)[ \t]*$/u.exec(line);

    if (clause?.groups?.['name'] === undefined) {
      continue;
    }

    const body: string[] = [];

    for (const following of lines.slice(index + 1)) {
      if (!following.trim().startsWith('--')) {
        break;
      }
      body.push(following);
    }

    found.set(`${scope}.${clause.groups['name']}`, flatten(body));
  }

  return found;
}

/** Every figure a `config` block states as a number. `Duration` is not one. */
function figures(text: string): Map<string, number> {
  const found = new Map<string, number>();
  const pattern =
    /^[ \t]*(?<name>\w+)[ \t]*:[ \t]*(?:Integer|Decimal)[ \t]*=[ \t]*(?<value>[0-9.]+)/gmu;

  for (const match of text.matchAll(pattern)) {
    if (match.groups?.['name'] !== undefined && match.groups['value'] !== undefined) {
      found.set(match.groups['name'], Number(match.groups['value']));
    }
  }

  return found;
}

const SPECS = resolve(process.cwd(), 'docs', 'specs');

/** Every module this game keeps, at any depth, which is what `just check-specs` reads. */
function gameModules(): string[] {
  return readdirSync(SPECS, { encoding: 'utf8', recursive: true })
    .filter((name) => name.endsWith('.allium'))
    .sort();
}

function gameModule(name: string): string {
  return readFileSync(resolve(SPECS, name), 'utf8');
}

/** The root module, named after this game as `package.json` is. */
function rootModule(): string {
  const { name } = JSON.parse(readFileSync(resolve(process.cwd(), 'package.json'), 'utf8')) as {
    name: string;
  };

  return `${name}.allium`;
}

/** Which platform module states each figure, and what `config.ts` mirrors it as. */
const FIGURES = [
  { figure: 'minimum_text_contrast', module: 'appearance.allium', mirrored: MINIMUM_TEXT_CONTRAST },
  {
    figure: 'minimum_boundary_contrast',
    module: 'appearance.allium',
    mirrored: MINIMUM_BOUNDARY_CONTRAST
  },
  { figure: 'minimum_touch_target', module: 'operation.allium', mirrored: MINIMUM_TOUCH_TARGET },
  {
    figure: 'narrowest_supported_width',
    module: 'operation.allium',
    mirrored: NARROWEST_SUPPORTED_WIDTH
  },
  {
    figure: 'minimum_state_separation',
    module: 'play-surfaces.allium',
    mirrored: MINIMUM_STATE_SEPARATION
  },
  {
    figure: 'minimum_mark_separation',
    module: 'play-surfaces.allium',
    mirrored: MINIMUM_MARK_SEPARATION
  }
] as const;

const MODULES = ['appearance.allium', 'operation.allium', 'play-surfaces.allium'] as const;

describe('the platform specifications this game restates', () => {
  it.each(MODULES)('reads %s from the installed package', (module) => {
    expect(platformPath(`specs/${module}`)).toContain('node_modules');
  });

  it.each(RESTATED.flatMap((entry) => entry.clauses.map((name) => ({ ...entry, name }))))(
    '$file states $name exactly as $module does',
    ({ module, theirs, file, ours, alias, name }) => {
      const platform = clauses(platformFile(`specs/${module}`)).get(`${theirs}.${name}`);
      const restated = clauses(gameModule(file)).get(`${ours}.${name}`);

      expect(platform, `${module} no longer states ${theirs}.${name}`).toBeDefined();
      expect(restated, `${file} no longer states ${ours}.${name}`).toBeDefined();
      expect(
        alias === null ? restated : (restated ?? '').replaceAll(`${alias}/config.`, 'config.')
      ).toBe(platform);
    }
  );

  it.each(FIGURES)('agrees with $module on config.$figure', ({ figure, module, mirrored }) => {
    const platform = figures(platformFile(`specs/${module}`)).get(figure);
    const root = rootModule();

    expect(platform, `${module} no longer states ${figure}`).toBeDefined();
    expect(mirrored, `src/lib/config.ts disagrees with ${module} on ${figure}`).toBe(platform);
    // The root module states every platform figure. Another module states one
    // only where it has a surface for it, and every module that states one
    // states the same value.
    expect(
      figures(gameModule(root)).get(figure),
      `${root} no longer states ${figure}`
    ).toBeDefined();
    for (const name of gameModules()) {
      const stated = figures(gameModule(name)).get(figure);
      if (stated !== undefined) {
        expect(stated, `${name} disagrees with ${module} on ${figure}`).toBe(platform);
      }
    }
  });

  /*
   * The version is what makes drift visible, and a lockfile alone would not
   * say it: this asserts the tree these comparisons just read is the one
   * `package.json` pins, so a stale `node_modules` reports itself rather than
   * quietly proving the wrong thing.
   */
  it('reads the version package.json pins', () => {
    const installed = JSON.parse(platformFile('package.json')) as { version: string };
    const pinned = JSON.parse(readFileSync(resolve(process.cwd(), 'package.json'), 'utf8')) as {
      dependencies: Record<string, string>;
    };

    expect(pinned.dependencies['@steven-cutting/biscuit-games']).toBe(installed.version);
  });
});
