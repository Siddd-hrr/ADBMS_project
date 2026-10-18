
"""Validation functions for expense form inputs."""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation

CATEGORIES = [
    "Food & Dining",
    "Transport",
    "Education",
    "Shopping",
    "Bills",
    "Healthcare",
    "Other",
]

PAYMENT_METHODS = [
    "Cash",
    "UPI",
    "Card",
    "Bank Transfer",
]


class ValidationError(ValueError):
    """Raised when an input value is invalid."""


def validate_title(value: str) -> str:
    title = value.strip()

    if not 2 <= len(title) <= 80:
        raise ValidationError(
            "Title must contain between 2 and 80 characters."
        )

    return title


def parse_amount(value: str) -> Decimal:
    try:
        amount = Decimal(value.strip())
    except (InvalidOperation, ValueError):
        raise ValidationError("Enter a valid amount, e.g. 250.50.")

    if not amount.is_finite() or amount <= 0:
        raise ValidationError("Amount must be greater than zero.")

    if amount.as_tuple().exponent < -2:
        raise ValidationError(
            "Amount can contain at most two decimal places."
        )

    if amount.adjusted() > 11:
        raise ValidationError("Amount is too large.")

    return amount.quantize(Decimal("0.01"))


def validate_category(value: str) -> str:
    if value not in CATEGORIES:
        raise ValidationError("Select a valid category.")

    return value


def validate_payment_method(value: str) -> str:
    if value not in PAYMENT_METHODS:
        raise ValidationError("Select a valid payment method.")

    return value


def parse_expense_date(value: str) -> date:
    value = value.strip()

    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        try:
            parsed_date = datetime.strptime(
                value, "%d/%m/%Y"
            ).date()
        except ValueError:
            raise ValidationError(
                "Enter the date as YYYY-MM-DD or DD/MM/YYYY."
            )

    if parsed_date > date.today():
        raise ValidationError("Future dates are not allowed.")

    return parsed_date


def validate_description(value: str) -> str:
    description = value.strip()

    if len(description) > 250:
        raise ValidationError(
            "Description must be 250 characters or fewer."
        )

    return description
