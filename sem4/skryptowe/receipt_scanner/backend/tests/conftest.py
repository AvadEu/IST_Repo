import os
import tempfile

# Konfiguracja środowiska testowego MUSI być ustawiona przed importem aplikacji,
# ponieważ Settings() oraz mount StaticFiles są tworzone na poziomie importu.
os.environ.setdefault("UPLOAD_DIR", tempfile.mkdtemp(prefix="uploads_test_"))
os.environ.setdefault("DB_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def sample_image_path(tmp_path):
    """Tworzy tymczasowy obrazek PNG z prostym tekstem i zwraca jego ścieżkę."""
    path = tmp_path / "sample.png"
    image = Image.new("RGB", (400, 200), color="white")
    draw = ImageDraw.Draw(image)
    draw.text((20, 80), "BIEDRONKA", fill="black")
    image.save(path)
    return str(path)


@pytest.fixture
def client():
    """TestClient z bazą SQLite in-memory podstawioną pod get_db()."""
    from app.db.session import Base, get_db
    from app.main import app

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_receipt_payload():
    """Przykładowe dane sparsowanego paragonu (wynik parser_service)."""
    from datetime import date
    from decimal import Decimal

    return {
        "store_name": "Biedronka",
        "date": date(2024, 3, 15),
        "total_amount": Decimal("15.98"),
        "items": [
            {"name": "Chleb razowy", "amount": Decimal("4.50")},
            {"name": "Mleko 3,2%", "amount": Decimal("3.99")},
            {"name": "Maslo extra", "amount": Decimal("7.49")},
        ],
    }
