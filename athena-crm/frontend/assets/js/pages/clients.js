const clientsPage = {
  _clients: [],

  async init() {
    await this.loadClients();
    this._bindSearch();
  },

  async loadClients(q = '') {
    try {
      const clients = await api.getClients(q);
      this._clients = clients;
      state.set('clients', clients);
      this.renderTable(clients);
    } catch (e) { toast.error('Erro ao carregar clientes'); }
  },

  renderTable(clients) {
    const countEl = document.getElementById('clients-count');
    if (countEl) countEl.textContent = `${clients.length} clientes`;

    const tbody = document.getElementById('clients-table-body');
    if (!tbody) return;

    if (!clients.length) {
      tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;padding:2rem;color:var(--text-muted)">Nenhum cliente encontrado.</td></tr>`;
      return;
    }

    tbody.innerHTML = clients.map((r, i) => {
      const pct   = r.churn_risk_score;
      const color = pct >= 70 ? 'var(--danger)' : pct >= 40 ? 'var(--warning)' : 'var(--success)';
      return `<tr class="animate-fade" style="animation-delay:${i * 0.02}s">
        <td><strong>${r.name}</strong></td>
        <td><code style="font-size:.78rem;background:var(--bg-input);padding:2px 6px;border-radius:4px">${r.external_id}</code></td>
        <td>${utils.fmt.currency(r.ltv)}</td>
        <td>${utils.fmt.currency(r.avg_ticket)}</td>
        <td>${utils.fmt.date(r.last_purchase_date)}</td>
        <td><span style="color:${color};font-weight:700">${pct.toFixed(0)}%</span></td>
        <td>${r.is_at_risk
          ? '<span class="badge badge-red"><i class="ph-fill ph-warning"></i> Em Risco</span>'
          : '<span class="badge badge-green"><i class="ph-fill ph-check-circle"></i> Saudável</span>'}</td>
        <td><a href="client-detail.html?id=${r.id}" class="btn btn-sm btn-secondary"><i class="ph ph-eye"></i> Ver</a></td>
      </tr>`;
    }).join('');

    // Wire up sortable headers
    utils.initSortableTable(
      'clients-main-table',
      () => this._clients,
      (sorted) => this.renderTable(sorted)
    );
  },

  _bindSearch() {
    const input = document.getElementById('client-search');
    if (!input) return;
    input.addEventListener('input', utils.debounce(async (e) => {
      await this.loadClients(e.target.value.trim());
    }, 350));
  },
};

window.clientsPage = clientsPage;
