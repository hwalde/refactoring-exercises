# Hint 1: Code-Smells identifizieren und TypeScript-Legacy-Struktur verstehen

## Was zu tun ist
Beginne mit einer gründlichen Analyse des bestehenden TypeScript-Codes. Identifiziere die verschiedenen Code-Smells und Probleme in der aktuellen Implementierung.

**Wichtige Fragen:**
- Welche Verantwortlichkeiten hat die `PodcastThing` Klasse alles übernommen?
- Wo siehst du duplizierte Code-Stellen?
- Welche Methoden sind zu lang und machen zu viele verschiedene Dinge?
- Wo werden externe Abhängigkeiten (File I/O, HTTP Requests) direkt verwendet?
- Wo wird `any` verwendet und welche konkreten Types sollten stattdessen definiert werden?

## Code-Smells zu identifizieren
- **God Class**: Eine Klasse, die zu viele Verantwortlichkeiten hat
- **Long Method**: Methoden die zu viele verschiedene Aufgaben erledigen
- **Duplicate Code**: Gleiche oder sehr ähnliche Code-Stellen
- **Feature Envy**: Code der zu viel über andere Objekte weiß
- **Primitive Obsession**: Übergebrauch von `any` Types und primitiven Datentypen
- **Data Clumps**: Daten die oft zusammen auftreten aber nicht gruppiert sind
- **Missing Type Safety**: Fehlende TypeScript-Typisierung und Interface-Definitionen

## TypeScript-spezifische Probleme
- **Any Obsession**: Wo wird `any` verwendet statt spezifischer Types?
- **Missing Interfaces**: Welche Datenstrukturen brauchen Interface-Definitionen?
- **String Literals**: Wo könnten Union Types (`'add' | 'list' | 'download'`) verwendet werden?
- **Runtime vs Compile-time**: Wo sind Type Guards für Runtime-Validierung nötig?
- **Immutability**: Wo könnten `readonly` Properties sinnvoll sein?

## Worauf achten
- Trenne nicht die Funktionalität - das äußere Verhalten muss identisch bleiben
- Konzentriere dich darauf WAS der Code macht, nicht WIE er es macht
- Die Tests definieren das erwartete Verhalten - sie müssen weiter laufen
- Dokumentiere dir die verschiedenen Verantwortlichkeiten die du findest
- Notiere dir alle Stellen wo `any` verwendet wird und überlege konkrete Types

## Nächster Schritt
Sobald du die Probleme identifiziert hast, überlege dir welche logischen Gruppen von Verantwortlichkeiten du erkennen kannst. Was gehört zu "Podcast-Verwaltung", was zu "Episode-Download", was zu "Daten-Export" etc.? Welche TypeScript-Interfaces und Union Types würden diese Domänen am besten repräsentieren?