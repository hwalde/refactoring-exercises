# Hint 1: Problem erkennen und kategorisieren

## Was zu tun ist

Beginne mit einer systematischen Analyse der `ReportGenerator` Klasse. Duplicate Code kommt in verschiedenen Formen vor:

- **Identischer Code**: Exakt gleiche Code-Blöcke
- **Ähnliche Algorithmen**: Gleiche Logik mit kleinen Variationen
- **Verwandte Funktionalität**: Ähnliche Schritte mit unterschiedlichen Daten

Schaue dir die drei Berichtsmethoden genau an. Welche Teile sind exakt identisch? Welche sind sehr ähnlich aber nicht identisch?

## Worauf achten

- Vergleiche die Header-Erstellung in allen drei Berichten - was ist gleich, was unterscheidet sich?
- Betrachte die Datenverarbeitungslogik - welche Berechnungen werden überall gemacht?
- Analysiere die Summary-Formatierung - welche Patterns erkennst du?
- Schaue dir die Footer-Erstellung an - gibt es Gemeinsamkeiten?
- Untersuche die Export-Methoden - welche Schritte sind ähnlich?

## Nächster Schritt

Erstelle eine Liste der gefundenen Duplikationen und gruppiere sie:
1. Was ist exakt identisch? (→ Extract Method)
2. Was ist ähnlich aber mit Variationen? (→ Extract Method mit Parametern)
3. Welche komplexeren Patterns siehst du? (→ Template Method oder Extract Class)

Denke an die "Rule of Three" - refactoriere erst wenn der Code dreimal vorkommt (außer bei offensichtlichen Fällen).