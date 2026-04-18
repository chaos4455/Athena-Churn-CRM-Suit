const table = {
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
