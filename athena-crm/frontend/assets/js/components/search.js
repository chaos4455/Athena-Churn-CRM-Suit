/* Busca global no header + utilitário de API de clientes. */
const search = {
  _cardsCache: null,

  async _cardsForFilter() {
    if (!this._cardsCache) {
      try {
        this._cardsCache = await api.getCards({ archived: false });
      } catch {
        this._cardsCache = [];
      }
    }
    return this._cardsCache;
  },

  /** Busca typeahead legada (callback com lista). */
  init(inputId, onResult) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener('input', utils.debounce(async (e) => {
      const q = e.target.value.trim();
      if (q.length < 2) { onResult([]); return; }
      try {
        const results = await api.getClients(q);
        onResult(results);
      } catch (err) { toast.error(err.message); }
    }, 350));
  },

  /** Barra do topo: clientes (API) + cards (filtro local sobre cache). */
  initGlobal() {
    const input = document.getElementById('global-search');
    const panel = document.getElementById('global-search-results');
    if (!input || !panel) return;

    const escapeHtml = (s) => String(s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/"/g, '&quot;');

    const hide = () => {
      panel.hidden = true;
      panel.innerHTML = '';
    };

    const showResults = (clients, cardHits) => {
      const rows = [];
      if (clients.length) {
        rows.push('<div class="global-search-section">Clientes</div>');
        clients.slice(0, 8).forEach((c) => {
          rows.push(
            `<a class="global-search-item" href="client-detail.html?id=${encodeURIComponent(c.id)}">` +
            `<span class="global-search-item-title">${escapeHtml(c.name)}</span>` +
            `<span class="global-search-item-meta">${escapeHtml(c.external_id || '')}</span></a>`
          );
        });
      }
      if (cardHits.length) {
        rows.push('<div class="global-search-section">Cards</div>');
        cardHits.forEach((c) => {
          const href = c.client_id
            ? `client-detail.html?id=${encodeURIComponent(c.client_id)}`
            : 'actions.html';
          rows.push(
            `<a class="global-search-item" href="${href}">` +
            `<span class="global-search-item-title">${escapeHtml(c.title || 'Card')}</span>` +
            `<span class="global-search-item-meta">${escapeHtml(c.client_name || '')}</span></a>`
          );
        });
      }
      if (!rows.length) {
        panel.innerHTML = '<div class="global-search-empty">Nenhum resultado</div>';
      } else {
        panel.innerHTML = rows.join('');
      }
      panel.hidden = false;
    };

    input.addEventListener('input', utils.debounce(async (e) => {
      const q = e.target.value.trim();
      if (q.length < 2) {
        hide();
        return;
      }
      try {
        const [clients, cards] = await Promise.all([
          api.getClients(q),
          this._cardsForFilter(),
        ]);
        const ql = q.toLowerCase();
        const cardHits = cards.filter((c) =>
          (c.title && c.title.toLowerCase().includes(ql)) ||
          (c.client_name && String(c.client_name).toLowerCase().includes(ql))
        ).slice(0, 8);
        showResults(clients || [], cardHits);
      } catch (err) {
        toast.error(err.message || 'Erro na busca');
      }
    }, 350));

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') hide();
    });

    document.addEventListener('click', (e) => {
      const wrap = input.closest('.header-search-wrap');
      if (wrap && !wrap.contains(e.target)) hide();
    });

    input.addEventListener('focus', () => {
      if (panel.innerHTML && !panel.hidden) return;
      if (input.value.trim().length >= 2) {
        input.dispatchEvent(new Event('input', { bubbles: true }));
      }
    });
  },
};
window.search = search;
