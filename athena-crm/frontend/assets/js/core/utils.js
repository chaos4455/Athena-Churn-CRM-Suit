const utils = {
  fmt: {
    currency: (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0),
    number:   (v) => new Intl.NumberFormat('pt-BR').format(v || 0),
    date:     (v) => v ? new Date(v).toLocaleDateString('pt-BR') : '—',
    datetime: (v) => v ? new Date(v).toLocaleString('pt-BR') : '—',
    percent:  (v) => `${(v || 0).toFixed(1)}%`,
  },

  stageMeta: {
    backlog:        { label: 'Backlog',        color: 'gray',   icon: 'ph-tray' },
    in_progress:    { label: 'Em Andamento',   color: 'blue',   icon: 'ph-arrow-right' },
    in_negotiation: { label: 'Em Negociação',  color: 'orange', icon: 'ph-handshake' },
    converted:      { label: 'Convertido',     color: 'green',  icon: 'ph-check-circle' },
    declined:       { label: 'Declinado',      color: 'red',    icon: 'ph-x-circle' },
  },

  actionMeta: {
    call:      { label: 'Ligação',    icon: 'ph-phone' },
    email:     { label: 'E-mail',     icon: 'ph-envelope' },
    meeting:   { label: 'Reunião',    icon: 'ph-users' },
    whatsapp:  { label: 'WhatsApp',   icon: 'ph-whatsapp-logo' },
    note:      { label: 'Nota',       icon: 'ph-note' },
    proposal:  { label: 'Proposta',   icon: 'ph-file-text' },
  },

  stageBadge(stage) {
    const m = utils.stageMeta[stage] || { label: stage, color: 'gray' };
    return `<span class="badge badge-${m.color}">${m.label}</span>`;
  },

  // ── Reference number parser ───────────────────────────────
  // Parses action descriptions for known prefixes and returns
  // a structured object with type, number, notes, and an HTML badge.
  //
  // Recognized patterns (from stage-ref-modal.js):
  //   "Orçamento registrado: ORC-2025-001 — obs"
  //   "Pedido confirmado: PED-2025-001 — obs"
  //   "Declínio registrado: Motivo — obs"
  parseActionRef(description) {
    if (!description) return null;

    const patterns = [
      {
        prefix:    'Orçamento registrado:',
        type:      'orcamento',
        label:     'Orçamento',
        icon:      'ph-handshake',
        badgeCls:  'ref-badge--orange',
        stageCls:  'badge-orange',
      },
      {
        prefix:    'Pedido confirmado:',
        type:      'pedido',
        label:     'Pedido',
        icon:      'ph-check-circle',
        badgeCls:  'ref-badge--green',
        stageCls:  'badge-green',
      },
      {
        prefix:    'Declínio registrado:',
        type:      'declinio',
        label:     'Motivo',
        icon:      'ph-x-circle',
        badgeCls:  'ref-badge--red',
        stageCls:  'badge-red',
      },
    ];

    for (const p of patterns) {
      if (description.startsWith(p.prefix)) {
        const rest  = description.slice(p.prefix.length).trim();
        const parts = rest.split(' — ');
        const ref   = parts[0]?.trim() || '';
        const notes = parts.slice(1).join(' — ').trim() || null;
        return { ...p, ref, notes, raw: description };
      }
    }
    return null;
  },

  // Renders a reference badge HTML string
  refBadge(parsed) {
    if (!parsed) return '';
    return `
      <span class="ref-badge ${parsed.badgeCls}" title="${parsed.raw}">
        <i class="ph ${parsed.icon}"></i>
        <span class="ref-badge-label">${parsed.label}:</span>
        <strong class="ref-badge-num">${parsed.ref}</strong>
        ${parsed.notes ? `<span class="ref-badge-notes">— ${parsed.notes}</span>` : ''}
      </span>`;
  },

  // ── Sortable table helper ─────────────────────────────────
  // Call once after rendering a table to make headers clickable.
  // tableId: the <table> element id
  // getRows: () => array of data objects
  // renderFn: (sortedRows) => void  (re-renders tbody)
  // colMap: { 'th text or data-col': 'dataKey' }
  initSortableTable(tableId, getRows, renderFn) {
    const tbl = document.getElementById(tableId);
    if (!tbl) return;
    tbl.querySelectorAll('th[data-col]').forEach(th => {
      th.style.cursor = 'pointer';
      th.style.userSelect = 'none';
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        const cur = th.dataset.sortDir || '';
        // Reset all headers in this table
        tbl.querySelectorAll('th[data-col]').forEach(h => {
          delete h.dataset.sortDir;
          const i = h.querySelector('i.sort-icon');
          if (i) i.className = 'ph ph-arrows-down-up sort-icon';
        });
        // Toggle direction
        const dir = cur === 'desc' ? 'asc' : 'desc';
        th.dataset.sortDir = dir;
        const icon = th.querySelector('i.sort-icon');
        if (icon) icon.className = `ph ph-sort-${dir === 'desc' ? 'descending' : 'ascending'} sort-icon`;

        const rows = [...getRows()];
        rows.sort((a, b) => {
          const av = typeof a[col] === 'string' ? a[col].toLowerCase() : (a[col] ?? 0);
          const bv = typeof b[col] === 'string' ? b[col].toLowerCase() : (b[col] ?? 0);
          if (av < bv) return dir === 'desc' ? 1 : -1;
          if (av > bv) return dir === 'desc' ? -1 : 1;
          return 0;
        });
        renderFn(rows);
      });
    });
  },

  // Renders a sort icon inside a th — call when building th HTML
  sortIcon() {
    return `<i class="ph ph-arrows-down-up sort-icon" style="font-size:.7rem;opacity:.4;margin-left:4px;vertical-align:middle"></i>`;
  },

  debounce(fn, ms = 300) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  },

  qs:  (sel, ctx = document) => ctx.querySelector(sel),
  qsa: (sel, ctx = document) => [...ctx.querySelectorAll(sel)],

  el(tag, cls = '', html = '') {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  },
};

window.utils = utils;
