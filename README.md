# Youtube Webcrawler for RPC-Lex

## Beschreibung

Das Repository enthält sämtliche Programme für die Untersuchung der Verteilung von RPC-Inhalten (Right-Wing Populist Conspiracy Discourse) innerhalb ausgewählter deutschprachiger Youtube Kanäle.
Dafür werden Kanäle des RPC-Spektrums als Diskurs untersucht, indem die Untertitel der Videos zunächst vom Webcrawler heruntergeladen werden und anschließend die prozentuale Verteilung der Inhalte
mit Hilfe eines Dictionaries widergegeben werden. Dafür wurde auch eine Gewichtung des Dictionaries nach der Grundwortfrequenz (nach dem [DEREKO](https://www.ids-mannheim.de/digspra/kl/projekte/korpora/) initialisiert.
Zuletzt werden die Ergebnisse der Berechnungen in CSV Dateien gespeichert und über Streamlit visualisiert.

## Verwendete Methode und Dictionary

Das Vorgehen orientiert sich an der folgenden Studie:

[Puschmann, C., Karakurt, H., Amlinger, C., Gess, N., & Nachtwey, O. (2022). RPC-Lex: A dictionary to measure German right-wing populist conspiracy discourse online. Convergence, 28(4), 1144-1171.](https://doi.org/10.1177/13548565221109440
).

Das in der Studie verwendete Dictionary ist das [RPC-Lex](https://osf.io/s48cj/). (License: CC0 1.0 Universal)

## Anleitung

1. Zunächst sollten im Setup (setup_yt_channel_transcripts.py) die Google Developer Key (API-Key ist auf Google Cloud zu finden), sowie sämtliche Zielverzeichnisse für Transkripte, CSV-Tabellen, Pfade zum Dictionary (unter dem obigen Link herunterzuladen) und die Liste der gewünschten Kanal-IDs eingetragen werden. Die Kanal-IDs lassen sich unter den Kanaldetails -> Kanal teilen -> Kanal-ID kopieren finden.
2. Der Webcrawler (yt_crawler_channel_transcripts.py) prüft den Kanal auf Videos mit vorhandenen deutschen Untertiteln und speichert diese in einem ausgwählten Zielverzeichnis (kanal_zielverzeichnis) im txt-Format. Anschließend wird ein Übersichtsbericht "transcripts_overview.csv" in das CSV-Zielverzeichnis gespeichert.
3. In "wordlist.py" wird eine vollständige Wortliste für die jeweiligen Kanäle erzeugt und in "wordlist.csv" gespeichert.
4. In "rpc_wordlist.py" wird die Wortliste mithilfe des RPC-Lex auf die Grundwortfrequenzen und die Kategorie-Codes des Dictionaries ergänzt und in der "updated_wordlist.csv" gespeichert.
5. In "clean_wordlist.py" wird überprüft, inwieweit die Liste gültige Werte bezüglich der Grundwortfrequenzen der Wörter enthält und es werden alle Missings, sowie alle Wörter mit Grundwortfrequenz über 100.000 aus der Wordliste entfernt. Das Ergebnis wird in die Datei "wordlist_cleaned.csv" gespeichert.
6. In "rpc_percentage.py" wird schließlich die Verteilung der Inhalte (nach Category Codes) unter Berücksichtigung der Gewichtung in kulminierten Prozentwerten berechnet und in "ergebnisse_prozent.csv" gespeichert.
7. Der Launcher (rpc_lex_launcher.py) führt letztlich die "streamlit.py" aus und zeigt die erechnete Verteilung der Inhalte in Balkendiagrammen für jeden Kanal und liefert auch einige allgemeine Zahlen aus der "transcripts_overview.csv" mit.
8. "Sutbitle.py" ist ein schlichter Webcrawler um die Transkripte einzelner Videos zu erhalten. "pd_dataview.py" lässt sich nutzen, um sich die zwischenergebnisse in Pandas Dataview anzusehen.
9. Innerhalb der Projektmappe lassen sich alte Ergebnisse zur Überprüfung der Ergebnisse finden.
