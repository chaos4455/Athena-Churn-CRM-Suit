const theme = {
  init() {
    const saved = localStorage.getItem('athena-theme') || 'light';
    this.apply(saved);
  },
  apply(mode) {
    const dark = mode === 'dark';
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('athena-theme', mode);
    const icon = document.getElementById('theme-icon');
    if (icon) icon.className = dark ? 'ph ph-sun' : 'ph ph-moon';
  },
  toggle() {
    const isDark = document.documentElement.classList.contains('dark');
    this.apply(isDark ? 'light' : 'dark');
  },
};

window.theme = theme;
