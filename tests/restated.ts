import type { Restatement } from './platform';

/*
 * What this game restates from the platform's specifications, and where.
 *
 * Empty until the game restates a clause. When a module under docs/specs/
 * copies a platform `@guarantee` or `@invariant` word for word — a contract it
 * fulfils, a surface it inherits — the copy is listed here, and
 * `tests/platformSpecs.test.ts` holds it equal to the text the package ships.
 * Poodl's table is the worked example: its `game.allium` restates
 * `operation.allium`'s `DirectManipulation` under the same name with no alias,
 * and its `settings.allium` restates `appearance.allium`'s `Appearance` through
 * the alias `game`.
 */
export const RESTATED: readonly Restatement[] = [];
