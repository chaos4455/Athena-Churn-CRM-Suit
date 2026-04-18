// Simple hash-based router for SPA navigation
const router = {
  routes: {},
  register(hash, fn) { this.routes[hash] = fn; },
  navigate(hash) { window.location.hash = hash; },
  init() {
    window.addEventListener('hashchange', () => this._resolve());
    this._resolve();
  },
  _resolve() {
    const hash = window.location.hash || '#dashboard';
    const fn = this.routes[hash];
    if (fn) fn();
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === hash);
    });
  },
};

window.router = router;
