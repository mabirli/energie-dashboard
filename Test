import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Energie-Dashboard", layout="wide")

st.title("Energie-Dashboard für Industrie & Gewerbe")

# Sidebar mit den Modulen
st.sidebar.header("Module")
module = st.sidebar.selectbox(
    "Wähle ein Modul",
    [
        "Lastganganalyse",
        "Hochlastzeitfenster",
        "Monetärer Nutzen",
        "Nebenkostenabrechnung",
        "Rechnungsprüfung",
        "Marktdaten & Preise",
        "Nachhaltigkeitsreporting",
        "Rechnungsprüfung Strom & Gas",
        "Leistungsspitzen & Netzentgelte",
        "Energieverbrauchsmanagement"
    ]
)

st.write(f"**Aktiviertes Modul:** {module}")

# Beispielhafte Daten oder Platzhalter für jedes Modul
if module == "Lastganganalyse":
    st.info("Hier kannst du deine RLM-Daten im 15-Minuten-Takt analysieren.")
    uploaded_file = st.file_uploader("Lade deine RLM-Daten hoch", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())
        st.line_chart(data['Leistung (kW)'])

elif module == "Hochlastzeitfenster":
    st.warning("Berechne deine Teilnahme an Hochlastzeitfenstern und mögliche Einsparungen.")

elif module == "Monetärer Nutzen":
    st.success("Berechnung des finanziellen Vorteils durch Netzentgeltreduzierung.")
    leistung = st.number_input("Gib die Leistung in kW an", min_value=0)
    st.write(f"Monetärer Nutzen bei {leistung} kW Leistung: {leistung * 0.15} Euro")

elif module == "Nebenkostenabrechnung":
    st.info("Modul zur Erstellung von Nebenkostenabrechnungen für Vermieter.")

elif module == "Rechnungsprüfung":
    st.error("Automatische Validierung deiner Strom- und Gasrechnungen.")

elif module == "Marktdaten & Preise":
    st.info("Live-Preise von EPEX Spot, EEX, TTF & THE mit Preisgrenzen-Alerts.")
    # Hier kannst du API-Daten von Börsen einfügen, z.B. mit einer API-Abfrage
    # Placeholder-Daten für Marktpreise
    epex_price = np.random.rand() * 100  # Platzhalter für EPEX Spot
    eex_price = np.random.rand() * 100   # Platzhalter für EEX
    st.write(f"EPEX Spot Preis: {epex_price:.2f} €/MWh")
    st.write(f"EEX Preis: {eex_price:.2f} €/MWh")
    st.line_chart([epex_price, eex_price])

elif module == "Nachhaltigkeitsreporting":
    st.success("Erstelle ESG-konforme Berichte und Carbon Footprint Auswertungen.")

elif module == "Rechnungsprüfung Strom & Gas":
    st.subheader("Strom- und Gasrechnungsprüfung")
    # Platzhalter für die Rechnungsprüfung
    rechnung = st.number_input("Gib den Rechnungsbetrag ein", min_value=0)
    st.write(f"Prüfung der Rechnung für {rechnung} Euro")

elif module == "Leistungsspitzen & Netzentgelte":
    st.subheader("Leistungsspitzen und Netzentgelte")
    st.info("Berechnung der Leistungsspitzen und Reduzierung der Konzessionsabgabe.")
    leistungsspitze = st.number_input("Leistungsspitze in kW", min_value=0)
    st.write(f"Reduzierung der Konzessionsabgabe bei {leistungsspitze} kW: {leistungsspitze * 0.1} Euro")

elif module == "Energieverbrauchsmanagement":
    st.subheader("Energieverbrauchsmanagement")
    st.info("Verwalte alle Energieverbrauchsdaten und Rechnungen.")
    uploaded_file = st.file_uploader("Lade deine Energieverbrauchsdaten hoch", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())
        st.line_chart(data['Verbrauch'])
