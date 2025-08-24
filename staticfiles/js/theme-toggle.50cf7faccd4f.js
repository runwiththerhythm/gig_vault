(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  if (!btn) return;
  function setTheme(next){ root.setAttribute('data-theme', next); localStorage.setItem('gv-theme', next); }
  btn.addEventListener('click', () => setTheme((root.getAttribute('data-theme')||'light') === 'dark' ? 'light' : 'dark'));
})();
