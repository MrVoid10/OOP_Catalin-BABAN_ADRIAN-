# DB.py

import psycopg2
from dotenv import load_dotenv

load_dotenv()

link = "postgresql://DATABASE_owner:Y2echvX5QsDa@ep-summer-mud-a28zm8td.eu-central-1.aws.neon.tech/DATABASE?sslmode=require"

class User:
    def __init__(self, username, email, hashed_password):
        self.username = username
        self.email = email
        self.hashed_password = hashed_password

def conn_to_db():
    try:
        conn = psycopg2.connect(link)  # Replace with your actual connection string
        print("Connected successfully!")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def get_user_by_email(email):
    try:
        conn = conn_to_db()
        cur = conn.cursor()

        cur.execute('SELECT username, email, password FROM users WHERE email = %s;', (email,))
        user_data = cur.fetchone()

        conn.close()

        if user_data:
            return User(*user_data)
        else:
            return None

    except psycopg2.Error as e:
        print(f"Error retrieving user data: {e}")
        return None

def get_users_by_name(name):
    try:
        conn = conn_to_db()
        cur = conn.cursor()

        cur.execute('SELECT username, email, password FROM users WHERE username ILIKE %s;', (f"%{name}%",))
        users_data = cur.fetchall()

        conn.close()

        return [User(*row) for row in users_data]

    except psycopg2.Error as e:
        print(f"Error retrieving users data: {e}")
        return None

def update_user_password(email, new_password):
    try:
        conn = conn_to_db()
        cur = conn.cursor()

        cur.execute('UPDATE users SET password = %s WHERE email = %s;', (new_password, email))
        conn.commit()

        conn.close()

        print("Password updated successfully!")
        return True

    except psycopg2.Error as e:
        print(f"Error updating password: {e}")
        return False

def delete_user_by_email(email):
    try:
        conn = conn_to_db()
        cur = conn.cursor()

        cur.execute('DELETE FROM users WHERE email = %s;', (email,))
        conn.commit()

        conn.close()

        print("User deleted successfully!")
        return True

    except psycopg2.Error as e:
        print(f"Error deleting user: {e}")
        return False

def add_user(user):
    try:
        conn = psycopg2.connect(link) 
        cur = conn.cursor()

        # Execute the INSERT query
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s);',
                    (user.username, user.email, user.hashed_password))
        conn.commit()  # Commit the changes

        # Close the connection
        conn.close()

        print("User added successfully!")
        return True

    except psycopg2.Error as e:
        print(f"Error adding user: {e}")
        return False
