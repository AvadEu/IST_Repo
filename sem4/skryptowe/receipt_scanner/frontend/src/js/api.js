const BASE = '/api';

/**
 * Wrapper na fetch — zwraca sparsowany JSON, rzuca Error z treścią `detail` z API.
 */
async function apiFetch(path, options = {}) {
  const response = await fetch(`${BASE}${path}`, options);

  if (!response.ok) {
    let detail = `Błąd ${response.status}`;
    try {
      const body = await response.json();
      if (body && body.detail) {
        detail = typeof body.detail === 'string'
          ? body.detail
          : JSON.stringify(body.detail);
      }
    } catch (_) {
      /* odpowiedź bez JSON — zostaw domyślny komunikat */
    }
    throw new Error(detail);
  }

  if (response.status === 204) return null;
  return response.json();
}

/** Formatuje liczbę jako kwotę w PLN. */
function formatPLN(value) {
  const num = Number(value || 0);
  return num.toLocaleString('pl-PL', { style: 'currency', currency: 'PLN' });
}
