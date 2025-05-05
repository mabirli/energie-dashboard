
import streamlit as st
import sqlite3
from datetime import datetime

# Datenbank einrichten
conn = sqlite3.connect('fb_clone.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
''')
conn.commit()

# Sitzungs-Status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''

# Funktionen
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def create_post(user_id, content):
    cursor.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()

def get_posts():
    cursor.execute('''
    SELECT users.username, posts.content, posts.timestamp 
    FROM posts JOIN users ON posts.user_id = users.id 
    ORDER BY posts.timestamp DESC
    ''')
    return cursor.fetchall()

# Benutzeroberfläche
st.title("Mini-Facebook in Streamlit")

if not st.session_state.logged_in:
    st.subheader("Anmeldung")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")

    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Erfolgreich angemeldet!")
        else:
            st.error("Falscher Benutzername oder Passwort")

    st.subheader("Registrieren")
    reg_user = st.text_input("Neuer Benutzername")
    reg_pass = st.text_input("Neues Passwort", type="password")
    if st.button("Registrieren"):
        if register_user(reg_user, reg_pass):
            st.success("Registrierung erfolgreich! Jetzt einloggen.")
        else:
            st.error("Benutzername existiert bereits.")
else:
    st.success(f"Willkommen, {st.session_state.username}!")
    if st.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ''

    st.subheader("Erstelle einen Beitrag")
    content = st.text_area("Was machst du gerade?")
    if st.button("Posten"):
        user_id = get_user_id(st.session_state.username)
        if content.strip():
            create_post(user_id, content)
            st.success("Beitrag veröffentlicht.")
        else:
            st.warning("Bitte gib einen Text ein.")

    st.subheader("Neueste Beiträge")
    posts = get_posts()
    for user, content, time in posts:
        st.markdown(f"**{user}** schrieb am {time[:16]}:")
        st.info(content)
