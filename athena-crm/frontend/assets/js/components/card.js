/* ============================================================
   Athena CRM — Card Detail Modal
   ============================================================ */

const cardDetail = {
  _currentCard: null,
  _sellers:     [],

  // ── Type/icon map ─────────────────────────────────────────
  _typeMap: {
    call:     { icon: 'ph-phone',         label: 'Ligação',   cls: 'call'     },
    email:    { icon: 'ph-envelope',      label: 'E-mail',    cls: 'email'    },
    meeting:  { icon: 'ph-users',         label: 'Reunião',   cls: 'meeting'  },
    whatsapp: { icon: 'ph-whatsapp-logo', label: 'WhatsApp',  cls: 'whatsapp' },
    note:     { icon: 'ph-note',          label: 'Nota',      cls: 'note'     },
    proposal: { icon: 'ph-file-text',     label: 'Proposta',  cls: 'proposal' },
  },

  _statusColors: {
    pending:    { color: 'var(--warning)',  bg: 'var(--warning-bg)',  label: 'Pendente'   },
    completed:  { color: 'var(--success)',  bg: 'var(--success-bg)',  label: 'Concluída'  },
    cancelled:  { color: 'var(--danger)',   bg: 'var(--danger-bg)',   label: 'Cancelada'  },
  },

  // ── Open modal ────────────────────────────────────────────
  async open(cardData) {
    const overlay = document.getElementById('modal-card-detail');
    if (!overlay) return;
    this._currentCard = cardData;

    // Load actions + sellers in parallel
    let actions = [];
    try {
      [actions, this._sellers] = await Promise.all([
        api.getActions({ card_id: cardData.id }),
        this._sellers.length ? Promise.resolve(this._sellers) : api.getSellers(),
      ]);
    } catch (_) {}

    this._fillInfo(overlay, cardData);
    this._fillActions(overlay, actions, cardData);
    this._bindForm(overlay, cardData);

    modal.open('modal-card-detail');
  },

  // ── Fill card info panel ──────────────────────────────────
  _fillInfo(overlay, c) {
    const set = (id, val) => {
      const el = overlay.querySelector('#' + id);
      if (el) el.innerHTML = val;
    };

    // Short card ID
    const shortId = c.id ? c.id.split('-')[0].toUpperCase() : '—';

    set('modal-card-title', `
      ${c.title || c.client_name || 'Card'}
      <span style="font-size:.7rem;font-weight:400;color:var(--text-muted);margin-left:6px">#${shortId}</span>
    `);
    set('modal-card-client',        c.client_name || '—');
    set('modal-card-seller',        c.seller_name || '—');
    set('modal-card-stage',         utils.stageBadge(c.stage));
    set('modal-card-cycle',         c.cycle_id
      ? `<span class="badge badge-gray">${c.cycle_id}</span>` : '—');
    set('modal-card-branch',        c.branch
      ? `<span class="badge badge-purple"><i class="ph ph-buildings"></i> ${c.branch}</span>` : '—');
    set('modal-card-state',         c.state
      ? `<span class="badge badge-blue"><i class="ph ph-map-pin"></i> ${c.state}</span>` : '—');
    set('modal-card-ltv',           utils.fmt.currency(c.ltv));
    set('modal-card-ticket',        utils.fmt.currency(c.avg_ticket));
    set('modal-card-risk',          utils.fmt.currency(c.value_at_risk));
    set('modal-card-last-purchase', utils.fmt.date(c.last_purchase_date));

    // Card ID chip
    const idEl = overlay.querySelector('#modal-card-id');
    if (idEl) {
      idEl.innerHTML = `
        <span style="font-family:monospace;font-size:.7rem;background:var(--bg-input);
          border:1px solid var(--border);padding:2px 8px;border-radius:4px;
          color:var(--text-secondary);user-select:all;cursor:copy"
          title="Clique para copiar" onclick="navigator.clipboard?.writeText('${c.id}');toast?.info('ID copiado!')">
          ${c.id}
        </span>`;
    }
  },

  // ── Fill actions list ─────────────────────────────────────
  _fillActions(overlay, actions, cardData) {
    const actList = overlay.querySelector('#modal-card-actions');
    if (!actList) return;

    if (!actions.length) {
      actList.innerHTML = `
        <div class="empty-state" style="padding:1.5rem">
          <i class="ph ph-chat-text"></i>
          <p>Nenhuma ação registrada neste card.</p>
        </div>`;
      return;
    }

    // Stage metadata for card result display
    const stageMeta = {
      backlog:        { label: 'Backlog',        icon: 'ph-tray',         badgeCls: 'badge-gray'   },
      in_progress:    { label: 'Em Andamento',   icon: 'ph-arrow-right',  badgeCls: 'badge-blue'   },
      in_negotiation: { label: 'Em Negociação',  icon: 'ph-handshake',    badgeCls: 'badge-orange' },
      converted:      { label: 'Convertido',     icon: 'ph-check-circle', badgeCls: 'badge-green'  },
      declined:       { label: 'Declinado',      icon: 'ph-x-circle',     badgeCls: 'badge-red'    },
    };

    actList.innerHTML = actions.map(a => {
      const meta        = this._typeMap[a.action_type] || { icon: 'ph-activity', label: a.action_type, cls: 'note' };
      const statusMeta  = this._statusColors[a.status] || this._statusColors.pending;
      const shortCardId = a.card_id ? a.card_id.split('-')[0].toUpperCase() : '—';

      // ── Parse reference number ─────────────────────────────
      const ref = utils.parseActionRef(a.description);

      // ── Card result block ──────────────────────────────────
      const sm         = stageMeta[a.card_stage] || null;
      const isArchived = a.card_is_archived;
      const archivedAt = a.card_archived_at ? utils.fmt.date(a.card_archived_at) : null;
      const cycle      = a.card_cycle_id || '—';

      let resultHtml = '';
      if (sm) {
        let resultLabel = sm.label;
        let resultNote  = '';

        if (isArchived) {
          if (a.card_stage === 'converted')      resultLabel = 'Convertido e Arquivado ✓';
          else if (a.card_stage === 'declined')  resultLabel = 'Declinado e Arquivado ✗';
          else                                   resultLabel = sm.label + ' (Arquivado)';
          resultNote = archivedAt
            ? `Arquivado em ${archivedAt} · Ciclo ${cycle}`
            : `Arquivado · Ciclo ${cycle}`;
        } else {
          resultNote = `Ciclo ativo: ${cycle}`;
        }

        resultHtml = `
          <div class="action-result">
            <div class="action-result-label">
              <i class="ph ph-flag-checkered"></i> Resultado do Card
            </div>
            <div class="action-result-body">
              <span class="badge ${sm.badgeCls}" style="font-size:.72rem">
                <i class="ph ${sm.icon}"></i> ${resultLabel}
              </span>
              ${isArchived
                ? `<span class="badge badge-gray" style="font-size:.65rem"><i class="ph ph-archive"></i> Arquivado</span>`
                : `<span class="badge badge-purple" style="font-size:.65rem"><i class="ph ph-circle-notch"></i> Ativo</span>`}
              <span class="action-result-note">${resultNote}</span>
            </div>
          </div>`;
      }

      return `
        <div class="action-item animate-fade">
          <div class="action-icon action-icon--${meta.cls}">
            <i class="ph ${meta.icon}"></i>
          </div>
          <div class="action-body">
            <div class="action-header">
              <span class="action-type-label">${meta.label}</span>
              <span class="action-status-pill" style="background:${statusMeta.bg};color:${statusMeta.color}">
                ${statusMeta.label}
              </span>
              <span class="action-time">
                <i class="ph ph-clock"></i> ${utils.fmt.datetime(a.created_at)}
              </span>
            </div>
            <div class="action-chips">
              ${a.client_name ? `
                <a href="client-detail.html?id=${a.client_id}" class="action-chip action-chip--client"
                   title="Ver cliente" onclick="modal.closeAll()">
                  <i class="ph ph-user"></i> ${a.client_name}
                </a>` : ''}
              <span class="action-chip action-chip--card" title="ID do Card: ${a.card_id}"
                onclick="navigator.clipboard?.writeText('${a.card_id}');toast?.info('ID do card copiado!')">
                <i class="ph ph-kanban"></i>
                ${a.card_title || 'Card #' + shortCardId}
                <span style="font-family:monospace;font-size:.6rem;opacity:.6">#${shortCardId}</span>
              </span>
              ${a.seller_name ? `
                <span class="action-chip action-chip--seller">
                  <i class="ph ph-user-circle"></i> ${a.seller_name}
                </span>` : ''}
            </div>
            <div class="action-description">${ref ? '' : a.description}</div>
            ${ref ? utils.refBadge(ref) : ''}
            ${a.outcome ? `
              <div class="action-outcome">
                <i class="ph ph-check-circle"></i> ${a.outcome}
              </div>` : ''}
            ${resultHtml}
          </div>
        </div>`;
    }).join('');
  },

  // ── Bind action form ──────────────────────────────────────
  _bindForm(overlay, cardData) {
    // Populate seller select
    const sellerSel = overlay.querySelector('[name="seller_id"]');
    if (sellerSel && sellerSel.tagName === 'SELECT' && this._sellers.length) {
      const current = sellerSel.value;
      sellerSel.innerHTML = '<option value="">Selecione o vendedor</option>' +
        this._sellers.map(s => {
          const role = { admin: 'Admin', manager: 'Gerente', seller: 'Vendedor' }[s.role] || s.role;
          return `<option value="${s.id}">${s.name} — ${role}</option>`;
        }).join('');
      if (current) sellerSel.value = current;
    }

    // Pre-fill hidden fields
    const cardIdInput   = overlay.querySelector('#form-card-action-card-id');
    const clientIdInput = overlay.querySelector('#form-card-action-client-id');
    if (cardIdInput)   cardIdInput.value   = cardData.id;
    if (clientIdInput) clientIdInput.value = cardData.client_id;

    // Bind submit (once)
    const form = overlay.querySelector('#form-card-action');
    if (!form || form._bound) return;
    form._bound = true;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd  = new FormData(form);
      const btn = form.querySelector('[type="submit"]');

      if (btn) { btn.disabled = true; btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Registrando...'; }

      try {
        await api.createAction({
          card_id:     fd.get('card_id'),
          client_id:   fd.get('client_id'),
          seller_id:   fd.get('seller_id'),
          action_type: fd.get('action_type'),
          description: fd.get('description'),
        });
        toast.success('Ação registrada!');

        // Reset but keep card/client ids
        const cid = fd.get('card_id');
        const lid = fd.get('client_id');
        form.reset();
        form.querySelector('[name="card_id"]').value   = cid;
        form.querySelector('[name="client_id"]').value = lid;

        // Reload actions
        await this.open(cardData);
      } catch (err) {
        toast.error(err.message);
      } finally {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="ph ph-paper-plane-tilt"></i> Registrar Ação'; }
      }
    });
  },
};

window.cardDetail = cardDetail;
