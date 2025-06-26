# Podcast Manager Refaktorierung

## Aufgabenstellung
Ein Legacy-Podcast-Manager wurde als monolithische Klasse implementiert und zeigt typische Code-Smells einer schlecht strukturierten Anwendung. Ihre Aufgabe ist es, diesen Code zu refaktorieren und in eine saubere, wartbare Architektur zu überführen.

## Problem(e)
Der bestehende Code in `src/PodcastManager.php` weist mehrere kritische Code-Smells auf:

- **God Class**: Die `PodcastThing` Klasse übernimmt zu viele Verantwortlichkeiten
- **Long Method**: Methoden wie `doStuff()` sind zu lang und machen zu viele verschiedene Dinge
- **Duplicate Code**: Datenbankoperationen und Logging-Code sind mehrfach dupliziert
- **Feature Envy**: Direkter Zugriff auf externe APIs und File-System
- **Primitive Obsession**: Übergebrauch von Arrays und Strings statt Domain-Objekten
- **Data Clumps**: Zusammengehörige Daten werden nicht gruppiert

## Was zu tun ist
1. **Analysieren** Sie den bestehenden Code und identifizieren Sie alle Code-Smells
2. **Refaktorieren** Sie schrittweise und extrahieren Sie separate Klassen für verschiedene Verantwortlichkeiten
3. **Implementieren** Sie eine saubere Architektur mit:
   - Domain-Modellen für Podcast und Episode
   - Service-Klassen für spezifische Geschäftslogik
   - Repository für Datenzugriff
   - Dependency Injection für bessere Testbarkeit
4. **Stellen Sie sicher**, dass das äußere Verhalten identisch bleibt

## Akzeptanzkriterien
- ✅ Alle bestehenden Tests müssen weiterhin erfolgreich durchlaufen
- ✅ Code ist in logische, fokussierte Klassen aufgeteilt
- ✅ Jede Klasse folgt dem Single Responsibility Principle
- ✅ Keine Code-Duplikation mehr vorhanden
- ✅ Externe Abhängigkeiten sind gekapselt und injizierbar
- ✅ Domain-Logik ist von Infrastructure-Code getrennt
- ✅ Error-Handling ist robust und benutzerfreundlich
- ✅ Code folgt PSR-12 Standards

## Hinweise
- Arbeiten Sie iterativ - führen Sie nach jedem Refaktorierungs-Schritt die Tests aus
- Das äußere Verhalten der Anwendung darf sich nicht ändern
- Konzentrieren Sie sich auf die Struktur, nicht auf neue Features
- Nutzen Sie die Hints wenn Sie nicht weiterkommen
- Die Musterlösung zeigt eine mögliche Architektur, aber andere Ansätze sind auch valid

## Tests ausführen
Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/LegacyModernization/PodcastManager/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\LegacyModernization\PodcastManager\
```

## Dateien
- `src/PodcastManager.php` - Der zu refaktorierende Legacy-Code
- `PodcastManagerTest.php` - Black-Box-Tests die das erwartete Verhalten definieren
- `hints/` - Gestaffelte Hinweise für die Refaktorierung
- `solution/` - Eine mögliche Musterlösung

## Zusätzliche Validierung
```bash
# Static Analysis
vendor/bin/phpstan analyse exercises/LegacyModernization/PodcastManager/

# Code Style
vendor/bin/php-cs-fixer fix --dry-run --diff exercises/LegacyModernization/PodcastManager/
```