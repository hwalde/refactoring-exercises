# Podcast Manager Refaktorierung

## Aufgabenstellung
Ein Legacy-Podcast-Manager wurde als monolithische Klasse implementiert und zeigt typische Code-Smells einer schlecht strukturierten TypeScript-Anwendung. Ihre Aufgabe ist es, diesen Code zu refaktorieren und in eine saubere, wartbare Architektur zu überführen.

## Problem(e)
Der bestehende Code in `src/PodcastManager.ts` weist mehrere kritische Code-Smells auf:

- **God Class**: Die `PodcastThing` Klasse übernimmt zu viele Verantwortlichkeiten
- **Long Method**: Methoden wie `doStuff()` sind zu lang und machen zu viele verschiedene Dinge
- **Duplicate Code**: Datenbankoperationen und Logging-Code sind mehrfach dupliziert
- **Feature Envy**: Direkter Zugriff auf externe APIs und File-System
- **Primitive Obsession**: Übergebrauch von `any` Types und Strings statt Domain-Objekten
- **Data Clumps**: Zusammengehörige Daten werden nicht gruppiert
- **Fehlende Typisierung**: Extensive Verwendung von `any` anstatt spezifischer TypeScript-Interfaces

## Was zu tun ist
1. **Analysieren** Sie den bestehenden Code und identifizieren Sie alle Code-Smells
2. **Refaktorieren** Sie schrittweise und extrahieren Sie separate Klassen für verschiedene Verantwortlichkeiten
3. **Implementieren** Sie eine saubere TypeScript-Architektur mit:
   - Starke Typisierung mit Interfaces und Union Types
   - Domain-Modellen für Podcast und Episode
   - Service-Klassen für spezifische Geschäftslogik
   - Repository für Datenzugriff
   - Dependency Injection für bessere Testbarkeit
   - Proper Error-Handling mit Custom Exception-Types
4. **Stellen Sie sicher**, dass das äußere Verhalten identisch bleibt

## Akzeptanzkriterien
- ✅ Alle bestehenden Tests müssen weiterhin erfolgreich durchlaufen
- ✅ Code ist in logische, fokussierte Klassen aufgeteilt
- ✅ Jede Klasse folgt dem Single Responsibility Principle
- ✅ Keine Code-Duplikation mehr vorhanden
- ✅ Externe Abhängigkeiten sind gekapselt und injizierbar
- ✅ Domain-Logik ist von Infrastructure-Code getrennt
- ✅ Vollständige TypeScript-Typisierung ohne `any` Types
- ✅ Proper Union Types für begrenzte Wertebereiche (Commands, Status, etc.)
- ✅ Readonly Properties für Immutability wo sinnvoll
- ✅ Type Guards für Runtime-Validierung
- ✅ Error-Handling ist robust und benutzerfreundlich
- ✅ Code folgt modernen TypeScript-Standards

## Hinweise
- Arbeiten Sie iterativ - führen Sie nach jedem Refaktorierungs-Schritt die Tests aus
- Das äußere Verhalten der Anwendung darf sich nicht ändern
- Konzentrieren Sie sich auf die Struktur, nicht auf neue Features
- Nutzen Sie TypeScript-spezifische Features wie Interfaces, Union Types und Type Guards
- Nutzen Sie die Hints wenn Sie nicht weiterkommen
- Die Musterlösung zeigt eine mögliche Architektur, aber andere Ansätze sind auch valid

## Tests ausführen
Vom typescript-Verzeichnis ausgehend:

```bash
npm test -- --testPathPattern="legacy-modernization/podcast-manager"
```

## TypeScript-spezifische Validierungen
```bash
# Type Checking
npm run typecheck

# Linting
npm run lint

# Code Formatting
npm run format:check
```

## Dateien
- `src/PodcastManager.ts` - Der zu refaktorierende Legacy-Code
- `tests/PodcastManager.test.ts` - Strukturelle Tests die das erwartete Verhalten definieren
- `hints/` - Gestaffelte Hinweise für die Refaktorierung
- `solution/` - Eine mögliche Musterlösung

## TypeScript-Features die Sie verwenden sollten
- **Interfaces**: Für Datenstrukturen (Podcast, Episode, Config)
- **Union Types**: Für begrenzte Wertebereiche (`'add' | 'list' | 'download'` etc.)
- **Type Guards**: Für Runtime-Validierung (`isPodcast(obj)`, `isValidCommand(cmd)`)
- **Readonly Properties**: Für unveränderliche Daten
- **Branded Types**: Für ID-Unterscheidung zur Compile-Zeit (fortgeschritten)
- **Generic Constraints**: Für typ-sichere Operationen
- **Custom Error Types**: Mit extends Error für spezifische Fehlerbehandlung
- **Async/Await**: Korrekte Promise-Behandlung mit Types

## Zusätzliche Herausforderungen (Optional)
- Implementieren Sie ein Plugin-System für verschiedene Export-Formate
- Fügen Sie Retry-Logik für Netzwerk-Operationen hinzu
- Implementieren Sie Caching für RSS-Feeds
- Erstellen Sie ein Event-System für Podcast-Updates