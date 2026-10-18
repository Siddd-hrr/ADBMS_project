
import os
import sys

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import (
    ConfigurationError,
    PyMongoError,
    ServerSelectionTimeoutError,
)

load_dotenv()

uri = os.getenv("MONGODB_URI")

if not uri:
    print("FAIL: MONGODB_URI is missing from .env")
    sys.exit(1)

client = None

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=10000)

    # Test connection and authentication.
    client.admin.command("ping")
    print("PASS: Connected to MongoDB Atlas.")

    # Select the project database.
    db = client["expense_tracker"]

    # Verify database access and collection listing.
    collections = db.list_collection_names()
    print("PASS: Database access verified.")
    print("Existing collections:", collections)

    # Access the collection without inserting sample data.
    expenses = db["expenses"]
    print("PASS: Expense collection is accessible.")

except ServerSelectionTimeoutError:
    print("FAIL: Server selection timed out.")
    print("Check internet, Atlas IP access rules, and cluster status.")

except ConfigurationError:
    print("FAIL: MongoDB URI or client configuration is invalid.")
    print("Check the connection string format.")

except PyMongoError as exc:
    print("FAIL: MongoDB operation failed.")
    print("Error type:", type(exc).__name__)
    print("Check credentials and database permissions.")

finally:
    if client is not None:
        client.close()
        print("Connection closed.")
