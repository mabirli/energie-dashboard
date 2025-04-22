
import streamlit as st

st.set_page_config(page_title="Energie-Dashboard", layout="wide")

st.title("Energie-Dashboard für Industrie & Gewerbe")

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
        "Nachhaltigkeitsreporting"
    ]
)

st.write(f"**Aktiviertes Modul:** {module}")

if module == "Lastganganalyse":
    st.info("Hier kannst du deine RLM-Daten im 15-Minuten-Takt analysieren.")
    # Beispielhafte Visualisierung
    st.line_chart({"Leistung (kW)": [100, 120, 90, 140, 130, 150, 110]})
elif module == "Hochlastzeitfenster":
    st.warning("Berechne deine Teilnahme an Hochlastzeitfenstern und mögliche Einsparungen.")
elif module == "Monetärer Nutzen":
    st.success("Hier wird der finanzielle Vorteil durch Netzentgeltreduzierung & Co angezeigt.")
elif module == "Nebenkostenabrechnung":
    st.info("Modul zur Erstellung von Nebenkostenabrechnungen für Vermieter.")
elif module == "Rechnungsprüfung":
    st.error("Automatische Validierung deiner Strom- und Gasrechnungen mit Tarifen und Umlagen.")
elif module == "Marktdaten & Preise":
    st.info("Live-Preise von EPEX Spot, EEX, TTF & THE mit Preisgrenzen-Alerts.")
elif module == "Nachhaltigkeitsreporting":
    st.success("Erstelle ESG-konforme Berichte und Carbon Footprint Auswertungen.")
