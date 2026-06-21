from unittest.mock import patch

import pytest
from PIL import Image

from app.services import ocr_service


def test_extract_text_returns_string(sample_image_path):
    """extract_text zwraca string (Tesseract zamockowany, by nie wymagać binarki)."""
    with patch(
        "app.services.ocr_service.pytesseract.image_to_string",
        return_value="BIEDRONKA\n",
    ) as mock_ocr:
        result = ocr_service.extract_text(sample_image_path)

    assert isinstance(result, str)
    assert result == "BIEDRONKA"
    mock_ocr.assert_called_once()


def test_extract_text_empty_file_raises(tmp_path):
    """Pusty / nieprawidłowy plik obrazu powinien rzucić wyjątek."""
    bad = tmp_path / "empty.png"
    bad.write_bytes(b"")
    with pytest.raises(Exception):
        ocr_service.extract_text(str(bad))


def test_preprocess_upscales_small_image(sample_image_path):
    """preprocess_image skaluje mały obraz do min. 1800px szerokości i binaryzuje."""
    result = ocr_service.preprocess_image(sample_image_path)

    assert isinstance(result, Image.Image)
    assert result.width >= ocr_service.MIN_WIDTH


def test_tesseract_not_found_raises_runtime_error(sample_image_path):
    """Brak Tesseracta jest tłumaczony na czytelny RuntimeError."""
    import pytesseract

    with patch(
        "app.services.ocr_service.pytesseract.image_to_string",
        side_effect=pytesseract.TesseractNotFoundError(),
    ):
        with pytest.raises(RuntimeError):
            ocr_service.extract_text(sample_image_path)
