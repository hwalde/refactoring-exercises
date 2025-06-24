# Hint 1: Problem erkennen und analysieren

## Was zu tun ist

Bevor du mit dem Refactoring beginnst, musst du das Problem genau verstehen:

1. **Durchgehe die `CustomerService` Klasse systematisch** - Welche verschiedenen Verantwortlichkeiten erkennst du?
2. **Identifiziere die Änderungsgründe** - Aus welchen verschiedenen Gründen müsste diese Klasse in der Zukunft geändert werden?
3. **Gruppiere zusammengehörige Methoden** - Welche Methoden arbeiten mit ähnlichen Daten oder erfüllen verwandte Aufgaben?

## Leitfragen zum Nachdenken

- **Authentifizierung**: Welche Methoden beschäftigen sich mit Login, Passwörtern und Account-Sicherheit?
- **Kontaktdaten**: Welche Methoden verwalten persönliche Informationen und Adressen?
- **Marketing**: Welche Methoden behandeln Marketing-Präferenzen und Kampagnen?
- **Bestellungen**: Welche Methoden beschäftigen sich mit Käufen und Kaufhistorie?

## Worauf achten

- **Datengruppen**: Welche privaten Properties (Map-Strukturen) gehören thematisch zusammen?
- **Methodenabhängigkeiten**: Welche Methoden rufen sich gegenseitig auf?
- **Business Rules**: Welche Validierungen und Geschäftsregeln gehören zu welchem Bereich?
- **Single Responsibility Principle**: Was würde passieren, wenn sich Marketing-Requirements ändern? Müsste die ganze Klasse angefasst werden?

## TypeScript-spezifische Überlegungen

- **Interface-Gruppierung**: Welche Interfaces gehören zu welchem Concern (z.B. `MarketingPreferences`, `Address`, `Order`)?
- **Type-Sicherheit**: Wie kannst du Union Types nutzen, um verschiedene Status-Bereiche klar zu trennen?
- **Map-Verwaltung**: Welche `Map<number, T>` Strukturen gehören zu welchem Service?

## Nächster Schritt

Erstelle eine Liste oder Mindmap mit den verschiedenen Verantwortlichkeiten. Notiere dir:
- Welche Concerns (Bereiche) du identifiziert hast
- Welche Methoden zu welchem Concern gehören
- Welche Datenstrukturen (Maps, Interfaces) von welchen Methoden verwendet werden
- Welche Interfaces und Types zu welchem Service gehören sollten

Diese Analyse ist die Grundlage für die systematische Extraktion der Services im nächsten Schritt.