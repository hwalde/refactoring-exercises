# Hint 1: Den Berechnungsblock identifizieren

## Was zu tun ist

Schaue dir die `generateReport()`-Methode genau an. Du wirst feststellen, dass sie zwei verschiedene Dinge macht:

1. **Statistiken berechnen** - Zählung der aktiven Items und Prozentsatz-Berechnung
2. **Bericht formatieren** - String-Zusammenstellung für die Ausgabe

Identifiziere den Berechnungsblock, der extrahiert werden sollte:
- Wo beginnt die Berechnung?
- Welche Variablen werden für die Berechnung verwendet?
- Was wird am Ende der Berechnung produziert?

## Worauf achten

- Der Berechnungsblock arbeitet mit den `items` des Managers
- Es werden mehrere Werte berechnet: Gesamtanzahl, aktive Items, Prozentsatz
- Die Berechnung ist von der Formatierung des Berichts getrennt

## Nächster Schritt

Überlege dir, welche Parameter deine neue `calculateStatistics()`-Methode benötigt und was sie zurückgeben sollte. Welche TypeScript-Typen wären dafür geeignet?