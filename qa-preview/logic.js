export function installDodgeControls({ container, leftButton, rightButton, restartButton, move, reset }) {
  const isEditable = (t) => t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
  const onKey = (e) => {
    if (isEditable(e.target)) return;
    const k = e.key;
    if (k === 'ArrowLeft' || k === 'a' || k === 'A') { e.preventDefault(); move(-1); }
    else if (k === 'ArrowRight' || k === 'd' || k === 'D') { e.preventDefault(); move(1); }
  };
  const onLeft = () => move(-1);
  const onRight = () => move(1);
  const onRestart = () => reset();
  let sx = 0, sy = 0;
  const onTouchStart = (e) => {
    if (e.touches.length !== 1) return;
    sx = e.touches[0].clientX;
    sy = e.touches[0].clientY;
  };
  const onTouchEnd = (e) => {
    if (e.changedTouches.length !== 1) return;
    const dx = e.changedTouches[0].clientX - sx;
    const dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) >= 45 && Math.abs(dx) > Math.abs(dy)) move(dx > 0 ? 1 : -1);
  };
  leftButton.addEventListener('click', onLeft);
  rightButton.addEventListener('click', onRight);
  restartButton.addEventListener('click', onRestart);
  window.addEventListener('keydown', onKey);
  container.addEventListener('touchstart', onTouchStart, { passive: true });
  container.addEventListener('touchend', onTouchEnd, { passive: true });
  return function dispose() {
    leftButton.removeEventListener('click', onLeft);
    rightButton.removeEventListener('click', onRight);
    restartButton.removeEventListener('click', onRestart);
    window.removeEventListener('keydown', onKey);
    container.removeEventListener('touchstart', onTouchStart);
    container.removeEventListener('touchend', onTouchEnd);
  };
}
