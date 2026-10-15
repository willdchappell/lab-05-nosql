#!/usr/bin/env python3
"""Print a bookstore inventory report from MongoDB Atlas."""

import logging
import os
import sys

from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Status messages go to logging; the report itself is printed in main.
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

# Read Atlas credentials from the environment, the same way Lab 03 reads GITHUB_USER.
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Mix starter authors (Neil Gaiman, Terry Pratchett) with one added in Case Study 1.
AUTHOR_IDS = ["author_002", "author_003", "author_004"]


def connect_client():
    """Open a MongoClient using the Atlas URL and credentials from the environment."""
    if not all([MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, MONGODB_ATLAS_PWD]):
        raise ValueError(
            "Set MONGODB_ATLAS_URL, MONGODB_ATLAS_USER, and MONGODB_ATLAS_PWD "
            "before running this script."
        )

    # Username and password are passed separately so they are not stored in the script.
    return MongoClient(
        MONGODB_ATLAS_URL,
        username=MONGODB_ATLAS_USER,
        password=MONGODB_ATLAS_PWD,
        connectTimeoutMS=20000,
        retryWrites=True,
    )


def print_author_books(authors, books, author_ids):
    """Print each author's name and the title and year of every linked book."""
    # count_documents counts how many of the listed ids exist in the authors collection.
    author_count = authors.count_documents({"_id": {"$in": author_ids}})
    print(f"Authors: {author_count}")
    print()

    # Walk the list in order so co-authored books appear under each author.
    for author_id in author_ids:
        author = authors.find_one({"_id": author_id})
        if author is None:
            log.warning("No author document found for _id=%s", author_id)
            continue

        print(author["name"])
        # Join: books.author_ids holds this author's _id (not a hardcoded title list).
        for book in books.find({"author_ids": author["_id"]}):
            print(f"  {book['title']} ({book['published_year']})")
        print()


def main():
    """Connect to Atlas, join authors to books, and print the inventory report."""
    client = None
    try:
        client = connect_client()
        # Ping confirms the handshake succeeded before we query collections.
        client.admin.command("ping")
        log.info("Connected to MongoDB Atlas.")

        db = client.bookstore
        authors = db.authors
        books = db.books

        print_author_books(authors, books, AUTHOR_IDS)
        # Flush stdout so the report is not delayed behind logging on stderr.
        sys.stdout.flush()
    except (PyMongoError, ValueError) as exc:
        log.error("Could not complete the bookstore report: %s", exc)
        sys.exit(1)
    finally:
        # Always close the client, including after an error.
        if client is not None:
            client.close()
            log.info("Closed the MongoDB client.")


if __name__ == "__main__":
    main()
