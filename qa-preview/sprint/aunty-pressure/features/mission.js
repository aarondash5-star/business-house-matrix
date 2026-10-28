export function createFeatureEngine({ onState } = {}) {
  const INITIAL = { value: 0, tier: 'CLEAR', dodges: 0, hits: 0, processedWave: 0 };
  const THRESHOLDS = [0, 1, 3, 5];
  const NAMES = ['CLEAR', 'WATCHED', 'CHASED', 'ALERT'];
  let state = { ...INITIAL };
  function tierFor(v) {
    let t = 0;
    for (let i = 0; i < THRESHOLDS.length; i++) {
      if (v >= THRESHOLDS[i]) t = i;
    }
    return NAMES[t];
  }
  function emit() {
    const copy = { ...state };
    if (typeof onState === 'function') onState(copy);
    return copy;
  }
  function apply(evt) {
    if (!evt || typeof evt !== 'object') return;
    if (evt.wave !== state.processedWave + 1) return;
    if (evt.lastOutcome !== 'dodge' && evt.lastOutcome !== 'hit') return;
    if (evt.lastOutcome === 'dodge') {
      state.dodges += 1;
      state.value = Math.min(5, state.value + 1);
    } else {
      state.hits += 1;
      state.value = Math.max(0, state.value - 2);
    }
    state.processedWave = evt.wave;
    state.tier = tierFor(state.value);
    emit();
  }
  function reset() {
    state = { ...INITIAL };
    emit();
  }
  function snapshot() {
    return { ...state };
  }
  emit();
  return { apply, reset, snapshot };
}

