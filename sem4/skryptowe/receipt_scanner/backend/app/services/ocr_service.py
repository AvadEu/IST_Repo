"""Serwis OCR — wstępne przetwarzanie obrazu i ekstrakcja tekstu Tesseractem."""

import cv2
import numpy as np
import pytesseract
from PIL import Image

MIN_WIDTH = 1800


def preprocess_image(image_path: str) -> Image.Image:
    """Wczytaj obraz i przygotuj go pod OCR.

    Kroki: skala szarości → binaryzacja Otsu → upscaling do min. 1800px szerokości.
    """
    pil_image = Image.open(image_path)
    pil_image.load()  # wymusza odczyt — wykrywa uszkodzone/puste pliki

    gray = cv2.cvtColor(np.array(pil_image.convert("RGB")), cv2.COLOR_RGB2GRAY)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    height, width = binary.shape[:2]
    if width < MIN_WIDTH:
        scale = MIN_WIDTH / width
        binary = cv2.resize(
            binary,
            (MIN_WIDTH, int(height * scale)),
            interpolation=cv2.INTER_CUBIC,
        )

    return Image.fromarray(binary)


def extract_text(image_path: str) -> str:
    """Wykonaj OCR na przetworzonym obrazie i zwróć oczyszczony tekst."""
    image = preprocess_image(image_path)
    try:
        text = pytesseract.image_to_string(image, lang="pol+eng")
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError(
            "Tesseract OCR nie jest zainstalowany lub niedostępny w PATH."
        ) from exc
    return text.strip()
