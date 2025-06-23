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
- Timestamp-Generierung, Content-Transformation, Result-Formatierung - kann das abstrahiert werden?

## TypeScript-spezifische Strategien

- **Generische Methoden**: Wie könntest du eine Methode erstellen, die mit verschiedenen Datentypen arbeitet?
- **Union Types**: Welche Parameter könnten von verschiedenen Typen sein?
- **Type Guards**: Wo brauchst du Runtime-Checks für verschiedene Datenstrukturen?
- **Function Types**: Könntest du Callback-Funktionen für unterschiedliche Formatierungen verwenden?

## Worauf achten

- **Starte klein**: Beginne mit dem offensichtlichsten duplizierten Code
- **Namen sind wichtig**: Extrahierte Methoden sollen aussagekräftig heißen
- **Parameter überlegen**: Was muss von außen kommen, was kann fest sein?
- **Tests im Auge behalten**: Nach jedem Schritt sollen alle Tests grün bleiben
- **Nicht überabstrahieren**: Manchmal ist etwas nur zufällig ähnlich
- **Type Safety**: Stelle sicher, dass alle extrahierten Methoden vollständig typisiert sind

## Nächster Schritt

Beginne mit dem Header oder Footer - das ist der einfachste Fall von identischem Code. 

Frage dich:
- Welche Parameter braucht eine `createHeader()`-Methode?
- Wie kannst du den Report-Titel flexibel machen?
- Sollte das Datum ebenfalls parametrisierbar sein?
- Welchen Return-Type hat diese Methode?

Dann arbeite dich zu den Berechnungsalgorithmen vor. Welche gemeinsame Methode könnte die ganzen `total`, `count`, `max`, `min` Berechnungen übernehmen? Wie könntest du sie generisch gestalten?