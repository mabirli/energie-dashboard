
import streamlit as st
import sqlite3
from datetime import datetime
from PIL import Image
import os

# Datenbankverbindung
conn = sqlite3.connect('crm_system.db', check_same_thread=False)
cursor = conn.cursor()

# Tabellen erstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    phone TEXT,
    country_code TEXT,
    profile_image TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    school_training TEXT,
    school_start TEXT,
    school_end TEXT,
    job_training TEXT,
    job_start TEXT,
    job_end TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    level TEXT,
    certificate TEXT,
    language TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    field TEXT,
    months INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS airports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    selected_airports TEXT
)
""")

conn.commit()

# Sitzung
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ''

# Hilfsfunktionen
def register_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return cursor.fetchone()

def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

# App UI
st.title("CRM & Profilverwaltung")

if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Benutzername")
    password = st.text_input("Passwort", type="password")
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Erfolgreich eingeloggt!")
        else:
            st.error("Login fehlgeschlagen.")

    st.subheader("Registrieren")
    new_user = st.text_input("Neuer Benutzername")
    new_pass = st.text_input("Neues Passwort", type="password")
    if st.button("Registrieren"):
        if register_user(new_user, new_pass):
            st.success("Registrierung erfolgreich!")
        else:
            st.error("Benutzername bereits vergeben.")
else:
    st.success(f"Eingeloggt als {st.session_state.username}")
    if st.button("Abmelden"):
        st.session_state.logged_in = False
        st.session_state.username = ''

    user_id = get_user_id(st.session_state.username)

    st.header("Profilinformationen")

    firstname = st.text_input("Vorname")
    lastname = st.text_input("Nachname")
    email = st.text_input("E-Mail")
    country_code = st.selectbox("Ländervorwahl", ["+49", "+43", "+55", "+1"], help="Wähle deine internationale Vorwahl")
    phone = st.text_input("Telefonnummer")

    uploaded_image = st.file_uploader("Profilbild hochladen", type=["jpg", "png", "jpeg"])

    image_path = ""
    if uploaded_image:
        image_path = f"images/{user_id}_{uploaded_image.name}"
        os.makedirs("images", exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(uploaded_image.getbuffer())
        st.image(Image.open(uploaded_image), width=150)

    if st.button("Profil speichern"):
        cursor.execute("""
        UPDATE users SET firstname=?, lastname=?, email=?, phone=?, country_code=?, profile_image=?
        WHERE username=?
        """, (firstname, lastname, email, phone, country_code, image_path, st.session_state.username))
        conn.commit()
        st.success("Profil gespeichert.")

    st.header("Ausbildung")

    school_training = st.text_input("Schulausbildung", help="Beispiel: Gymnasium")
    school_start = st.date_input("Beginn Schulausbildung")
    school_end = st.date_input("Ende Schulausbildung")
    job_training = st.text_input("Berufsausbildung", help="Beispiel: KFZ-Mechaniker")
    job_start = st.date_input("Beginn Berufsausbildung")
    job_end = st.date_input("Ende Berufsausbildung")

    if st.button("Ausbildung speichern"):
        cursor.execute("""
        INSERT INTO education (user_id, school_training, school_start, school_end, job_training, job_start, job_end)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, school_training, school_start, school_end, job_training, job_start, job_end))
        conn.commit()
        st.success("Ausbildung gespeichert.")

    st.header("Sprachkenntnisse")

    language_level = st.selectbox("Deutsch-Sprachniveau", ["A1", "A2", "B1", "B2", "C1", "C2"], help="Wähle dein aktuelles Deutschniveau")
    has_cert = st.checkbox("Zertifikat vorhanden?")
    cert_type = ""
    if has_cert:
        cert_type = st.selectbox("Zertifikat", ["ÖSD", "Goethe", "TELC"], help="Welches Zertifikat hast du?")
    foreign_language = st.multiselect("Weitere Sprachen", ["Englisch", "Spanisch", "Französisch", "Italienisch", "Portugiesisch"], help="Welche weiteren Sprachen sprichst du?")

    if st.button("Sprachkenntnisse speichern"):
        cursor.execute("INSERT INTO languages (user_id, level, certificate, language) VALUES (?, ?, ?, ?)",
                       (user_id, language_level, cert_type if has_cert else "kein Zertifikat", "Deutsch"))
        for lang in foreign_language:
            cursor.execute("INSERT INTO languages (user_id, level, certificate, language) VALUES (?, ?, ?, ?)",
                           (user_id, "", "", lang))
        conn.commit()
        st.success("Sprachkenntnisse gespeichert.")

    st.header("Berufserfahrung")

    field = st.selectbox("Berufsfeld", ["Bau", "IT", "Pflege", "Gastronomie", "Transport"], help="In welchem Bereich hast du gearbeitet?")
    months = st.number_input("Erfahrung in Monaten", min_value=0, step=1)

    if st.button("Erfahrung speichern"):
        cursor.execute("INSERT INTO experience (user_id, field, months) VALUES (?, ?, ?)", (user_id, field, months))
        conn.commit()
        st.success("Erfahrung gespeichert.")

    st.header("Flughafen-Auswahl")
    airport_choices = [
        "GRU – São Paulo-Guarulhos",
        "GIG – Rio de Janeiro-Galeão",
        "CNF – Belo Horizonte",
        "POA – Porto Alegre",
        "BSB – Brasília",
        "REC – Recife",
        "SSA – Salvador",
        "CWB – Curitiba"
    ]
    selected_airports = st.multiselect("Nächstgelegener Flughafen", airport_choices, help="Wähle den nächstgelegenen Flughafen in Brasilien")

    if st.button("Flughafen speichern"):
        cursor.execute("INSERT INTO airports (user_id, selected_airports) VALUES (?, ?)", (user_id, ", ".join(selected_airports)))
        conn.commit()
        st.success("Flughafen gespeichert.")
