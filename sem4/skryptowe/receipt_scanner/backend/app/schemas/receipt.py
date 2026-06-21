"""Schematy pydantic v2 do walidacji i serializacji odpowiedzi API."""

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ReceiptItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    amount: Decimal | None
    category: str | None


class ReceiptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    store_name: str | None
    receipt_date: date | None
    total_amount: Decimal | None
    image_path: str | None
    created_at: datetime
    items: list[ReceiptItemRead]


class ReceiptListItem(BaseModel):
    """Uproszczony widok listy — bez pozycji."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    store_name: str | None
    receipt_date: date | None
    total_amount: Decimal | None
    image_path: str | None
    created_at: datetime


class DashboardSummary(BaseModel):
    total_spent: float
    receipt_count: int
    by_category: dict[str, float]
    by_month: dict[str, float]
