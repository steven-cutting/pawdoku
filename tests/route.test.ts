// tests/route.test.ts
import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { GAME_NAME, GAME_TITLE } from '../src/lib/brand';
import Page from '../src/routes/+page.svelte';

describe('the page', () => {
  it('carries the heading the platform header draws for this game', () => {
    render(Page);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      `biscuit games / ${GAME_NAME}`
    );
  });

  it('titles the document after the game', () => {
    render(Page);

    expect(document.title).toBe(GAME_TITLE);
  });

  it('has a main landmark to put the game in', () => {
    render(Page);

    expect(screen.getByRole('main')).toBeInTheDocument();
  });
});
