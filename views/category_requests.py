
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


def create_category(category):
    """Adds a category to the database when they register

    Args:
        category (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created category
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Categories (label) values (?)
        """, (
            category['label'],
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })


def delete_category(id):
    """Deletes a category from the database

    Args:
        id (integer): The integer representing the id of a specific category

    Returns:
        None
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Categories
        WHERE id = ?
        """, (id, ))
