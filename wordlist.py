import os
import glob
import pandas as pd
from collections import Counter
from setup_yt_channel_transcripts import kanal_ordner, csv_zielverzeichnis

# Initialisiere Counter für jeden Ordner und einen für alle Ordner zusammen
counter_gesamt = Counter()
counter_ordner = [Counter() for _ in kanal_ordner]

# Ändere die Namen der Ordner für die Spaltenbezeichnung
ordner_namen = [os.path.basename(os.path.normpath(ordner_pfad)) for ordner_pfad in kanal_ordner]

for ordner_index, ordner_pfad in enumerate(kanal_ordner):
    if not isinstance(ordner_pfad, str):
        continue
    for dateipfad in glob.glob(os.path.join(ordner_pfad, '*.txt')):
        with open(dateipfad, 'r', encoding='utf-8') as datei:
            worte = datei.read().lower().split()
            counter_ordner[ordner_index].update(worte)
            counter_gesamt.update(worte)

# Erstelle ein DataFrame aus dem gesamten Counter
df = pd.DataFrame(counter_gesamt.items(), columns=['term', 'freq_total'])

# Füge die Frequenzen aus jedem Ordner hinzu, benannt nach dem Ordner
for i, (counter, ordner_name) in enumerate(zip(counter_ordner, ordner_namen)):
    df[ordner_name] = df['term'].map(counter)

# Optional: Sortiere das DataFrame nach 'freq_total' absteigend
df.sort_values(by='freq_total', ascending=False, inplace=True)

csv_pfad = os.path.join(csv_zielverzeichnis, 'wordlist.csv')

# Speichere das DataFrame als CSV
df.to_csv(csv_pfad, index=False)
