export function createFeedbackPresenter({ root }) {
  const game = root.getElementById('game');
  const msg = root.getElementById('game-message');
  function render(state) {
    if (!game || !msg) return;
    const outcome = state.gameOver ? 'game-over' : state.lastOutcome;
    game.dataset.outcome = outcome;
    let text;
    if (outcome === 'game-over') {
      text = 'The reception is over. Tap reset to play again and try a new dance.';
    } else if (outcome === 'dodge') {
      text = 'Nice dodge! You slipped past the hazard and kept the rhythm going.';
    } else if (outcome === 'hit') {
      text = 'Caught by the hazard! Aunty Radar noticed the stumble, but keep going.';
    } else {
      text = 'Ready for the next wave. Watch Aunty Radar and change lanes to dodge.';
    }
    msg.textContent = text;
    msg.setAttribute('role', 'status');
    msg.setAttribute('aria-live', 'polite');
  }
  function dispose() {}
  return { render, dispose };
}

