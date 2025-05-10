
import sqlite3
import json
from models import Category


def get_all_categories():
    """Gets all categories from the database

    Args:
        None

    Returns:
        json string: JSON representation of categories
        """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT 
              id, label
            FROM Categories
            ORDER BY LOWER(label)
                          """)

        categories = []
        rowset = db_cursor.fetchall()
        for row in rowset:
            category = Category(id=row['id'],
                                label=row['label']
                                )
            categories.append(category.__dict__)

    return categories
