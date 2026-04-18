/* ============================================================
   Athena CRM — Kanban Component
   - Full-column drag-drop, drop on cards or empty space
   - Sort: LTV ↑↓ | Ticket Médio ↑↓ | Interação Recente
   ============================================================ */

const kanban = {
  STAGES: ['backlog', 'in_progress', 'in_negotiation', 'converted', 'declined'],

  _container:     null,
  _onCardClick:   null,
  _onStageChange: null,
  _params:        {},
  _cards:         [],
  _sort:          null,

  // Drag state — module-level so it survives re-renders
  _dragged:     null,
  _draggedId:   null,
  _draggedStage: null,
  _isDragging:  false,

  // ── Init ──────────────────────────────────────────────────
  async init(containerId, onCardClick, onStageChange, params = {}) {
    this._container     = document.getElementById(containerId);
    this._onCardClick   = onCardClick;
    this._onStageChange = onStageChange;
    this._params        = params;
    await this.load();
  },

  async load() {
    try {
      const cards = await api.getCards(this._params || {});
      this._cards = cards;
      state.set('cards', cards);

      // Fetch refs for cards in key stages (in_negotiation, converted, declined)
      await this._loadCardRefs(cards);

      this.render(cards);
      this._updateSortHint();
    } catch (e) { toast.error('Erro ao carregar cards: ' + e.message); }
  },

  // Fetch the latest reference action for relevant cards
  _cardRefs: {}, // card_id → parsed ref object

  async _loadCardRefs(cards) {
    const relevant = cards.filter(c =>
      ['in_negotiation','converted','declined'].includes(c.stage) && !c.is_archived
    );
    if (!relevant.length) return;

    try {
      // Fetch all actions (limit to avoid overload)
      const actions = await api.getActions({ limit: 500 });
      this._cardRefs = {};
      actions.forEach(a => {
        const ref = utils.parseActionRef(a.description);
        if (ref && a.card_id) {
          if (!this._cardRefs[a.card_id] ||
              new Date(a.created_at) > new Date(this._cardRefs[a.card_id]._created_at)) {
            this._cardRefs[a.card_id] = { ...ref, _created_at: a.created_at };
          }
        }
      });
    } catch (_) {}
  },

  // ── Sort ──────────────────────────────────────────────────
  setSort(key) {
    if (key === 'recent') {
      this._sort = this._sort === 'recent' ? null : 'recent';
    } else if (this._sort === key + '_desc') {
      this._sort = key + '_asc';
    } else if (this._sort === key + '_asc') {
      this._sort = null;
    } else {
      this._sort = key + '_desc';
    }
    this._updateSortButtons();
    this._updateSortHint();
    this.render(this._cards);
  },

  _sortCards(cards) {
    if (!this._sort) return [...cards];
    return [...cards].sort((a, b) => {
      switch (this._sort) {
        case 'ltv_desc':    return (b.ltv || 0) - (a.ltv || 0);
        case 'ltv_asc':     return (a.ltv || 0) - (b.ltv || 0);
        case 'ticket_desc': return (b.avg_ticket || 0) - (a.avg_ticket || 0);
        case 'ticket_asc':  return (a.avg_ticket || 0) - (b.avg_ticket || 0);
        case 'recent': {
          const ta = new Date(a.updated_at || a.created_at || 0).getTime();
          const tb = new Date(b.updated_at || b.created_at || 0).getTime();
          return tb - ta;
        }
        default: return 0;
      }
    });
  },

  _updateSortButtons() {
    document.querySelectorAll('[data-kanban-sort]').forEach(btn => {
      const key      = btn.dataset.kanbanSort;
      const isActive = this._sort && this._sort.startsWith(key);
      btn.classList.toggle('ksort-active', !!isActive);
      const icon = btn.querySelector('i');
      if (!icon) return;
      if (this._sort === key + '_asc') {
        icon.className = 'ph ph-sort-ascending';
      } else {
        icon.className = key === 'recent' ? 'ph ph-clock-counter-clockwise' : 'ph ph-sort-descending';
      }
    });
  },

  _updateSortHint() {
    const hint = document.getElementById('ksort-hint');
    if (!hint) return;
    const labels = {
      ltv_desc:    'LTV: maior primeiro',
      ltv_asc:     'LTV: menor primeiro',
      ticket_desc: 'Ticket: maior primeiro',
      ticket_asc:  'Ticket: menor primeiro',
      recent:      'Interação mais recente primeiro',
    };
    hint.textContent = this._sort ? labels[this._sort] || '' : '';
  },

  // ── Render ────────────────────────────────────────────────
  render(cards) {
    if (!this._container) return;
    this._container.innerHTML = '';

    const sorted = this._sortCards(cards);

    this.STAGES.forEach(stage => {
      const stageCards = sorted.filter(c => c.stage === stage);
      const meta       = utils.stageMeta[stage];

      const col = utils.el('div', 'kanban-col');
      col.dataset.stage = stage;

      // Header
      const stageColor = {
        backlog: '#94a3b8', in_progress: '#3b82f6',
        in_negotiation: '#f59e0b', converted: '#10b981', declined: '#ef4444',
      }[stage] || '#94a3b8';

      const totalRisk = stageCards.reduce((s, c) => s + (c.value_at_risk || 0), 0);
      const totalLtv  = stageCards.reduce((s, c) => s + (c.ltv || 0), 0);

      const header = utils.el('div', 'kanban-col-header');
      header.innerHTML = `
        <div style="display:flex;align-items:center;gap:7px;flex:1;min-width:0">
          <span style="width:8px;height:8px;border-radius:50%;background:${stageColor};flex-shrink:0"></span>
          <span class="kanban-col-title">${meta.label}</span>
          <span class="kanban-col-count">${stageCards.length}</span>
        </div>
        ${stageCards.length ? `
        <div style="font-size:.6rem;color:var(--text-muted);text-align:right;line-height:1.5;flex-shrink:0">
          <div style="color:var(--danger);font-weight:700">${utils.fmt.currency(totalRisk)}</div>
          <div>LTV ${utils.fmt.currency(totalLtv)}</div>
        </div>` : ''}`;
      col.appendChild(header);

      // Body
      const body = utils.el('div', 'kanban-col-body');
      body.dataset.stage = stage;

      stageCards.forEach(card => body.appendChild(this._buildCard(card)));

      if (!stageCards.length) {
        const empty = utils.el('div', 'kanban-empty-col');
        empty.innerHTML = `<i class="ph ph-tray"></i><span>Arraste cards aqui</span>`;
        body.appendChild(empty);
      }

      col.appendChild(body);
      this._container.appendChild(col);
    });

    this._bindDrag();
  },

  // ── Build card ────────────────────────────────────────────
  _buildCard(card) {
    const el = utils.el('div', 'kanban-card animate-fade');
    el.dataset.id    = card.id;
    el.dataset.stage = card.stage;

    // Only draggable if not archived
    if (!card.is_archived) {
      el.setAttribute('draggable', 'true');
    }

    const archivedBadge = card.is_archived
      ? `<span class="badge badge-gray" style="font-size:.58rem;padding:1px 6px">Arquivado</span>` : '';

    const daysAgo = card.last_purchase_date
      ? Math.floor((Date.now() - new Date(card.last_purchase_date)) / 86400000)
      : null;
    const daysColor = daysAgo === null ? 'var(--text-muted)'
      : daysAgo > 90 ? 'var(--danger)'
      : daysAgo > 60 ? 'var(--warning)'
      : 'var(--success)';

    const score      = card.churn_risk_score || 0;
    const scoreColor = score >= 70 ? 'var(--danger)' : score >= 40 ? 'var(--warning)' : 'var(--success)';

    el.innerHTML = `
      <div class="kc-header">
        <div class="kc-name">${card.client_name} ${archivedBadge}</div>
        <div class="kc-risk">${utils.fmt.currency(card.value_at_risk)}</div>
      </div>
      <div class="kc-score-bar">
        <div class="kc-score-fill" style="width:${Math.min(score,100)}%;background:${scoreColor}"></div>
      </div>
      <div class="kc-meta">
        <div class="kc-meta-row"><i class="ph ph-user-circle"></i><span>${card.seller_name || '—'}</span></div>
        <div class="kc-meta-row">
          <i class="ph ph-trend-up" style="color:var(--brand-primary)"></i>
          <span>LTV <strong>${utils.fmt.currency(card.ltv)}</strong></span>
        </div>
        <div class="kc-meta-row">
          <i class="ph ph-receipt"></i>
          <span>Ticket <strong>${utils.fmt.currency(card.avg_ticket)}</strong></span>
        </div>
        <div class="kc-meta-row">
          <i class="ph ph-calendar-blank" style="color:${daysColor}"></i>
          <span style="color:${daysColor}">
            ${daysAgo !== null ? `${daysAgo}d sem compra` : utils.fmt.date(card.last_purchase_date)}
          </span>
        </div>
        ${card.branch ? `<div class="kc-meta-row"><i class="ph ph-buildings"></i><span>${card.branch.replace('Filial ','')} · ${card.state || '—'}</span></div>` : ''}
        ${card.cycle_id ? `<div class="kc-meta-row"><i class="ph ph-arrows-clockwise"></i><span>${card.cycle_id}</span></div>` : ''}
      </div>
      <div class="kc-footer">
        ${utils.stageBadge(card.stage)}
        <span style="font-size:.65rem;color:var(--text-muted)">
          <i class="ph ph-clock"></i> ${utils.fmt.date(card.updated_at || card.created_at)}
        </span>
      </div>
      ${this._cardRefs[card.id] ? `
      <div style="margin-top:.5rem;padding-top:.5rem;border-top:1px solid var(--border-light)">
        ${utils.refBadge(this._cardRefs[card.id])}
      </div>` : ''}`;

    // Click — only open if we didn't just drag
    el.addEventListener('click', () => {
      if (this._isDragging) return;
      this._onCardClick && this._onCardClick(card);
    });

    return el;
  },

  // ── Drag & Drop ───────────────────────────────────────────
  _bindDrag() {
    // Use event delegation on the container for better reliability
    this._container.addEventListener('dragstart', (e) => {
      const card = e.target.closest('.kanban-card[draggable="true"]');
      if (!card) return;

      this._dragged      = card;
      this._draggedId    = card.dataset.id;
      this._draggedStage = card.closest('.kanban-col-body')?.dataset.stage;
      this._isDragging   = true;

      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', this._draggedId);

      // Style the dragged card — use opacity via class AFTER dataTransfer is set
      // so the browser captures the ghost image first
      setTimeout(() => {
        if (card) card.classList.add('kc-dragging');
      }, 0);
    }, true);

    this._container.addEventListener('dragend', (e) => {
      const card = e.target.closest('.kanban-card');
      if (card) card.classList.remove('kc-dragging');

      // Remove all highlights and placeholders
      this._container.querySelectorAll('.kanban-col-body').forEach(b => {
        b.classList.remove('kc-col-over');
      });
      this._container.querySelectorAll('.kc-placeholder').forEach(p => p.remove());

      // Reset drag state after a longer delay to ensure drop fires first
      setTimeout(() => {
        this._isDragging   = false;
        this._dragged      = null;
        this._draggedId    = null;
        this._draggedStage = null;
      }, 200);
    }, true);

    // Dragover — on each column body
    this._container.querySelectorAll('.kanban-col-body').forEach(body => {

      body.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        if (!this._draggedId) return;

        body.classList.add('kc-col-over');

        // Remove existing placeholder
        body.querySelectorAll('.kc-placeholder').forEach(p => p.remove());

        // Insert placeholder at correct position
        const afterEl = this._getInsertionPoint(body, e.clientY);
        const ph      = this._makePlaceholder();
        if (afterEl) {
          body.insertBefore(ph, afterEl);
        } else {
          body.appendChild(ph);
        }
      });

      body.addEventListener('dragleave', (e) => {
        if (!body.contains(e.relatedTarget)) {
          body.classList.remove('kc-col-over');
          body.querySelectorAll('.kc-placeholder').forEach(p => p.remove());
        }
      });

      body.addEventListener('drop', async (e) => {
        e.preventDefault();
        body.classList.remove('kc-col-over');
        body.querySelectorAll('.kc-placeholder').forEach(p => p.remove());

        // Capture synchronously before any async/timeout resets them
        const id       = e.dataTransfer.getData('text/plain') || this._draggedId;
        const newStage = body.dataset.stage;
        const oldStage = this._draggedStage;

        if (!id || !newStage) return;
        if (newStage === oldStage) return;

        // ── Stages that require a reference number ─────────
        if (newStage === 'in_negotiation' || newStage === 'converted' || newStage === 'declined') {
          const card = this._cards.find(c => c.id === id);
          const ok   = await stageRefModal.prompt(newStage, card, oldStage);
          if (!ok) return; // user cancelled or transition blocked
        }

        await this._commitMove(id, newStage);
      });
    });
  },

  async _commitMove(id, newStage) {
    try {
      await api.moveCard(id, newStage);
      toast.success(`Movido para ${utils.stageMeta[newStage]?.label || newStage}`);
      this._onStageChange && this._onStageChange(id, newStage);
      const card = this._cards.find(c => c.id === id);
      if (card) {
        card.stage      = newStage;
        card.updated_at = new Date().toISOString();
      }
      // Reload refs since a new action was just created
      await this._loadCardRefs(this._cards);
      this.render(this._cards);
    } catch (err) {
      toast.error(err.message);
    }
  },

  _makePlaceholder() {
    const ph = document.createElement('div');
    ph.className = 'kc-placeholder';
    return ph;
  },

  _getInsertionPoint(container, y) {
    const cards = [...container.querySelectorAll('.kanban-card:not(.kc-dragging):not(.kc-placeholder)')];
    return cards.reduce((closest, child) => {
      const box    = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset, element: child };
      }
      return closest;
    }, { offset: Number.NEGATIVE_INFINITY }).element;
  },
};

window.kanban = kanban;
