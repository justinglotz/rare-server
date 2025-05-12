import sqlite3
import json
from models import Posts

def get_all_posts():
    """Fetch all posts from the database."""
    with sqlite3.connect("./db.sqlite3") as conn:
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
    with sqlite3.connect("./db.sqlite3") as conn:
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


def create_post(new_post):
    """Insert a new post into the database."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (new_post['user_id'], new_post['category_id'], new_post['title'], new_post['publication_date'], new_post['image_url'], new_post['content'], new_post['approved']))

        # Get the last inserted row id (primary key)
        id = db_cursor.lastrowid

    return json.dumps({
        'taken': id,
        'valid': True
    })


def delete_post(id):
    """Delete a post from the database by its ID."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id,))


def update_post(id, updated_post):
    """Update an existing post's details in the database."""
    with sqlite3.connect("./db.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Posts
        SET
            title = ?,
            publication_date = ?,
            image_url = ?,
            content = ?,
            approved = ?
        WHERE id = ?
        """, (updated_post['title'], updated_post['publication_date'], updated_post['image_url'], updated_post['content'], updated_post['approved'], id))

        # Check if any rows were affected
        rows_affected = db_cursor.rowcount

  # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True