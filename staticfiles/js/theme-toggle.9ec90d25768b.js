/* jshint esversion: 6, browser: true */

(function () {
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  if (!btn) return;

  function setTheme(next){
    root.setAttribute('data-theme', next);
    localStorage.setItem('gv-theme', next);
    btn.setAttribute('aria-pressed', String(next === 'dark'));
    btn.innerHTML = next === 'dark' ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
    // adjust button style for contrast
    btn.className = next === 'dark' ? 'btn btn-dark shadow rounded-pill' : 'btn btn-light shadow rounded-pill';
  }

  const current = root.getAttribute('data-theme') || 'light';
  setTheme(current);

  btn.addEventListener('click', () => {
    const cur = root.getAttribute('data-theme') || 'light';
    setTheme(cur === 'dark' ? 'light' : 'dark');
  });
})();
