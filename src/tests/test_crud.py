
import os
from datetime import datetime, timezone
from decimal import Decimal

from dotenv import load_dotenv
from pymongo import MongoClient
from bson.decimal128 import Decimal128

load_dotenv()

uri = os.getenv("MONGODB_URI")
if not uri:
    raise RuntimeError("MONGODB_URI is missing from .env")

client = MongoClient(uri, serverSelectionTimeoutMS=10000)
collection = client["expense_tracker"]["expenses"]

test_id = None

try:
    client.admin.command("ping")

    # CREATE
    result = collection.insert_one({
        "title": "TEMP CRUD TEST",
        "amount": Decimal128(Decimal("12.50")),
        "category": "Other",
        "date": datetime.now(timezone.utc),
        "payment_method": "Cash",
        "description": "Temporary verification record",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    })
    test_id = result.inserted_id
    print("PASS: Create")

    # READ
    document = collection.find_one({"_id": test_id})
    assert document is not None
    assert document["amount"].to_decimal() == Decimal("12.50")
    print("PASS: Read")

    # UPDATE
    result = collection.update_one(
        {"_id": test_id},
        {"$set": {
            "title": "TEMP CRUD TEST UPDATED",
            "updated_at": datetime.now(timezone.utc),
        }},
    )
    assert result.matched_count == 1

    document = collection.find_one({"_id": test_id})
    assert document["title"] == "TEMP CRUD TEST UPDATED"
    print("PASS: Update")

finally:
    try:
        if test_id is not None:
            result = collection.delete_one({"_id": test_id})
            if result.deleted_count == 1:
                print("PASS: Delete (temporary record removed)")
            else:
                print("WARNING: Temporary record was not removed.")
                print("Temporary record ID:", test_id)
    finally:
        client.close()
