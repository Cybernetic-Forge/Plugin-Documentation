(function () {
  const key = 'cybernetic-forge-theme';
  const root = document.documentElement;

  function applyTheme(theme) {
    root.setAttribute('data-cf-theme', theme);
    if (toggle) {
      toggle.textContent = theme === 'light' ? 'Switch To Dark' : 'Switch To Light';
      toggle.setAttribute('aria-label', toggle.textContent);
    }
  }

  function resolvePreferredTheme() {
    const saved = localStorage.getItem(key);
    if (saved === 'light' || saved === 'dark') {
      return saved;
    }
    return 'dark';
  }

  function toggleTheme() {
    const next = root.getAttribute('data-cf-theme') === 'light' ? 'dark' : 'light';
    localStorage.setItem(key, next);
    applyTheme(next);
  }

  const toggle = document.createElement('button');
  toggle.className = 'cf-theme-toggle';
  toggle.type = 'button';
  toggle.addEventListener('click', toggleTheme);

  const mount = () => {
    if (!document.body || document.querySelector('.cf-theme-toggle')) {
      return;
    }
    document.body.appendChild(toggle);
    applyTheme(resolvePreferredTheme());
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();

