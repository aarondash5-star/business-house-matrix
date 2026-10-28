const INITIAL = { streak: 0, best: 0, bonus: 0, rank: 'CALM', lastOutcome: 'ready', processedWave: 0 };
function rankFor(s) { if (s >= 3) return 'LEGEND'; if (s === 2) return 'FIRE'; if (s === 1) return 'SPARK'; return 'CALM'; }
function clone(s) { return { streak: s.streak, best: s.best, bonus: s.bonus, rank: s.rank, lastOutcome: s.lastOutcome, processedWave: s.processedWave }; }
export function createStreakEngine({ onState } = {}) {
  let state = clone(INITIAL);
  if (typeof onState === 'function') onState(clone(state));
  function apply(encounterState) {
    if (!encounterState || typeof encounterState !== 'object') return;
    const wave = encounterState.wave;
    const outcome = encounterState.lastOutcome;
    if (typeof wave !== 'number' || !Number.isFinite(wave) || wave < 0 || Math.floor(wave) !== wave) return;
    if (outcome !== 'dodge' && outcome !== 'hit') return;
    if (wave !== state.processedWave + 1) return;
    if (outcome === 'dodge') { state.streak += 1; state.best = Math.max(state.best, state.streak); state.bonus += state.streak * 25; } else { state.streak = 0; }
    state.rank = rankFor(state.streak);
    state.lastOutcome = outcome;
    state.processedWave = wave;
    if (typeof onState === 'function') onState(clone(state));
  }
  function reset() { state = clone(INITIAL); if (typeof onState === 'function') onState(clone(state)); }
  function snapshot() { return clone(state); }
  return { apply, reset, snapshot };
}
