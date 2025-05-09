import sqlite3
import json
from models import Comment

def get_comments_by_post (post_id):
    """uses one param through post_id, queries the Comments SQL dataset, 
    returns all instaces of comments with matching post_id"""
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
            comment = Comment(row["id"], row["author_id"],row["post_id"],row["content"])
            comments.append(comment.__dict__)
    return comments
