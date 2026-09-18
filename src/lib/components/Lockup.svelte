<script lang="ts">
  import { Wordmark } from '@steven-cutting/biscuit-games';

  import { GAME_NAME } from '$lib/brand';

  /**
   * This game's lockup: the platform's words, and then its own.
   *
   * The platform's `Wordmark` draws it, given a `product`, so the display face,
   * the weight, the tracking and the `words` class `HeaderBar` reaches into
   * to collapse the words below about 26rem are all the platform's. The route
   * hands this to `HeaderBar` as its `brand` snippet, and the page's only `h1`
   * reads "biscuit games / <GAME_NAME>".
   *
   * No markup of its own and no `{#if}`: a component with a branch nothing
   * renders is a branch the coverage floor counts against the whole tree.
   */
</script>

<Wordmark product={GAME_NAME} />
