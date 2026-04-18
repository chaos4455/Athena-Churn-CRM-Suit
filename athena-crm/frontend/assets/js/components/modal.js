const modal = {
  open(id)  { document.getElementById(id)?.classList.add('open'); },
  close(id) { document.getElementById(id)?.classList.remove('open'); },
  closeAll() { document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open')); },
  confirm(message) { return window.confirm(message); },
};

// Close on overlay click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) modal.closeAll();
  if (e.target.classList.contains('modal-close'))   modal.closeAll();
});

window.modal = modal;
