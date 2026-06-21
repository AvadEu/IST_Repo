const PAGE_SIZE = 20;
let skip = 0;

const tableBody = document.getElementById('tableBody');
const emptyEl = document.getElementById('empty');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const pageInfo = document.getElementById('pageInfo');
const modalContainer = document.getElementById('modalContainer');

function formatDate(value) {
  return value || '—';
}

async function loadReceipts() {
  try {
    const receipts = await apiFetch(`/receipts?skip=${skip}&limit=${PAGE_SIZE}`);
    renderTable(receipts);
    updatePagination(receipts.length);
  } catch (err) {
    tableBody.innerHTML = '';
    emptyEl.hidden = false;
    emptyEl.textContent = `Błąd ładowania: ${err.message}`;
  }
}

function renderTable(receipts) {
  tableBody.innerHTML = '';
  emptyEl.hidden = receipts.length > 0;

  for (const r of receipts) {
    const tr = document.createElement('tr');
    const thumb = r.image_path
      ? `<img class="thumb" src="/uploads/${r.image_path}" alt="paragon">`
      : '—';
    tr.innerHTML = `
      <td>${thumb}</td>
      <td>${r.store_name || '—'}</td>
      <td>${formatDate(r.receipt_date)}</td>
      <td>${formatPLN(r.total_amount)}</td>
      <td>
        <button data-id="${r.id}" class="detailsBtn">Szczegóły</button>
        <button data-id="${r.id}" class="danger deleteBtn">Usuń</button>
      </td>
    `;
    tableBody.appendChild(tr);
  }

  document.querySelectorAll('.detailsBtn').forEach((btn) =>
    btn.addEventListener('click', () => showDetails(btn.dataset.id))
  );
  document.querySelectorAll('.deleteBtn').forEach((btn) =>
    btn.addEventListener('click', () => deleteReceipt(btn.dataset.id))
  );
}

function updatePagination(count) {
  const page = Math.floor(skip / PAGE_SIZE) + 1;
  pageInfo.textContent = `Strona ${page}`;
  prevBtn.disabled = skip === 0;
  nextBtn.disabled = count < PAGE_SIZE;
}

async function showDetails(id) {
  try {
    const r = await apiFetch(`/receipts/${id}`);
    const rows = (r.items || []).map((it) => `
      <tr>
        <td>${it.name}</td>
        <td><span class="badge">${it.category || 'Inne'}</span></td>
        <td>${formatPLN(it.amount)}</td>
      </tr>`).join('');

    modalContainer.innerHTML = `
      <div class="modal-overlay" id="overlay">
        <div class="modal">
          <h2>${r.store_name || 'Paragon'}</h2>
          <p>Data: ${formatDate(r.receipt_date)} · Suma: <strong>${formatPLN(r.total_amount)}</strong></p>
          <table>
            <thead><tr><th>Pozycja</th><th>Kategoria</th><th>Kwota</th></tr></thead>
            <tbody>${rows || '<tr><td colspan="3">Brak pozycji</td></tr>'}</tbody>
          </table>
          <div style="margin-top:16px; text-align:right;">
            <button id="closeModal" class="secondary">Zamknij</button>
          </div>
        </div>
      </div>`;

    document.getElementById('closeModal').addEventListener('click', closeModal);
    document.getElementById('overlay').addEventListener('click', (e) => {
      if (e.target.id === 'overlay') closeModal();
    });
  } catch (err) {
    alert(`Błąd: ${err.message}`);
  }
}

function closeModal() {
  modalContainer.innerHTML = '';
}

async function deleteReceipt(id) {
  if (!confirm('Usunąć ten paragon?')) return;
  try {
    await apiFetch(`/receipts/${id}`, { method: 'DELETE' });
    loadReceipts();
  } catch (err) {
    alert(`Błąd usuwania: ${err.message}`);
  }
}

prevBtn.addEventListener('click', () => {
  if (skip >= PAGE_SIZE) {
    skip -= PAGE_SIZE;
    loadReceipts();
  }
});
nextBtn.addEventListener('click', () => {
  skip += PAGE_SIZE;
  loadReceipts();
});

loadReceipts();
