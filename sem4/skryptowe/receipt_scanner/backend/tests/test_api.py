import io
from unittest.mock import patch

from PIL import Image


def _png_bytes() -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", (50, 50), color="white").save(buf, format="PNG")
    return buf.getvalue()


def _upload(client, content_type="image/png", filename="receipt.png"):
    """Wgrywa paragon z zamockowanym OCR (bez wymogu Tesseract)."""
    fake_text = "BIEDRONKA\n2024-03-15\nChleb 4,50\nSUMA 4,50"
    with patch(
        "app.services.ocr_service.pytesseract.image_to_string",
        return_value=fake_text,
    ):
        return client.post(
            "/api/receipts/upload",
            files={"file": (filename, _png_bytes(), content_type)},
        )


def test_upload_receipt(client):
    resp = _upload(client)
    assert resp.status_code == 201
    data = resp.json()
    assert data["store_name"] == "BIEDRONKA"
    assert data["total_amount"] == "4.50"
    assert len(data["items"]) >= 1
    assert "id" in data


def test_list_receipts(client):
    _upload(client)
    resp = client.get("/api/receipts")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert "items" not in data[0]  # widok listy bez pozycji


def test_get_receipt_details(client):
    receipt_id = _upload(client).json()["id"]
    resp = client.get(f"/api/receipts/{receipt_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == receipt_id
    assert isinstance(data["items"], list)


def test_get_receipt_not_found(client):
    resp = client.get("/api/receipts/9999")
    assert resp.status_code == 404


def test_delete_receipt(client):
    receipt_id = _upload(client).json()["id"]
    resp = client.delete(f"/api/receipts/{receipt_id}")
    assert resp.status_code == 204
    assert client.get(f"/api/receipts/{receipt_id}").status_code == 404


def test_dashboard_summary_structure(client):
    _upload(client)
    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {
        "total_spent", "receipt_count", "by_category", "by_month",
    }
    assert data["receipt_count"] == 1
    assert isinstance(data["by_category"], dict)
    assert isinstance(data["by_month"], dict)
    assert len(data["by_month"]) == 6


def test_upload_pdf_rejected(client):
    resp = client.post(
        "/api/receipts/upload",
        files={"file": ("doc.pdf", b"%PDF-1.4 fake", "application/pdf")},
    )
    assert resp.status_code == 422
