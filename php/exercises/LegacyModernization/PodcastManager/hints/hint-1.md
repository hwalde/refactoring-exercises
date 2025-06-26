# Hint 1: Code-Smells identifizieren und Legacy-Struktur verstehen

## Was zu tun ist
Beginne mit einer gründlichen Analyse des bestehenden Codes. Identifiziere die verschiedenen Code-Smells und Probleme in der aktuellen Implementierung.

**Wichtige Fragen:**
- Welche Verantwortlichkeiten hat die `PodcastThing` Klasse alles übernommen?
- Wo siehst du duplizierte Code-Stellen?
- Welche Methoden sind zu lang und machen zu viele verschiedene Dinge?
- Wo werden externe Abhängigkeiten (File I/O, HTTP Requests) direkt verwendet?

## Code-Smells zu identifizieren
- **God Class**: Eine Klasse, die zu viele Verantwortlichkeiten hat
- **Long Method**: Methoden die zu viele verschiedene Aufgaben erledigen
- **Duplicate Code**: Gleiche oder sehr ähnliche Code-Stellen
- **Feature Envy**: Code der zu viel über andere Objekte weiß
- **Primitive Obsession**: Übergebrauch von primitiven Datentypen
- **Data Clumps**: Daten die oft zusammen auftreten aber nicht gruppiert sind

## Worauf achten
- Trenne nicht die Funktionalität - das äußere Verhalten muss identisch bleiben
- Konzentriere dich darauf WAS der Code macht, nicht WIE er es macht
- Die Tests definieren das erwartete Verhalten - sie müssen weiter laufen
- Dokumentiere dir die verschiedenen Verantwortlichkeiten die du findest

## Nächster Schritt
Sobald du die Probleme identifiziert hast, überlege dir welche logischen Gruppen von Verantwortlichkeiten du erkennen kannst. Was gehört zu "Podcast-Verwaltung", was zu "Episode-Download", was zu "Daten-Export" etc.?