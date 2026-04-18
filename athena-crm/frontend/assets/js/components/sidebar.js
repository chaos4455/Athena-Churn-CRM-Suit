const sidebar = {
  init() {
    const toggle  = document.getElementById('sidebar-toggle');
    const el      = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    const open  = () => { el?.classList.add('open');    overlay?.classList.add('show'); };
    const close = () => { el?.classList.remove('open'); overlay?.classList.remove('show'); };

    toggle?.addEventListener('click', () => {
      el?.classList.contains('open') ? close() : open();
    });
    overlay?.addEventListener('click', close);

    // Close on nav link click (mobile)
    el?.querySelectorAll('.nav-link').forEach(a => {
      a.addEventListener('click', () => {
        if (window.innerWidth <= 768) close();
      });
    });
  },
};
window.sidebar = sidebar;
