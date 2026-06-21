import pytest
from PIL import Image, ImageDraw


@pytest.fixture
def sample_image_path(tmp_path):
    """Tworzy tymczasowy obrazek PNG z prostym tekstem i zwraca jego ścieżkę."""
    path = tmp_path / "sample.png"
    image = Image.new("RGB", (400, 200), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((20, 80), "BIEDRONKA", fill="black")
    image.save(path)
    return str(path)
