const toast = {
  _container: null,
  _ensure() {
    if (!this._container) {
      this._container = document.createElement('div');
      this._container.className = 'toast-container';
      document.body.appendChild(this._container);
    }
  },
  show(message, type = 'info', duration = 3500) {
    this._ensure();
    const icons = { success: 'ph-check-circle', error: 'ph-x-circle', info: 'ph-info' };
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<i class="ph-fill ${icons[type] || icons.info}" style="font-size:1.1rem"></i><span>${message}</span>`;
    this._container.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(100%)'; t.style.transition = 'all .3s'; setTimeout(() => t.remove(), 300); }, duration);
  },
  success: (msg) => toast.show(msg, 'success'),
  error:   (msg) => toast.show(msg, 'error'),
  info:    (msg) => toast.show(msg, 'info'),
};
window.toast = toast;
