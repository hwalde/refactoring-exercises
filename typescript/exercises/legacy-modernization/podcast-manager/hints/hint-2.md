# Hint 2: Schrittweise Refaktorierung und TypeScript-Klassen-Extraktion

## Was zu tun ist
Jetzt wo du die Probleme identifiziert hast, beginne mit der schrittweisen Refaktorierung. Arbeite iterativ und stelle sicher, dass die Tests nach jedem Schritt weiter funktionieren.

**Extrahiere separate Klassen für verschiedene Verantwortlichkeiten:**
- Welche Klasse könnte für das Parsen von RSS-Feeds zuständig sein?
- Was wäre eine sinnvolle Abstraktion für Podcast- und Episode-Daten?
- Wie könnte eine Repository-Klasse für das Speichern/Laden von Daten aussehen?
- Welche Logik gehört in einen Service für Downloads?
- Wie würdest du die CLI-Befehle von der Geschäftslogik trennen?

## TypeScript-spezifische Refaktorierung-Strategie
- **Define Interfaces First**: Beginne mit klaren Interface-Definitionen für alle Datenstrukturen
- **Replace Any Types**: Ersetze alle `any` mit spezifischen Types
- **Extract Type Unions**: Erstelle Union Types für begrenzte Wertebereiche
- **Add Type Guards**: Implementiere Type Guards für Runtime-Validierung
- **Use Readonly Properties**: Mache unveränderliche Daten readonly
- **Extract Method**: Teile lange Methoden in kleinere, typ-sichere Methoden auf

## TypeScript-Features zu nutzen
- **Interface Definitions**: Für Podcast, Episode, Config, DatabaseSchema
- **Union Types**: Für Commands (`'add' | 'list' | 'download'`), Status, Formate
- **Type Guards**: `isPodcast()`, `isValidCommand()`, `isEpisode()`
- **Generic Constraints**: Für typ-sichere Repository-Operationen
- **Custom Error Types**: Mit `extends Error` für spezifische Fehlerbehandlung
- **Branded Types**: Für ID-Unterscheidung (PodcastId, EpisodeId)

## Worauf achten
- Führe nach jedem Refaktorierung-Schritt `npm run typecheck` aus
- Ändere nur die interne Struktur, nicht das äußere Verhalten
- Verwende sprechende Namen für Interfaces und Types
- Halte die Klassen fokussiert - jede sollte nur eine Verantwortlichkeit haben
- Nutze TypeScript's Compile-Time-Checks für Robustheit
- Implementiere proper async/await-Patterns mit korrekten Promise-Types

## Beispiel-Interface-Struktur (ohne Implementation!)
```typescript
interface Podcast {
  readonly id: PodcastId;
  readonly title: string;
  readonly url: string;
  readonly tags: ReadonlyArray<string>;
}

type Command = 'add' | 'list' | 'download' | 'export' | 'tag' | 'cleanup';
type ExportFormat = 'json' | 'txt';
```

## Nächster Schritt
Überlege dir wie die verschiedenen Klassen miteinander interagieren sollen. Welche Interfaces brauchst du? Wie wird die Dependency Injection aussehen? Welche Klasse orchestriert die anderen? Denke über Error-Handling mit Custom Exception-Types nach.