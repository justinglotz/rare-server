import sqlite3
import json
from models import Posts

def get_all_posts():
    """Fetch all posts from the database."""
    with sqlite3.connect("./loaddata.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content,
            a.approved
        FROM Posts a
        """)

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate through dataset to build Post instances
        for row in dataset:
            post = Posts(row['id'], row['user_id'], row['category_id'], row['title'], row['publication_date'], row['image_url'], row['content'], row['approved'])
            posts.append(post.__dict__)  # Append the dictionary of the Post instance

    return posts



def get_single_post(id):
    """Fetch a single post from the database by its ID."""
    with sqlite3.connect("./loaddata.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.user_id,
            category_id,
            a.title,
            a.publication_date,
            a.image_url,
            a.content,
            a.approved
        FROM Posts a
        WHERE a.id = ?
        """, (id,))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create Post instance from the data
        if data:
            posts = Posts(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date'], data['image_url'], data['content'], data['approved'])
            return posts.__dict__  # Return the post dictionary representation
        else:
            return None  # If no post was found
