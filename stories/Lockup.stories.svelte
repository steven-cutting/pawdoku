<script module lang="ts">
  import { HeaderBar } from '@steven-cutting/biscuit-games';
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import { expect, fn, within } from 'storybook/test';

  import { GAME_NAME } from '../src/lib/brand';
  import Lockup from '../src/lib/components/Lockup.svelte';
  import { MINIMUM_TOUCH_TARGET, NARROWEST_SUPPORTED_WIDTH } from '../src/lib/config';

  // The gutters `.shell` gives the page at every width, so a frame here leaves
  // the header exactly the room the route does.
  const SHELL_GUTTER = '1rem';
  const FRAME_WIDTH = `${String(NARROWEST_SUPPORTED_WIDTH)}px`;
  const LOCKUP = `biscuit games / ${GAME_NAME}`;

  const OVERVIEW = [
    'This game’s lockup: the platform’s words and then its own, drawn by the platform’s',
    '`Wordmark` through its `product` prop. The route hands it to `HeaderBar` as the `brand`',
    'snippet, so the page’s only `h1` names the page rather than the platform alone.',
    '',
    'No governing surface — this is brand, decided upstream. The mark is `aria-hidden`: the',
    'words are the whole accessible text, which the first play holds.',
    '',
    'The second story is the evidence that the lockup meets the platform’s collapse contract,',
    'which is a class name and nothing else: `Wordmark` puts the words in an element of class',
    '`words`, so below about 26rem the header hides them and keeps the mark rather than',
    'overflowing a phone.'
  ].join('\n');

  const { Story } = defineMeta({
    title: 'Brand/Lockup',
    component: Lockup,
    tags: ['autodocs'],
    parameters: { docs: { description: { component: OVERVIEW } } }
  });

  // One action, so the narrow story has a control to measure and
  // MINIMUM_TOUCH_TARGET has a use; no chip, because this game has no state yet.
  const ACTIONS = [
    { icon: 'settings', label: 'Settings', popup: 'dialog', onclick: fn() }
  ] as const;
</script>

<Story
  name="Lockup"
  play={async ({ canvasElement }) => {
    const canvas = within(canvasElement);

    // Two assertions because neither holds the claim alone: a text query matches
    // an element's own text nodes, so the words are found whether or not the
    // mark beside them is hidden. The mark is held silent on its own.
    await expect(canvas.getByText('b')).toHaveAttribute('aria-hidden', 'true');
    await expect(canvas.getByText(/biscuit/).textContent).toBe(LOCKUP);
  }}
/>

<!--
  The lockup inside the platform's header, at the narrowest width the
  specification supports. This is where the collapse contract is proved: the
  platform hides an element of class `words` below about 26rem and leaves the
  mark, and it reaches into whatever the brand snippet drew to do it.
-->
<Story
  name="In the header at the narrowest supported width"
  parameters={{
    docs: { story: { inline: false } },
    /*
     * The collapse keys on the viewport (`max-width: 26rem`), and the story
     * run's default viewport is 1200px wide. Without this pin the play would
     * measure the uncollapsed header inside a narrow frame, and the state a
     * phone actually renders would be evidence nowhere.
     */
    viewport: {
      viewports: {
        narrowest: {
          name: 'Narrowest supported',
          styles: { width: FRAME_WIDTH, height: '568px' }
        }
      },
      defaultViewport: 'narrowest'
    }
  }}
  play={async ({ canvasElement }) => {
    // DirectManipulation.@invariant EveryControlIsAComfortableTarget
    const frame = canvasElement.querySelector<HTMLElement>('[data-frame]');

    if (frame === null) {
      throw new Error('This story has no frame to measure the header against');
    }

    await expect(frame.scrollWidth).toBeLessThanOrEqual(frame.clientWidth);

    for (const control of within(canvasElement).getAllByRole('button')) {
      const box = control.getBoundingClientRect();

      await expect(box.width).toBeGreaterThanOrEqual(MINIMUM_TOUCH_TARGET);
      await expect(box.height).toBeGreaterThanOrEqual(MINIMUM_TOUCH_TARGET);
    }

    // The words leave the layout here, not the accessibility tree: the page's
    // only h1 keeps its name when the lockup collapses to the mark.
    const heading = within(canvasElement).getByRole('heading', {
      level: 1,
      name: LOCKUP
    });

    /*
     * And they do leave it. Measured rather than read off a declaration,
     * because the box is what the viewport pin above decides: at the story
     * run's default 1200px the media query never matches, the words lay out at
     * their natural width, and every other assertion in this play passes
     * anyway — the frame does not overflow, the targets are whole, the heading
     * has its name. Without this line a pin that silently stopped applying
     * would leave the collapse evidence of nothing, and it is also what would
     * catch this lockup spelling the platform's class differently.
     */
    await expect(
      within(heading)
        .getByText(/^biscuit/)
        .getBoundingClientRect().width
    ).toBeLessThanOrEqual(1);
  }}
>
  {#snippet template()}
    <div data-frame style="inline-size: {FRAME_WIDTH}; padding-inline: {SHELL_GUTTER}">
      <HeaderBar actions={ACTIONS}>
        {#snippet brand()}
          <Lockup />
        {/snippet}
      </HeaderBar>
    </div>
  {/snippet}
</Story>

<Story
  name="Dark theme"
  globals={{ theme: 'dark' }}
  parameters={{ docs: { story: { inline: false } } }}
  play={async () => {
    await expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
  }}
/>
