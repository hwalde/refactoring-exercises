# Podcast Manager Refaktorierung

## Aufgabenstellung
Ein Legacy-Podcast-Manager wurde als monolithische Klasse implementiert und zeigt typische Code-Smells einer schlecht strukturierten Anwendung. Ihre Aufgabe ist es, diesen Code zu refaktorieren und in eine saubere, wartbare Architektur zu überführen.

## Problem(e)
Der bestehende Code in `src/podcast_manager.py` weist mehrere kritische Code-Smells auf:

- **God Class**: Die `PodcastThing` Klasse übernimmt zu viele Verantwortlichkeiten
- **Long Method**: Methoden wie `do_stuff()` sind zu lang und machen zu viele verschiedene Dinge
- **Duplicate Code**: Datenbankoperationen und Logging-Code sind mehrfach dupliziert
- **Feature Envy**: Direkter Zugriff auf externe APIs und File-System
- **Primitive Obsession**: Übergebrauch von Dictionaries und Strings statt Domain-Objekten
- **Data Clumps**: Zusammengehörige Daten werden nicht gruppiert

## Was zu tun ist
1. **Analysieren** Sie den bestehenden Code und identifizieren Sie alle Code-Smells
2. **Refaktorieren** Sie schrittweise und extrahieren Sie separate Klassen für verschiedene Verantwortlichkeiten
3. **Implementieren** Sie eine saubere Architektur mit:
   - Domain-Modellen für Podcast und Episode (mit @dataclass)
   - Service-Klassen für spezifische Geschäftslogik
   - Repository für Datenzugriff
   - Dependency Injection für bessere Testbarkeit
   - Type Hints für alle Funktionen und Parameter
4. **Stellen Sie sicher**, dass das äußere Verhalten identisch bleibt

## Akzeptanzkriterien
- ✅ Alle bestehenden Tests müssen weiterhin erfolgreich durchlaufen
- ✅ Code ist in logische, fokussierte Klassen aufgeteilt
- ✅ Jede Klasse folgt dem Single Responsibility Principle
- ✅ Keine Code-Duplikation mehr vorhanden
- ✅ Externe Abhängigkeiten sind gekapselt und injizierbar
- ✅ Domain-Logik ist von Infrastructure-Code getrennt
- ✅ Error-Handling ist robust und benutzerfreundlich
- ✅ Code folgt PEP 8 Standards
- ✅ Type Hints sind vollständig und korrekt
- ✅ Docstrings für alle öffentlichen Methoden und Klassen

## Hinweise
- Arbeiten Sie iterativ - führen Sie nach jedem Refaktorierungs-Schritt die Tests aus
- Das äußere Verhalten der Anwendung darf sich nicht ändern
- Konzentrieren Sie sich auf die Struktur, nicht auf neue Features
- Nutzen Sie Python-spezifische Features wie @dataclass für Value Objects
- Verwenden Sie Type Hints für eine bessere Code-Dokumentation
- Nutzen Sie die Hints wenn Sie nicht weiterkommen
- Die Musterlösung zeigt eine mögliche Architektur, aber andere Ansätze sind auch valid

## Tests ausführen
Vom python-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
source venv/bin/activate && pytest exercises/legacy-modernization/podcast-manager/tests/ -v
```

**Unter Windows:**
```cmd
venv\Scripts\activate && pytest exercises\legacy-modernization\podcast-manager\tests\ -v
```

## Dateien
- `src/podcast_manager.py` - Der zu refaktorierende Legacy-Code
- `tests/test_podcast_manager.py` - Black-Box-Tests die das erwartete Verhalten definieren
- `hints/` - Gestaffelte Hinweise für die Refaktorierung
- `solution/` - Eine mögliche Musterlösung

## Zusätzliche Validierung
```bash
# Type Checking
mypy exercises/legacy-modernization/podcast-manager/src/

# Code Style
black --check exercises/legacy-modernization/podcast-manager/
ruff check exercises/legacy-modernization/podcast-manager/
```