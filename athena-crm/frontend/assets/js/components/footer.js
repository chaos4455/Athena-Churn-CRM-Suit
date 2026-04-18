const footer = {
  init() {
    const el = document.getElementById('footer-year');
    if (el) el.textContent = new Date().getFullYear();
  },
};
window.footer = footer;
