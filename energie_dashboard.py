
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
        "Datenmanagement"
    ]
)

st.write(f"**Aktiviertes Modul:** {module}")

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
    epex_price = np.random.rand() * 100
    eex_price = np.random.rand() * 100
    st.write(f"EPEX Spot Preis: {epex_price:.2f} €/MWh")
    st.write(f"EEX Preis: {eex_price:.2f} €/MWh")
    st.line_chart([epex_price, eex_price])

elif module == "Nachhaltigkeitsreporting":
    st.success("Erstelle ESG-konforme Berichte und Carbon Footprint Auswertungen.")

elif module == "Rechnungsprüfung Strom & Gas":
    st.subheader("Strom- und Gasrechnungsprüfung")
    rechnung = st.number_input("Gib den Rechnungsbetrag ein", min_value=0)
    st.write(f"Prüfung der Rechnung für {rechnung} Euro")

elif module == "Leistungsspitzen & Netzentgelte":
    st.subheader("Leistungsspitzen und Netzentgelte")
    st.info("Berechnung der Leistungsspitzen und Reduzierung der Konzessionsabgabe.")
    leistungsspitze = st.number_input("Leistungsspitze in kW", min_value=0)
    st.write(f"Reduzierung der Konzessionsabgabe bei {leistungsspitze} kW: {leistungsspitze * 0.1} Euro")

elif module == "Datenmanagement":
    st.subheader("Datenmanagement")
    st.info("Verwalte alle Energieverbrauchsdaten und Rechnungen interaktiv.")

    monate = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]

    spalten = [
        "HT kWh", "NT kWh", "Gesamtverbrauch", "Gemessene Leistung",
        "Berechnete Leistung", "Energiepreis", "Grundpreis",
        "Messpreis", "Nettokosten"
    ]

    data = pd.DataFrame(0.0, index=monate, columns=spalten)

    edited_data = st.data_editor(
        data,
        num_rows="fixed",
        use_container_width=True,
        disabled=False,
        key="verbrauchstabelle"
    )

    summe_ht = edited_data["HT kWh"].sum()
    summe_nt = edited_data["NT kWh"].sum()
    summe_gesamt = edited_data["Gesamtverbrauch"].sum()

    st.markdown("### Gesamtsummen für 2024")
    st.write(f"**Summe HT kWh:** {summe_ht:.2f}")
    st.write(f"**Summe NT kWh:** {summe_nt:.2f}")
    st.write(f"**Gesamtverbrauch:** {summe_gesamt:.2f}")
