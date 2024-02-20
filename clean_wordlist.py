import pandas as pd
import os
from setup_yt_channel_transcripts import csv_zielverzeichnis

def clean_csv(input_csv_path, output_csv_path):
    # Laden der CSV-Datei
    df = pd.read_csv(input_csv_path)
    
    # Zeige einige ursprüngliche Werte von 'dereko_frequency'
    print("Einige ursprüngliche 'dereko_frequency' Werte:")
    print(df['dereko_frequency'].head())
    print("\nStatistiken von 'dereko_frequency' vor der Filterung:")
    print(df['dereko_frequency'].describe())
    # Versuche, das Format der 'dereko_frequency' Werte zu bereinigen
    df['dereko_frequency'] = df['dereko_frequency'].str.replace(',', '.').str.extract('(\d+\.\d+|\d+)').astype(float)
    
    # Überprüfen, wie viele gültige 'dereko_frequency' Werte existieren
    valid_values_count = df['dereko_frequency'].notna().sum()
    print(f"Anzahl gültiger 'dereko_frequency' Werte: {valid_values_count}")

    # Filter- und Bereinigungslogik...
    cleaned_df = df.dropna(subset=['dereko_frequency'])
    cleaned_df = cleaned_df[cleaned_df['dereko_frequency'] <= 100000]
    
    # Speichern der bereinigten Daten in eine neue CSV-Datei
    cleaned_df.to_csv(output_csv_path, index=False)
    print(f"Bereinigte Daten wurden gespeichert unter: {output_csv_path}")

# Pfade für die Ein- und Ausgabe-CSV anpassen
output_csv_path = os.path.join(csv_zielverzeichnis, 'wordlist_cleaned.csv')
input_csv_path = os.path.join(csv_zielverzeichnis, 'updated_wordlist.csv')

# Funktion aufrufen
clean_csv(input_csv_path, output_csv_path)

