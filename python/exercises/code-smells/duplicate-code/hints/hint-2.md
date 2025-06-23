# Hint 2: Refactoring-Strategien anwenden

## Was zu tun ist

Jetzt kannst du mit dem schrittweisen Refactoring beginnen. Arbeite dich von den einfachsten zu den komplexeren Duplikationen vor:

**Für identischen Code:**
- Identifiziere Code-Blöcke die exakt gleich sind
- Überlege welche Parameter diese Methoden brauchen würden
- Wie könntest du die kleinen Unterschiede (wie Titel) über Parameter lösen?

**Für ähnliche Algorithmen:**
- Welche Berechnungslogik siehst du in allen drei Berichten?
- Welche Werte werden berechnet? (Total, Count, Average, Min, Max)
- Wie könntest du die verschiedenen Datenfelder parametrisieren?

**Für verwandte Funktionalität:**
- Die Export-Methoden haben ähnliche Schritte - welche sind das?
- Filename-Generierung, Content-Transformation, Result-Formatierung - kann das abstrahiert werden?

## Worauf achten

- **Starte klein**: Beginne mit dem offensichtlichsten duplizierten Code
- **Namen sind wichtig**: Extrahierte Methoden sollen aussagekräftig heißen (PEP 8: snake_case)
- **Parameter überlegen**: Was muss von außen kommen, was kann fest sein?
- **Tests im Auge behalten**: Nach jedem Schritt sollen alle Tests grün bleiben
- **Nicht überabstrahieren**: Manchmal ist etwas nur zufällig ähnlich

**Python-spezifische Tipps:**
- Nutze Type Hints für alle Parameter: `def create_header(title: str) -> str:`
- Verwende Optional[T] für optionale Parameter
- Erwäge dataclasses für strukturierte Daten (wenn mehr als 3-4 Parameter)
- Private Methoden beginnen mit Unterstrich: `def _calculate_statistics(...)`

## Nächster Schritt

Beginne mit dem Header oder Footer - das ist der einfachste Fall von identischem Code. 

Frage dich:
- Welche Parameter braucht eine `_create_header()`-Methode?
- Wie kannst du den Report-Titel flexibel machen?
- Sollte das Datum ebenfalls parametrisierbar sein?

Dann arbeite dich zu den Berechnungsalgorithmen vor. Welche gemeinsame Methode könnte die ganzen `total`, `count`, `max`, `min` Berechnungen übernehmen?

**Denkansätze für Statistics-Berechnung:**
- Welches Datenfeld soll extrahiert werden? (Parameter: `value_field: str`)
- Wie könntest du die Dictionary-Zugriffe parametrisieren?
- Was ist der Return-Type? Ein Dict mit den berechneten Werten?
- Welche Edge-Cases musst du behandeln? (Leere Listen, fehlerhafte Daten)