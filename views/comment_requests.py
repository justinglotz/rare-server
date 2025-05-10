import sqlite3
import json
from models import Comment


def get_comments_by_post(post_id):
    """uses one param through post_id, queries the Comments SQL dataset, 
    returns all instances of comments with matching post_id"""
    with sqlite3.connect("./db.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        com_post_cursor = conn.cursor()

        com_post_cursor.execute("""
          SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content
          FROM Comments c
          WHERE c.post_id = ?
          """, (post_id, ))

        comments = []
        comments_dataset = com_post_cursor.fetchall()

        for row in comments_dataset:
            comment = Comment(row["id"], row["author_id"],
                              row["post_id"], row["content"])
            comments.append(comment.__dict__)
    return comments


def create_comments(new_comment):
    """Creates a comment for the dataset through an SQL INSERT query, 
    returns new instace of comment"""

    with sqlite3.connect ('./db.sqlite3') as conn:
        create_c_cursor = conn.cursor()

        create_c_cursor.execute("""
        INSERT INTO Comments (author_id, post_id, content)
        VALUES (?, ?, ?)
        """, (new_comment['author_id'],new_comment['post_id'], new_comment['content'], ))

        id = create_c_cursor.lastrowid

        new_comment['id'] = id

    return new_comment

def delete_comments(id):
    """uses one param through id, deletes a comment 
    from the dataset through an SQL DELETE FROM query, 
    returns new instace of comment"""
    with sqlite3.connect('./db.sqlite3') as conn:

        delete_c_cursor = conn.cursor()

        delete_c_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))
