const API_BASE = 'http://localhost:8000/api/v1';

const api = {
  async request(method, path, body = null) {
    const opts = { method, headers: { 'Content-Type': 'application/json' } };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'API error');
    }
    if (res.status === 204) return null;
    return res.json();
  },
  get:    (path)       => api.request('GET',    path),
  post:   (path, body) => api.request('POST',   path, body),
  patch:  (path, body) => api.request('PATCH',  path, body),
  delete: (path)       => api.request('DELETE', path),

  // ── Dashboard ──────────────────────────────────────────────
  getDashboard: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/dashboard/indicators${q ? '?' + q : ''}`);
  },
  getFilterOptions: () => api.get('/dashboard/filters'),

  // ── Performance ────────────────────────────────────────────
  getTeamPerformance: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/performance/team${q ? '?' + q : ''}`);
  },
  getSellerPerformance: (sellerId, params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/performance/${sellerId}${q ? '?' + q : ''}`);
  },

  // ── Cards ──────────────────────────────────────────────────
  getCards: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/cards/${q ? '?' + q : ''}`);
  },
  getCard:    (id)        => api.get(`/cards/${id}`),
  createCard: (body)      => api.post('/cards/', body),
  updateCard: (id, body)  => api.patch(`/cards/${id}`, body),
  moveCard:   (id, stage) => api.patch(`/cards/${id}/stage`, { stage }),
  deleteCard: (id)        => api.delete(`/cards/${id}`),

  // ── Clients ────────────────────────────────────────────────
  getClients: (params = {}) => {
    let p = params;
    if (typeof params === 'string') {
      p = params.trim() ? { search: params.trim() } : {};
    }
    const filtered = Object.fromEntries(
      Object.entries(p).filter(([, v]) => v != null && v !== '')
    );
    const q = new URLSearchParams(filtered).toString();
    return api.get(`/clients/${q ? '?' + q : ''}`);
  },
  getClient:        (id)                  => api.get(`/clients/${id}`),
  getClientHistory: (id, params = {})     => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/clients/${id}/history${q ? '?' + q : ''}`);
  },

  // ── Actions ────────────────────────────────────────────────
  getActions:    (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/actions/${q ? '?' + q : ''}`);
  },
  createAction:  (body)       => api.post('/actions/', body),
  updateAction:  (id, body)   => api.patch(`/actions/${id}`, body),
  deleteAction:  (id)         => api.delete(`/actions/${id}`),

  // ── Sellers ────────────────────────────────────────────────
  getSellers:    ()     => api.get('/sellers/'),
  createSeller:  (body) => api.post('/sellers/', body),

  // ── ETL ────────────────────────────────────────────────────
  ingestClients: (body) => api.post('/etl/clients', body),
  ingestCards:   (body) => api.post('/etl/cards',   body),

  // ── Cycles ─────────────────────────────────────────────────
  closeCycle: (password, cycle_id = null) =>
    api.post('/cycles/close', { password, cycle_id }),
};

window.api = api;
