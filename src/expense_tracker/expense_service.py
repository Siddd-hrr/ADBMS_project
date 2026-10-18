
"""Business logic for managing expenses."""

import re
from datetime import datetime, timezone
from decimal import Decimal

from bson import ObjectId
from pymongo.collection import Collection

from .database import get_expenses_collection
from .models import Expense


class ExpenseNotFoundError(LookupError):
    """Raised when an expense no longer exists."""


class ExpenseService:
    def __init__(self, collection: Collection | None = None):
        self.collection = (
            collection
            if collection is not None
            else get_expenses_collection()
        )

    # CREATE
    def create(self, expense: Expense) -> ObjectId:
        result = self.collection.insert_one(
            expense.to_document()
        )
        return result.inserted_id

    # READ + SEARCH + FILTER
    def list_expenses(
        self,
        search: str = "",
        category: str = "All",
        payment_method: str = "All",
    ) -> list[Expense]:

        query = {}

        if category != "All":
            query["category"] = category

        if payment_method != "All":
            query["payment_method"] = payment_method

        if search.strip():
            pattern = re.escape(search.strip())
            query["$or"] = [
                {
                    "title": {
                        "$regex": pattern,
                        "$options": "i",
                    }
                },
                {
                    "description": {
                        "$regex": pattern,
                        "$options": "i",
                    }
                },
            ]

        documents = self.collection.find(query).sort(
            [("date", -1), ("created_at", -1)]
        )

        return [
            Expense.from_document(document)
            for document in documents
        ]

    # UPDATE
    def update(
        self,
        expense_id: ObjectId,
        expense: Expense,
    ) -> None:

        expense.updated_at = datetime.now(timezone.utc)
        document = expense.to_document()

        document.pop("_id", None)
        document.pop("created_at", None)

        result = self.collection.update_one(
            {"_id": expense_id},
            {"$set": document},
        )

        if result.matched_count == 0:
            raise ExpenseNotFoundError(
                "The selected expense no longer exists."
            )

    # DELETE
    def delete(self, expense_id: ObjectId) -> None:
        result = self.collection.delete_one(
            {"_id": expense_id}
        )

        if result.deleted_count == 0:
            raise ExpenseNotFoundError(
                "The selected expense no longer exists."
            )

    # SUMMARY
    def summary(
        self,
        search: str = "",
        category: str = "All",
        payment_method: str = "All",
    ) -> tuple[Decimal, int]:

        expenses = self.list_expenses(
            search, category, payment_method
        )

        total = sum(
            (expense.amount for expense in expenses),
            Decimal("0.00"),
        )

        return total, len(expenses)
