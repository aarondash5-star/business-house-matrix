export function createHudPresenter({ root }) {
  const laneNames = ['LEFT', 'CENTER', 'RIGHT'];
  const pad = (n, l) => String(n).padStart(l, '0');
  const hearts = (h) => (h <= 0 ? '—' : '♥ '.repeat(h).trim());
  const el = (id) => root.getElementById(id);
  const game = el('game');
  const hazardLane = el('hazard-lane');
  const encScore = el('enc-score');
  const encHearts = el('enc-hearts');
  const encWave = el('enc-wave');
  const goNext = el('go-next');
  function render(state) {
    if (!game || !hazardLane || !encScore || !encHearts || !encWave || !goNext) return;
    const h = Math.max(0, Math.min(2, state.hazard | 0));
    hazardLane.textContent = laneNames[h];
    hazardLane.setAttribute('aria-label', 'Hazard lane: ' + laneNames[h]);
    encScore.textContent = pad(state.score, 3);
    const heartsText = hearts(state.hearts);
    encHearts.textContent = heartsText;
    encHearts.setAttribute('aria-label', 'Hearts remaining: ' + state.hearts);
    encWave.textContent = pad(state.wave + 1, 2);
    game.dataset.gameOver = String(!!state.gameOver);
    goNext.disabled = !!state.gameOver;
  }
  function dispose() {}
  return { render, dispose };
}

