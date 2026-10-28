export function createFeatureEngine({ onState } = {}) {
  const INITIAL = { value: 0, tier: 'CALM', dodges: 0, hits: 0, processedWave: 0 };
  const THRESHOLDS = [0, 1, 3, 5];
  const NAMES = ['CALM', 'FOCUS', 'FLOW', 'ZEN'];
  let state = { ...INITIAL };
  function tierFor(v) {
    let t = 0;
    for (let i = 0; i < THRESHOLDS.length; i++) {
      if (v >= THRESHOLDS[i]) t = i;
    }
    return NAMES[t];
  }
  function notify() {
    if (typeof onState === 'function') onState({ ...state });
  }
  notify();
  return {
    apply(evt) {
      if (!evt || typeof evt !== 'object') return;
      const w = evt.wave;
      if (typeof w !== 'number' || !Number.isInteger(w)) return;
      if (w !== state.processedWave + 1) return;
      const o = evt.lastOutcome;
      if (o !== 'dodge' && o !== 'hit') return;
      if (o === 'dodge') {
        state.dodges += 1;
        state.value = Math.min(5, state.value + 1);
      } else {
        state.hits += 1;
        state.value = Math.max(0, state.value - 2);
      }
      state.processedWave = w;
      state.tier = tierFor(state.value);
      notify();
    },
    reset() {
      state = { ...INITIAL };
      notify();
    },
    snapshot() {
      return { ...state };
    }
  };
}
