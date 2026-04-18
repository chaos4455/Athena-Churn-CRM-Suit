const state = (() => {
  const _store = {
    dashboard: null,
    cards: [],
    clients: [],
    actions: [],
    sellers: [],
    currentClient: null,
    currentCard: null,
    filters: { stage: null, seller: null },
  };
  const _listeners = {};

  return {
    get: (key) => _store[key],
    set(key, value) {
      _store[key] = value;
      (_listeners[key] || []).forEach(fn => fn(value));
    },
    on(key, fn) {
      if (!_listeners[key]) _listeners[key] = [];
      _listeners[key].push(fn);
    },
    off(key, fn) {
      if (_listeners[key]) _listeners[key] = _listeners[key].filter(f => f !== fn);
    },
  };
})();

window.state = state;
