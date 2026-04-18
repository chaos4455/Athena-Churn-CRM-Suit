const actionsPage = {
  _filters: { branch: '', state: '', seller_id: '', archived: false },

  async init() {
    await this._loadFilterOptions();
    await this.loadKanban();
    this._bindNewCard();
    this._bindFilters();
  },

  async _loadFilterOptions() {
    try {
      const [opts, sellers] = await Promise.all([api.getFilterOptions(), api.getSellers()]);
      state.set('sellers', sellers);
      this._populateSelect('kanban-filter-branch', opts.branches, 'Todas as Filiais');
      this._populateSelect('kanban-filter-state',  opts.states,   'Todos os Estados');
      this._populateSelect('kanban-filter-seller', sellers.map(s => s.id),
        'Todos os Vendedores', sellers.map(s => s.name));

      // Preenche selects do modal de novo card
      const sellerSel = document.getElementById('new-card-seller');
      if (sellerSel) {
        sellerSel.innerHTML = '<option value="">Selecione o vendedor</option>' +
          sellers.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
      }
    } catch (_) {}
  },

  _populateSelect(id, values, placeholder, labels = null) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = `<option value="">${placeholder}</option>` +
      values.map((v, i) => `<option value="${v}">${labels ? labels[i] : v}</option>`).join('');
  },

  _bindFilters() {
    [['kanban-filter-branch','branch'],['kanban-filter-state','state'],['kanban-filter-seller','seller_id']]
      .forEach(([id, key]) => {
        document.getElementById(id)?.addEventListener('change', async (e) => {
          this._filters[key] = e.target.value;
          await this.loadKanban();
        });
      });

    document.getElementById('kanban-toggle-archived')?.addEventListener('change', async (e) => {
      this._filters.archived = e.target.checked;
      await this.loadKanban();
    });
  },

  async loadKanban() {
    const params = { archived: this._filters.archived };
    if (this._filters.branch)    params.branch    = this._filters.branch;
    if (this._filters.state)     params.state     = this._filters.state;
    if (this._filters.seller_id) params.seller_id = this._filters.seller_id;

    await kanban.init('kanban-board',
      (card) => cardDetail.open(card),
      () => {},
      params,
    );
  },

  _bindNewCard() {
    document.getElementById('btn-new-card')?.addEventListener('click', () => modal.open('modal-new-card'));

    document.getElementById('form-new-card')?.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(e.target);
      try {
        await api.createCard({
          client_id:    fd.get('client_id'),
          seller_id:    fd.get('seller_id'),
          title:        fd.get('title'),
          description:  fd.get('description'),
          value_at_risk: parseFloat(fd.get('value_at_risk') || 0),
          branch:       fd.get('branch') || null,
          state:        fd.get('state')  || null,
          cycle_id:     fd.get('cycle_id') || null,
        });
        toast.success('Card criado!');
        modal.closeAll();
        e.target.reset();
        await this.loadKanban();
      } catch (err) { toast.error(err.message); }
    });
  },
};

window.actionsPage = actionsPage;
