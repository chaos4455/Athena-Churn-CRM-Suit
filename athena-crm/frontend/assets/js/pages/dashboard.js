/* ============================================================
   Athena CRM — Dashboard Page
   Real data from API — no fake projections
   ============================================================ */

const dashboardPage = {
  _charts:      {},
  _filters:     { branch: '', state: '', seller_id: '' },
  _data:        null,
  _perfData:    null,
  _sortKey:     'conv',   // 'conv' | 'cards'

  // ── Stage palette ─────────────────────────────────────────
  _stageColors: {
    backlog:        '#94a3b8',
    in_progress:    '#3b82f6',
    in_negotiation: '#f59e0b',
    converted:      '#10b981',
    declined:       '#ef4444',
  },
  _stageLabels: {
    backlog:        'Backlog',
    in_progress:    'Em Andamento',
    in_negotiation: 'Em Negociação',
    converted:      'Convertido',
    declined:       'Declinado',
  },

  // ── Entry point ───────────────────────────────────────────
  async init() {
    this._setCycle();
    await this._loadFilterOptions();
    this._bindFilters();
    await this._loadAll();
  },

  async refresh() {
    const btn = document.getElementById('btn-refresh');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="ph ph-spinner animate-spin"></i> Atualizando...'; }
    await this._loadAll();
    if (btn) { btn.disabled = false; btn.innerHTML = '<i class="ph ph-arrows-clockwise"></i> Atualizar'; }
  },

  _setCycle() {
    const el = document.getElementById('dash-cycle');
    if (el) {
      const now = new Date();
      el.textContent = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    }
  },

  // ── Filters ───────────────────────────────────────────────
  async _loadFilterOptions() {
    try {
      const [opts, sellers] = await Promise.all([
        api.getFilterOptions(),
        api.getSellers(),
      ]);
      this._populateSelect('filter-branch', opts.branches || [], 'Todas as Filiais');
      this._populateSelect('filter-state',  opts.states   || [], 'Todos os Estados');

      // Seller filter
      const selEl = document.getElementById('filter-seller');
      if (selEl) {
        selEl.innerHTML = '<option value="">Todos os Vendedores</option>' +
          sellers.map(s => {
            const role = { admin: 'Admin', manager: 'Gerente', seller: 'Vendedor' }[s.role] || s.role;
            return `<option value="${s.id}">${s.name} (${role})</option>`;
          }).join('');
      }
    } catch (_) {}
  },

  _populateSelect(id, items, placeholder) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = `<option value="">${placeholder}</option>` +
      items.map(v => `<option value="${v}">${v}</option>`).join('');
  },

  _bindFilters() {
    document.getElementById('filter-branch')?.addEventListener('change', async (e) => {
      this._filters.branch = e.target.value;
      await this._loadAll();
    });
    document.getElementById('filter-state')?.addEventListener('change', async (e) => {
      this._filters.state = e.target.value;
      await this._loadAll();
    });
    document.getElementById('filter-seller')?.addEventListener('change', async (e) => {
      this._filters.seller_id = e.target.value;
      await this._loadAll();
    });
  },

  // ── Load everything ───────────────────────────────────────
  async _loadAll() {
    try {
      const params = {};
      if (this._filters.branch)    params.branch    = this._filters.branch;
      if (this._filters.state)     params.state     = this._filters.state;
      if (this._filters.seller_id) params.seller_id = this._filters.seller_id;

      // Performance table also respects all filters
      const perfParams = { ...params };

      const [data, perf] = await Promise.all([
        api.getDashboard(params),
        api.getTeamPerformance(perfParams),
      ]);

      this._data     = data;
      this._perfData = perf;
      state.set('dashboard', data);

      this._updateSellerBanner();
      this._renderKPIs(data);
      this._renderPipeline(data);
      this._renderCharts(data);
      this._renderBreakdownBranch(data.by_branch || {});
      this._renderBreakdownState(data.by_state   || {});
      this._renderSellerCycle(perf);
      this._renderSellerHistory(perf);
    } catch (e) {
      toast.error('Erro ao carregar dashboard: ' + e.message);
    }
  },

  // ── Seller context banner ─────────────────────────────────
  _updateSellerBanner() {
    // Remove existing banner
    document.getElementById('seller-active-banner')?.remove();

    if (!this._filters.seller_id) return;

    const selEl = document.getElementById('filter-seller');
    const sellerName = selEl?.options[selEl.selectedIndex]?.text || 'Vendedor';

    const banner = document.createElement('div');
    banner.id = 'seller-active-banner';
    banner.style.cssText = `
      display:flex; align-items:center; gap:.75rem;
      background:var(--brand-light); border:1.5px solid var(--brand-secondary);
      border-radius:var(--radius-md); padding:.625rem 1rem;
      margin-bottom:1rem; font-size:.82rem; color:var(--brand-primary);
      font-weight:600; animation:fadeIn .25s ease both;
    `;
    banner.innerHTML = `
      <i class="ph-fill ph-user-circle" style="font-size:1.1rem"></i>
      Filtrando por vendedor: <strong>${sellerName}</strong>
      — todos os indicadores, gráficos e tabelas refletem apenas este vendedor.
      <button onclick="document.getElementById('filter-seller').value='';dashboardPage._filters.seller_id='';dashboardPage._loadAll()"
        style="margin-left:auto;background:none;border:none;cursor:pointer;color:var(--brand-primary);font-size:.8rem;display:flex;align-items:center;gap:4px;font-weight:600;white-space:nowrap">
        <i class="ph ph-x-circle"></i> Limpar
      </button>
    `;

    // Insert after page header
    const header = document.querySelector('.dash-header');
    header?.insertAdjacentElement('afterend', banner);
  },

  // ── Sort sellers ──────────────────────────────────────────
  sortSellers(key) {
    this._sortKey = key;
    if (this._perfData) this._renderSellerHistory(this._perfData);

    // Visual feedback on sort buttons
    ['conv','cards'].forEach(k => {
      const btn = document.getElementById('btn-sort-' + k);
      if (btn) btn.classList.toggle('btn-primary', k === key);
      if (btn) btn.classList.toggle('btn-secondary', k !== key);
    });
  },

  // ── KPI Row 1 ─────────────────────────────────────────────
  _renderKPIs(data) {
    const sc    = data.stage_counts || {};
    const conv  = sc.converted || 0;
    const total = data.total_cards || 1;
    const rate  = ((conv / total) * 100).toFixed(1);

    this._set('kpi-total-cards',    utils.fmt.number(data.total_cards));
    this._set('kpi-at-risk',        utils.fmt.number(data.clients_at_risk));
    this._set('kpi-value-risk',     utils.fmt.currency(data.total_value_at_risk));
    this._set('kpi-avg-ticket',     utils.fmt.currency(data.avg_ticket_at_risk));
    this._set('kpi-converted-main', utils.fmt.number(conv));
    this._set('kpi-conv-rate',      rate + '%');
  },

  // ── KPI Row 2 — Pipeline ──────────────────────────────────
  _renderPipeline(data) {
    const sc    = data.stage_counts || {};
    const total = data.total_cards  || 1;

    const stages = [
      { key: 'backlog',        kpiId: 'kpi-backlog',      pctId: 'pct-backlog' },
      { key: 'in_progress',    kpiId: 'kpi-in-progress',  pctId: 'pct-in-progress' },
      { key: 'in_negotiation', kpiId: 'kpi-in-neg',       pctId: 'pct-in-neg' },
      { key: 'converted',      kpiId: 'kpi-converted',    pctId: 'pct-converted' },
      { key: 'declined',       kpiId: 'kpi-declined',     pctId: 'pct-declined' },
    ];

    stages.forEach(({ key, kpiId, pctId }) => {
      const val = sc[key] || 0;
      const pct = ((val / total) * 100).toFixed(0);
      this._set(kpiId, val);
      this._set(pctId, pct + '%');
    });
  },

  // ── Charts ────────────────────────────────────────────────
  _renderCharts(data) {
    Object.values(this._charts).forEach(c => c?.destroy?.());
    this._charts = {};

    const sc       = data.stage_counts || {};
    const byBranch = data.by_branch    || {};

    this._chartValueByStage(sc, data.total_value_at_risk);
    this._chartPipelineDoughnut(sc);
    this._chartBranchCards(byBranch);
    this._chartBranchRisk(byBranch);
    this._chartBranchConversion(byBranch);
  },

  _chartValueByStage(sc, totalRisk) {
    const stageOrder = ['backlog','in_progress','in_negotiation','converted','declined'];
    const total  = stageOrder.reduce((s, k) => s + (sc[k] || 0), 0) || 1;
    const values = stageOrder.map(k => Math.round(totalRisk * ((sc[k] || 0) / total)));
    const labels = stageOrder.map(k => this._stageLabels[k]);
    const colors = stageOrder.map(k => this._stageColors[k]);

    const ctx = document.getElementById('chart-value-stage')?.getContext('2d');
    if (!ctx) return;
    const d = charts._defaults();
    this._charts.valueStage = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [{ label: 'Valor em Risco (R$)', data: values,
          backgroundColor: colors.map(c => c + 'cc'), borderColor: colors,
          borderWidth: 1.5, borderRadius: 6, borderSkipped: false }],
      },
      options: {
        responsive: true, maintainAspectRatio: false, indexAxis: 'y',
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: c => ' ' + utils.fmt.currency(c.parsed.x) } } },
        scales: {
          x: { grid: { color: d.gridColor }, ticks: { color: d.textColor,
            callback: v => 'R$' + (v >= 1000 ? (v/1000).toFixed(0)+'k' : v) } },
          y: { grid: { display: false }, ticks: { color: d.textColor, font: { size: 11 } } },
        },
      },
    });
  },

  _chartPipelineDoughnut(sc) {
    const stageOrder = ['backlog','in_progress','in_negotiation','converted','declined'];
    const ctx = document.getElementById('chart-stages')?.getContext('2d');
    if (!ctx) return;
    const d = charts._defaults();
    this._charts.doughnut = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: stageOrder.map(k => this._stageLabels[k]),
        datasets: [{ data: stageOrder.map(k => sc[k] || 0),
          backgroundColor: stageOrder.map(k => this._stageColors[k]),
          borderWidth: 0, hoverOffset: 10 }],
      },
      options: {
        responsive: true, maintainAspectRatio: false, cutout: '68%',
        plugins: {
          legend: { position: 'bottom', labels: { color: d.textColor,
            font: { family: d.fontFamily, size: 11 }, padding: 12, boxWidth: 10, boxHeight: 10 } },
          tooltip: { callbacks: { label: c => ` ${c.label}: ${c.parsed} cards` } },
        },
      },
    });
  },

  _chartBranchCards(byBranch) {
    const entries = Object.entries(byBranch);
    if (!entries.length) return;
    const labels = entries.map(([k]) => k.replace('Filial ', ''));
    const values = entries.map(([, v]) => v.total_cards || 0);
    const colors = ['#7c3aed','#3b82f6','#10b981','#f59e0b','#ef4444'];
    const ctx = document.getElementById('chart-branch-cards')?.getContext('2d');
    if (!ctx) return;
    const d = charts._defaults();
    this._charts.branchCards = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Cards', data: values,
        backgroundColor: colors.slice(0, labels.length).map(c => c + 'bb'),
        borderColor: colors.slice(0, labels.length),
        borderWidth: 1.5, borderRadius: 5, borderSkipped: false }] },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: d.textColor, font: { size: 10 } } },
          y: { grid: { color: d.gridColor }, ticks: { color: d.textColor, precision: 0 } },
        } },
    });
  },

  _chartBranchRisk(byBranch) {
    const entries = Object.entries(byBranch);
    if (!entries.length) return;
    const labels = entries.map(([k]) => k.replace('Filial ', ''));
    const values = entries.map(([, v]) => Math.round(v.total_value_at_risk || 0));
    const ctx = document.getElementById('chart-branch-risk')?.getContext('2d');
    if (!ctx) return;
    const d = charts._defaults();
    const grad = ctx.createLinearGradient(0, 0, 0, 180);
    grad.addColorStop(0, '#ef444488'); grad.addColorStop(1, '#ef444422');
    this._charts.branchRisk = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Valor em Risco', data: values,
        backgroundColor: grad, borderColor: '#ef4444',
        borderWidth: 1.5, borderRadius: 5, borderSkipped: false }] },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: c => ' ' + utils.fmt.currency(c.parsed.y) } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: d.textColor, font: { size: 10 } } },
          y: { grid: { color: d.gridColor }, ticks: { color: d.textColor,
            callback: v => v >= 1000 ? 'R$'+(v/1000).toFixed(0)+'k' : 'R$'+v } },
        } },
    });
  },

  _chartBranchConversion(byBranch) {
    const entries = Object.entries(byBranch);
    if (!entries.length) return;
    const labels    = entries.map(([k]) => k.replace('Filial ', ''));
    const converted = entries.map(([, v]) => v.stage_counts?.converted || 0);
    const total     = entries.map(([, v]) => v.total_cards || 0);
    const rates     = total.map((t, i) => t > 0 ? +((converted[i] / t) * 100).toFixed(1) : 0);
    const ctx = document.getElementById('chart-branch-conv')?.getContext('2d');
    if (!ctx) return;
    const d = charts._defaults();
    const grad = ctx.createLinearGradient(0, 0, 0, 180);
    grad.addColorStop(0, '#10b98188'); grad.addColorStop(1, '#10b98122');
    this._charts.branchConv = new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Taxa de Conversão (%)', data: rates,
        backgroundColor: grad, borderColor: '#10b981',
        borderWidth: 1.5, borderRadius: 5, borderSkipped: false }] },
      options: { responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false },
          tooltip: { callbacks: { label: c => ` ${c.parsed.y}%` } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: d.textColor, font: { size: 10 } } },
          y: { grid: { color: d.gridColor }, max: 100,
            ticks: { color: d.textColor, callback: v => v + '%' } },
        } },
    });
  },

  // ── Breakdown tables ──────────────────────────────────────
  _renderBreakdownBranch(data) {
    const entries = Object.entries(data);
    const badge   = document.getElementById('branch-total-badge');
    if (badge) badge.textContent = entries.length + ' filiais';
    const tbody = document.getElementById('breakdown-branch');
    if (!tbody) return;
    if (!entries.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:1.5rem">Sem dados</td></tr>';
      return;
    }
    this._renderBreakdownBranchRows(entries);

    utils.initSortableTable(
      'breakdown-branch-table',
      () => Object.entries(this._data?.by_branch || {}).map(([k, v]) => ({ _key: k, ...v, _conv: v.stage_counts?.converted || 0 })),
      (sorted) => this._renderBreakdownBranchRows(sorted.map(r => [r._key, r]))
    );
  },

  _renderBreakdownBranchRows(entries) {
    const tbody = document.getElementById('breakdown-branch');
    if (!tbody) return;
    const maxRisk = Math.max(...entries.map(([, v]) => v.total_value_at_risk || 0)) || 1;
    tbody.innerHTML = entries.map(([key, v]) => {
      const cards = v.total_cards || 0;
      const risk  = v.total_value_at_risk || 0;
      const conv  = v.stage_counts?.converted || 0;
      const rate  = cards > 0 ? ((conv / cards) * 100).toFixed(0) : 0;
      const pct   = ((risk / maxRisk) * 100).toFixed(0);
      return `<tr>
        <td><div style="display:flex;align-items:center;gap:7px">
          <div style="width:8px;height:8px;border-radius:50%;background:var(--brand-primary);flex-shrink:0"></div>
          <span class="bk-name">${key.replace('Filial ', '')}</span>
        </div></td>
        <td><span class="badge badge-purple">${utils.fmt.number(cards)}</span></td>
        <td class="bk-risk">${utils.fmt.currency(risk)}</td>
        <td><span class="badge badge-${conv > 0 ? 'green' : 'gray'}">${conv}</span></td>
        <td><div class="bk-bar-wrap">
          <div class="bk-bar"><div class="bk-bar-fill" style="width:${pct}%"></div></div>
          <span style="font-size:.68rem;color:var(--text-muted);min-width:28px">${rate}%</span>
        </div></td>
      </tr>`;
    }).join('');
  },

  _renderBreakdownState(data) {
    const entries = Object.entries(data).sort(([, a], [, b]) => (b.total_value_at_risk || 0) - (a.total_value_at_risk || 0));
    const badge   = document.getElementById('state-total-badge');
    if (badge) badge.textContent = entries.length + ' estados';
    const tbody = document.getElementById('breakdown-state');
    if (!tbody) return;
    if (!entries.length) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted);padding:1.5rem">Sem dados</td></tr>';
      return;
    }
    this._renderBreakdownStateRows(entries);

    utils.initSortableTable(
      'breakdown-state-table',
      () => Object.entries(this._data?.by_state || {}).map(([k, v]) => ({ _key: k, ...v, _conv: v.stage_counts?.converted || 0 })),
      (sorted) => this._renderBreakdownStateRows(sorted.map(r => [r._key, r]))
    );
  },

  _renderBreakdownStateRows(entries) {
    const tbody = document.getElementById('breakdown-state');
    if (!tbody) return;
    const maxRisk = Math.max(...entries.map(([, v]) => v.total_value_at_risk || 0)) || 1;
    tbody.innerHTML = entries.map(([key, v]) => {
      const cards = v.total_cards || 0;
      const risk  = v.total_value_at_risk || 0;
      const conv  = v.stage_counts?.converted || 0;
      const rate  = cards > 0 ? ((conv / cards) * 100).toFixed(0) : 0;
      const pct   = ((risk / maxRisk) * 100).toFixed(0);
      const riskPct  = (risk / maxRisk) * 100;
      const dotColor = riskPct > 66 ? 'var(--danger)' : riskPct > 33 ? 'var(--warning)' : 'var(--success)';
      return `<tr>
        <td><div style="display:flex;align-items:center;gap:7px">
          <div style="width:8px;height:8px;border-radius:50%;background:${dotColor};flex-shrink:0"></div>
          <span class="bk-name">${key}</span>
        </div></td>
        <td><span class="badge badge-blue">${utils.fmt.number(cards)}</span></td>
        <td class="bk-risk">${utils.fmt.currency(risk)}</td>
        <td><span class="badge badge-${conv > 0 ? 'green' : 'gray'}">${conv}</span></td>
        <td><div class="bk-bar-wrap">
          <div class="bk-bar"><div class="bk-bar-fill" style="width:${pct}%;background:${dotColor}"></div></div>
          <span style="font-size:.68rem;color:var(--text-muted);min-width:28px">${rate}%</span>
        </div></td>
      </tr>`;
    }).join('');
  },

  // ── Seller tables ─────────────────────────────────────────

  // Ciclo atual — todos os vendedores com seus cards do ciclo
  _renderSellerCycle(perf) {
    const sellers = perf?.sellers || [];
    const badge   = document.getElementById('seller-cycle-badge');
    if (badge) badge.textContent = sellers.length + ' vendedores';

    const tbody = document.getElementById('seller-cycle-tbody');
    if (!tbody) return;

    const filtered = this._filters.seller_id
      ? sellers.filter(s => s.seller_id === this._filters.seller_id)
      : sellers;

    this._renderSellerCycleRows(filtered);

    // Wire sortable headers
    utils.initSortableTable(
      'seller-cycle-table',
      () => this._filters.seller_id
        ? (this._perfData?.sellers || []).filter(s => s.seller_id === this._filters.seller_id)
        : (this._perfData?.sellers || []),
      (sorted) => this._renderSellerCycleRows(sorted)
    );
  },

  _renderSellerCycleRows(filtered) {
    const tbody = document.getElementById('seller-cycle-tbody');
    if (!tbody) return;

    if (!filtered.length) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text-muted);padding:1.5rem">Sem dados</td></tr>';
      return;
    }

    tbody.innerHTML = filtered.map(s => {
      const initials  = s.seller_name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
      const convColor = s.conversion_rate >= 50 ? 'var(--success)' : s.conversion_rate >= 20 ? 'var(--warning)' : 'var(--danger)';
      return `<tr>
        <td>
          <div class="seller-chip">
            <div class="seller-avatar-sm">${initials}</div>
            <div>
              <div class="seller-name-sm">${s.seller_name}</div>
              <div class="seller-role-sm">${s.branch || '—'}</div>
            </div>
          </div>
        </td>
        <td><span class="badge badge-gray" style="font-size:.65rem">${s.branch ? s.branch.replace('Filial ','') : '—'}</span></td>
        <td><span class="badge badge-purple">${s.total_cards}</span></td>
        <td><span style="color:var(--text-secondary);font-weight:600">${s.backlog}</span></td>
        <td><span style="color:var(--info);font-weight:600">${s.in_progress}</span></td>
        <td><span style="color:var(--warning);font-weight:600">${s.in_negotiation}</span></td>
        <td><span style="color:var(--success);font-weight:700">${s.converted}</span></td>
        <td><span style="color:var(--danger);font-weight:600">${s.declined}</span></td>
        <td><span class="badge badge-blue">${s.total_actions}</span></td>
        <td>
          <div class="conv-bar-wrap">
            <div class="conv-bar">
              <div class="conv-bar-fill" style="width:${Math.min(s.conversion_rate,100)}%;background:${convColor}"></div>
            </div>
            <span class="conv-bar-label" style="color:${convColor}">${s.conversion_rate.toFixed(1)}%</span>
          </div>
        </td>
      </tr>`;
    }).join('');
  },

  // Performance histórica — ordenável, com ranking
  _renderSellerHistory(perf) {
    const sellers = [...(perf?.sellers || [])];
    const badge   = document.getElementById('seller-hist-badge');
    if (badge) badge.textContent = sellers.length + ' vendedores';

    // Sort
    if (this._sortKey === 'conv') {
      sellers.sort((a, b) => b.conversion_rate - a.conversion_rate);
    } else {
      sellers.sort((a, b) => b.total_cards - a.total_cards);
    }

    const filtered = this._filters.seller_id
      ? sellers.filter(s => s.seller_id === this._filters.seller_id)
      : sellers;

    this._renderSellerHistRows(filtered);

    // Wire sortable headers (column click overrides quick-sort buttons)
    utils.initSortableTable(
      'seller-hist-table',
      () => {
        const base = this._filters.seller_id
          ? (this._perfData?.sellers || []).filter(s => s.seller_id === this._filters.seller_id)
          : (this._perfData?.sellers || []);
        return base.map((s, i) => ({ ...s, _perf: Math.min(100, Math.round(s.conversion_rate * 0.7 + Math.min(s.total_actions * 2, 30))) }));
      },
      (sorted) => this._renderSellerHistRows(sorted)
    );
  },

  _renderSellerHistRows(filtered) {
    const tbody = document.getElementById('seller-hist-tbody');
    if (!tbody) return;

    if (!filtered.length) {
      tbody.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text-muted);padding:1.5rem">Sem dados</td></tr>';
      return;
    }

    const maxCards = Math.max(...filtered.map(s => s.total_cards)) || 1;

    tbody.innerHTML = filtered.map((s, i) => {
      const rank      = i + 1;
      const rankCls   = rank === 1 ? 'rank-1' : rank === 2 ? 'rank-2' : rank === 3 ? 'rank-3' : 'rank-n';
      const initials  = s.seller_name.split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
      const convRate  = s.conversion_rate;
      const convColor = convRate >= 50 ? 'var(--success)' : convRate >= 20 ? 'var(--warning)' : 'var(--danger)';
      const cardsPct  = ((s.total_cards / maxCards) * 100).toFixed(0);
      const perfScore = s._perf ?? Math.min(100, Math.round(convRate * 0.7 + Math.min(s.total_actions * 2, 30)));
      const perfColor = perfScore >= 60 ? 'var(--success)' : perfScore >= 30 ? 'var(--warning)' : 'var(--danger)';

      return `<tr>
        <td><div class="rank-badge ${rankCls}">${rank}</div></td>
        <td>
          <div class="seller-chip">
            <div class="seller-avatar-sm">${initials}</div>
            <div>
              <div class="seller-name-sm">${s.seller_name}</div>
              <div class="seller-role-sm">${s.state || '—'}</div>
            </div>
          </div>
        </td>
        <td><span class="badge badge-gray" style="font-size:.65rem">${s.branch ? s.branch.replace('Filial ','') : '—'}</span></td>
        <td>
          <div class="bk-bar-wrap">
            <div class="bk-bar"><div class="bk-bar-fill" style="width:${cardsPct}%"></div></div>
            <span style="font-size:.75rem;font-weight:700;min-width:20px">${s.total_cards}</span>
          </div>
        </td>
        <td><span class="badge badge-green">${s.converted}</span></td>
        <td><span class="badge badge-red">${s.declined}</span></td>
        <td><span style="color:var(--info);font-weight:600">${s.in_progress}</span></td>
        <td><span class="badge badge-blue">${s.total_actions}</span></td>
        <td>
          <div class="conv-bar-wrap">
            <div class="conv-bar">
              <div class="conv-bar-fill" style="width:${Math.min(convRate,100)}%;background:${convColor}"></div>
            </div>
            <span class="conv-bar-label" style="color:${convColor}">${convRate.toFixed(1)}%</span>
          </div>
        </td>
        <td>
          <div class="conv-bar-wrap">
            <div class="conv-bar">
              <div class="conv-bar-fill" style="width:${perfScore}%;background:${perfColor}"></div>
            </div>
            <span class="conv-bar-label" style="color:${perfColor}">${perfScore}</span>
          </div>
        </td>
      </tr>`;
    }).join('');
  },

  // ── Helpers ───────────────────────────────────────────────
  _set(id, val) {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = val;
    el.classList.remove('flash');
    void el.offsetWidth;
    el.classList.add('flash');
    setTimeout(() => el.classList.remove('flash'), 800);
  },
};

window.dashboardPage = dashboardPage;
