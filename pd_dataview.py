import os
import pandas as pd
from setup_yt_channel_transcripts import csv_zielverzeichnis 


csv = "transcripts_overview.csv"

csv_datei = os.path.join(csv_zielverzeichnis, csv)

df = pd.read_csv(csv_datei, delimiter=';')

print(df)