export function createFeaturePresenter({ root } = {}) {
  const scope = root || document;
  const panel = scope.querySelector('#sprint-feature-panel');
  const valueEl = scope.querySelector('#sprint-value');
  const tierEl = scope.querySelector('#sprint-tier');
  const dodgesEl = scope.querySelector('#sprint-dodges');
  const hitsEl = scope.querySelector('#sprint-hits');
  function render(s) {
    if (!s || !panel) return;
    const v = Number.isFinite(s.value) ? s.value : 0;
    const tier = String(s.tier || 'CLEAR').toUpperCase();
    const dodges = Number.isFinite(s.dodges) ? s.dodges : 0;
    const hits = Number.isFinite(s.hits) ? s.hits : 0;
    if (valueEl) valueEl.textContent = v + '/5';
    if (tierEl) tierEl.textContent = tier;
    if (dodgesEl) dodgesEl.textContent = dodges + ' DODGES';
    if (hitsEl) hitsEl.textContent = hits + ' HITS';
    panel.dataset.tier = tier.toLowerCase();
    panel.setAttribute('aria-label', 'Aunty Pressure ' + v + ' of 5, tier ' + tier + ', ' + dodges + ' dodges, ' + hits + ' hits');
  }
  function dispose() {}
  return { render, dispose };
}

