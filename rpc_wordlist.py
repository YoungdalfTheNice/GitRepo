import os
import pandas as pd
from setup_yt_channel_transcripts import csv_zielverzeichnis

csv_pfad = os.path.join(csv_zielverzeichnis, 'updated_wordlist.csv')
rpc_pfad = os.path.join(csv_zielverzeichnis, 'rpc_lex.csv')
wordlist = os.path.join(csv_zielverzeichnis, 'wordlist.csv')

# Laden der CSV-Dateien
rpc_lex_df = pd.read_csv(rpc_pfad, sep=';')
wordlist_df = pd.read_csv(wordlist, sep=',')

# Erstellen eines leeren DataFrames für das Ergebnis
df = pd.DataFrame(columns=wordlist_df.columns.tolist() + ['category_code', 'dereko_frequency'])

# Durchlaufen aller Wörter in wordlist_df
for index, row in wordlist_df.iterrows():
    term = row['term']
    matches = rpc_lex_df[rpc_lex_df['term'] == term]

    if not matches.empty:
        for _, match in matches.iterrows():
            # Aktualisieren der Zeile mit den neuen Informationen
            new_row = row.copy()
            new_row['category_code'] = match['category_code']
            new_row['dereko_frequency'] = match['dereko_frequency']
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    else:
        # Wenn keine Übereinstimmung gefunden wurde, die ursprüngliche Zeile beibehalten
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)


# Speichere das DataFrame als CSV
df.to_csv(csv_pfad, index=False)
