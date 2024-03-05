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

1. Zunächst 
