import pandas as pd
import os
from setup_yt_channel_transcripts import csv_zielverzeichnis

## Gewichtung nach DeReKo-Grundwortfrequenz

def kumulierte_prozentuale_anteile_berechnen(csv_path):
    df = pd.read_csv(csv_path)
    
    # Identifizierung der Indexposition von 'category_code', um relevante Spalten zu bestimmen
    end_index = df.columns.get_loc('category_code')
    relevante_spalten = df.columns[1:end_index]  # 'term' wird übersprungen, da es der erste Eintrag ist
    
    print(f"Relevante Spalten: {relevante_spalten}")
    
    ergebnisse = pd.DataFrame()
    
    for spalte in relevante_spalten:
        df[spalte] = pd.to_numeric(df[spalte], errors='coerce')  # Konvertierung in numerische Werte
        kumulierte_werte = df.groupby('category_code')[spalte].sum()
        gesamtwert = kumulierte_werte.sum()
        
        if gesamtwert == 0:
            print(f"Gesamtwert in Spalte {spalte} ist 0. Überspringe Berechnung.")
            continue
        
        prozentuale_anteile = (kumulierte_werte / gesamtwert) * 100
        ergebnisse[spalte + '_prozent'] = prozentuale_anteile
    
    if ergebnisse.empty:
        print("Keine Ergebnisse berechnet.")
    else:
        print("Ergebnisse berechnet.")
    
    return ergebnisse

csv_path = os.path.join(csv_zielverzeichnis, 'wordlist_cleaned.csv')
ergebnisse = kumulierte_prozentuale_anteile_berechnen(csv_path)
if not ergebnisse.empty:
    ergebnisse.to_csv(os.path.join(csv_zielverzeichnis, 'ergebnisse_prozent.csv'))
    print("Ergebnisse gespeichert.")
else:
    print("Keine Ergebnisse zum Speichern.")
