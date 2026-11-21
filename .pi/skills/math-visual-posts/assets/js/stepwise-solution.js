/* Progressive enhancement for math solution steps.
 * Without JS, every proof step remains visible and readable.
 * Copy into a post only when progressive disclosure actually helps learning.
 */
(() => {
  for (const root of document.querySelectorAll('[data-solution-stepper]')) {
    const steps = [...root.querySelectorAll('[data-solution-step]')];
    const controls = root.querySelector('[data-stepper-controls]');
    const prev = root.querySelector('[data-stepper-prev]');
    const next = root.querySelector('[data-stepper-next]');
    const all = root.querySelector('[data-stepper-all]');
    const status = root.querySelector('[data-stepper-status]');
    if (steps.length < 2 || !controls || !prev || !next || !all || !status) continue;

    let position = 0;
    let showAll = false;
    function render() {
      steps.forEach((step, i) => {
        step.hidden = !showAll && i !== position;
        step.setAttribute('aria-current', !showAll && i === position ? 'step' : 'false');
      });
      prev.disabled = showAll || position === 0;
      next.disabled = showAll || position === steps.length - 1;
      all.textContent = showAll ? '按步骤查看' : '展开全部步骤';
      all.setAttribute('aria-pressed', String(showAll));
      status.textContent = showAll
        ? '全部 ' + steps.length + ' 步已展开'
        : '第 ' + (position + 1) + ' / ' + steps.length + ' 步';
    }
    prev.addEventListener('click', () => {
      if (position > 0 && !showAll) { position -= 1; render(); }
    });
    next.addEventListener('click', () => {
      if (position < steps.length - 1 && !showAll) { position += 1; render(); }
    });
    all.addEventListener('click', () => { showAll = !showAll; render(); });
    // All proof content is already present in the original HTML.
    controls.hidden = false;
    render();
  }
})();
