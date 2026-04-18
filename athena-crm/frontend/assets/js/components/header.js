const header = {
  init() {
    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) themeBtn.addEventListener('click', () => theme.toggle());
  },
};
window.header = header;
