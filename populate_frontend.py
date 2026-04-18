"""
Athena CRM - Churn Management Suite
Popula todos os arquivos do frontend (HTML, CSS, JS).
Rode: python populate_frontend.py
Desenvolvido pela O2 Data
"""

import os

BASE = os.path.join("athena-crm", "frontend")
FILES = {}

# ══════════════════════════════════════════════════════════════════════════════
# CSS — variables.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/variables.css"] = """:root {
  /* Background */
  --bg-body: #f0f2f8;
  --bg-sidebar: #ffffff;
  --bg-card: #ffffff;
  --bg-input: #f8f9fc;

  /* Text */
  --text-primary: #1a1d2e;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  /* Brand — Roxo / Gradiente */
  --brand-primary: #7c3aed;
  --brand-secondary: #a78bfa;
  --brand-light: #ede9fe;
  --brand-gradient: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
  --brand-gradient-soft: linear-gradient(135deg, rgba(124,58,237,.12) 0%, rgba(167,139,250,.08) 100%);

  /* Status */
  --success: #10b981;
  --success-bg: rgba(16,185,129,.1);
  --warning: #f59e0b;
  --warning-bg: rgba(245,158,11,.1);
  --danger: #ef4444;
  --danger-bg: rgba(239,68,68,.1);
  --info: #3b82f6;
  --info-bg: rgba(59,130,246,.1);

  /* Border */
  --border: #e5e7eb;
  --border-focus: var(--brand-primary);

  /* Shadow */
  --shadow-xs: 0 1px 2px rgba(0,0,0,.05);
  --shadow-sm: 0 2px 8px rgba(0,0,0,.07);
  --shadow-md: 0 4px 16px rgba(0,0,0,.10);
  --shadow-lg: 0 10px 30px rgba(0,0,0,.12);
  --shadow-brand: 0 8px 24px rgba(124,58,237,.25);

  /* Radius */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 18px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* Sidebar */
  --sidebar-width: 260px;
  --header-height: 72px;

  /* Transition */
  --transition: all .25s cubic-bezier(.4,0,.2,1);
  --transition-slow: all .4s cubic-bezier(.4,0,.2,1);
}

/* ── Dark Mode (html = escopo de tokens, evita flash no viewport) ── */
html.dark {
  --bg-body: #0d0f1a;
  --bg-sidebar: #13162a;
  --bg-card: #181b2e;
  --bg-input: #1e2235;
  --text-primary: #f1f3fa;
  --text-secondary: #9ca3af;
  --text-muted: #6b7280;
  --border: #252840;
  --brand-light: rgba(124,58,237,.18);
  --shadow-xs: 0 1px 2px rgba(0,0,0,.4);
  --shadow-sm: 0 2px 8px rgba(0,0,0,.4);
  --shadow-md: 0 4px 16px rgba(0,0,0,.5);
  --shadow-lg: 0 10px 30px rgba(0,0,0,.6);
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — reset.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/reset.css"] = """*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { font-size: 16px; scroll-behavior: smooth; }
body { font-family: 'Inter', sans-serif; background: var(--bg-body); color: var(--text-primary); transition: var(--transition); overflow-x: hidden; }
a { text-decoration: none; color: inherit; }
ul, ol { list-style: none; }
button { cursor: pointer; border: none; background: none; font-family: inherit; }
input, select, textarea { font-family: inherit; outline: none; }
img { max-width: 100%; display: block; }
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — layout.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/layout.css"] = """.app {
  display: grid;
  grid-template-columns: var(--sidebar-width) 1fr;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  position: fixed;
  top: 0; left: 0;
  width: var(--sidebar-width);
  height: 100vh;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  padding: 1.5rem 1rem;
  z-index: 100;
  transition: var(--transition);
  overflow-y: auto;
}

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 .5rem 2rem;
}
.sidebar-logo .logo-icon {
  width: 38px; height: 38px;
  background: var(--brand-gradient);
  border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 1.1rem;
  box-shadow: var(--shadow-brand);
  flex-shrink: 0;
}
.sidebar-logo .logo-text { font-size: .95rem; font-weight: 700; line-height: 1.2; }
.sidebar-logo .logo-text span { display: block; font-size: .7rem; font-weight: 400; color: var(--text-secondary); }

.nav-section { margin-bottom: 1.5rem; }
.nav-label {
  font-size: .68rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: 1.2px; color: var(--text-muted);
  padding: 0 .75rem; margin-bottom: .5rem; display: block;
}
.nav-item { margin-bottom: 2px; }
.nav-link {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: .875rem; font-weight: 500;
  transition: var(--transition);
}
.nav-link i { font-size: 1.1rem; flex-shrink: 0; }
.nav-link:hover { background: var(--brand-light); color: var(--brand-primary); }
.nav-link.active {
  background: var(--brand-gradient);
  color: #fff;
  box-shadow: var(--shadow-brand);
}
.nav-link .badge-count {
  margin-left: auto;
  background: var(--danger);
  color: #fff;
  font-size: .65rem; font-weight: 700;
  padding: 1px 6px; border-radius: var(--radius-full);
}

.sidebar-footer {
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border);
  font-size: .75rem; color: var(--text-muted);
  text-align: center;
}

/* ── Main ── */
.main {
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* ── Header ── */
.header {
  position: sticky; top: 0; z-index: 50;
  height: var(--header-height);
  background: rgba(255,255,255,.8);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center;
  padding: 0 2rem;
  gap: 1rem;
  transition: var(--transition);
}
html.dark .header { background: rgba(19,22,42,.85); }

.header-search {
  display: flex; align-items: center; gap: 8px;
  background: var(--bg-input);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  padding: 8px 16px;
  flex: 1; max-width: 360px;
  transition: var(--transition);
}
.header-search:focus-within { border-color: var(--brand-primary); box-shadow: 0 0 0 3px var(--brand-light); }
.header-search input { background: none; border: none; color: var(--text-primary); font-size: .875rem; width: 100%; }
.header-search i { color: var(--text-muted); font-size: 1rem; }

.header-actions { margin-left: auto; display: flex; align-items: center; gap: .75rem; }
.icon-btn {
  width: 38px; height: 38px;
  border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  color: var(--text-secondary); font-size: 1.1rem;
  transition: var(--transition); position: relative;
}
.icon-btn:hover { background: var(--brand-light); color: var(--brand-primary); }
.icon-btn .dot {
  position: absolute; top: 6px; right: 6px;
  width: 8px; height: 8px;
  background: var(--danger); border-radius: 50%;
  border: 2px solid var(--bg-card);
}

.user-chip {
  display: flex; align-items: center; gap: 8px;
  padding: 4px 12px 4px 4px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  cursor: pointer; transition: var(--transition);
}
.user-chip:hover { border-color: var(--brand-primary); background: var(--brand-light); }
.user-chip .avatar {
  width: 30px; height: 30px; border-radius: 50%;
  background: var(--brand-gradient);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: .75rem; font-weight: 700;
}
.user-chip .user-info { line-height: 1.2; }
.user-chip .user-name { font-size: .8rem; font-weight: 600; }
.user-chip .user-role { font-size: .68rem; color: var(--text-muted); }

/* ── Content ── */
.content { padding: 2rem; flex: 1; }

/* ── Footer ── */
.footer {
  padding: 1.25rem 2rem;
  border-top: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  font-size: .78rem; color: var(--text-muted);
}
.footer .footer-brand { display: flex; align-items: center; gap: 6px; font-weight: 600; color: var(--brand-primary); }

/* ── Page Header ── */
.page-header {
  display: flex; align-items: flex-end; justify-content: space-between;
  margin-bottom: 2rem;
}
.page-title { font-size: 1.6rem; font-weight: 700; margin-bottom: .25rem; }
.page-subtitle { font-size: .875rem; color: var(--text-secondary); }

/* ── Responsive ── */
@media (max-width: 1024px) {
  .app { grid-template-columns: 1fr; }
  .sidebar { transform: translateX(-100%); }
  .sidebar.open { transform: translateX(0); }
  .main { margin-left: 0; }
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — components.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/components.css"] = """/* ── Buttons ── */
.btn {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 9px 18px; border-radius: var(--radius-sm);
  font-size: .875rem; font-weight: 600;
  transition: var(--transition); cursor: pointer;
}
.btn-primary { background: var(--brand-gradient); color: #fff; box-shadow: var(--shadow-brand); }
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 28px rgba(124,58,237,.35); }
.btn-secondary { background: var(--bg-input); color: var(--text-primary); border: 1px solid var(--border); }
.btn-secondary:hover { border-color: var(--brand-primary); color: var(--brand-primary); }
.btn-danger { background: var(--danger-bg); color: var(--danger); }
.btn-danger:hover { background: var(--danger); color: #fff; }
.btn-sm { padding: 6px 12px; font-size: .8rem; }
.btn-icon { padding: 8px; border-radius: var(--radius-sm); }

/* ── Cards ── */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-xs);
  transition: var(--transition);
}
.card:hover { box-shadow: var(--shadow-md); transform: translateY(-3px); border-color: var(--brand-light); }
.card-flat { box-shadow: none; }
.card-flat:hover { transform: none; }

/* ── KPI Card ── */
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  box-shadow: var(--shadow-xs);
  transition: var(--transition);
  position: relative; overflow: hidden;
}
.kpi-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: var(--brand-gradient);
  opacity: 0; transition: var(--transition);
}
.kpi-card:hover { box-shadow: var(--shadow-brand); transform: translateY(-4px); border-color: var(--brand-secondary); }
.kpi-card:hover::before { opacity: 1; }
.kpi-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem; }
.kpi-label { font-size: .8rem; font-weight: 600; color: var(--text-secondary); text-transform: uppercase; letter-spacing: .5px; }
.kpi-icon {
  width: 42px; height: 42px; border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
}
.kpi-icon.purple { background: var(--brand-light); color: var(--brand-primary); }
.kpi-icon.green  { background: var(--success-bg); color: var(--success); }
.kpi-icon.orange { background: var(--warning-bg); color: var(--warning); }
.kpi-icon.red    { background: var(--danger-bg);  color: var(--danger); }
.kpi-icon.blue   { background: var(--info-bg);    color: var(--info); }
.kpi-value { font-size: 2rem; font-weight: 800; line-height: 1; margin-bottom: .4rem; }
.kpi-trend { font-size: .8rem; font-weight: 500; display: flex; align-items: center; gap: 4px; }
.kpi-trend.up   { color: var(--success); }
.kpi-trend.down { color: var(--danger); }
.kpi-trend.neutral { color: var(--text-muted); }

/* ── Grid ── */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.25rem; margin-bottom: 2rem; }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.grid-2-1 { display: grid; grid-template-columns: 2fr 1fr; gap: 1.25rem; }
@media (max-width: 1100px) { .grid-2-1, .grid-2, .grid-3 { grid-template-columns: 1fr; } }

/* ── Badge / Status ── */
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: var(--radius-full);
  font-size: .72rem; font-weight: 700;
}
.badge-purple  { background: var(--brand-light);  color: var(--brand-primary); }
.badge-green   { background: var(--success-bg);   color: var(--success); }
.badge-orange  { background: var(--warning-bg);   color: var(--warning); }
.badge-red     { background: var(--danger-bg);    color: var(--danger); }
.badge-blue    { background: var(--info-bg);      color: var(--info); }
.badge-gray    { background: rgba(107,114,128,.1); color: var(--text-secondary); }

/* ── Table ── */
.table-wrap { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; }
thead th {
  text-align: left; padding: .75rem 1rem;
  font-size: .72rem; font-weight: 700; text-transform: uppercase;
  letter-spacing: .5px; color: var(--text-muted);
  background: var(--bg-input); border-bottom: 1px solid var(--border);
}
tbody td { padding: .875rem 1rem; border-bottom: 1px solid var(--border); font-size: .875rem; }
tbody tr:last-child td { border-bottom: none; }
tbody tr { transition: var(--transition); }
tbody tr:hover td { background: var(--brand-light); cursor: pointer; }

/* ── Form ── */
.form-group { margin-bottom: 1rem; }
.form-label { display: block; font-size: .8rem; font-weight: 600; margin-bottom: .4rem; color: var(--text-secondary); }
.form-control {
  width: 100%; padding: 9px 12px;
  background: var(--bg-input); border: 1px solid var(--border);
  border-radius: var(--radius-sm); color: var(--text-primary);
  font-size: .875rem; transition: var(--transition);
}
.form-control:focus { border-color: var(--brand-primary); box-shadow: 0 0 0 3px var(--brand-light); }
select.form-control { cursor: pointer; }

/* ── Modal ── */
.modal-overlay {
  position: fixed; inset: 0; z-index: 200;
  background: rgba(0,0,0,.5); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: var(--transition);
}
.modal-overlay.open { opacity: 1; pointer-events: all; }
.modal {
  background: var(--bg-card); border-radius: var(--radius-xl);
  padding: 2rem; width: 100%; max-width: 520px;
  box-shadow: var(--shadow-lg);
  transform: translateY(20px) scale(.97); transition: var(--transition);
}
.modal-overlay.open .modal { transform: translateY(0) scale(1); }
.modal-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.modal-title { font-size: 1.1rem; font-weight: 700; }
.modal-close { color: var(--text-muted); font-size: 1.2rem; }
.modal-close:hover { color: var(--danger); }
.modal-footer { display: flex; gap: .75rem; justify-content: flex-end; margin-top: 1.5rem; }

/* ── Toast ── */
.toast-container { position: fixed; bottom: 1.5rem; right: 1.5rem; z-index: 999; display: flex; flex-direction: column; gap: .5rem; }
.toast {
  display: flex; align-items: center; gap: 10px;
  padding: .875rem 1.25rem;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-md); box-shadow: var(--shadow-lg);
  font-size: .875rem; min-width: 280px;
  animation: slideInRight .3s ease;
}
.toast.success { border-left: 4px solid var(--success); }
.toast.error   { border-left: 4px solid var(--danger); }
.toast.info    { border-left: 4px solid var(--brand-primary); }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* ── Kanban ── */
.kanban-board { display: flex; gap: 1rem; overflow-x: auto; padding-bottom: 1rem; }
.kanban-col {
  flex-shrink: 0; width: 280px;
  background: var(--bg-input); border-radius: var(--radius-lg);
  padding: 1rem; display: flex; flex-direction: column; gap: .75rem;
}
.kanban-col-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: .25rem;
}
.kanban-col-title { font-size: .8rem; font-weight: 700; text-transform: uppercase; letter-spacing: .5px; }
.kanban-col-count {
  background: var(--brand-light); color: var(--brand-primary);
  font-size: .7rem; font-weight: 700;
  padding: 2px 8px; border-radius: var(--radius-full);
}
.kanban-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: var(--radius-md); padding: 1rem;
  box-shadow: var(--shadow-xs); cursor: grab;
  transition: var(--transition);
}
.kanban-card:hover { box-shadow: var(--shadow-brand); border-color: var(--brand-secondary); transform: translateY(-2px); }
.kanban-card.dragging { opacity: .5; cursor: grabbing; }
.kanban-card-name { font-size: .875rem; font-weight: 600; margin-bottom: .5rem; }
.kanban-card-meta { font-size: .75rem; color: var(--text-secondary); display: flex; flex-direction: column; gap: 3px; }
.kanban-card-meta span { display: flex; align-items: center; gap: 5px; }
.kanban-card-footer { display: flex; align-items: center; justify-content: space-between; margin-top: .75rem; padding-top: .75rem; border-top: 1px solid var(--border); }
.kanban-drop-zone { min-height: 60px; border: 2px dashed var(--border); border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; color: var(--text-muted); font-size: .8rem; }
.kanban-drop-zone.drag-over { border-color: var(--brand-primary); background: var(--brand-light); }

/* ── Chart container ── */
.chart-wrap { position: relative; height: 280px; }

/* ── Empty state ── */
.empty-state { text-align: center; padding: 3rem 1rem; color: var(--text-muted); }
.empty-state i { font-size: 3rem; margin-bottom: 1rem; opacity: .4; }
.empty-state p { font-size: .9rem; }

/* ── Divider ── */
.divider { height: 1px; background: var(--border); margin: 1.5rem 0; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--brand-secondary); }
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — animations.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/animations.css"] = """@keyframes fadeIn { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeInLeft { from { opacity:0; transform:translateX(-16px); } to { opacity:1; transform:translateX(0); } }
@keyframes scaleIn { from { opacity:0; transform:scale(.95); } to { opacity:1; transform:scale(1); } }
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:.5; } }
@keyframes spin { to { transform:rotate(360deg); } }
@keyframes shimmer { 0% { background-position:-200% 0; } 100% { background-position:200% 0; } }

.animate-fade   { animation: fadeIn .4s ease both; }
.animate-left   { animation: fadeInLeft .4s ease both; }
.animate-scale  { animation: scaleIn .3s ease both; }
.animate-pulse  { animation: pulse 2s infinite; }
.animate-spin   { animation: spin 1s linear infinite; }

/* Stagger children */
.stagger > *:nth-child(1) { animation-delay: .05s; }
.stagger > *:nth-child(2) { animation-delay: .10s; }
.stagger > *:nth-child(3) { animation-delay: .15s; }
.stagger > *:nth-child(4) { animation-delay: .20s; }
.stagger > *:nth-child(5) { animation-delay: .25s; }
.stagger > *:nth-child(6) { animation-delay: .30s; }

/* Skeleton loader */
.skeleton {
  background: linear-gradient(90deg, var(--border) 25%, var(--bg-input) 50%, var(--border) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-sm);
}

/* Flash update */
@keyframes flashUpdate { 0% { background: var(--brand-light); } 100% { background: transparent; } }
.flash { animation: flashUpdate .8s ease; }
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — dark-theme.css  (overrides já estão em variables.css via html.dark)
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/dark-theme.css"] = """/* Extra dark-mode overrides beyond CSS variables */
html.dark .header { border-bottom-color: var(--border); }
html.dark .sidebar { border-right-color: var(--border); }
html.dark .kanban-col { background: rgba(255,255,255,.03); }
html.dark thead th { background: rgba(255,255,255,.04); }
html.dark .form-control { background: var(--bg-input); color: var(--text-primary); }
html.dark .modal { border: 1px solid var(--border); }
"""

# ══════════════════════════════════════════════════════════════════════════════
# CSS — responsive.css
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/css/responsive.css"] = """@media (max-width: 1280px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .content { padding: 1rem; }
  .page-header { flex-direction: column; align-items: flex-start; gap: .75rem; }
  .kpi-grid { grid-template-columns: 1fr 1fr; }
  .header-search { display: none; }
  .kanban-board { flex-direction: column; }
  .kanban-col { width: 100%; }
}
@media (max-width: 480px) {
  .kpi-grid { grid-template-columns: 1fr; }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
}
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/api.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/api.js"] = """const API_BASE = 'http://localhost:8000/api/v1';

const api = {
  async request(method, path, body = null) {
    const opts = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) opts.body = JSON.stringify(body);
    const res = await fetch(API_BASE + path, opts);
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(err.detail || 'API error');
    }
    if (res.status === 204) return null;
    return res.json();
  },
  get:    (path)        => api.request('GET',    path),
  post:   (path, body)  => api.request('POST',   path, body),
  patch:  (path, body)  => api.request('PATCH',  path, body),
  delete: (path)        => api.request('DELETE', path),

  // Dashboard
  getDashboard:      ()           => api.get('/dashboard/indicators'),
  getPerformance:    (sellerId)   => api.get(`/performance/${sellerId}`),

  // Cards
  getCards:          (params='') => api.get(`/cards/${params}`),
  getCard:           (id)        => api.get(`/cards/${id}`),
  createCard:        (body)      => api.post('/cards/', body),
  updateCard:        (id, body)  => api.patch(`/cards/${id}`, body),
  moveCard:          (id, stage) => api.patch(`/cards/${id}/stage`, { stage }),
  deleteCard:        (id)        => api.delete(`/cards/${id}`),

  // Clients
  getClients:        (q='')      => api.get(`/clients/?search=${q}`),
  getClient:         (id)        => api.get(`/clients/${id}`),
  getClientHistory:  (id)        => api.get(`/clients/${id}/history`),

  // Actions
  getActions:        (params='') => api.get(`/actions/${params}`),
  createAction:      (body)      => api.post('/actions/', body),
  updateAction:      (id, body)  => api.patch(`/actions/${id}`, body),
  deleteAction:      (id)        => api.delete(`/actions/${id}`),

  // Sellers
  getSellers:        ()          => api.get('/sellers/'),
  createSeller:      (body)      => api.post('/sellers/', body),

  // ETL
  ingestClients:     (body)      => api.post('/etl/clients', body),
  ingestCards:       (body)      => api.post('/etl/cards', body),
};

window.api = api;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/state.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/state.js"] = """const state = (() => {
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
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/theme.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/theme.js"] = """const theme = {
  init() {
    const saved = localStorage.getItem('athena-theme') || 'light';
    this.apply(saved);
  },
  apply(mode) {
    const dark = mode === 'dark';
    document.documentElement.classList.toggle('dark', dark);
    localStorage.setItem('athena-theme', mode);
    const icon = document.getElementById('theme-icon');
    if (icon) icon.className = dark ? 'ph ph-sun' : 'ph ph-moon';
  },
  toggle() {
    const isDark = document.documentElement.classList.contains('dark');
    this.apply(isDark ? 'light' : 'dark');
  },
};

window.theme = theme;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/utils.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/utils.js"] = """const utils = {
  fmt: {
    currency: (v) => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0),
    number:   (v) => new Intl.NumberFormat('pt-BR').format(v || 0),
    date:     (v) => v ? new Date(v).toLocaleDateString('pt-BR') : '—',
    datetime: (v) => v ? new Date(v).toLocaleString('pt-BR') : '—',
    percent:  (v) => `${(v || 0).toFixed(1)}%`,
  },

  stageMeta: {
    backlog:        { label: 'Backlog',        color: 'gray',   icon: 'ph-tray' },
    in_progress:    { label: 'Em Andamento',   color: 'blue',   icon: 'ph-arrow-right' },
    in_negotiation: { label: 'Em Negociação',  color: 'orange', icon: 'ph-handshake' },
    converted:      { label: 'Convertido',     color: 'green',  icon: 'ph-check-circle' },
    declined:       { label: 'Declinado',      color: 'red',    icon: 'ph-x-circle' },
  },

  actionMeta: {
    call:      { label: 'Ligação',    icon: 'ph-phone' },
    email:     { label: 'E-mail',     icon: 'ph-envelope' },
    meeting:   { label: 'Reunião',    icon: 'ph-users' },
    whatsapp:  { label: 'WhatsApp',   icon: 'ph-whatsapp-logo' },
    note:      { label: 'Nota',       icon: 'ph-note' },
    proposal:  { label: 'Proposta',   icon: 'ph-file-text' },
  },

  stageBadge(stage) {
    const m = utils.stageMeta[stage] || { label: stage, color: 'gray' };
    return `<span class="badge badge-${m.color}">${m.label}</span>`;
  },

  debounce(fn, ms = 300) {
    let t;
    return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
  },

  qs:  (sel, ctx = document) => ctx.querySelector(sel),
  qsa: (sel, ctx = document) => [...ctx.querySelectorAll(sel)],

  el(tag, cls = '', html = '') {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (html) e.innerHTML = html;
    return e;
  },
};

window.utils = utils;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/router.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/router.js"] = """// Simple hash-based router for SPA navigation
const router = {
  routes: {},
  register(hash, fn) { this.routes[hash] = fn; },
  navigate(hash) { window.location.hash = hash; },
  init() {
    window.addEventListener('hashchange', () => this._resolve());
    this._resolve();
  },
  _resolve() {
    const hash = window.location.hash || '#dashboard';
    const fn = this.routes[hash];
    if (fn) fn();
    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(a => {
      a.classList.toggle('active', a.getAttribute('href') === hash);
    });
  },
};

window.router = router;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — core/auth.js  (placeholder — login será implementado depois)
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/core/auth.js"] = """// Auth placeholder — JWT login será implementado em fase posterior.
const auth = {
  getToken: () => localStorage.getItem('athena-token'),
  setToken: (t) => localStorage.setItem('athena-token', t),
  clear:    () => localStorage.removeItem('athena-token'),
  isLogged: () => true, // sem login por ora
};
window.auth = auth;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/toast.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/toast.js"] = """const toast = {
  _container: null,
  _ensure() {
    if (!this._container) {
      this._container = document.createElement('div');
      this._container.className = 'toast-container';
      document.body.appendChild(this._container);
    }
  },
  show(message, type = 'info', duration = 3500) {
    this._ensure();
    const icons = { success: 'ph-check-circle', error: 'ph-x-circle', info: 'ph-info' };
    const t = document.createElement('div');
    t.className = `toast ${type}`;
    t.innerHTML = `<i class="ph-fill ${icons[type] || icons.info}" style="font-size:1.1rem"></i><span>${message}</span>`;
    this._container.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; t.style.transform = 'translateX(100%)'; t.style.transition = 'all .3s'; setTimeout(() => t.remove(), 300); }, duration);
  },
  success: (msg) => toast.show(msg, 'success'),
  error:   (msg) => toast.show(msg, 'error'),
  info:    (msg) => toast.show(msg, 'info'),
};
window.toast = toast;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/modal.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/modal.js"] = """const modal = {
  open(id)  { document.getElementById(id)?.classList.add('open'); },
  close(id) { document.getElementById(id)?.classList.remove('open'); },
  closeAll() { document.querySelectorAll('.modal-overlay.open').forEach(m => m.classList.remove('open')); },
  confirm(message) { return window.confirm(message); },
};

// Close on overlay click
document.addEventListener('click', (e) => {
  if (e.target.classList.contains('modal-overlay')) modal.closeAll();
  if (e.target.classList.contains('modal-close'))   modal.closeAll();
});

window.modal = modal;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/sidebar.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/sidebar.js"] = """const sidebar = {
  init() {
    const toggle = document.getElementById('sidebar-toggle');
    const el = document.querySelector('.sidebar');
    if (toggle && el) {
      toggle.addEventListener('click', () => el.classList.toggle('open'));
    }
  },
};
window.sidebar = sidebar;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/header.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/header.js"] = """const header = {
  init() {
    const themeBtn = document.getElementById('theme-btn');
    if (themeBtn) themeBtn.addEventListener('click', () => theme.toggle());
  },
};
window.header = header;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/footer.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/footer.js"] = """const footer = {
  init() {
    const el = document.getElementById('footer-year');
    if (el) el.textContent = new Date().getFullYear();
  },
};
window.footer = footer;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/charts.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/charts.js"] = """const charts = {
  _defaults() {
    const dark = document.documentElement.classList.contains('dark');
    return {
      gridColor:  dark ? 'rgba(255,255,255,.06)' : 'rgba(0,0,0,.06)',
      textColor:  dark ? '#9ca3af' : '#6b7280',
      fontFamily: "'Inter', sans-serif",
    };
  },

  gradient(ctx, color1 = '#7c3aed', color2 = 'transparent') {
    const g = ctx.createLinearGradient(0, 0, 0, 300);
    g.addColorStop(0, color1 + '55');
    g.addColorStop(1, color2);
    return g;
  },

  line(canvasId, labels, datasets, opts = {}) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return null;
    const d = this._defaults();
    return new Chart(ctx, {
      type: 'line',
      data: { labels, datasets },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'top', align: 'end', labels: { color: d.textColor, font: { family: d.fontFamily, size: 12 }, boxWidth: 12 } } },
        scales: {
          x: { grid: { display: false }, ticks: { color: d.textColor } },
          y: { grid: { color: d.gridColor, drawBorder: false }, ticks: { color: d.textColor } },
        },
        ...opts,
      },
    });
  },

  doughnut(canvasId, labels, data, colors) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return null;
    const d = this._defaults();
    return new Chart(ctx, {
      type: 'doughnut',
      data: { labels, datasets: [{ data, backgroundColor: colors, borderWidth: 0, hoverOffset: 8 }] },
      options: {
        responsive: true, maintainAspectRatio: false,
        cutout: '72%',
        plugins: { legend: { position: 'bottom', labels: { color: d.textColor, font: { family: d.fontFamily, size: 12 }, padding: 16 } } },
      },
    });
  },

  bar(canvasId, labels, datasets, opts = {}) {
    const ctx = document.getElementById(canvasId)?.getContext('2d');
    if (!ctx) return null;
    const d = this._defaults();
    return new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: d.textColor } },
          y: { grid: { color: d.gridColor }, ticks: { color: d.textColor } },
        },
        ...opts,
      },
    });
  },
};

window.charts = charts;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/kanban.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/kanban.js"] = """const kanban = {
  STAGES: ['backlog', 'in_progress', 'in_negotiation', 'converted', 'declined'],

  async init(containerId, onCardClick, onStageChange) {
    this._container = document.getElementById(containerId);
    this._onCardClick = onCardClick;
    this._onStageChange = onStageChange;
    await this.load();
  },

  async load() {
    try {
      const cards = await api.getCards();
      state.set('cards', cards);
      this.render(cards);
    } catch (e) { toast.error('Erro ao carregar cards: ' + e.message); }
  },

  render(cards) {
    if (!this._container) return;
    this._container.innerHTML = '';
    this.STAGES.forEach(stage => {
      const stageCards = cards.filter(c => c.stage === stage);
      const meta = utils.stageMeta[stage];
      const col = utils.el('div', 'kanban-col');
      col.dataset.stage = stage;
      col.innerHTML = `
        <div class="kanban-col-header">
          <span class="kanban-col-title">${meta.label}</span>
          <span class="kanban-col-count">${stageCards.length}</span>
        </div>
      `;
      stageCards.forEach(card => col.appendChild(this._buildCard(card)));
      const drop = utils.el('div', 'kanban-drop-zone', '<i class="ph ph-plus"></i> Soltar aqui');
      drop.dataset.stage = stage;
      col.appendChild(drop);
      this._container.appendChild(col);
    });
    this._bindDrag();
  },

  _buildCard(card) {
    const el = utils.el('div', 'kanban-card animate-fade');
    el.draggable = true;
    el.dataset.id = card.id;
    el.innerHTML = `
      <div class="kanban-card-name">${card.client_name}</div>
      <div class="kanban-card-meta">
        <span><i class="ph ph-identification-card"></i> ${card.client_id.slice(0,8)}...</span>
        <span><i class="ph ph-calendar-blank"></i> ${utils.fmt.date(card.last_purchase_date)}</span>
        <span><i class="ph ph-currency-dollar"></i> LTV ${utils.fmt.currency(card.ltv)}</span>
        <span><i class="ph ph-receipt"></i> Ticket ${utils.fmt.currency(card.avg_ticket)}</span>
      </div>
      <div class="kanban-card-footer">
        ${utils.stageBadge(card.stage)}
        <span style="font-size:.75rem;color:var(--danger);font-weight:600">${utils.fmt.currency(card.value_at_risk)}</span>
      </div>
    `;
    el.addEventListener('click', () => this._onCardClick && this._onCardClick(card));
    return el;
  },

  _bindDrag() {
    let dragged = null;
    this._container.querySelectorAll('.kanban-card').forEach(card => {
      card.addEventListener('dragstart', () => { dragged = card; card.classList.add('dragging'); });
      card.addEventListener('dragend',   () => { dragged = null; card.classList.remove('dragging'); });
    });
    this._container.querySelectorAll('.kanban-drop-zone').forEach(zone => {
      zone.addEventListener('dragover',  (e) => { e.preventDefault(); zone.classList.add('drag-over'); });
      zone.addEventListener('dragleave', ()  => zone.classList.remove('drag-over'));
      zone.addEventListener('drop', async (e) => {
        e.preventDefault();
        zone.classList.remove('drag-over');
        if (!dragged) return;
        const cardId = dragged.dataset.id;
        const newStage = zone.dataset.stage;
        try {
          await api.moveCard(cardId, newStage);
          toast.success('Card movido!');
          this._onStageChange && this._onStageChange(cardId, newStage);
          await this.load();
        } catch (err) { toast.error(err.message); }
      });
    });
  },
};

window.kanban = kanban;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/search.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/search.js"] = """const search = {
  init(inputId, onResult) {
    const input = document.getElementById(inputId);
    if (!input) return;
    input.addEventListener('input', utils.debounce(async (e) => {
      const q = e.target.value.trim();
      if (q.length < 2) { onResult([]); return; }
      try {
        const results = await api.getClients(q);
        onResult(results);
      } catch (err) { toast.error(err.message); }
    }, 350));
  },
};
window.search = search;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/table.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/table.js"] = """const table = {
  render(tbodyId, rows, columns) {
    const tbody = document.getElementById(tbodyId);
    if (!tbody) return;
    tbody.innerHTML = '';
    if (!rows.length) {
      tbody.innerHTML = `<tr><td colspan="${columns.length}" style="text-align:center;padding:2rem;color:var(--text-muted)">Nenhum registro encontrado.</td></tr>`;
      return;
    }
    rows.forEach((row, i) => {
      const tr = document.createElement('tr');
      tr.className = 'animate-fade';
      tr.style.animationDelay = `${i * 0.03}s`;
      columns.forEach(col => {
        const td = document.createElement('td');
        td.innerHTML = col.render ? col.render(row) : (row[col.key] ?? '—');
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  },
};
window.table = table;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — components/card.js  (detail card modal)
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/components/card.js"] = """const cardDetail = {
  async open(cardData) {
    const overlay = document.getElementById('modal-card-detail');
    if (!overlay) return;
    const [actions] = await Promise.all([
      api.getActions(`?card_id=${cardData.id}`),
    ]);
    overlay.querySelector('#modal-card-title').textContent = cardData.title || cardData.client_name;
    overlay.querySelector('#modal-card-client').textContent = cardData.client_name;
    overlay.querySelector('#modal-card-ltv').textContent = utils.fmt.currency(cardData.ltv);
    overlay.querySelector('#modal-card-ticket').textContent = utils.fmt.currency(cardData.avg_ticket);
    overlay.querySelector('#modal-card-risk').textContent = utils.fmt.currency(cardData.value_at_risk);
    overlay.querySelector('#modal-card-stage').innerHTML = utils.stageBadge(cardData.stage);
    overlay.querySelector('#modal-card-last-purchase').textContent = utils.fmt.date(cardData.last_purchase_date);

    const actList = overlay.querySelector('#modal-card-actions');
    actList.innerHTML = actions.length
      ? actions.map(a => `
          <div class="card card-flat" style="padding:.75rem;margin-bottom:.5rem">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:.25rem">
              <i class="ph ${utils.actionMeta[a.action_type]?.icon || 'ph-activity'}" style="color:var(--brand-primary)"></i>
              <strong style="font-size:.8rem">${utils.actionMeta[a.action_type]?.label || a.action_type}</strong>
              ${utils.stageBadge(a.status)}
              <span style="margin-left:auto;font-size:.72rem;color:var(--text-muted)">${utils.fmt.datetime(a.created_at)}</span>
            </div>
            <p style="font-size:.8rem;color:var(--text-secondary)">${a.description}</p>
            ${a.outcome ? `<p style="font-size:.78rem;color:var(--success);margin-top:.25rem"><i class="ph ph-check"></i> ${a.outcome}</p>` : ''}
          </div>`)
        .join('')
      : '<p style="color:var(--text-muted);font-size:.85rem">Nenhuma ação registrada.</p>';

    modal.open('modal-card-detail');
  },
};
window.cardDetail = cardDetail;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — pages/dashboard.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/pages/dashboard.js"] = """const dashboardPage = {
  _charts: {},

  async init() {
    await this.loadKPIs();
    await this.loadCharts();
  },

  async loadKPIs() {
    try {
      const data = await api.getDashboard();
      state.set('dashboard', data);
      utils.qs('#kpi-total-cards').textContent    = utils.fmt.number(data.total_cards);
      utils.qs('#kpi-at-risk').textContent        = utils.fmt.number(data.clients_at_risk);
      utils.qs('#kpi-value-risk').textContent     = utils.fmt.currency(data.total_value_at_risk);
      utils.qs('#kpi-avg-ticket').textContent     = utils.fmt.currency(data.avg_ticket_at_risk);
      utils.qs('#kpi-opportunities').textContent  = utils.fmt.number(data.total_opportunities);

      // Stage pills
      const stages = data.stage_counts || {};
      utils.qs('#kpi-converted')?.textContent    && (utils.qs('#kpi-converted').textContent    = stages.converted    || 0);
      utils.qs('#kpi-declined')?.textContent     && (utils.qs('#kpi-declined').textContent     = stages.declined     || 0);
      utils.qs('#kpi-in-progress')?.textContent  && (utils.qs('#kpi-in-progress').textContent  = stages.in_progress  || 0);
    } catch (e) { toast.error('Erro ao carregar indicadores'); }
  },

  async loadCharts() {
    const months = ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'];
    const now = new Date().getMonth();
    const labels = months.slice(Math.max(0, now - 5), now + 1);

    // Line chart — value at risk trend (mock until historical endpoint)
    const ctx = document.getElementById('chart-risk-trend')?.getContext('2d');
    if (ctx) {
      const grad = ctx.createLinearGradient(0, 0, 0, 280);
      grad.addColorStop(0, 'rgba(124,58,237,.35)');
      grad.addColorStop(1, 'rgba(124,58,237,0)');
      this._charts.line = charts.line('chart-risk-trend', labels, [
        { label: 'Valor em Risco', data: labels.map(() => Math.random() * 80000 + 20000), borderColor: '#7c3aed', backgroundColor: grad, fill: true, tension: .4, borderWidth: 2.5, pointRadius: 4, pointBackgroundColor: '#fff', pointBorderColor: '#7c3aed', pointBorderWidth: 2 },
        { label: 'Convertido',     data: labels.map(() => Math.random() * 40000 + 5000),  borderColor: '#10b981', backgroundColor: 'transparent', tension: .4, borderWidth: 2, borderDash: [5,4], pointRadius: 0 },
      ]);
    }

    // Doughnut — stage distribution
    const dash = state.get('dashboard');
    if (dash) {
      const sc = dash.stage_counts || {};
      charts.doughnut('chart-stages',
        ['Backlog','Em Andamento','Negociação','Convertido','Declinado'],
        [sc.backlog||0, sc.in_progress||0, sc.in_negotiation||0, sc.converted||0, sc.declined||0],
        ['#7c3aed','#3b82f6','#f59e0b','#10b981','#ef4444']
      );
    }
  },
};

window.dashboardPage = dashboardPage;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — pages/actions.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/pages/actions.js"] = """const actionsPage = {
  async init() {
    await this.loadKanban();
    this._bindNewCard();
  },

  async loadKanban() {
    await kanban.init('kanban-board',
      (card) => cardDetail.open(card),
      () => {}
    );
  },

  _bindNewCard() {
    const btn = document.getElementById('btn-new-card');
    if (!btn) return;
    btn.addEventListener('click', () => modal.open('modal-new-card'));

    const form = document.getElementById('form-new-card');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      try {
        await api.createCard({
          client_id:    fd.get('client_id'),
          seller_id:    fd.get('seller_id'),
          title:        fd.get('title'),
          description:  fd.get('description'),
          value_at_risk: parseFloat(fd.get('value_at_risk') || 0),
        });
        toast.success('Card criado!');
        modal.closeAll();
        form.reset();
        await kanban.load();
      } catch (err) { toast.error(err.message); }
    });
  },
};

window.actionsPage = actionsPage;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — pages/performance.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/pages/performance.js"] = """const performancePage = {
  async init() {
    await this.loadSellers();
    await this.loadTable();
    await this.loadCharts();
  },

  async loadSellers() {
    try {
      const sellers = await api.getSellers();
      state.set('sellers', sellers);
      const sel = document.getElementById('filter-seller');
      if (sel) {
        sel.innerHTML = '<option value="">Todos os vendedores</option>' +
          sellers.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
        sel.addEventListener('change', () => this.loadTable(sel.value));
      }
    } catch (e) {}
  },

  async loadTable(sellerId = '') {
    try {
      const cards = await api.getCards(sellerId ? `?seller_id=${sellerId}` : '');
      const cols = [
        { key: 'client_name', render: r => `<strong>${r.client_name}</strong>` },
        { key: 'stage',       render: r => utils.stageBadge(r.stage) },
        { key: 'value_at_risk', render: r => `<span style="color:var(--danger);font-weight:600">${utils.fmt.currency(r.value_at_risk)}</span>` },
        { key: 'avg_ticket',  render: r => utils.fmt.currency(r.avg_ticket) },
        { key: 'ltv',         render: r => utils.fmt.currency(r.ltv) },
        { key: 'created_at',  render: r => utils.fmt.date(r.created_at) },
      ];
      table.render('perf-table-body', cards, cols);
    } catch (e) { toast.error('Erro ao carregar performance'); }
  },

  async loadCharts() {
    const cards = state.get('cards') || await api.getCards();
    const stages = kanban.STAGES;
    const counts = stages.map(s => cards.filter(c => c.stage === s).length);
    charts.bar('chart-perf-stages',
      stages.map(s => utils.stageMeta[s].label),
      [{ data: counts, backgroundColor: ['#7c3aed','#3b82f6','#f59e0b','#10b981','#ef4444'], borderRadius: 6 }]
    );
  },
};

window.performancePage = performancePage;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — pages/clients.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/pages/clients.js"] = """const clientsPage = {
  async init() {
    await this.loadClients();
    this._bindSearch();
  },

  async loadClients(q = '') {
    try {
      const clients = await api.getClients(q);
      state.set('clients', clients);
      this.renderTable(clients);
    } catch (e) { toast.error('Erro ao carregar clientes'); }
  },

  renderTable(clients) {
    const cols = [
      { key: 'name',        render: r => `<strong>${r.name}</strong>` },
      { key: 'external_id', render: r => `<code style="font-size:.78rem;background:var(--bg-input);padding:2px 6px;border-radius:4px">${r.external_id}</code>` },
      { key: 'ltv',         render: r => utils.fmt.currency(r.ltv) },
      { key: 'avg_ticket',  render: r => utils.fmt.currency(r.avg_ticket) },
      { key: 'last_purchase_date', render: r => utils.fmt.date(r.last_purchase_date) },
      { key: 'churn_risk_score', render: r => {
          const pct = r.churn_risk_score;
          const color = pct >= 70 ? 'var(--danger)' : pct >= 40 ? 'var(--warning)' : 'var(--success)';
          return `<span style="color:${color};font-weight:700">${pct.toFixed(0)}%</span>`;
        }
      },
      { key: 'is_at_risk', render: r => r.is_at_risk
          ? '<span class="badge badge-red"><i class="ph-fill ph-warning"></i> Em Risco</span>'
          : '<span class="badge badge-green"><i class="ph-fill ph-check-circle"></i> Saudável</span>'
      },
      { key: 'actions', render: r => `<a href="pages/client-detail.html?id=${r.id}" class="btn btn-sm btn-secondary"><i class="ph ph-eye"></i> Ver</a>` },
    ];
    table.render('clients-table-body', clients, cols);
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
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — pages/client-detail.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/pages/client-detail.js"] = """const clientDetailPage = {
  async init() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    if (!id) { toast.error('ID do cliente não informado'); return; }
    await this.load(id);
  },

  async load(id) {
    try {
      const [client, history, cards] = await Promise.all([
        api.getClient(id),
        api.getClientHistory(id),
        api.getCards(`?client_id=${id}`),
      ]);
      state.set('currentClient', client);
      this.renderHeader(client);
      this.renderHistory(history);
      this.renderCards(cards);
      this._bindAddHistory(id);
    } catch (e) { toast.error('Erro ao carregar cliente: ' + e.message); }
  },

  renderHeader(c) {
    utils.qs('#client-name')?.textContent        && (utils.qs('#client-name').textContent        = c.name);
    utils.qs('#client-external-id')?.textContent && (utils.qs('#client-external-id').textContent = c.external_id);
    utils.qs('#client-ltv')?.textContent         && (utils.qs('#client-ltv').textContent         = utils.fmt.currency(c.ltv));
    utils.qs('#client-ticket')?.textContent      && (utils.qs('#client-ticket').textContent      = utils.fmt.currency(c.avg_ticket));
    utils.qs('#client-last-purchase')?.textContent && (utils.qs('#client-last-purchase').textContent = utils.fmt.date(c.last_purchase_date));
    utils.qs('#client-risk-score')?.textContent  && (utils.qs('#client-risk-score').textContent  = c.churn_risk_score.toFixed(0) + '%');
    const badge = utils.qs('#client-risk-badge');
    if (badge) badge.innerHTML = c.is_at_risk
      ? '<span class="badge badge-red"><i class="ph-fill ph-warning"></i> Em Risco</span>'
      : '<span class="badge badge-green"><i class="ph-fill ph-check-circle"></i> Saudável</span>';
  },

  renderHistory(history) {
    const el = utils.qs('#client-history-list');
    if (!el) return;
    el.innerHTML = history.length
      ? history.map(h => `
          <div class="card card-flat" style="padding:.875rem;margin-bottom:.5rem;border-left:3px solid var(--brand-primary)">
            <div style="display:flex;justify-content:space-between;margin-bottom:.25rem">
              <strong style="font-size:.8rem">${h.card_id ? 'Card' : 'Registro Manual'}</strong>
              <span style="font-size:.72rem;color:var(--text-muted)">${utils.fmt.datetime(h.created_at)}</span>
            </div>
            <p style="font-size:.85rem;color:var(--text-secondary)">${h.content}</p>
          </div>`).join('')
      : '<p style="color:var(--text-muted);font-size:.85rem">Nenhum histórico registrado.</p>';
  },

  renderCards(cards) {
    const el = utils.qs('#client-cards-list');
    if (!el) return;
    el.innerHTML = cards.length
      ? cards.map(c => `
          <div class="card" style="padding:1rem;cursor:pointer" onclick="cardDetail.open(${JSON.stringify(c).replace(/"/g,'&quot;')})">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.5rem">
              <strong style="font-size:.875rem">${c.title || 'Card'}</strong>
              ${utils.stageBadge(c.stage)}
            </div>
            <div style="font-size:.78rem;color:var(--text-secondary)">
              Valor em risco: <strong style="color:var(--danger)">${utils.fmt.currency(c.value_at_risk)}</strong>
              &nbsp;·&nbsp; Criado em ${utils.fmt.date(c.created_at)}
            </div>
          </div>`).join('')
      : '<p style="color:var(--text-muted);font-size:.85rem">Nenhum card criado para este cliente.</p>';
  },

  _bindAddHistory(clientId) {
    const form = utils.qs('#form-add-history');
    if (!form) return;
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(form);
      try {
        await api.createAction({
          card_id:     fd.get('card_id') || '00000000-0000-0000-0000-000000000000',
          client_id:   clientId,
          seller_id:   fd.get('seller_id'),
          action_type: fd.get('action_type'),
          description: fd.get('description'),
        });
        toast.success('Histórico registrado!');
        form.reset();
        await this.load(clientId);
      } catch (err) { toast.error(err.message); }
    });
  },
};

window.clientDetailPage = clientDetailPage;
"""

# ══════════════════════════════════════════════════════════════════════════════
# JS — app.js
# ══════════════════════════════════════════════════════════════════════════════
FILES["assets/js/app.js"] = """// Athena CRM — App bootstrap
document.addEventListener('DOMContentLoaded', () => {
  theme.init();
  header.init();
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
"""

# ══════════════════════════════════════════════════════════════════════════════
# HTML — Shared snippet builders
# ══════════════════════════════════════════════════════════════════════════════

def _head(title, extra_css=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Athena CRM</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link rel="stylesheet" href="../assets/css/variables.css">
  <link rel="stylesheet" href="../assets/css/reset.css">
  <link rel="stylesheet" href="../assets/css/layout.css">
  <link rel="stylesheet" href="../assets/css/components.css">
  <link rel="stylesheet" href="../assets/css/animations.css">
  <link rel="stylesheet" href="../assets/css/dark-theme.css">
  <link rel="stylesheet" href="../assets/css/responsive.css">
  {extra_css}
</head>"""

def _sidebar(active):
    links = [
        ("#dashboard",   "ph-squares-four",   "Dashboard",      "dashboard"),
        ("#actions",     "ph-kanban",          "Ações / Kanban", "actions"),
        ("#performance", "ph-chart-bar",       "Performance",    "performance"),
        ("#clients",     "ph-users",           "Clientes",       "clients"),
    ]
    items = ""
    for href, icon, label, key in links:
        active_cls = " active" if key == active else ""
        items += f'<li class="nav-item"><a href="{href}" class="nav-link{active_cls}"><i class="ph {icon}"></i>{label}</a></li>\n'
    return f"""
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="logo-icon"><i class="ph-fill ph-brain"></i></div>
      <div class="logo-text">Athena CRM<span>Churn Management Suite</span></div>
    </div>
    <nav>
      <div class="nav-section">
        <span class="nav-label">Principal</span>
        <ul>{items}</ul>
      </div>
    </nav>
    <div class="sidebar-footer">
      <div style="margin-bottom:.25rem;font-weight:600;color:var(--brand-primary)">O2 Data</div>
      &copy; <span id="footer-year"></span> Athena CRM
    </div>
  </aside>"""

def _header(title, subtitle=""):
    return f"""
  <header class="header">
    <button class="icon-btn" id="sidebar-toggle" style="display:none"><i class="ph ph-list"></i></button>
    <div class="header-search">
      <i class="ph ph-magnifying-glass"></i>
      <input type="text" placeholder="Buscar clientes, cards...">
    </div>
    <div class="header-actions">
      <button class="icon-btn" id="theme-btn" title="Alternar tema">
        <i class="ph ph-moon" id="theme-icon"></i>
      </button>
      <button class="icon-btn" title="Notificações">
        <i class="ph ph-bell"></i>
        <span class="dot"></span>
      </button>
      <div class="user-chip">
        <div class="avatar">AD</div>
        <div class="user-info">
          <div class="user-name">Admin</div>
          <div class="user-role">Gestor</div>
        </div>
      </div>
    </div>
  </header>"""

def _footer():
    return """
  <footer class="footer">
    <div class="footer-brand"><i class="ph-fill ph-brain"></i> Athena CRM</div>
    <span>Churn Management Suite — Desenvolvido pela <strong>O2 Data</strong></span>
    <span>&copy; <span id="footer-year"></span></span>
  </footer>"""

def _scripts(page, extra=""):
    return f"""
  <script src="../assets/js/core/api.js"></script>
  <script src="../assets/js/core/state.js"></script>
  <script src="../assets/js/core/theme.js"></script>
  <script src="../assets/js/core/utils.js"></script>
  <script src="../assets/js/core/router.js"></script>
  <script src="../assets/js/core/auth.js"></script>
  <script src="../assets/js/components/toast.js"></script>
  <script src="../assets/js/components/modal.js"></script>
  <script src="../assets/js/components/sidebar.js"></script>
  <script src="../assets/js/components/header.js"></script>
  <script src="../assets/js/components/footer.js"></script>
  <script src="../assets/js/components/charts.js"></script>
  <script src="../assets/js/components/kanban.js"></script>
  <script src="../assets/js/components/card.js"></script>
  <script src="../assets/js/components/table.js"></script>
  <script src="../assets/js/components/search.js"></script>
  {extra}
  <script src="../assets/js/pages/{page}.js"></script>
  <script src="../assets/js/app.js"></script>
</body></html>"""

# ══════════════════════════════════════════════════════════════════════════════
# HTML — pages/dashboard.html
# ══════════════════════════════════════════════════════════════════════════════
FILES["pages/dashboard.html"] = _head("Dashboard") + """
<body data-page="dashboard">
<div class="app">
""" + _sidebar("dashboard") + """
  <div class="main">
""" + _header("Dashboard") + """
    <div class="content animate-fade">
      <div class="page-header">
        <div>
          <h1 class="page-title">Dashboard</h1>
          <p class="page-subtitle">Indicadores de churn em tempo real</p>
        </div>
        <button class="btn btn-primary" onclick="dashboardPage.loadKPIs()">
          <i class="ph ph-arrows-clockwise"></i> Atualizar
        </button>
      </div>

      <!-- KPIs -->
      <div class="kpi-grid stagger">
        <div class="kpi-card animate-fade">
          <div class="kpi-header">
            <span class="kpi-label">Total de Cards</span>
            <div class="kpi-icon purple"><i class="ph-fill ph-kanban"></i></div>
          </div>
          <div class="kpi-value" id="kpi-total-cards">—</div>
          <div class="kpi-trend neutral"><i class="ph ph-minus"></i> Ações ativas</div>
        </div>
        <div class="kpi-card animate-fade">
          <div class="kpi-header">
            <span class="kpi-label">Clientes em Risco</span>
            <div class="kpi-icon red"><i class="ph-fill ph-warning-circle"></i></div>
          </div>
          <div class="kpi-value" id="kpi-at-risk">—</div>
          <div class="kpi-trend down"><i class="ph ph-trend-up"></i> Detectados</div>
        </div>
        <div class="kpi-card animate-fade">
          <div class="kpi-header">
            <span class="kpi-label">Valor em Risco</span>
            <div class="kpi-icon orange"><i class="ph-fill ph-currency-dollar"></i></div>
          </div>
          <div class="kpi-value" id="kpi-value-risk">—</div>
          <div class="kpi-trend down"><i class="ph ph-trend-up"></i> Total exposto</div>
        </div>
        <div class="kpi-card animate-fade">
          <div class="kpi-header">
            <span class="kpi-label">Ticket Médio (Risco)</span>
            <div class="kpi-icon blue"><i class="ph-fill ph-receipt"></i></div>
          </div>
          <div class="kpi-value" id="kpi-avg-ticket">—</div>
          <div class="kpi-trend neutral"><i class="ph ph-minus"></i> Clientes em risco</div>
        </div>
        <div class="kpi-card animate-fade">
          <div class="kpi-header">
            <span class="kpi-label">Oportunidades</span>
            <div class="kpi-icon green"><i class="ph-fill ph-handshake"></i></div>
          </div>
          <div class="kpi-value" id="kpi-opportunities">—</div>
          <div class="kpi-trend up"><i class="ph ph-trend-up"></i> Em negociação</div>
        </div>
      </div>

      <!-- Stage pills -->
      <div class="grid-2-1" style="margin-bottom:2rem">
        <div class="card">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
            <span style="font-weight:700">Distribuição por Estágio</span>
          </div>
          <div style="display:flex;gap:.75rem;flex-wrap:wrap">
            <div class="kpi-card" style="flex:1;min-width:120px;padding:1rem">
              <div class="kpi-label">Em Andamento</div>
              <div class="kpi-value" style="font-size:1.5rem" id="kpi-in-progress">—</div>
            </div>
            <div class="kpi-card" style="flex:1;min-width:120px;padding:1rem">
              <div class="kpi-label">Convertido</div>
              <div class="kpi-value" style="font-size:1.5rem;color:var(--success)" id="kpi-converted">—</div>
            </div>
            <div class="kpi-card" style="flex:1;min-width:120px;padding:1rem">
              <div class="kpi-label">Declinado</div>
              <div class="kpi-value" style="font-size:1.5rem;color:var(--danger)" id="kpi-declined">—</div>
            </div>
          </div>
        </div>
        <div class="card">
          <div style="font-weight:700;margin-bottom:.5rem">Estágios</div>
          <div class="chart-wrap"><canvas id="chart-stages"></canvas></div>
        </div>
      </div>

      <!-- Line chart -->
      <div class="card">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem">
          <span style="font-weight:700">Tendência de Valor em Risco</span>
        </div>
        <div class="chart-wrap"><canvas id="chart-risk-trend"></canvas></div>
      </div>
    </div>
""" + _footer() + """
  </div>
</div>
""" + _scripts("dashboard")

# ══════════════════════════════════════════════════════════════════════════════
# HTML — pages/actions.html
# ══════════════════════════════════════════════════════════════════════════════
FILES["pages/actions.html"] = _head("Ações") + """
<body data-page="actions">
<div class="app">
""" + _sidebar("actions") + """
  <div class="main">
""" + _header("Ações") + """
    <div class="content animate-fade">
      <div class="page-header">
        <div>
          <h1 class="page-title">Ações / Kanban</h1>
          <p class="page-subtitle">Gerencie o fluxo de churn dos seus clientes</p>
        </div>
        <button class="btn btn-primary" id="btn-new-card">
          <i class="ph ph-plus"></i> Novo Card
        </button>
      </div>

      <!-- Kanban Board -->
      <div id="kanban-board" class="kanban-board"></div>
    </div>
""" + _footer() + """
  </div>
</div>

<!-- Modal: Novo Card -->
<div class="modal-overlay" id="modal-new-card">
  <div class="modal animate-scale">
    <div class="modal-header">
      <span class="modal-title"><i class="ph ph-plus-circle" style="color:var(--brand-primary)"></i> Novo Card</span>
      <button class="modal-close icon-btn"><i class="ph ph-x"></i></button>
    </div>
    <form id="form-new-card">
      <div class="form-group">
        <label class="form-label">ID do Cliente</label>
        <input name="client_id" class="form-control" placeholder="UUID do cliente" required>
      </div>
      <div class="form-group">
        <label class="form-label">ID do Vendedor</label>
        <input name="seller_id" class="form-control" placeholder="UUID do vendedor" required>
      </div>
      <div class="form-group">
        <label class="form-label">Título</label>
        <input name="title" class="form-control" placeholder="Ex: Risco de churn detectado" required>
      </div>
      <div class="form-group">
        <label class="form-label">Descrição</label>
        <textarea name="description" class="form-control" rows="3" placeholder="Detalhes da ação..."></textarea>
      </div>
      <div class="form-group">
        <label class="form-label">Valor em Risco (R$)</label>
        <input name="value_at_risk" type="number" step="0.01" class="form-control" placeholder="0.00">
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary modal-close">Cancelar</button>
        <button type="submit" class="btn btn-primary"><i class="ph ph-check"></i> Criar Card</button>
      </div>
    </form>
  </div>
</div>

<!-- Modal: Card Detail -->
<div class="modal-overlay" id="modal-card-detail">
  <div class="modal animate-scale" style="max-width:600px">
    <div class="modal-header">
      <span class="modal-title" id="modal-card-title">Detalhe do Card</span>
      <button class="modal-close icon-btn"><i class="ph ph-x"></i></button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1rem">
      <div><span style="font-size:.75rem;color:var(--text-muted)">Cliente</span><div style="font-weight:600" id="modal-card-client">—</div></div>
      <div><span style="font-size:.75rem;color:var(--text-muted)">Estágio</span><div id="modal-card-stage">—</div></div>
      <div><span style="font-size:.75rem;color:var(--text-muted)">LTV</span><div style="font-weight:600" id="modal-card-ltv">—</div></div>
      <div><span style="font-size:.75rem;color:var(--text-muted)">Ticket Médio</span><div style="font-weight:600" id="modal-card-ticket">—</div></div>
      <div><span style="font-size:.75rem;color:var(--text-muted)">Valor em Risco</span><div style="font-weight:700;color:var(--danger)" id="modal-card-risk">—</div></div>
      <div><span style="font-size:.75rem;color:var(--text-muted)">Última Compra</span><div id="modal-card-last-purchase">—</div></div>
    </div>
    <div class="divider"></div>
    <div style="font-weight:700;margin-bottom:.75rem">Histórico de Ações</div>
    <div id="modal-card-actions" style="max-height:260px;overflow-y:auto"></div>
  </div>
</div>
""" + _scripts("actions")

# ══════════════════════════════════════════════════════════════════════════════
# HTML — pages/performance.html
# ══════════════════════════════════════════════════════════════════════════════
FILES["pages/performance.html"] = _head("Performance") + """
<body data-page="performance">
<div class="app">
""" + _sidebar("performance") + """
  <div class="main">
""" + _header("Performance") + """
    <div class="content animate-fade">
      <div class="page-header">
        <div>
          <h1 class="page-title">Performance</h1>
          <p class="page-subtitle">Acompanhe conversões, pendências e resultados por vendedor</p>
        </div>
        <select class="form-control" id="filter-seller" style="width:220px"></select>
      </div>

      <div class="grid-2-1" style="margin-bottom:2rem">
        <div class="card">
          <div style="font-weight:700;margin-bottom:1rem">Cards por Estágio</div>
          <div class="chart-wrap"><canvas id="chart-perf-stages"></canvas></div>
        </div>
        <div class="card">
          <div style="font-weight:700;margin-bottom:1rem">Legenda</div>
          <div style="display:flex;flex-direction:column;gap:.5rem">
            <div class="badge badge-gray" style="justify-content:flex-start">Backlog</div>
            <div class="badge badge-blue" style="justify-content:flex-start">Em Andamento</div>
            <div class="badge badge-orange" style="justify-content:flex-start">Em Negociação</div>
            <div class="badge badge-green" style="justify-content:flex-start">Convertido</div>
            <div class="badge badge-red" style="justify-content:flex-start">Declinado</div>
          </div>
        </div>
      </div>

      <div class="card card-flat" style="border:1px solid var(--border)">
        <div style="display:flex;align-items:center;justify-content:space-between;padding:1.25rem 1.5rem;border-bottom:1px solid var(--border)">
          <span style="font-weight:700">Todos os Cards</span>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Cliente</th><th>Estágio</th><th>Valor em Risco</th>
                <th>Ticket Médio</th><th>LTV</th><th>Criado em</th>
              </tr>
            </thead>
            <tbody id="perf-table-body"></tbody>
          </table>
        </div>
      </div>
    </div>
""" + _footer() + """
  </div>
</div>
""" + _scripts("performance")

# ══════════════════════════════════════════════════════════════════════════════
# HTML — pages/clients.html
# ══════════════════════════════════════════════════════════════════════════════
FILES["pages/clients.html"] = _head("Clientes") + """
<body data-page="clients">
<div class="app">
""" + _sidebar("clients") + """
  <div class="main">
""" + _header("Clientes") + """
    <div class="content animate-fade">
      <div class="page-header">
        <div>
          <h1 class="page-title">Clientes</h1>
          <p class="page-subtitle">Pesquise por nome ou ID externo</p>
        </div>
      </div>

      <div class="card card-flat" style="border:1px solid var(--border)">
        <div style="padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;gap:1rem;align-items:center">
          <div class="header-search" style="max-width:360px;flex:1">
            <i class="ph ph-magnifying-glass"></i>
            <input type="text" id="client-search" placeholder="Buscar por nome ou ID...">
          </div>
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th><th>ID Externo</th><th>LTV</th>
                <th>Ticket Médio</th><th>Última Compra</th>
                <th>Score Churn</th><th>Status</th><th></th>
              </tr>
            </thead>
            <tbody id="clients-table-body"></tbody>
          </table>
        </div>
      </div>
    </div>
""" + _footer() + """
  </div>
</div>
""" + _scripts("clients")

# ══════════════════════════════════════════════════════════════════════════════
# HTML — pages/client-detail.html
# ══════════════════════════════════════════════════════════════════════════════
FILES["pages/client-detail.html"] = _head("Detalhe do Cliente") + """
<body data-page="client-detail">
<div class="app">
""" + _sidebar("clients") + """
  <div class="main">
""" + _header("Detalhe do Cliente") + """
    <div class="content animate-fade">
      <a href="clients.html" class="btn btn-secondary btn-sm" style="margin-bottom:1.5rem;display:inline-flex">
        <i class="ph ph-arrow-left"></i> Voltar
      </a>

      <!-- Client Header -->
      <div class="card" style="margin-bottom:1.5rem">
        <div style="display:flex;align-items:center;gap:1.5rem;flex-wrap:wrap">
          <div style="width:64px;height:64px;border-radius:50%;background:var(--brand-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-size:1.5rem;font-weight:700;flex-shrink:0">
            <i class="ph-fill ph-user"></i>
          </div>
          <div style="flex:1">
            <h2 style="font-size:1.4rem;font-weight:800;margin-bottom:.25rem" id="client-name">—</h2>
            <div style="display:flex;align-items:center;gap:.75rem;flex-wrap:wrap">
              <code style="font-size:.78rem;background:var(--bg-input);padding:2px 8px;border-radius:4px" id="client-external-id">—</code>
              <span id="client-risk-badge"></span>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;text-align:center">
            <div><div style="font-size:.72rem;color:var(--text-muted)">LTV</div><div style="font-weight:700;font-size:1rem" id="client-ltv">—</div></div>
            <div><div style="font-size:.72rem;color:var(--text-muted)">Ticket Médio</div><div style="font-weight:700;font-size:1rem" id="client-ticket">—</div></div>
            <div><div style="font-size:.72rem;color:var(--text-muted)">Score Churn</div><div style="font-weight:700;font-size:1rem" id="client-risk-score">—</div></div>
          </div>
        </div>
      </div>

      <div class="grid-2">
        <!-- Cards do cliente -->
        <div>
          <div style="font-weight:700;margin-bottom:1rem">Cards Criados</div>
          <div id="client-cards-list"></div>
        </div>

        <!-- Histórico -->
        <div>
          <div style="font-weight:700;margin-bottom:1rem">Histórico de Interações</div>
          <div id="client-history-list" style="max-height:400px;overflow-y:auto;margin-bottom:1rem"></div>

          <!-- Registrar ação manual -->
          <div class="card" style="padding:1.25rem">
            <div style="font-weight:700;margin-bottom:1rem;font-size:.9rem">Registrar Interação</div>
            <form id="form-add-history">
              <div class="form-group">
                <label class="form-label">Tipo</label>
                <select name="action_type" class="form-control">
                  <option value="call">Ligação</option>
                  <option value="email">E-mail</option>
                  <option value="meeting">Reunião</option>
                  <option value="whatsapp">WhatsApp</option>
                  <option value="note">Nota</option>
                  <option value="proposal">Proposta</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">ID do Vendedor</label>
                <input name="seller_id" class="form-control" placeholder="UUID do vendedor" required>
              </div>
              <div class="form-group">
                <label class="form-label">Descrição</label>
                <textarea name="description" class="form-control" rows="3" placeholder="Descreva a interação..." required></textarea>
              </div>
              <button type="submit" class="btn btn-primary" style="width:100%">
                <i class="ph ph-paper-plane-tilt"></i> Registrar
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
""" + _footer() + """
  </div>
</div>
""" + _scripts("client-detail")

# ══════════════════════════════════════════════════════════════════════════════
# HTML — index.html (root — redirect to dashboard)
# ══════════════════════════════════════════════════════════════════════════════
FILES["../index.html"] = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=pages/dashboard.html">
  <title>Athena CRM</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  <style>
    :root { --brand-gradient: linear-gradient(135deg,#7c3aed,#a78bfa); }
    * { margin:0; padding:0; box-sizing:border-box; font-family:'Inter',sans-serif; }
    body { min-height:100vh; display:flex; align-items:center; justify-content:center; background:#0d0f1a; }
    .splash { text-align:center; color:#fff; }
    .logo { width:72px; height:72px; background:var(--brand-gradient); border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:2rem; margin:0 auto 1.5rem; box-shadow:0 16px 40px rgba(124,58,237,.4); }
    h1 { font-size:2rem; font-weight:800; margin-bottom:.5rem; }
    p { color:#9ca3af; margin-bottom:1.5rem; }
    a { display:inline-flex; align-items:center; gap:8px; padding:12px 28px; background:var(--brand-gradient); color:#fff; border-radius:12px; font-weight:600; text-decoration:none; box-shadow:0 8px 24px rgba(124,58,237,.35); }
  </style>
</head>
<body>
  <div class="splash">
    <div class="logo"><i class="ph-fill ph-brain"></i></div>
    <h1>Athena CRM</h1>
    <p>Churn Management Suite — O2 Data</p>
    <a href="pages/dashboard.html"><i class="ph ph-arrow-right"></i> Entrar</a>
  </div>
</body>
</html>
"""

# ══════════════════════════════════════════════════════════════════════════════
# WRITER
# ══════════════════════════════════════════════════════════════════════════════

def write_files():
    print("=" * 60)
    print("  Athena CRM — Populando frontend")
    print("=" * 60)
    ok = 0
    for rel_path, content in FILES.items():
        full_path = os.path.join(BASE, rel_path)
        os.makedirs(os.path.dirname(os.path.abspath(full_path)), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  ✅  {full_path}")
        ok += 1
    print()
    print(f"  {ok} arquivos escritos com sucesso!")
    print("=" * 60)
    print()
    print("  Abra: athena-crm/frontend/index.html")
    print("  Ou sirva com: python -m http.server 3000 (dentro de frontend/)")
    print()


if __name__ == "__main__":
    write_files()
