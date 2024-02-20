import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from setup_yt_channel_transcripts import csv_zielverzeichnis

# Pfad zur CSV-Datei
csv_path = os.path.join(csv_zielverzeichnis, 'ergebnisse_prozent.csv')
df = pd.read_csv(csv_path)

st.title("Untersuchung rechtspopulistischer und verschwörungstheoretischer Inhalte auf ausgewählten YouTube-Kanälen")
st.write("\n")
st.subheader('Prozentuale Verteilung der Inhalte')
st.write("\n\n")
# Legendenbeschriftungen und deren category_codes
legend_info = {
    'SCAN': 'Scandalization (SCAN)',
    'SUSP': 'Suspicion/manipulation (SUSP)',
    'EXPO': 'Exposure/revelation (EXPO)',
    'DIST': 'Markers of distance (DIST)',
    'CONS': 'Conspiracy (CONS)',
    'ASEM': 'Antisemitism (ASEM)',
    'ELIT': 'Anti-elitism (ELIT)',
    'APOC': 'Apocalypse/downfall (APOC)',
    'PROT': 'Protest/rebellion (PROT)',
    'NAT': 'Nationalism (NAT)',
    'ISLA': 'Anti-immigration/islamophobia (ISLA)',
    'GEND': 'Anti-gender/anti-feminism (GEND)',
    'ESO': 'Esotericism (ESO)'
}

# Eine feste Farbpalette für die Kategorien definieren
farben = plt.cm.tab20(range(len(legend_info)))

# Erstellen Sie eine Farbzuordnung basierend auf den category_codes
category_colors = {code: farben[i] for i, code in enumerate(legend_info.keys())}

# Erstellen der Diagramme
for spalte in df.columns:
    if spalte != 'category_code':
        label = spalte.replace('_per_freq_prozent', '').replace('_prozent', '')  # Suffixe entfernen
        st.subheader(f'Verteilung: {label}')
        
        fig, ax = plt.subplots(figsize=(10, 8))  # Größe des Plots anpassen
        
        # Daten für das Diagramm vorbereiten und sortieren
        sortierte_df = df[['category_code', spalte]].dropna().sort_values(by=spalte)
        
        # Farben für die aktuellen Kategorien zuordnen
        balken_farben = [category_colors[code] if code in category_colors else 'grey' for code in sortierte_df['category_code']]
        
        # Horizontales Balkendiagramm erstellen
        ax.barh(sortierte_df['category_code'], sortierte_df[spalte], color=balken_farben)
        
        plt.xlabel('Prozent')
        plt.tight_layout()
        
        # Angepasste Legende basierend auf den definierten Labels
        handles = [plt.Rectangle((0,0),1,1, color=category_colors[code]) for code in legend_info.keys()]
        ax.legend(handles, legend_info.values(), title="Category Codes")
        
        st.pyplot(fig)

# Pfad zur "transcript_overview.csv" Datei
csv_overview = os.path.join(csv_zielverzeichnis, 'transcripts_overview.csv')

# Laden des DataFrames
df_overview = pd.read_csv(csv_overview, delimiter=';')

# Titel der Streamlit-Seite
st.title("Übersicht über die YouTube-Kanal Transkripte")

# Anzeigen des DataFrames in der Anwendung
st.write("Hier ist eine Übersicht über die Transkripte der analysierten YouTube-Kanäle:")

# Möglichkeit zur Anzeige des gesamten DataFrames oder eines Ausschnitts
if st.checkbox('Gesamtes DataFrame anzeigen'):
    st.dataframe(df_overview)
else:
    # Anzahl der Zeilen, die angezeigt werden sollen
    rows_to_show = st.slider('Anzahl der anzuzeigenden Zeilen', min_value=5, max_value=min(50, len(df_overview)), value=10)
    st.dataframe(df_overview.head(rows_to_show))

# Optional: Anzeigen von Statistiken oder Zusammenfassungen des DataFrames
if st.checkbox('Statistiken anzeigen'):
    st.write(df_overview.describe())
