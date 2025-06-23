# Hint 2: Parameter Objects erstellen

## Was zu tun ist

Basierend auf deinen identifizierten Data Clumps solltest du jetzt Parameter Objects erstellen:

- **Erstelle separate Klassen** für jede Parameter-Gruppe
- **Verwende dataclasses** mit frozen=True um Unveränderlichkeit zu gewährleisten
- **Verlagere die Validierung** in die __post_init__ Methoden der Parameter Objects
- **Implementiere Factory-Methoden** für bessere Lesbarkeit

## Worauf achten

- **Validierung zentralisieren**: Die Validierungslogik aus der EventManager-Klasse gehört zu den Daten
- **Tell-Don't-Ask anwenden**: Welche Operationen arbeiten mit diesen Daten und können als Methoden hinzugefügt werden?
- **Naming Convention**: Wähle beschreibende Namen die die fachliche Bedeutung widerspiegeln
- **Type Hints**: Verwende vollständige Type Hints für alle Parameter und Rückgabewerte

## Nächster Schritt

Beginne mit dem einfachsten Parameter Object (z.B. Koordinaten mit nur 2 Parametern) und arbeite dich zu komplexeren vor. 

**Überlegungen:**
- Welche Methoden könnten zu einem "Koordinaten"-Objekt gehören? (Entfernungsberechnung?)
- Welche Operationen macht man typischerweise mit Datum/Zeit-Kombinationen?
- Wie kann man Adressdaten sinnvoll kapseln und welche Funktionalität gehört dazu?
- Was sind sinnvolle Validierungsregeln für E-Mail-Adressen und Telefonnummern?