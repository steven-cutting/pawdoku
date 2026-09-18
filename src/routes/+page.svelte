<script lang="ts">
  import { HeaderBar } from '@steven-cutting/biscuit-games';

  import { GAME_DESCRIPTION, GAME_TITLE } from '$lib/brand';
  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The whole application, assembled. Today that is the platform's chrome
   * carrying this game's lockup and a main landmark with nothing in it yet.
   *
   * Everything that differs per visitor — a stored game, the device
   * preferences, a token in the address bar — belongs after hydration, inside
   * `onMount`: `+layout.ts` prerenders every route, so module-scope work here
   * runs once in Node at build time. The three ports under `src/lib/ports/`
   * are built there when the game has a store to hand them to.
   *
   * Every selector below names an element or a class this markup carries,
   * because `svelte-check --fail-on-warnings` turns an unused selector into a
   * failed gate.
   */
</script>

<svelte:head>
  <title>{GAME_TITLE}</title>
  <meta name="description" content={GAME_DESCRIPTION} />
</svelte:head>

<div class="shell">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <p>Nothing to play yet. The board goes here.</p>
  </main>
</div>

<style>
  .shell {
    max-inline-size: var(--shell-max);
    margin-inline: auto;
    padding: 0 var(--shell-pad) var(--s-11);
  }

  main {
    padding-block-start: var(--s-6);
  }

  p {
    margin-block: 2rem;
    color: var(--text-2);
    text-align: center;
  }
</style>
