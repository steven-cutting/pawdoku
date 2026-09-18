/**
 * What this game is called, wherever the platform asks for a name.
 *
 * `GAME_NAME` is the words the lockup shows after the platform's own:
 * `Wordmark`'s `product` prop renders "biscuit games / <GAME_NAME>", and the
 * page's only `h1` reads exactly that. `GAME_TITLE` is the document title and
 * `GAME_DESCRIPTION` its description.
 *
 * A file of its own rather than lines in `config.ts`, because `config.ts`
 * holds only figures a specification also states, and because this is the
 * one place the name is written: every component, story and test reads it
 * from here. This file is the game's; a template update never touches it.
 */
export const GAME_NAME = 'pawdoku';
export const GAME_TITLE = 'Pawdoku';
export const GAME_DESCRIPTION = 'A sudoku puzzle game for Biscuit Games.';
