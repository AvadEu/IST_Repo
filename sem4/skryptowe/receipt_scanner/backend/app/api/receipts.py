"""Endpointy REST dla paragonów (CRUD + upload z pipeline OCR)."""

import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.config import settings
from app.db.session import get_db
from app.models.receipt import Receipt, ReceiptItem
from app.schemas.receipt import ReceiptListItem, ReceiptRead
from app.services import categorizer_service, ocr_service, parser_service

router = APIRouter(prefix="/receipts", tags=["receipts"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


@router.post("/upload", response_model=ReceiptRead, status_code=status.HTTP_201_CREATED)
async def upload_receipt(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> Receipt:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Dozwolone są wyłącznie pliki image/jpeg i image/png.",
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Plik przekracza dozwolony rozmiar 10 MB.",
        )

    os.makedirs(settings.upload_dir, exist_ok=True)
    ext = "png" if file.content_type == "image/png" else "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = os.path.join(settings.upload_dir, filename)
    with open(file_path, "wb") as fh:
        fh.write(content)

    # Pipeline OCR → parsowanie → kategoryzacja. Błąd OCR nie blokuje zapisu.
    raw_text = ""
    parsed = {"store_name": None, "date": None, "total_amount": None, "items": []}
    try:
        raw_text = ocr_service.extract_text(file_path)
        parsed = parser_service.parse_receipt(raw_text)
    except Exception:
        parsed["items"] = []

    categorized = categorizer_service.categorize_receipt(
        parsed.get("store_name"), parsed.get("items", [])
    )

    receipt = Receipt(
        store_name=parsed.get("store_name"),
        receipt_date=parsed.get("date"),
        total_amount=parsed.get("total_amount"),
        image_path=filename,
        raw_text=raw_text,
        items=[
            ReceiptItem(
                name=item["name"],
                amount=item.get("amount"),
                category=item.get("category"),
            )
            for item in categorized
        ],
    )
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


@router.get("", response_model=list[ReceiptListItem])
def list_receipts(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
) -> list[Receipt]:
    stmt = (
        select(Receipt)
        .order_by(Receipt.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return list(db.scalars(stmt).all())


@router.get("/{receipt_id}", response_model=ReceiptRead)
def get_receipt(receipt_id: int, db: Session = Depends(get_db)) -> Receipt:
    stmt = (
        select(Receipt)
        .where(Receipt.id == receipt_id)
        .options(selectinload(Receipt.items))
    )
    receipt = db.scalars(stmt).first()
    if receipt is None:
        raise HTTPException(status_code=404, detail="Paragon nie istnieje.")
    return receipt


@router.delete("/{receipt_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)) -> None:
    receipt = db.get(Receipt, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Paragon nie istnieje.")

    if receipt.image_path:
        file_path = os.path.join(settings.upload_dir, receipt.image_path)
        if os.path.exists(file_path):
            os.remove(file_path)

    db.delete(receipt)
    db.commit()
