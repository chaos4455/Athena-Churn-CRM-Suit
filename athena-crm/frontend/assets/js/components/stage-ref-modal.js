/* ============================================================
   Athena CRM — Stage Reference Modal
   Handles:
   - in_negotiation → requires Orçamento number
   - converted      → requires Pedido number
   - declined       → requires Motivo (from in_negotiation only)
   - Blocks: in_negotiation cards cannot go back to backlog/in_progress
   ============================================================ */

const stageRefModal = {
  _resolve:  null,
  _card:     null,
  _stage:    null,
  _sellers:  [],

  // ── Stage transition rules ────────────────────────────────
  // Returns { allowed: bool, reason: string } for a given move
  validateTransition(fromStage, toStage) {
    // Cards in negotiation can only go forward (converted or declined)
    if (fromStage === 'in_negotiation') {
      if (toStage === 'backlog' || toStage === 'in_progress') {
        return {
          allowed: false,
          reason:  'Um card em negociação só pode ser movido para Convertido ou Declinado.',
        };
      }
    }
    return { allowed: true };
  },

  // ── Stage config ──────────────────────────────────────────
  _cfg: {
    in_negotiation: {
      title:         'Registrar Orçamento',
      accentColor:   'var(--warning)',
      accentBg:      'var(--warning-bg)',
      icon:          'ph-handshake',
      inputLabel:    'Número do Orçamento',
      placeholder:   'Ex: ORC-2025-001',
      hint:          'Informe o número do orçamento enviado ao cliente.',
      confirmText:   'Mover para Em Negociação',
      confirmClass:  'btn-warning',
      actionType:    'proposal',
      historyPrefix: 'Orçamento registrado',
      showNotes:     true,
      refRequired:   true,
    },
    converted: {
      title:         'Confirmar Pedido',
      accentColor:   'var(--success)',
      accentBg:      'var(--success-bg)',
      icon:          'ph-check-circle',
      inputLabel:    'Número do Pedido',
      placeholder:   'Ex: PED-2025-001',
      hint:          'Informe o número do pedido confirmado pelo cliente.',
      confirmText:   'Confirmar Conversão ✓',
      confirmClass:  'btn-success-custom',
      actionType:    'proposal',
      historyPrefix: 'Pedido confirmado',
      showNotes:     true,
      refRequired:   true,
    },
    declined: {
      title:         'Registrar Declínio',
      accentColor:   'var(--danger)',
      accentBg:      'var(--danger-bg)',
      icon:          'ph-x-circle',
      inputLabel:    null,          // no ref number for declined
      placeholder:   null,
      hint:          null,
      confirmText:   'Confirmar Declínio',
      confirmClass:  'btn-danger',
      actionType:    'note',
      historyPrefix: 'Declínio registrado',
      showNotes:     true,
      refRequired:   false,
    },
  },

  // ── Public: prompt ────────────────────────────────────────
  // Returns Promise<boolean> — true = confirmed & action saved, false = cancelled
  async prompt(toStage, card, fromStage) {
    // Validate transition first
    if (fromStage) {
      const check = this.validateTransition(fromStage, toStage);
      if (!check.allowed) {
        toast.error(check.reason);
        return false;
      }
    }

    const cfg = this._cfg[toStage];
    if (!cfg) return true; // no modal needed for other stages

    this._stage = toStage;
    this._card  = card;

    await this._loadSellers();
    this._render(cfg, card);

    document.getElementById('modal-stage-ref').classList.add('open');
    setTimeout(() => {
      const inp = document.getElementById('stage-ref-input');
      const mot = document.getElementById('stage-ref-motivo');
      (inp || mot)?.focus();
    }, 120);

    return new Promise(resolve => { this._resolve = resolve; });
  },

  // ── Render modal content ──────────────────────────────────
  _render(cfg, card) {
    const q = id => document.getElementById(id);

    // Title & accent
    q('stage-ref-title-text').textContent = cfg.title;
    const titleIcon = q('stage-ref-title-icon');
    if (titleIcon) {
      titleIcon.className = `ph-fill ${cfg.icon}`;
      titleIcon.style.color = cfg.accentColor;
    }

    // Accent bar
    const bar = q('stage-ref-accent-bar');
    if (bar) bar.style.background = cfg.accentColor;

    // Card context
    if (card) {
      q('stage-ref-client-name').textContent = card.client_name || '—';
      q('stage-ref-card-title').textContent  = card.title || card.client_name || '—';
      q('stage-ref-risk').textContent        = utils.fmt.currency(card.value_at_risk || 0);
      q('stage-ref-ltv').textContent         = utils.fmt.currency(card.ltv || 0);
    }

    // Reference number field
    const refGroup = q('stage-ref-ref-group');
    if (refGroup) {
      refGroup.style.display = cfg.inputLabel ? '' : 'none';
    }
    if (cfg.inputLabel) {
      q('stage-ref-input-label').textContent = cfg.inputLabel;
      q('stage-ref-input').placeholder       = cfg.placeholder || '';
      q('stage-ref-hint').textContent        = cfg.hint || '';
      q('stage-ref-input').value             = '';
    }

    // Motivo field (declined only)
    const motivoGroup = q('stage-ref-motivo-group');
    if (motivoGroup) {
      motivoGroup.style.display = (this._stage === 'declined') ? '' : 'none';
    }
    if (q('stage-ref-motivo')) q('stage-ref-motivo').value = '';

    // Notes
    const notesGroup = q('stage-ref-notes-group');
    if (notesGroup) notesGroup.style.display = cfg.showNotes ? '' : 'none';
    if (q('stage-ref-notes')) q('stage-ref-notes').value = '';

    // Confirm button
    const confirmBtn = q('stage-ref-confirm-btn');
    if (confirmBtn) {
      confirmBtn.className = `btn ${cfg.confirmClass || 'btn-primary'}`;
      confirmBtn.disabled  = false;
      confirmBtn.innerHTML = `<i class="ph ph-check-circle"></i> <span>${cfg.confirmText}</span>`;
    }

    // Seller
    this._populateSellers();
  },

  // ── Sellers ───────────────────────────────────────────────
  async _loadSellers() {
    if (this._sellers.length) return;
    try { this._sellers = await api.getSellers(); } catch (_) {}
  },

  _populateSellers() {
    const sel = document.getElementById('stage-ref-seller');
    if (!sel) return;
    sel.innerHTML = '<option value="">Selecione o vendedor</option>' +
      this._sellers.map(s => {
        const role = { admin: 'Admin', manager: 'Gerente', seller: 'Vendedor' }[s.role] || s.role;
        return `<option value="${s.id}">${s.name} — ${role}</option>`;
      }).join('');
    if (this._card?.seller_id) sel.value = this._card.seller_id;
  },

  // ── Confirm ───────────────────────────────────────────────
  async _confirm() {
    const cfg      = this._cfg[this._stage];
    const refNum   = document.getElementById('stage-ref-input')?.value?.trim();
    const motivo   = document.getElementById('stage-ref-motivo')?.value?.trim();
    const notes    = document.getElementById('stage-ref-notes')?.value?.trim();
    const sellerId = document.getElementById('stage-ref-seller')?.value;

    // Validate ref number
    if (cfg.refRequired && !refNum) {
      this._shake('stage-ref-input');
      toast.error(`Informe o ${cfg.inputLabel.toLowerCase()}`);
      return;
    }

    // Validate motivo for declined
    if (this._stage === 'declined' && !motivo) {
      this._shake('stage-ref-motivo');
      toast.error('Informe o motivo do declínio');
      return;
    }

    if (!sellerId) {
      toast.error('Selecione o vendedor responsável');
      return;
    }

    // Disable button
    const btn = document.getElementById('stage-ref-confirm-btn');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Salvando...'; }

    try {
      // Build description
      let description = '';
      if (this._stage === 'declined') {
        description = `${cfg.historyPrefix}: ${motivo}` + (notes ? ` — ${notes}` : '');
      } else {
        description = `${cfg.historyPrefix}: ${refNum}` + (notes ? ` — ${notes}` : '');
      }

      await api.createAction({
        card_id:     this._card.id,
        client_id:   this._card.client_id,
        seller_id:   sellerId,
        action_type: cfg.actionType,
        description,
      });

      // Capture resolve BEFORE closing (close nulls it)
      const resolve = this._resolve;
      this._close();
      resolve?.(true);   // ← fire AFTER close, using captured reference

    } catch (err) {
      toast.error('Erro ao registrar: ' + err.message);
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `<i class="ph ph-check-circle"></i> <span>${cfg.confirmText}</span>`;
      }
    }
  },

  _cancel() {
    // Capture resolve BEFORE closing
    const resolve = this._resolve;
    this._close();
    resolve?.(false);
  },

  _close() {
    document.getElementById('modal-stage-ref')?.classList.remove('open');
    this._resolve = null;
  },

  _shake(inputId) {
    const el = document.getElementById(inputId);
    if (!el) return;
    el.classList.add('input-error');
    el.focus();
    setTimeout(() => el.classList.remove('input-error'), 1000);
  },

  // ── Init (bind events once) ───────────────────────────────
  init() {
    document.getElementById('stage-ref-confirm-btn')
      ?.addEventListener('click', () => this._confirm());

    ['stage-ref-cancel', 'stage-ref-cancel-btn'].forEach(id => {
      document.getElementById(id)?.addEventListener('click', () => this._cancel());
    });

    document.getElementById('stage-ref-input')
      ?.addEventListener('keydown', e => {
        if (e.key === 'Enter')  { e.preventDefault(); this._confirm(); }
        if (e.key === 'Escape') this._cancel();
      });

    document.getElementById('stage-ref-motivo')
      ?.addEventListener('keydown', e => {
        if (e.key === 'Escape') this._cancel();
      });

    document.getElementById('modal-stage-ref')
      ?.addEventListener('click', e => {
        if (e.target.id === 'modal-stage-ref') this._cancel();
      });
  },
};

document.addEventListener('DOMContentLoaded', () => stageRefModal.init());
window.stageRefModal = stageRefModal;
