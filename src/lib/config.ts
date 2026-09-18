/**
 * Values the specifications declare in their `config` blocks.
 *
 * These are the only numbers in the implementation that a specification also
 * states, so they live in one place and are named after the spec parameter
 * they mirror. Changing one here without changing it in `docs/specs/` is drift.
 *
 * All six are the platform's, stated in the modules
 * `@steven-cutting/biscuit-games` ships and restated by name in this game's
 * root module. `tests/platformSpecs.test.ts` holds this file, that module and
 * the shipped text equal. A figure this game alone states — an attempt count,
 * a board size — belongs below these, mirrored from the module that states it.
 */

/**
 * `appearance.allium` — `config.minimum_text_contrast` and
 * `config.minimum_boundary_contrast`, as WCAG 2.2 computes a ratio.
 *
 * The two AA bars: text against what is behind it, and anything that is not
 * text — a control's boundary, a state indicator — against what is adjacent
 * to it.
 */
export const MINIMUM_TEXT_CONTRAST = 4.5;
export const MINIMUM_BOUNDARY_CONTRAST = 3.0;

/**
 * `operation.allium` — `config.minimum_touch_target`, in CSS pixels.
 *
 * Across a control, in both directions, for
 * `DirectManipulation.EveryControlIsAComfortableTarget`. That invariant names
 * the two shapes it cannot be met in and says what each owes instead, rather
 * than stating a size alone.
 */
export const MINIMUM_TOUCH_TARGET = 44;

/**
 * `operation.allium` — `config.narrowest_supported_width`, in CSS pixels.
 *
 * The narrowest viewport the game is playable on without scrolling sideways,
 * which is the width every target and spacing figure has to survive.
 */
export const NARROWEST_SUPPORTED_WIDTH = 320;

/**
 * `play-surfaces.allium` — `config.minimum_state_separation`.
 *
 * How far a cell nothing is known about sits from one that has been marked.
 * No standard supplies this figure, because standards ask a colour to stand
 * off its background rather than off another state, and marks sit side by side.
 */
export const MINIMUM_STATE_SEPARATION = 3.0;

/**
 * `play-surfaces.allium` — `config.minimum_mark_separation`.
 *
 * How far absent sits from exact, and that pair only. Lower than the figure
 * above deliberately: four states 3 to one apart would need a range of 27 to
 * one, which no palette has. The specification's own reasoning for the gap is
 * worth reading before either number is touched.
 */
export const MINIMUM_MARK_SEPARATION = 2.0;
