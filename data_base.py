import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL,
    age INTEGER,
    name TEXT,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
     id INTEGER PRIMARY KEY AUTOINCREMENT, 
     title TEXT NOT NULL,
     content TEXT,
     user_id INTEGER NOT NULL,
     FOREIGN KEY(user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()


def get_post(user_id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts WHERE user_id=?''', (user_id,))
    post = cursor.fetchall()
    conn.close()
    return post


def get_posts():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM posts ''',())
    posts = cursor.fetchall()
    conn.close()
    return posts


def make_post(title,content,user_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO posts (title,content,user_id) VALUES (?,?,?) ''', (title,content,user_id))


def get_login(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, username, password FROM users WHERE username=?
    ''', (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def get_profile(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute(''' 
    SELECT * FROM users WHERE username=?
    ''', (username,))
    profile = cursor.fetchone()
    conn.close()
    return profile


def create_user(username,password,email):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username,password,email) VALUES (?,?,?)''', (username,password,email))
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return user_id
