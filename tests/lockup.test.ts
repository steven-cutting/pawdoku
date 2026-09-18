// tests/lockup.test.ts
import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { GAME_NAME } from '../src/lib/brand';
import Lockup from '../src/lib/components/Lockup.svelte';

describe('Lockup', () => {
  // Two assertions because neither holds the claim alone: a text query matches
  // an element's own text nodes, so the words are found whether or not the
  // mark beside them is hidden. The mark is held silent on its own.
  it('names this game after the platform, with the mark silent', () => {
    render(Lockup, {});

    expect(screen.getByText('b')).toHaveAttribute('aria-hidden', 'true');
    expect(screen.getByText(/biscuit/).textContent).toBe(`biscuit games / ${GAME_NAME}`);
  });
});
