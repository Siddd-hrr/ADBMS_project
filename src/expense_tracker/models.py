
"""Expense data model."""

from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal

from bson import ObjectId
from bson.decimal128 import Decimal128


@dataclass
class Expense:
    title: str
    amount: Decimal
    category: str
    date: date
    payment_method: str
    description: str = ""
    id: ObjectId | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_document(self) -> dict:
        """Convert an Expense object into a MongoDB document."""

        now = datetime.now(timezone.utc)

        return {
            **({"_id": self.id} if self.id is not None else {}),
            "title": self.title.strip(),
            "amount": Decimal128(self.amount),
            "category": self.category,
            "date": datetime.combine(
                self.date, time.min, tzinfo=timezone.utc
            ),
            "payment_method": self.payment_method,
            "description": self.description.strip(),
            "created_at": self.created_at or now,
            "updated_at": self.updated_at or now,
        }

    @classmethod
    def from_document(cls, document: dict) -> "Expense":
        """Convert a MongoDB document into an Expense object."""

        stored_date = document["date"]
        expense_date = (
            stored_date.date()
            if isinstance(stored_date, datetime)
            else stored_date
        )

        stored_amount = document["amount"]
        amount = (
            stored_amount.to_decimal()
            if isinstance(stored_amount, Decimal128)
            else Decimal(str(stored_amount))
        )

        return cls(
            id=document["_id"],
            title=document["title"],
            amount=amount,
            category=document["category"],
            date=expense_date,
            payment_method=document["payment_method"],
            description=document.get("description", ""),
            created_at=document.get("created_at"),
            updated_at=document.get("updated_at"),
        )
