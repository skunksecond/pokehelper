(function () {
  function requestClose() {
    const button = document.querySelector('.eontimer-exit-btn');
    if (button) {
      button.disabled = true;
      button.textContent = 'Closing…';
    }

    fetch('/eontimer/close', { method: 'GET' }).catch(() => {
      window.location.reload();
    });
  }

  function ensureExitButton() {
    if (document.querySelector('.eontimer-exit-btn')) {
      return;
    }

    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'eontimer-exit-btn';
    button.textContent = 'Return to menu';
    button.addEventListener('click', (event) => {
      event.preventDefault();
      requestClose();
    });

    document.body.appendChild(button);
  }

  document.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (key === 'escape' || key === 'q' || key === 'x') {
      event.preventDefault();
      requestClose();
    }
  });

  window.addEventListener('DOMContentLoaded', ensureExitButton);
  ensureExitButton();
})();
