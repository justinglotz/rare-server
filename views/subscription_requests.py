import sqlite3
import json
from datetime import datetime
from models import Subscription


def get_all_subscriptions():
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
                          SELECT 
                          id,
                          follower_id,
                          author_id,
                          created_on
                          from Subscriptions
                          """)
        subscriptions = []
        rowset = db_cursor.fetchall()
        for row in rowset:
            subscription = Subscription(id=row['id'],
                                        follower_id=row['follower_id'],
                                        author_id=row['author_id'],
                                        created_on=row['created_on'])
            subscriptions.append(subscription.__dict__)

    return subscriptions


def create_subscription(subscription):
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
                      Insert into Subscriptions (follower_id, author_id, created_on) values (?, ?, ?)
                      """, (
            subscription['follower_id'],
            subscription['author_id'],
            datetime.now()
        ))
        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })
