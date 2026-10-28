export function createFeaturePresenter({ root } = {}) {
  const r = root || document;
  let panel = r.querySelector('#sprint-feature-panel');
  let valueEl = r.querySelector('#sprint-value');
  let tierEl = r.querySelector('#sprint-tier');
  let dodgesEl = r.querySelector('#sprint-dodges');
  let hitsEl = r.querySelector('#sprint-hits');
  if (!panel) {
    panel = document.createElement('div');
    panel.id = 'sprint-feature-panel';
    panel.className = 'sprint-feature-panel';
    panel.setAttribute('role', 'status');
    panel.setAttribute('aria-live', 'polite');
    valueEl = document.createElement('span');
    valueEl.id = 'sprint-value';
    valueEl.className = 'sprint-value';
    tierEl = document.createElement('span');
    tierEl.id = 'sprint-tier';
    tierEl.className = 'sprint-tier';
    dodgesEl = document.createElement('span');
    dodgesEl.id = 'sprint-dodges';
    dodgesEl.className = 'sprint-dodges';
    hitsEl = document.createElement('span');
    hitsEl.id = 'sprint-hits';
    hitsEl.className = 'sprint-hits';
    panel.appendChild(valueEl);
    panel.appendChild(tierEl);
    panel.appendChild(dodgesEl);
    panel.appendChild(hitsEl);
    r.appendChild(panel);
  }
  function render(s) {
    if (!s || typeof s !== 'object') return;
    const v = Number.isFinite(s.value) ? s.value : 0;
    const tier = String(s.tier || 'CALM').toUpperCase();
    const d = Number.isFinite(s.dodges) ? s.dodges : 0;
    const h = Number.isFinite(s.hits) ? s.hits : 0;
    if (valueEl) valueEl.textContent = v + '/5';
    if (tierEl) tierEl.textContent = tier;
    if (dodgesEl) dodgesEl.textContent = d + ' DODGES';
    if (hitsEl) hitsEl.textContent = h + ' HITS';
    if (panel) {
      panel.dataset.tier = tier.toLowerCase();
      panel.setAttribute('aria-label', 'Momentum Meter: ' + v + ' of 5, tier ' + tier + ', ' + d + ' dodges, ' + h + ' hits');
    }
  }
  function dispose() {
    if (panel && panel.parentNode) panel.parentNode.removeChild(panel);
    panel = null;
    valueEl = null;
    tierEl = null;
    dodgesEl = null;
    hitsEl = null;
  }
  return { render, dispose };
}
