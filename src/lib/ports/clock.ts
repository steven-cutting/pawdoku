/**
 * The current moment, in milliseconds since the epoch.
 *
 * A specification reads `now` when something starts and when it ends. A test
 * that has to wait real seconds to watch a countdown expire is not a test
 * worth having, so time arrives through a port.
 */
export interface ClockPort {
  now(): number;
}

/** The system clock. The source is an argument so tests never stub a global. */
export function createSystemClock(source: () => number = Date.now): ClockPort {
  return { now: () => source() };
}

/** A clock a test can move. It never advances on its own. */
export interface FakeClock extends ClockPort {
  advance(milliseconds: number): void;
  set(moment: number): void;
}

export function createFakeClock(start = 0): FakeClock {
  let moment = start;
  return {
    now: () => moment,
    advance: (milliseconds) => {
      moment += milliseconds;
    },
    set: (next) => {
      moment = next;
    }
  };
}
