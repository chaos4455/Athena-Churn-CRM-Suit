const charts = {
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
