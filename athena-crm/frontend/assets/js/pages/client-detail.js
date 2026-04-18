/* ============================================================
   Athena CRM — Client Detail Page
   Tabs: Cards History | Interaction History
   ============================================================ */

const clientDetailPage = {
  _clientId: null,
  _cards:    [],
  _history:  [],

  // ── Type metadata ─────────────────────────────────────────
  _typeMap: {
    call:     { icon: 'ph-phone',        label: 'Ligação',   cls: 'call'     },
    email:    { icon: 'ph-envelope',     label: 'E-mail',    cls: 'email'    },
    meeting:  { icon: 'ph-users',        label: 'Reunião',   cls: 'meeting'  },
    whatsapp: { icon: 'ph-whatsapp-logo',label: 'WhatsApp',  cls: 'whatsapp' },
    note:     { icon: 'ph-note',         label: 'Nota',      cls: 'note'     },
    proposal: { icon: 'ph-file-text',    label: 'Proposta',  cls: 'proposal' },
    card:     { icon: 'ph-kanban',       label: 'Via Card',  cls: 'card'     },
  },

  // ── Init ──────────────────────────────────────────────────
  async init() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    if (!id) { toast.error('ID do cliente não informado'); return; }
    this._clientId = id;

    this._bindTabs();
    this._bindTypePills();

    await Promise.all([
      this._loadSellers(),
      this.load(id),
    ]);
  },

  // ── Tab switching ─────────────────────────────────────────
  _bindTabs() {
    document.querySelectorAll('.cd-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.cd-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.cd-panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById('panel-' + btn.dataset.tab)?.classList.add('active');
      });
    });
  },

  // ── Type pills ────────────────────────────────────────────
  _bindTypePills() {
    const container = document.getElementById('type-pills');
    const hidden    = document.getElementById('action-type-hidden');
    if (!container || !hidden) return;

    container.querySelectorAll('.type-pill').forEach(pill => {
      pill.addEventListener('click', () => {
        container.querySelectorAll('.type-pill').forEach(p => p.classList.remove('selected'));
        pill.classList.add('selected');
        hidden.value = pill.dataset.value;
      });
    });
  },

  // ── Load sellers into select ──────────────────────────────
  async _loadSellers() {
    try {
      const sellers = await api.getSellers();
      const sel = document.getElementById('history-seller-select');
      if (!sel) return;
      sel.innerHTML = '<option value="">Selecione o vendedor</option>' +
        sellers.map(s => {
          const roleLabel = { admin: 'Admin', manager: 'Gerente', seller: 'Vendedor' }[s.role] || s.role;
          return `<option value="${s.id}">${s.name} — ${roleLabel}</option>`;
        }).join('');
    } catch (_) {}
  },

  // ── Main data load ────────────────────────────────────────
  async load(id) {
    try {
      const [client, history, cards] = await Promise.all([
        api.getClient(id),
        api.getClientHistory(id),
        api.getCards({ client_id: id }),
      ]);
      this._cards   = cards;
      this._history = history;

      state.set('currentClient', client);
      this._renderHero(client, cards);
      this._renderCards(cards);
      this._renderHistory(history);
      this._bindForm(id);
    } catch (e) {
      toast.error('Erro ao carregar cliente: ' + e.message);
    }
  },

  // ── Hero profile ──────────────────────────────────────────
  _renderHero(c, cards) {
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    set('client-name',          c.name);
    set('client-external-id',   c.external_id);
    set('client-ltv',           utils.fmt.currency(c.ltv));
    set('client-ticket',        utils.fmt.currency(c.avg_ticket));
    set('client-last-purchase', utils.fmt.date(c.last_purchase_date));
    set('client-cards-count',   cards.length);

    // Score with color
    const scoreEl = document.getElementById('client-risk-score');
    if (scoreEl) {
      const s = c.churn_risk_score;
      scoreEl.textContent = s.toFixed(0) + '%';
      scoreEl.style.color = s >= 70 ? 'var(--danger)' : s >= 40 ? 'var(--warning)' : 'var(--success)';
    }

    // Risk badge
    const riskBadge = document.getElementById('client-risk-badge');
    if (riskBadge) riskBadge.innerHTML = c.is_at_risk
      ? '<span class="badge badge-red"><i class="ph-fill ph-warning"></i> Em Risco</span>'
      : '<span class="badge badge-green"><i class="ph-fill ph-check-circle"></i> Saudável</span>';

    // Branch / state badges
    const branchBadge = document.getElementById('client-branch-badge');
    if (branchBadge && c.branch)
      branchBadge.innerHTML = `<span class="badge badge-purple"><i class="ph ph-buildings"></i> ${c.branch}</span>`;

    const stateBadge = document.getElementById('client-state-badge');
    if (stateBadge && c.state)
      stateBadge.innerHTML = `<span class="badge badge-blue"><i class="ph ph-map-pin"></i> ${c.state}</span>`;
  },

  // ── Cards panel ───────────────────────────────────────────
  _renderCards(cards) {
    const el = document.getElementById('client-cards-list');
    if (!el) return;

    // Update tab count
    const countEl = document.getElementById('tab-count-cards');
    if (countEl) countEl.textContent = cards.length;

    if (!cards.length) {
      el.innerHTML = `
        <div class="empty-state" style="grid-column:1/-1;padding:3rem">
          <i class="ph ph-kanban"></i>
          <p>Nenhum card criado para este cliente.</p>
        </div>`;
      return;
    }

    el.innerHTML = cards.map(c => {
      const stageMeta = utils.stageMeta[c.stage] || { label: c.stage, color: 'gray' };
      const daysAgo   = c.last_purchase_date
        ? Math.floor((Date.now() - new Date(c.last_purchase_date)) / 86400000)
        : null;

      return `
        <div class="cd-card-item animate-fade" onclick="cardDetail.open(${JSON.stringify(c).replace(/"/g, '&quot;')})">
          <div class="cd-card-header">
            <div class="cd-card-title">${c.title || c.client_name || 'Card'}</div>
            <span class="badge badge-${stageMeta.color}">${stageMeta.label}</span>
          </div>
          <div class="cd-card-body">
            <div class="cd-card-stat danger">
              <i class="ph ph-warning-circle" style="color:var(--danger)"></i>
              Risco: <strong>${utils.fmt.currency(c.value_at_risk)}</strong>
            </div>
            <div class="cd-card-stat">
              <i class="ph ph-trend-up" style="color:var(--brand-primary)"></i>
              LTV: <strong>${utils.fmt.currency(c.ltv)}</strong>
            </div>
            <div class="cd-card-stat">
              <i class="ph ph-receipt" style="color:var(--text-muted)"></i>
              Ticket: <strong>${utils.fmt.currency(c.avg_ticket)}</strong>
            </div>
            ${c.cycle_id ? `
            <div class="cd-card-stat">
              <i class="ph ph-arrows-clockwise" style="color:var(--text-muted)"></i>
              Ciclo: <strong>${c.cycle_id}</strong>
            </div>` : ''}
          </div>
          <div class="cd-card-footer">
            <span>
              <i class="ph ph-user-circle"></i>
              ${c.seller_name || '—'}
            </span>
            <span>
              ${daysAgo !== null
                ? `<i class="ph ph-calendar-blank"></i> ${daysAgo}d sem compra`
                : utils.fmt.date(c.created_at)}
            </span>
          </div>
        </div>`;
    }).join('');
  },

  // ── History panel ─────────────────────────────────────────
  _renderHistory(history) {
    const el = document.getElementById('client-history-list');
    if (!el) return;

    const countEl = document.getElementById('tab-count-history');
    if (countEl) countEl.textContent = history.length;

    if (!history.length) {
      el.innerHTML = `
        <div class="empty-state" style="padding:3rem">
          <i class="ph ph-clock-counter-clockwise"></i>
          <p>Nenhuma interação registrada ainda.<br>Use o formulário ao lado para começar.</p>
        </div>`;
      return;
    }

    // Stage result config
    const stageCfg = {
      backlog:        { label: 'Backlog',        cls: 'badge-gray',   icon: 'ph-tray'         },
      in_progress:    { label: 'Em Andamento',   cls: 'badge-blue',   icon: 'ph-arrow-right'  },
      in_negotiation: { label: 'Em Negociação',  cls: 'badge-orange', icon: 'ph-handshake'    },
      converted:      { label: 'Convertido ✓',   cls: 'badge-green',  icon: 'ph-check-circle' },
      declined:       { label: 'Declinado ✗',    cls: 'badge-red',    icon: 'ph-x-circle'     },
    };

    el.innerHTML = history.map(h => {
      const type = h.history_type || (h.card_id ? 'card' : 'note');
      const meta = this._typeMap[type] || this._typeMap.note;

      // ── Parse reference number ─────────────────────────────
      const ref = utils.parseActionRef(h.content);

      // ── Card result block ──────────────────────────────────
      const sc         = stageCfg[h.card_stage_now] || null;
      const isArchived = h.card_is_archived;
      const archivedAt = h.card_archived_at ? utils.fmt.date(h.card_archived_at) : null;
      const cycle      = h.card_cycle_id || h.cycle_id || null;
      const shortCardId = h.card_id ? h.card_id.split('-')[0].toUpperCase() : null;

      let resultHtml = '';
      if (sc) {
        let resultLabel = sc.label;
        let resultNote  = cycle ? `Ciclo: ${cycle}` : '';
        if (isArchived) {
          if (h.card_stage_now === 'converted')     resultLabel = 'Convertido e Arquivado ✓';
          else if (h.card_stage_now === 'declined') resultLabel = 'Declinado e Arquivado ✗';
          else                                      resultLabel = sc.label + ' (Arquivado)';
          if (archivedAt) resultNote = `Arquivado em ${archivedAt}` + (cycle ? ` · Ciclo ${cycle}` : '');
        }
        resultHtml = `
          <div class="cd-result-block">
            <div class="cd-result-label"><i class="ph ph-flag-checkered"></i> Resultado do Card</div>
            <div class="cd-result-body">
              <span class="badge ${sc.cls}" style="font-size:.72rem">
                <i class="ph ${sc.icon}"></i> ${resultLabel}
              </span>
              ${isArchived
                ? `<span class="badge badge-gray" style="font-size:.62rem"><i class="ph ph-archive"></i> Arquivado</span>`
                : `<span class="badge badge-purple" style="font-size:.62rem"><i class="ph ph-circle-notch"></i> Ativo</span>`}
              ${resultNote ? `<span class="cd-result-note">${resultNote}</span>` : ''}
            </div>
          </div>`;
      }

      // ── Card link chip ─────────────────────────────────────
      const cardChip = (h.card_id && h.card_id !== '00000000-0000-0000-0000-000000000000')
        ? `<button class="cd-chip cd-chip--card"
              onclick="clientDetailPage._openCard('${h.card_id}')"
              title="Ver card · ID: ${h.card_id}">
              <i class="ph ph-kanban"></i>
              ${h.card_title ? h.card_title.substring(0, 28) + (h.card_title.length > 28 ? '…' : '') : '#' + shortCardId}
           </button>`
        : '';

      // ── Seller chip ────────────────────────────────────────
      const sellerChip = h.seller_name
        ? `<span class="cd-chip cd-chip--seller">
             <i class="ph ph-user-circle"></i> ${h.seller_name}
           </span>`
        : '';

      // ── Cycle chip ─────────────────────────────────────────
      const cycleChip = cycle
        ? `<span class="cd-chip cd-chip--cycle">
             <i class="ph ph-arrows-clockwise"></i> ${cycle}
           </span>`
        : '';

      return `
        <div class="cd-timeline-item animate-fade">
          <div class="cd-timeline-dot ${meta.cls}">
            <i class="ph ${meta.icon}"></i>
          </div>
          <div class="cd-timeline-body">

            <!-- Header: type + time -->
            <div class="cd-timeline-header">
              <span class="cd-timeline-type">${meta.label}</span>
              ${h.card_stage
                ? `<span class="badge badge-gray" style="font-size:.6rem">${h.card_stage}</span>`
                : ''}
              <span class="cd-timeline-time">
                <i class="ph ph-clock"></i> ${utils.fmt.datetime(h.created_at)}
              </span>
            </div>

            <!-- Context chips: card + seller + cycle -->
            ${(cardChip || sellerChip || cycleChip) ? `
            <div class="cd-chips-row">
              ${cardChip}${sellerChip}${cycleChip}
            </div>` : ''}

            <!-- Content -->
            <div class="cd-timeline-text">${ref ? '' : h.content}</div>
            ${ref ? `<div style="margin-top:.35rem">${utils.refBadge(ref)}</div>` : ''}

            <!-- Card result -->
            ${resultHtml}

          </div>
        </div>`;
    }).join('');
  },

  // Open card detail modal from history
  async _openCard(cardId) {
    if (!cardId) return;
    try {
      const card = await api.getCard(cardId);
      cardDetail.open(card);
    } catch (e) {
      toast.error('Erro ao carregar card: ' + e.message);
    }
  },

  // ── Register form ─────────────────────────────────────────
  _bindForm(clientId) {
    const form = document.getElementById('form-add-history');
    if (!form || form._bound) return;
    form._bound = true;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd       = new FormData(form);
      const sellerId = fd.get('seller_id');
      const desc     = fd.get('description')?.trim();

      if (!sellerId) { toast.error('Selecione um vendedor'); return; }
      if (!desc)     { toast.error('Informe uma descrição'); return; }

      const btn = document.getElementById('btn-register-history');
      if (btn) { btn.disabled = true; btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Registrando...'; }

      try {
        await api.createAction({
          card_id:     '00000000-0000-0000-0000-000000000000',
          client_id:   clientId,
          seller_id:   sellerId,
          action_type: fd.get('action_type') || 'note',
          description: desc,
        });

        toast.success('Interação registrada com sucesso!');

        // Reset form but keep seller selection
        const sellerVal = sellerId;
        form.reset();
        document.getElementById('action-type-hidden').value = 'call';
        document.querySelectorAll('.type-pill').forEach(p => p.classList.remove('selected'));
        document.querySelector('.type-pill[data-value="call"]')?.classList.add('selected');
        document.getElementById('history-seller-select').value = sellerVal;

        // Reload history and switch to history tab
        const history = await api.getClientHistory(clientId);
        this._history = history;
        this._renderHistory(history);

        // Switch to history tab
        document.querySelector('.cd-tab[data-tab="history"]')?.click();

      } catch (err) {
        toast.error(err.message);
      } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="ph ph-paper-plane-tilt"></i> Registrar'; }
      }
    });
  },
};

window.clientDetailPage = clientDetailPage;
