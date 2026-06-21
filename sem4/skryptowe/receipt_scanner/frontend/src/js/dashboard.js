const CATEGORY_COLORS = {
  'Jedzenie': '#7F77DD',
  'Transport': '#1D9E75',
  'Dom': '#D85A30',
  'Zdrowie': '#378ADD',
  'Rozrywka': '#BA7517',
  'Inne': '#888780',
};

function monthLabel(key) {
  // "2024-03" → "03.2024"
  const [y, m] = key.split('-');
  return `${m}.${y}`;
}

async function loadDashboard() {
  let summary;
  try {
    summary = await apiFetch('/dashboard/summary');
  } catch (err) {
    document.getElementById('empty').hidden = false;
    document.getElementById('empty').textContent = `Błąd ładowania: ${err.message}`;
    return;
  }

  if (!summary.receipt_count) {
    document.getElementById('empty').hidden = false;
    document.getElementById('content').hidden = true;
    return;
  }

  document.getElementById('empty').hidden = true;
  document.getElementById('content').hidden = false;

  renderCards(summary);
  renderCategoryChart(summary.by_category);
  renderMonthChart(summary.by_month);
}

function renderCards(summary) {
  document.getElementById('totalSpent').textContent = formatPLN(summary.total_spent);
  document.getElementById('receiptCount').textContent = summary.receipt_count;

  const categories = Object.entries(summary.by_category || {});
  if (categories.length) {
    const top = categories.reduce((a, b) => (b[1] > a[1] ? b : a));
    document.getElementById('topCategory').textContent = top[0];
  } else {
    document.getElementById('topCategory').textContent = '—';
  }

  const months = Object.keys(summary.by_month || {});
  const currentKey = months[months.length - 1];
  document.getElementById('currentMonth').textContent =
    formatPLN(summary.by_month[currentKey] || 0);
}

function renderCategoryChart(byCategory) {
  const labels = Object.keys(byCategory);
  const values = Object.values(byCategory);
  const colors = labels.map((l) => CATEGORY_COLORS[l] || '#888780');

  new Chart(document.getElementById('categoryChart'), {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{ data: values, backgroundColor: colors }],
    },
    options: {
      plugins: { legend: { position: 'right' } },
    },
  });
}

function renderMonthChart(byMonth) {
  const labels = Object.keys(byMonth).map(monthLabel);
  const values = Object.values(byMonth);

  new Chart(document.getElementById('monthChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [{ label: 'Wydatki (PLN)', data: values, backgroundColor: '#7F77DD' }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { callback: (v) => `${v} zł` },
        },
      },
    },
  });
}

loadDashboard();
