// Auth placeholder — JWT login será implementado em fase posterior.
const auth = {
  getToken: () => localStorage.getItem('athena-token'),
  setToken: (t) => localStorage.setItem('athena-token', t),
  clear:    () => localStorage.removeItem('athena-token'),
  isLogged: () => true, // sem login por ora
};
window.auth = auth;
