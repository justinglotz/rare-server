import sqlite3
import json
from datetime import datetime
from models import User


def login_user(user):
    """Checks for the user in the database

    Args:
        user (dict): Contains the username and password of the user trying to login

    Returns:
        json string: If the user was found will return valid boolean of True and the user's id as the token
                     If the user was not found will return valid boolean False
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            select id, username
            from Users
            where username = ?
            and password = ?
        """, (user['username'], user['password']))

        user_from_db = db_cursor.fetchone()

        if user_from_db is not None:
            response = {
                'valid': True,
                'token': user_from_db['id']
            }
        else:
            response = {
                'valid': False
            }

        return json.dumps(response)


def get_all_users():
    """Gets all users from the database

    Args:
        None

    Returns:
        json string: JSON representation of users
        """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
            SELECT 
                first_name, last_name, email, username
            FROM Users
            ORDER BY LOWER(username)
                          """)

        users = []
        rowset = db_cursor.fetchall()
        for row in rowset:
            user = User(first_name=row['first_name'],
                        last_name=row['last_name'],
                        email=row['email'],
                        username=row['username'])
            users.append(user.all_users())

    return users


def get_single_user(id):
    """Gets a single user from the database

    Args:
        id (int): the user id for the user being referenced, should be unique per user
    """
    with sqlite3.connect("./db.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            u.first_name,
            u.last_name,
            u.profile_image_url,
            u.username,
            u.created_on,
            u.bio
        FROM Users u 
        WHERE u.id = ?
        """, (id, ))

    row = db_cursor.fetchone()

    user = User(
        first_name=row['first_name'], last_name=row['last_name'], profile_image_url=row[
            'profile_image_url'], username=row['username'], created_on=row['created_on'], bio=row['bio']
    )

    return user.single_user()


def create_user(user):
    """Adds a user to the database when they register

    Args:
        user (dictionary): The dictionary passed to the register post request

    Returns:
        json string: Contains the token of the newly created user
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert into Users (first_name, last_name, username, email, password, bio, created_on, active) values (?, ?, ?, ?, ?, ?, ?, 1)
        """, (
            user['first_name'],
            user['last_name'],
            user['username'],
            user['email'],
            user['password'],
            user['bio'],
            datetime.now()
        ))

        id = db_cursor.lastrowid

        return json.dumps({
            'token': id,
            'valid': True
        })


def delete_user(id):
    """Deletes a user from the database

    Args:
        id (integer): The integer representing the id of a specific user

    Returns:
        None
    """
    with sqlite3.connect('./db.sqlite3') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Users
        WHERE id = ?
        """, (id, ))
