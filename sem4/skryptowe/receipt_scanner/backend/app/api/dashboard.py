"""Endpoint podsumowania wydatków dla dashboardu."""

from collections import OrderedDict
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.receipt import Receipt, ReceiptItem
from app.schemas.receipt import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

MONTHS_BACK = 6


def _last_months(count: int) -> list[str]:
    today = date.today()
    months: list[str] = []
    year, month = today.year, today.month
    for _ in range(count):
        months.append(f"{year:04d}-{month:02d}")
        month -= 1
        if month == 0:
            month = 12
            year -= 1
    return list(reversed(months))


@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total_spent = db.scalar(select(func.coalesce(func.sum(Receipt.total_amount), 0)))
    receipt_count = db.scalar(select(func.count(Receipt.id))) or 0

    category_rows = db.execute(
        select(ReceiptItem.category, func.sum(ReceiptItem.amount))
        .group_by(ReceiptItem.category)
    ).all()
    by_category = {
        (category or "Inne"): float(amount or 0)
        for category, amount in category_rows
    }

    # Wydatki per miesiąc (ostatnie 6 miesięcy), zainicjalizowane zerami.
    # Agregacja po stronie Pythona — niezależna od dialektu bazy.
    by_month: "OrderedDict[str, float]" = OrderedDict(
        (m, 0.0) for m in _last_months(MONTHS_BACK)
    )
    dated_rows = db.execute(
        select(Receipt.receipt_date, Receipt.total_amount)
        .where(Receipt.receipt_date.isnot(None))
    ).all()
    for receipt_date, amount in dated_rows:
        key = f"{receipt_date.year:04d}-{receipt_date.month:02d}"
        if key in by_month:
            by_month[key] += float(amount or 0)

    return DashboardSummary(
        total_spent=float(total_spent or 0),
        receipt_count=int(receipt_count),
        by_category=by_category,
        by_month=dict(by_month),
    )
