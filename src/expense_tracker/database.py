
"""MongoDB Atlas connection management."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

load_dotenv()

DATABASE_NAME = "expense_tracker"
COLLECTION_NAME = "expenses"


class DatabaseConnectionError(RuntimeError):
    """Raised when MongoDB cannot be reached."""


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    uri = os.getenv("MONGODB_URI")

    if not uri or "<username>" in uri or "<cluster-host>" in uri:
        raise DatabaseConnectionError(
            "Please configure MONGODB_URI in your .env file."
        )

    client = MongoClient(uri, serverSelectionTimeoutMS=10000)

    try:
        client.admin.command("ping")
    except PyMongoError as exc:
        client.close()
        raise DatabaseConnectionError(
            "MongoDB connection failed. Check your URI, credentials, "
            "internet connection, and Atlas IP access settings."
        ) from exc

    return client


def get_expenses_collection() -> Collection:
    return get_client()[DATABASE_NAME][COLLECTION_NAME]


def close_connection() -> None:
    if get_client.cache_info().currsize:
        get_client().close()
        get_client.cache_clear()
