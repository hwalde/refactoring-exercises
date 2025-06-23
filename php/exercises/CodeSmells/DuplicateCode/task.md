# Duplicate Code Refactoring

## Aufgabenstellung

Du arbeitest an einem Reporting-System für ein Unternehmen. Die `ReportGenerator` Klasse erstellt verschiedene Berichte (Verkaufsberichte, Kundenberichte, Produktberichte) für das Management. Über die Zeit sind die Methoden zur Berichtserstellung gewachsen und enthalten nun viel doppelten Code. Verschiedene Berichtstypen verwenden ähnliche Logik für Datenformatierung, Headerzeilen, Footerberechnung und Export-Funktionalität.

## Problem(e)

Die `ReportGenerator` Klasse leidet unter **Duplicate Code** - einem Code Smell, bei dem dieselbe oder sehr ähnliche Logik an mehreren Stellen implementiert ist:

1. **Identischer Code**: Exakt gleiche Code-Blöcke in verschiedenen Berichtsmethoden (z.B. Header-Formatierung)
2. **Ähnliche Algorithmen**: Ähnliche Berechnungslogik mit kleinen Variationen (z.B. verschiedene Summierungen)
3. **Verwandte Funktionalität**: Ähnliche Schritte mit unterschiedlichen Daten (z.B. Export in verschiedene Formate)

Diese Duplikation führt zu:
- **Wartbarkeitsproblemen**: Änderungen müssen mehrfach gemacht werden
- **Fehleranfälligkeit**: Bugs müssen an mehreren Stellen gefixt werden  
- **Inkonsistenzen**: Verschiedene Stellen entwickeln sich unterschiedlich
- **Aufgeblähtem Code**: Unnötig viel Code für ähnliche Funktionalität

## Was zu tun ist

1. **Analysiere** die `ReportGenerator` Klasse und identifiziere alle Arten von doppeltem Code
2. **Kategorisiere** die gefundenen Duplikationen:
   - Exakt identischer Code → **Extract Method** verwenden
   - Ähnliche Algorithmen mit Variationen → **Extract Method** mit Parametern oder **Template Method** verwenden
   - Verwandte Funktionalität → **Extract Class** für gemeinsame Abstraktion erwägen
3. **Wende die Rule of Three an**: Refactoriere erst ab der dritten Wiederholung (außer bei offensichtlichen Fällen)
4. **Refactoriere schrittweise**:
   - Beginne mit dem offensichtlichsten doppelten Code
   - Extrahiere gemeinsame Methoden mit aussagekräftigen Namen
   - Parametrisiere Unterschiede, anstatt Code zu duplizieren
   - Erstelle bei Bedarf Helper-Klassen für komplexere gemeinsame Logik
5. **Stelle sicher**, dass alle Tests weiterhin grün bleiben
6. **Vermeide Überabstraktion**: Nicht jede Ähnlichkeit rechtfertigt eine gemeinsame Abstraktion

## Akzeptanzkriterien

- [ ] Alle bestehenden Tests laufen durch
- [ ] Identischer Code wurde durch **Extract Method** eliminiert
- [ ] Ähnliche Algorithmen wurden sinnvoll abstrahiert (Method/Template Method)
- [ ] Keine Logik-Duplikation zwischen verschiedenen Berichtsmethoden
- [ ] Extrahierte Methoden haben aussagekräftige Namen
- [ ] Parameter werden sinnvoll verwendet, um Variationen abzudecken
- [ ] Code ist besser strukturiert und wartbarer
- [ ] Keine Überabstraktion - gemeinsame Abstraktionen sind gerechtfertigt

## Hinweise

- **Beginne klein**: Starte mit dem offensichtlichsten doppelten Code
- **Rule of Three beachten**: Refactoriere ab dem dritten Auftreten
- **Teste nach jedem Schritt**: Stelle sicher, dass die Tests grün bleiben
- **Aussagekräftige Namen**: Extrahierte Methoden sollen klar beschreiben, was sie tun
- **Parametrisierung**: Nutze Parameter für Variationen, anstatt Code zu duplizieren
- **Template Method Pattern**: Für ähnliche Algorithmen mit verschiedenen Schritten
- **Extract Class**: Wenn gemeinsame Funktionalität komplex wird
- **Bei Unsicherheiten**: Schaue in die `hints/` für gestaffelte Hilfestellungen

## Tests ausführen

Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/CodeSmells/DuplicateCode/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\CodeSmells\DuplicateCode\
```

## Dateien

Die folgenden Dateien sollen bearbeitet werden:
- `ReportGenerator.php` - Die Hauptklasse mit dem Duplicate Code Problem
- `ReportGeneratorTest.php` - Tests bleiben unverändert und müssen weiterhin grün sein