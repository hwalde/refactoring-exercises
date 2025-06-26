# Podcast Manager - Legacy Modernization

## Übersicht
Diese Übung behandelt die Refaktorierung einer monolithischen Legacy-Anwendung zur Podcast-Verwaltung. Die Anwendung funktioniert korrekt, ist aber schlecht strukturiert und weist typische Code-Smells auf.

## Lernziele
- Identifikation von Code-Smells in Legacy-Code
- Schrittweise Refaktorierung ohne Funktionalitätsverlust
- Anwendung von SOLID-Prinzipien
- Trennung von Domain- und Infrastructure-Code
- Dependency Injection und Testbarkeit

## Anwendungsfunktionalität
Der Podcast Manager ist eine CLI-Anwendung mit folgenden Features:
- RSS-Feeds als Podcasts hinzufügen
- Episoden herunterladen
- Podcasts und Episoden auflisten
- Daten exportieren (JSON/TXT)
- Tags zu Podcasts hinzufügen
- Dateisystem-Cleanup

Siehe `PODCAST_PRD.md` für eine detaillierte Beschreibung des erwarteten Verhaltens.

## Struktur
```
PodcastManager/
├── src/
│   └── PodcastManager.php          # Legacy-Code (zu refaktorieren)
├── hints/
│   ├── hint-1.md                   # Code-Smell Identifikation
│   ├── hint-2.md                   # Schrittweise Refaktorierung
│   └── hint-3.md                   # Finale Architektur
├── solution/
│   ├── *.php                       # Refaktorierte Klassen
│   └── *Test.php                   # Tests für Musterlösung
├── task.md                         # Aufgabenbeschreibung
├── PodcastManagerTest.php          # Black-Box Tests
└── README.md                       # Diese Datei
```

## Code-Smells im Legacy-Code
- **God Class**: `PodcastThing` macht alles
- **Long Method**: `doStuff()` und `handleThings()` sind zu lang
- **Duplicate Code**: DB-Speicherung und Logging mehrfach dupliziert
- **Feature Envy**: Direkter File-I/O und HTTP-Zugriff
- **Primitive Obsession**: Arrays statt Domain-Objekten
- **Data Clumps**: Zusammengehörige Daten nicht gruppiert

## Durchführung
1. Führen Sie die Tests aus um das erwartete Verhalten zu verstehen
2. Analysieren Sie den Code in `src/PodcastManager.php`
3. Identifizieren Sie Code-Smells und Verbesserungsmöglichkeiten
4. Refaktorieren Sie schrittweise (Tests müssen weiter laufen!)
5. Nutzen Sie die Hints bei Bedarf
6. Vergleichen Sie Ihr Ergebnis mit der Musterlösung

## Wichtige Prinzipien
- **Tests first**: Die Tests definieren das erwartete Verhalten
- **Inkrementell**: Kleine Schritte, Tests nach jedem Schritt
- **Verhalten beibehalten**: Nur interne Struktur ändern
- **Clean Code**: Sprechende Namen, fokussierte Klassen
- **SOLID**: Single Responsibility, Dependency Inversion