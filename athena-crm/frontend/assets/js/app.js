// Athena CRM — App bootstrap
document.addEventListener('DOMContentLoaded', () => {
  theme.init();
  header.init();
  if (typeof search !== 'undefined' && search.initGlobal) search.initGlobal();
  sidebar.init();
  footer.init();

  // Detect current page and init
  const page = document.body.dataset.page;
  switch (page) {
    case 'dashboard':    dashboardPage.init();    break;
    case 'actions':      actionsPage.init();      break;
    case 'performance':  performancePage.init();  break;
    case 'clients':      clientsPage.init();      break;
    case 'client-detail': clientDetailPage.init(); break;
  }
});
