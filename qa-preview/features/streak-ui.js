function pad(n) { const s = String(Math.max(0, Math.floor(n))); return s.length < 3 ? s.padStart(3, '0') : s; }
export function createStreakPresenter({ root } = {}) {
  if (!root) return { render() {}, dispose() {} };
  const panel = root.getElementById ? root.getElementById('streak-panel') : root.querySelector('#streak-panel');
  const count = root.getElementById ? root.getElementById('streak-count') : root.querySelector('#streak-count');
  const best = root.getElementById ? root.getElementById('streak-best') : root.querySelector('#streak-best');
  const bonus = root.getElementById ? root.getElementById('streak-bonus') : root.querySelector('#streak-bonus');
  const rank = root.getElementById ? root.getElementById('streak-rank') : root.querySelector('#streak-rank');
  function render(state) {
    if (!state || !panel) return;
    const streak = Number.isFinite(state.streak) ? state.streak : 0;
    const bestV = Number.isFinite(state.best) ? state.best : 0;
    const bonusV = Number.isFinite(state.bonus) ? state.bonus : 0;
    const rankV = typeof state.rank === 'string' ? state.rank : 'CALM';
    if (count) count.textContent = String(streak);
    if (best) best.textContent = String(bestV);
    if (bonus) bonus.textContent = '+' + pad(bonusV);
    if (rank) rank.textContent = rankV;
    panel.dataset.tier = rankV.toLowerCase();
    panel.setAttribute('aria-label', 'Streak ' + rankV + ': ' + streak + ' current, ' + bestV + ' best, bonus +' + pad(bonusV));
  }
  function dispose() {}
  return { render, dispose };
}
