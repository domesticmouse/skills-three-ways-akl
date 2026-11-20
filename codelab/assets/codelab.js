const STORAGE_KEY = 'skills-three-ways-codelab-v1';

let lastMessage = '';
const copyTimers = new WeakMap();

async function copy(button, target, command = '--copy') {
  const text = target.matches('input, textarea') ? target.value : target.innerText.trim();
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    report(button, true);
  } catch {
    report(button, false);
  }
}

function report(button, ok) {
  const tip = button.nextElementSibling;
  if (!tip) return;
  clearTimeout(copyTimers.get(button));
  button.removeAttribute('data-copied');
  button.removeAttribute('data-failed');

  let message = ok ? 'Copied' : 'Copy failed';
  if (message === lastMessage) {
    message += '\u00A0';
  }
  lastMessage = message;

  tip.textContent = '';
  void button.offsetWidth;
  button.setAttribute(ok ? 'data-copied' : 'data-failed', '');
  requestAnimationFrame(() => {
    tip.textContent = message;
  });

  copyTimers.set(
    button,
    setTimeout(() => {
      button.removeAttribute('data-copied');
      button.removeAttribute('data-failed');
      tip.textContent = '';
    }, 2000)
  );
}

// Invoker Commands (with single fallback path when CommandEvent is unsupported)
document.addEventListener(
  'command',
  (event) => {
    if (typeof event.command === 'string' && event.command.startsWith('--copy')) {
      copy(event.source, event.target, event.command);
    }
  },
  true
);

if (!('CommandEvent' in window)) {
  document.addEventListener('click', (event) => {
    const button = event.target.closest('button[command^="--copy"]');
    if (!button) return;
    const targetId = button.getAttribute('commandfor');
    const target = targetId ? document.getElementById(targetId) : null;
    if (target) {
      copy(button, target, button.getAttribute('command') || '--copy');
    }
  });
}

function loadState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { completedSteps: [], checks: {} };
    const parsed = JSON.parse(raw);
    return {
      completedSteps: Array.isArray(parsed.completedSteps) ? parsed.completedSteps : [],
      checks: parsed.checks && typeof parsed.checks === 'object' ? parsed.checks : {},
    };
  } catch {
    return { completedSteps: [], checks: {} };
  }
}

function saveState(state) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch {
    // Ignore storage quota or private browsing errors
  }
}

function announceStatus(message) {
  const region = document.getElementById('codelab-status');
  if (!region) return;
  region.textContent = '';
  requestAnimationFrame(() => {
    region.textContent = message;
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const panels = Array.from(document.querySelectorAll('.step-panel'));
  const navLinks = Array.from(document.querySelectorAll('.step-nav-link'));
  const checkboxes = Array.from(document.querySelectorAll('.checklist input[type="checkbox"]'));
  const progressBar = document.getElementById('lab-progress');
  const progressText = document.getElementById('progress-text');
  const resetButton = document.getElementById('reset-progress-btn');

  let state = loadState();

  function syncProgressUi() {
    const completedSet = new Set(state.completedSteps);
    for (const link of navLinks) {
      const targetId = link.dataset.stepTarget;
      link.classList.toggle('is-completed', Boolean(targetId && completedSet.has(targetId)));
    }
    for (const panel of panels) {
      const stepId = panel.dataset.stepId;
      const completeBtn = panel.querySelector('[data-complete-step]');
      if (!completeBtn || !stepId) continue;
      const done = completedSet.has(stepId);
      const nextId = completeBtn.dataset.nextStep;
      const stepIdx = panel.dataset.stepIndex;
      if (nextId) {
        completeBtn.textContent = done
          ? `Lab ${stepIdx} Complete — Next →`
          : `Mark Lab ${stepIdx} Complete & Next →`;
      } else {
        completeBtn.textContent = done ? `Lab ${stepIdx} Completed ✓` : `Mark Lab ${stepIdx} Complete`;
      }
    }
    for (const box of checkboxes) {
      const checkId = box.dataset.checkId;
      if (checkId) {
        box.checked = Boolean(state.checks[checkId]);
      }
    }
    const count = completedSet.size;
    if (progressBar) {
      progressBar.value = count;
    }
    if (progressText) {
      progressText.textContent = `${count} of ${panels.length} labs complete`;
    }
  }

  function showStep(stepId, { moveFocus = false, updateHash = false } = {}) {
    const targetPanel = panels.find((panel) => panel.id === stepId) || panels[0];
    if (!targetPanel) return;

    for (const panel of panels) {
      panel.hidden = panel !== targetPanel;
    }
    for (const link of navLinks) {
      if (link.dataset.stepTarget === targetPanel.id) {
        link.setAttribute('aria-current', 'step');
      } else {
        link.removeAttribute('aria-current');
      }
    }

    const stepIndex = targetPanel.dataset.stepIndex || '0';
    const stepTitle = targetPanel.dataset.stepTitle || 'Skills Three Ways';
    document.title = `Lab ${stepIndex}: ${stepTitle} | Skills Three Ways Codelab`;

    if (updateHash && window.location.hash !== `#${targetPanel.id}`) {
      history.pushState(null, '', `#${targetPanel.id}`);
    }

    if (moveFocus) {
      window.scrollTo({ top: 0, behavior: 'auto' });
      const heading = targetPanel.querySelector('h1[tabindex="-1"]');
      if (heading) {
        heading.focus({ preventScroll: true });
      }
    }
  }

  for (const link of document.querySelectorAll('[data-step-target]')) {
    link.addEventListener('click', (event) => {
      const targetId = link.dataset.stepTarget;
      if (!targetId) return;
      event.preventDefault();
      showStep(targetId, { moveFocus: true, updateHash: true });
    });
  }

  for (const btn of document.querySelectorAll('[data-complete-step]')) {
    btn.addEventListener('click', () => {
      const stepId = btn.dataset.completeStep;
      const nextStepId = btn.dataset.nextStep;
      if (!stepId) return;
      if (!state.completedSteps.includes(stepId)) {
        state.completedSteps.push(stepId);
        saveState(state);
        syncProgressUi();
      }
      if (nextStepId) {
        announceStatus(`Marked ${stepId} complete. Moving to ${nextStepId}.`);
        showStep(nextStepId, { moveFocus: true, updateHash: true });
      } else {
        announceStatus('All labs marked complete. Well done!');
      }
    });
  }

  for (const box of checkboxes) {
    box.addEventListener('change', () => {
      const checkId = box.dataset.checkId;
      if (!checkId) return;
      state.checks[checkId] = box.checked;
      saveState(state);
    });
  }

  if (resetButton) {
    resetButton.addEventListener('click', () => {
      state = { completedSteps: [], checks: {} };
      saveState(state);
      syncProgressUi();
      announceStatus('Codelab progress reset.');
    });
  }

  window.addEventListener('hashchange', () => {
    const hashId = window.location.hash.replace(/^#/, '');
    if (hashId) {
      showStep(hashId, { moveFocus: true, updateHash: false });
    }
  });

  syncProgressUi();
  const initialHash = window.location.hash.replace(/^#/, '');
  showStep(initialHash || panels[0]?.id || 'step-0', { moveFocus: false, updateHash: false });
});
