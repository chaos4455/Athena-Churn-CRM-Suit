/* ============================================================
   Athena CRM — Performance Page
   ============================================================ */

const performancePage = {
  _activeTab:   'overview',
  _activeScope: 'current',
  _filters:     { branch: '', state: '', seller_id: '' },
  _charts:      {},
  _sellers:     [],

  // Sort state for sellers table
  _sort: { col: 'conversion_rate', dir: 'desc' },

  /** Ordenação da tabela «Todos os Cards» (Visão Geral) — independente da aba Vendedores */
  _overviewSort: { col: 'created_at', dir: 'desc' },
  _overviewCache: null,

  // ── Init ──────────────────────────────────────────────────
  async init() {
    await this._loadFilterOptions();
    this._bindTabs();
    this._bindScopeToggle();
    this._bindFilters();
    this._bindSortButtons();
    this._bindSellersColumnSort();
    this._bindOverviewColumnSort();
    await this.loadAll();
  },

  // ── Filter options ────────────────────────────────────────
  async _loadFilterOptions() {
    try {
      const [opts, sellers] = await Promise.all([
        api.getFilterOptions(),
        api.getSellers(),
      ]);
      this._sellers = sellers;
      state.set('sellers', sellers);
      this._populateSelect('perf-filter-branch', opts.branches, 'Todas as Filiais');
      this._populateSelect('perf-filter-state',  opts.states,   'Todos os Estados');
      this._populateSelect(
        'perf-filter-seller',
        sellers.map(s => s.id),
        'Todos os Vendedores',
        sellers.map(s => s.name)
      );
    } catch (_) {}
  },

  _populateSelect(id, values, placeholder, labels = null) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = `<option value="">${placeholder}</option>` +
      values.map((v, i) => `<option value="${v}">${labels ? labels[i] : v}</option>`).join('');
  },

  _bindFilters() {
    [['perf-filter-branch','branch'],['perf-filter-state','state'],['perf-filter-seller','seller_id']]
      .forEach(([id, key]) => {
        document.getElementById(id)?.addEventListener('change', async (e) => {
          this._filters[key] = e.target.value;
          await this.loadAll();
        });
      });
  },

  // ── Tabs ──────────────────────────────────────────────────
  _bindTabs() {
    document.querySelectorAll('[data-perf-tab]').forEach(btn => {
      btn.addEventListener('click', async () => {
        this._activeTab = btn.dataset.perfTab;
        document.querySelectorAll('[data-perf-tab]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        document.querySelectorAll('[data-perf-panel]').forEach(p => {
          p.style.display = p.dataset.perfPanel === this._activeTab ? '' : 'none';
        });
        await this.loadAll();
      });
    });
  },

  // ── Scope toggle ──────────────────────────────────────────
  _bindScopeToggle() {
    document.querySelectorAll('[data-scope]').forEach(btn => {
      btn.addEventListener('click', async () => {
        this._activeScope = btn.dataset.scope;
        document.querySelectorAll('[data-scope]').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        await this.loadAll();
      });
    });
  },

  // ── Sort buttons (quick sort) ─────────────────────────────
  _bindSortButtons() {
    document.querySelectorAll('.sort-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const col = btn.dataset.sort;
        if (this._sort.col === col) {
          this._sort.dir = this._sort.dir === 'desc' ? 'asc' : 'desc';
        } else {
          this._sort.col = col;
          this._sort.dir = 'desc';
        }
        document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this._loadSellers();
      });
    });
  },

  // ── Column header sort — apenas aba Vendedores ────────────
  _bindSellersColumnSort() {
    document.querySelectorAll('#sellers-table th.sortable').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (this._sort.col === col) {
          this._sort.dir = this._sort.dir === 'desc' ? 'asc' : 'desc';
        } else {
          this._sort.col = col;
          this._sort.dir = 'desc';
        }
        document.querySelectorAll('#sellers-table th.sortable').forEach(h => {
          h.classList.remove('asc', 'desc');
        });
        th.classList.add(this._sort.dir);
        this._loadSellers();
      });
    });
  },

  /** Clique nos TH da Visão Geral: reordena só a tabela (dados já em cache). */
  _bindOverviewColumnSort() {
    document.querySelectorAll('#perf-overview-table thead th.sortable').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.col;
        if (!col) return;
        if (this._overviewSort.col === col) {
          this._overviewSort.dir = this._overviewSort.dir === 'desc' ? 'asc' : 'desc';
        } else {
          this._overviewSort.col = col;
          this._overviewSort.dir = col === 'created_at' ? 'desc' : 'asc';
        }
        document.querySelectorAll('#perf-overview-table thead th.sortable').forEach(h => {
          h.classList.remove('asc', 'desc');
        });
        th.classList.add(this._overviewSort.dir);
        this._renderOverviewTableBody();
      });
    });
  },

  _stageOrderIdx(stage) {
    const order = ['backlog', 'in_progress', 'in_negotiation', 'converted', 'declined'];
    const i = order.indexOf(stage);
    return i >= 0 ? i : 99;
  },

  /** Comparação estável para colunas da overview (texto, número, data, estágio, referência). */
  _compareOverviewRows(a, b, col) {
    let av; let bv;
    switch (col) {
      case 'stage':
        av = this._stageOrderIdx(a.stage);
        bv = this._stageOrderIdx(b.stage);
        break;
      case 'reference':
        av = (a._refSort || '').toLowerCase();
        bv = (b._refSort || '').toLowerCase();
        break;
      case 'created_at':
        av = new Date(a.created_at).getTime() || 0;
        bv = new Date(b.created_at).getTime() || 0;
        break;
      case 'value_at_risk':
      case 'avg_ticket':
        av = Number(a[col]) || 0;
        bv = Number(b[col]) || 0;
        break;
      case 'cycle_id':
        av = String(a.cycle_id ?? '');
        bv = String(b.cycle_id ?? '');
        if (!Number.isNaN(Number(av)) && !Number.isNaN(Number(bv))) {
          av = Number(av);
          bv = Number(bv);
        } else {
          av = av.toLowerCase();
          bv = bv.toLowerCase();
        }
        break;
      default:
        av = String(a[col] ?? '').toLowerCase();
        bv = String(b[col] ?? '').toLowerCase();
    }
    if (av < bv) return -1;
    if (av > bv) return 1;
    return 0;
  },

  _sortedOverviewRows(cards, refMap) {
    const mul = this._overviewSort.dir === 'desc' ? -1 : 1;
    const rows = cards.map(r => ({
      ...r,
      _refSort: refMap[r.id]?.ref?.ref ?? '',
    }));
    rows.sort((a, b) => mul * this._compareOverviewRows(a, b, this._overviewSort.col));
    return rows;
  },

  _syncOverviewSortHeaders() {
    const { col, dir } = this._overviewSort;
    document.querySelectorAll('#perf-overview-table thead th.sortable').forEach(h => {
      h.classList.remove('asc', 'desc');
      if (h.dataset.col === col) h.classList.add(dir);
    });
  },

  /** Só redesenha tbody (após ordenar ou após fetch). */
  _renderOverviewTableBody() {
    const cache = this._overviewCache;
    const tbody = document.getElementById('perf-table-body');
    if (!cache || !tbody) return;

    const { cards, refMap } = cache;
    this._syncOverviewSortHeaders();
    const sorted = this._sortedOverviewRows(cards, refMap);

    tbody.innerHTML = sorted.map(r => {
      const cardRef = refMap[r.id];
      const refCell = cardRef ? utils.refBadge(cardRef.ref) : '—';
      const { _refSort, ...cardPayload } = r;
      return `
          <tr style="cursor:pointer" onclick='cardDetail.open(${JSON.stringify(cardPayload).replace(/'/g,"&#39;")})'>
            <td><strong>${r.client_name}</strong></td>
            <td><span style="font-size:.8rem;color:var(--text-secondary)">${r.seller_name || '—'}</span></td>
            <td>${r.branch ? `<span class="badge badge-purple">${r.branch}</span>` : '—'}</td>
            <td>${r.state  ? `<span class="badge badge-blue">${r.state}</span>`   : '—'}</td>
            <td>${utils.stageBadge(r.stage)}</td>
            <td>${refCell}</td>
            <td><span style="color:var(--danger);font-weight:700">${utils.fmt.currency(r.value_at_risk)}</span></td>
            <td>${utils.fmt.currency(r.avg_ticket)}</td>
            <td>${r.cycle_id ? `<span class="badge badge-gray">${r.cycle_id}</span>` : '—'}</td>
            <td style="font-size:.78rem;color:var(--text-muted)">${utils.fmt.date(r.created_at)}</td>
          </tr>`;
    }).join('');
  },

  _getParams() {
    const p = { archived: this._activeScope === 'history' };
    if (this._filters.branch)    p.branch    = this._filters.branch;
    if (this._filters.state)     p.state     = this._filters.state;
    if (this._filters.seller_id) p.seller_id = this._filters.seller_id;
    return p;
  },

  // ── Load all ──────────────────────────────────────────────
  async loadAll() {
    if (this._activeTab === 'overview') await this._loadOverview();
    if (this._activeTab === 'actions')  await this._loadActions();
    if (this._activeTab === 'sellers')  await this._loadSellers();
  },

  // ── Overview tab ──────────────────────────────────────────
  async _loadOverview() {
    try {
      const params = this._getParams();
      const [cards, allActions] = await Promise.all([
        api.getCards(params),
        api.getActions(this._filters.seller_id ? { seller_id: this._filters.seller_id } : {}),
      ]);
      state.set('cards', cards);

      // Build ref map: card_id → latest ref action
      const refMap = {};
      allActions.forEach(a => {
        const ref = utils.parseActionRef(a.description);
        if (ref && a.card_id) {
          // Keep the most recent one per card
          if (!refMap[a.card_id] || new Date(a.created_at) > new Date(refMap[a.card_id].created_at)) {
            refMap[a.card_id] = { ref, created_at: a.created_at };
          }
        }
      });

      const total     = cards.length;
      const converted = cards.filter(c => c.stage === 'converted').length;
      const declined  = cards.filter(c => c.stage === 'declined').length;
      const inNeg     = cards.filter(c => c.stage === 'in_negotiation').length;
      const inProg    = cards.filter(c => c.stage === 'in_progress').length;
      const valueRisk = cards.reduce((s, c) => s + (c.value_at_risk || 0), 0);
      const convRate  = total ? (converted / total * 100).toFixed(1) : 0;

      this._set('ov-total',     total);
      this._set('ov-converted', converted);
      this._set('ov-declined',  declined);
      this._set('ov-in-neg',    inNeg);
      this._set('ov-in-prog',   inProg);
      this._set('ov-value',     utils.fmt.currency(valueRisk));
      this._set('ov-conv-rate', convRate + '%');

      const countEl = document.getElementById('perf-count');
      if (countEl) countEl.textContent = `${total} registros`;

      this._overviewCache = { cards, refMap };
      this._renderOverviewTableBody();

      // Chart
      Object.values(this._charts).forEach(c => c?.destroy?.());
      this._charts = {};
      const stages = ['backlog','in_progress','in_negotiation','converted','declined'];
      const counts = stages.map(s => cards.filter(c => c.stage === s).length);
      this._charts.bar = charts.bar('chart-perf-stages',
        stages.map(s => utils.stageMeta[s].label),
        [{ data: counts,
           backgroundColor: ['#7c3aed','#3b82f6','#f59e0b','#10b981','#ef4444'],
           borderRadius: 6 }]
      );
    } catch (e) { toast.error('Erro ao carregar overview: ' + e.message); }
  },

  // ── Actions tab ───────────────────────────────────────────
  async _loadActions() {
    try {
      const params = {};
      if (this._filters.seller_id) params.seller_id = this._filters.seller_id;
      const actions = await api.getActions(params);

      const el = document.getElementById('actions-count');
      if (el) el.textContent = `${actions.length} ações`;

      const tbody = document.getElementById('actions-table-body');
      if (!tbody) return;

      if (!actions.length) {
        tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;padding:2rem;color:var(--text-muted)">
          <i class="ph ph-lightning" style="font-size:1.5rem;display:block;margin-bottom:.5rem;opacity:.3"></i>
          Nenhuma ação registrada
        </td></tr>`;
        return;
      }

      // Type chip CSS class map
      const typeClsMap = {
        call: 'call', email: 'email', meeting: 'meeting',
        whatsapp: 'whatsapp', note: 'note', proposal: 'proposal',
      };

      // Stage result config
      const stageCfg = {
        backlog:        { label: 'Backlog',       cls: 'badge-gray',   icon: 'ph-tray'         },
        in_progress:    { label: 'Em Andamento',  cls: 'badge-blue',   icon: 'ph-arrow-right'  },
        in_negotiation: { label: 'Em Negociação', cls: 'badge-orange', icon: 'ph-handshake'    },
        converted:      { label: 'Convertido ✓',  cls: 'badge-green',  icon: 'ph-check-circle' },
        declined:       { label: 'Declinado ✗',   cls: 'badge-red',    icon: 'ph-x-circle'     },
      };

      // Status config
      const statusCfg = {
        pending:       { label: 'Pendente',   cls: 'badge-orange' },
        completed:     { label: 'Concluída',  cls: 'badge-green'  },
        cancelled:     { label: 'Cancelada',  cls: 'badge-red'    },
        in_negotiation:{ label: 'Em Neg.',    cls: 'badge-orange' },
        converted:     { label: 'Convertido', cls: 'badge-green'  },
        declined:      { label: 'Declinado',  cls: 'badge-red'    },
        detected:      { label: 'Detectado',  cls: 'badge-blue'   },
      };

      tbody.innerHTML = actions.map(a => {
        const typeMeta   = utils.actionMeta[a.action_type] || { label: a.action_type, icon: 'ph-activity' };
        const typeCls    = typeClsMap[a.action_type] || 'note';
        const statusMeta = statusCfg[a.status] || { label: a.status, cls: 'badge-gray' };
        const sc         = stageCfg[a.card_stage] || null;
        const shortId    = a.card_id ? a.card_id.split('-')[0].toUpperCase() : '—';

        // ── Parse reference number ─────────────────────────
        const ref = utils.parseActionRef(a.description);

        // Result pill
        let resultHtml = '—';
        if (sc) {
          let label = sc.label;
          if (a.card_is_archived) {
            if (a.card_stage === 'converted')     label = 'Convertido e Arq. ✓';
            else if (a.card_stage === 'declined') label = 'Declinado e Arq. ✗';
            else                                  label = sc.label + ' (Arq.)';
          }
          const archiveBadge = a.card_is_archived
            ? `<span class="badge badge-gray" style="font-size:.6rem;margin-left:3px"><i class="ph ph-archive"></i></span>`
            : '';
          resultHtml = `
            <div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap">
              <span class="act-result-pill ${sc.cls}">
                <i class="ph ${sc.icon}"></i> ${label}
              </span>${archiveBadge}
              ${a.card_cycle_id ? `<span style="font-size:.62rem;color:var(--text-muted)">${a.card_cycle_id}</span>` : ''}
            </div>`;
        }

        // Seller info
        const sellerInfo = this._sellers.find(s => s.id === a.seller_id);
        const sellerBranch = sellerInfo?.branch
          ? `<span class="badge badge-gray" style="font-size:.6rem">${sellerInfo.branch.replace('Filial ','')}</span>`
          : '';

        return `
          <tr>
            <td>
              <span class="act-type-chip act-type-${typeCls}">
                <i class="ph ${typeMeta.icon}"></i> ${typeMeta.label}
              </span>
            </td>
            <td>
              ${a.client_name
                ? `<a href="client-detail.html?id=${a.client_id}" class="act-client-link">
                     <i class="ph ph-user"></i> ${a.client_name}
                   </a>`
                : `<span style="color:var(--text-muted);font-size:.78rem">${a.client_id?.split('-')[0] || '—'}</span>`}
            </td>
            <td>
              <button class="act-card-btn"
                onclick="performancePage._openCard('${a.card_id}')">
                <i class="ph ph-kanban"></i>
                ${a.card_title ? a.card_title.substring(0, 22) + (a.card_title.length > 22 ? '…' : '') : '#' + shortId}
              </button>
            </td>
            <td>
              <div style="display:flex;flex-direction:column;gap:2px">
                <span style="font-size:.8rem;font-weight:600">${a.seller_name || '—'}</span>
                ${sellerBranch}
              </div>
            </td>
            <td>
              ${sellerInfo?.branch
                ? `<span class="badge badge-purple" style="font-size:.65rem">${sellerInfo.branch.replace('Filial ','')}</span>`
                : '—'}
            </td>
            <td>
              <span class="act-desc" title="${a.description}">${ref ? utils.refBadge(ref) : a.description}</span>
            </td>
            <td>
              <span class="badge ${statusMeta.cls}">${statusMeta.label}</span>
            </td>
            <td>${resultHtml}</td>
            <td style="font-size:.75rem;color:var(--text-muted);white-space:nowrap">
              ${utils.fmt.datetime(a.created_at)}
            </td>
          </tr>`;
      }).join('');
    } catch (e) { toast.error('Erro ao carregar ações: ' + e.message); }
  },

  // Open card detail from action row
  async _openCard(cardId) {
    if (!cardId) return;
    try {
      const card = await api.getCard(cardId);
      cardDetail.open(card);
    } catch (e) {
      toast.error('Erro ao carregar card: ' + e.message);
    }
  },

  // ── Sellers tab ───────────────────────────────────────────
  async _loadSellers() {
    try {
      const params  = this._getParams();
      const team    = await api.getTeamPerformance(params);
      const sellers = [...(team.sellers || [])];

      // Sort
      const { col, dir } = this._sort;
      sellers.sort((a, b) => {
        const av = typeof a[col] === 'string' ? a[col].toLowerCase() : (a[col] ?? 0);
        const bv = typeof b[col] === 'string' ? b[col].toLowerCase() : (b[col] ?? 0);
        return dir === 'desc' ? (bv > av ? 1 : -1) : (av > bv ? 1 : -1);
      });

      document.querySelectorAll('#sellers-table th.sortable').forEach(th => {
        th.classList.remove('asc', 'desc');
        if (th.dataset.col === col) th.classList.add(dir);
      });

      // Totals banner
      const t  = team.totals;
      const el = document.getElementById('sellers-totals');
      if (el) {
        const teamRate = t.conversion_rate.toFixed(1);
        const rateColor = t.conversion_rate >= 50 ? 'var(--success)' : t.conversion_rate >= 25 ? 'var(--warning)' : 'var(--danger)';
        el.innerHTML = `
          <div style="display:flex;gap:1rem;flex-wrap:wrap;padding:.875rem 1.25rem;
            background:var(--brand-light);border:1px solid var(--brand-secondary);
            border-radius:var(--radius-md);font-size:.82rem;align-items:center">
            <span style="font-weight:700;color:var(--brand-primary)"><i class="ph ph-users-three"></i> Time</span>
            <span><strong>${t.total_cards}</strong> cards</span>
            <span style="color:var(--success)"><strong>${t.converted}</strong> convertidos</span>
            <span style="color:var(--danger)"><strong>${t.declined}</strong> declinados</span>
            <span style="color:var(--warning)"><strong>${t.in_negotiation}</strong> em negociação</span>
            <span style="color:var(--info)"><strong>${t.in_progress}</strong> em andamento</span>
            <span style="color:var(--text-muted)"><strong>${t.total_actions}</strong> ações</span>
            <span style="margin-left:auto;font-weight:800;font-size:.9rem;color:${rateColor}">${teamRate}% conversão</span>
          </div>`;
      }

      // Table
      const tbody = document.getElementById('sellers-table-body');
      if (!tbody) return;

      if (!sellers.length) {
        tbody.innerHTML = `<tr><td colspan="11" style="text-align:center;padding:2rem;color:var(--text-muted)">Sem dados</td></tr>`;
        return;
      }

      const maxCards = Math.max(...sellers.map(s => s.total_cards)) || 1;

      tbody.innerHTML = sellers.map((s, i) => {
        const rank     = i + 1;
        const rankCls  = rank === 1 ? 'rank-1' : rank === 2 ? 'rank-2' : rank === 3 ? 'rank-3' : 'rank-n';
        const initials = s.seller_name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
        const rate     = s.conversion_rate;
        const rateColor = rate >= 50 ? 'var(--success)' : rate >= 25 ? 'var(--warning)' : 'var(--danger)';
        const cardsPct  = ((s.total_cards / maxCards) * 100).toFixed(0);

        return `
          <tr>
            <td><span class="rank-badge ${rankCls}">${rank}</span></td>
            <td>
              <div class="seller-chip">
                <div class="seller-av">${initials}</div>
                <div>
                  <div class="seller-av-name">${s.seller_name}</div>
                  <div class="seller-av-sub">${s.state || '—'}</div>
                </div>
              </div>
            </td>
            <td>${s.branch ? `<span class="badge badge-purple" style="font-size:.65rem">${s.branch.replace('Filial ','')}</span>` : '—'}</td>
            <td>${s.state  ? `<span class="badge badge-blue"   style="font-size:.65rem">${s.state}</span>` : '—'}</td>
            <td>
              <div class="conv-bar-wrap">
                <div class="conv-bar">
                  <div class="conv-bar-fill" style="width:${cardsPct}%;background:var(--brand-primary)"></div>
                </div>
                <span style="font-size:.75rem;font-weight:700;min-width:20px">${s.total_cards}</span>
              </div>
            </td>
            <td><span class="badge badge-green">${s.converted}</span></td>
            <td><span class="badge badge-red">${s.declined}</span></td>
            <td><span style="color:var(--warning);font-weight:700">${s.in_negotiation}</span></td>
            <td>
              <div class="conv-bar-wrap">
                <div class="conv-bar">
                  <div class="conv-bar-fill" style="width:${Math.min(rate,100)}%;background:${rateColor}"></div>
                </div>
                <span class="conv-bar-lbl" style="color:${rateColor}">${rate.toFixed(1)}%</span>
              </div>
            </td>
            <td><span class="badge badge-blue">${s.total_actions}</span></td>
            <td>
              <button class="view-actions-btn"
                onclick="performancePage._viewSellerActions('${s.seller_id}','${s.seller_name.replace(/'/g,'\\\'')}')"
              >
                <i class="ph ph-lightning"></i> Ver Ações
              </button>
            </td>
          </tr>`;
      }).join('');
    } catch (e) { toast.error('Erro ao carregar vendedores: ' + e.message); }
  },

  // Jump to actions tab filtered by seller
  _viewSellerActions(sellerId, sellerName) {
    // Set filter
    this._filters.seller_id = sellerId;
    const sel = document.getElementById('perf-filter-seller');
    if (sel) sel.value = sellerId;

    // Switch to actions tab
    const actTab = document.querySelector('[data-perf-tab="actions"]');
    if (actTab) actTab.click();

    toast.info(`Ações de: ${sellerName}`);
  },

  _set(id, val) {
    const el = document.getElementById(id);
    if (el) el.textContent = val;
  },
};

window.performancePage = performancePage;
