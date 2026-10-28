export function createEncounterEngine({ onState }) {
  const pattern = [1, 0, 2, 1, 2, 0];
  const initialState = { playerLane: 1, hazard: 1, score: 0, hearts: 3, wave: 0, lastOutcome: 'ready', gameOver: false };
  let state = { ...initialState };

  const emit = () => {
    if (typeof onState === 'function') {
      onState({ ...state });
    }
  };

  const choose = (laneNumber) => {
    if (typeof laneNumber !== 'number' || !Number.isFinite(laneNumber)) return;
    const lane = Math.max(0, Math.min(2, Math.floor(laneNumber)));
    state.playerLane = lane;
    emit();
  };

  const advance = () => {
    if (state.gameOver) return;
    if (state.playerLane === state.hazard) {
      state.hearts -= 1;
      state.lastOutcome = 'hit';
      if (state.hearts <= 0) {
        state.hearts = 0;
        state.gameOver = true;
      }
    } else {
      state.score += 100;
      state.lastOutcome = 'dodge';
    }
    state.wave += 1;
    state.hazard = pattern[state.wave % 6];
    emit();
  };

  const reset = () => {
    state = { ...initialState };
    emit();
  };

  const snapshot = () => ({
    playerLane: state.playerLane,
    hazard: state.hazard,
    score: state.score,
    hearts: state.hearts,
    wave: state.wave,
    lastOutcome: state.lastOutcome,
    gameOver: state.gameOver
  });

  emit();

  return { choose, advance, reset, snapshot };
}
