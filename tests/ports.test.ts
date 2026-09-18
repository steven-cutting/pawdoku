import { describe, expect, it } from 'vitest';

import { createFakeClock, createSystemClock } from '../src/lib/ports/clock';
import { createCryptoRandom, createFakeRandom } from '../src/lib/ports/random';
import { createFakeStorage, createWebStorage, deviceStore } from '../src/lib/ports/storage';

/**
 * A working `Storage`, supplied to the adapter as an argument.
 *
 * jsdom exposes no `localStorage` under Node 26 — Node's own experimental
 * global shadows it and stays undefined without `--localstorage-file`. That
 * costs nothing here: the adapter takes its backing store as a parameter, so
 * the real code path is exercised without a browser and without stubbing a
 * global.
 */
function memoryStorage(): Storage {
  const entries = new Map<string, string>();
  return {
    get length(): number {
      return entries.size;
    },
    clear: () => {
      entries.clear();
    },
    getItem: (key: string) => entries.get(key) ?? null,
    key: (index: number) => [...entries.keys()][index] ?? null,
    removeItem: (key: string) => {
      entries.delete(key);
    },
    setItem: (key: string, value: string) => {
      entries.set(key, value);
    }
  };
}

/** A Storage whose every operation fails, as Safari's private mode does. */
function unusableStorage(): Storage {
  const refuse = (): never => {
    throw new Error('storage is unavailable');
  };
  return {
    get length(): number {
      return 0;
    },
    clear: refuse,
    getItem: refuse,
    key: refuse,
    removeItem: refuse,
    setItem: refuse
  };
}

/** A random source that hands out the given words in order. */
function sequenceSource(values: readonly number[]): Pick<Crypto, 'getRandomValues'> {
  let position = 0;
  return {
    getRandomValues<Target extends ArrayBufferView | null>(target: Target): Target {
      if (target instanceof Uint32Array) {
        target[0] = values[position] ?? 0;
        position += 1;
      }
      return target;
    }
  };
}

describe('storage port', () => {
  it('round-trips a value through the browser store', () => {
    const storage = createWebStorage(memoryStorage());

    expect(storage.read('game:game')).toBeNull();
    storage.write('game:game', '{"mode":"random"}');
    expect(storage.read('game:game')).toBe('{"mode":"random"}');

    storage.remove('game:game');
    expect(storage.read('game:game')).toBeNull();
  });

  it('stays usable where there is no store at all', () => {
    // The ambient default, in an environment that provides nothing. Losing
    // persistence must not cost the player the game.
    const storage = createWebStorage();

    expect(() => {
      storage.write('game:game', 'anything');
    }).not.toThrow();
    expect(storage.read('game:game')).toBeNull();
  });

  /*
   * Where the origin is opaque or the player has blocked site data, reading
   * `localStorage` throws rather than returning something unusable — which is
   * why the read cannot sit in a default argument. Nothing above this port sees
   * it: the page has to start.
   */
  it('stays usable where the store refuses to be read at all', () => {
    const storage = createWebStorage(
      deviceStore(() => {
        throw new DOMException('The operation is insecure.', 'SecurityError');
      })
    );

    expect(() => {
      storage.write('game:game', 'anything');
    }).not.toThrow();
    expect(storage.read('game:game')).toBeNull();
  });

  it('keeps working when the store refuses every operation', () => {
    const storage = createWebStorage(unusableStorage());

    expect(() => {
      storage.write('game:game', 'anything');
    }).not.toThrow();
    expect(() => {
      storage.remove('game:game');
    }).not.toThrow();
    expect(storage.read('game:game')).toBeNull();
  });

  it('offers the same contract in memory', () => {
    const storage = createFakeStorage({ 'game:settings': '{"hardMode":true}' });

    expect(storage.read('game:settings')).toBe('{"hardMode":true}');
    expect(storage.read('game:missing')).toBeNull();

    storage.write('game:settings', '{"hardMode":false}');
    expect(storage.read('game:settings')).toBe('{"hardMode":false}');

    storage.remove('game:settings');
    expect(storage.read('game:settings')).toBeNull();
  });

  it('starts empty when given nothing', () => {
    const storage = createFakeStorage();

    expect(storage.read('game:settings')).toBeNull();
  });
});

describe('random port', () => {
  it('draws from the platform source', () => {
    const random = createCryptoRandom(sequenceSource([7]));

    expect(random.uniformChoice(['a', 'b', 'c'])).toBe('b');
  });

  it('rejects a draw that would bias the low indices', () => {
    // With three candidates the top value of the 32-bit range has no partner,
    // so it is discarded and the next draw is used instead.
    const random = createCryptoRandom(sequenceSource([0xff_ff_ff_ff, 7]));

    expect(random.uniformChoice(['a', 'b', 'c'])).toBe('b');
  });

  it('uses the real platform source by default', () => {
    const random = createCryptoRandom();

    expect(['a', 'b', 'c']).toContain(random.uniformChoice(['a', 'b', 'c']));
  });

  it('walks a fixed sequence in tests, cycling when it runs out', () => {
    const random = createFakeRandom([2, 0]);
    const items = ['a', 'b', 'c'];

    expect(random.uniformChoice(items)).toBe('c');
    expect(random.uniformChoice(items)).toBe('a');
    expect(random.uniformChoice(items)).toBe('c');
  });

  it('wraps an offset that overruns the collection', () => {
    expect(createFakeRandom([4]).uniformChoice(['a', 'b', 'c'])).toBe('b');
    expect(createFakeRandom([]).uniformChoice(['a', 'b'])).toBe('a');
  });

  it('refuses to draw from nothing', () => {
    expect(() => createFakeRandom().uniformChoice([])).toThrow(/at least one candidate/);
    expect(() => createCryptoRandom(sequenceSource([0])).uniformChoice([])).toThrow(
      /at least one candidate/
    );
  });
});

describe('clock port', () => {
  it('reads the supplied time source', () => {
    expect(createSystemClock(() => 1_234).now()).toBe(1_234);
  });

  it('reads the system clock by default', () => {
    expect(createSystemClock().now()).toBeGreaterThan(0);
  });

  it('only moves when a test moves it', () => {
    const clock = createFakeClock(1_000);

    expect(clock.now()).toBe(1_000);
    clock.advance(5_000);
    expect(clock.now()).toBe(6_000);
    clock.set(0);
    expect(clock.now()).toBe(0);
  });

  it('starts at the epoch by default', () => {
    expect(createFakeClock().now()).toBe(0);
  });
});
