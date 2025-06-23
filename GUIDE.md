# Guide: Refactoring-Aufgaben erstellen

Dieser Guide erklärt, wie neue Refactoring-Aufgaben in den Projekten erstellt werden.

## ⚠️ WICHTIGER HINWEIS: Git-Befehle

**ALLE Git-Befehle in diesem Guide müssen im `refactoring-exercises/` Verzeichnis ausgeführt werden!**

Das Root-Verzeichnis des Projekts enthält ein separates Git-Repository. Stellen Sie sicher, dass Sie sich im richtigen Verzeichnis befinden:

```bash
# Korrekt - im refactoring-exercises Verzeichnis
cd /pfad/zum/projekt/refactoring-exercises
git status  # Zeigt den Status des refactoring-exercises Repos

# FALSCH - im Root-Verzeichnis
cd /pfad/zum/projekt
git status  # Zeigt den Status eines anderen Repos!
```

## Übersicht

Jede Aufgabe existiert in allen drei Sprachen (PHP, TypeScript, Python) mit identischer fachlicher Logik aber sprachspezifischen Best Practices.

## Aufgaben-Struktur

### Ordner-Layout
```
exercises/<kategorie>/<slug>/
├── task.md                 # Aufgabenbeschreibung mit YAML-Frontmatter
├── README.md              # Kurze Übersicht + Setup-Hinweise
├── src/                   # Zu refactorierender Code
│   └── <ClassName>.<ext>  # Hauptklasse mit Problem-Code
├── tests/                 # Tests (müssen grün bleiben!)
│   └── <ClassName>Test.<ext>
├── hints/                 # Gestaffelte Hinweise (optional)
│   ├── hint-1.md
│   ├── hint-2.md
│   └── hint-3.md
└── solution/              # Musterlösung (optional, für Trainer)
    ├── src/
    └── tests/
```

## Schritt-für-Schritt Anleitung

### 1. Thema der Übungsaufgabe festlegen

**Schritt 1a: USED_EXERCISE_TOPICS.md lesen**

Vor der Kategorie- und Slug-Bestimmung muss zunächst das fachliche Thema der Übungsaufgabe festgelegt werden. Lese die Datei `USED_EXERCISE_TOPICS.md`, um zu sehen, welche Themen bereits verwendet wurden.

**Schritt 1b: Thema bestimmen**

Das Thema beschreibt die fachliche Domäne der zu refactorierenden Klasse aus geschäftlicher Sicht. Beispiele für Themen:
- **UserController** - Benutzer-Verwaltung
- **OrderManager** - Bestellungsverarbeitung
- **OrderProcessor** - Bestellungsabwicklung
- **MeetingService** - Terminverwaltung
- **NewsRestController** - Nachrichten-API
- **NewsView** - Nachrichten-Anzeige
- **PaymentProcessor** - Zahlungsabwicklung
- **InventoryManager** - Lagerverwaltung
- **InvoiceGenerator** - Rechnungserstellung
- **EmailService** - E-Mail-Versendung

**WICHTIG**: Wähle ein Thema, das:
- Noch NICHT in `USED_EXERCISE_TOPICS.md` aufgeführt ist
- Realistische Geschäftslogik repräsentiert
- Für die geplante Refactoring-Aufgabe geeignet ist

**Schritt 1c: Thema in USED_EXERCISE_TOPICS.md eintragen**

Sobald das Thema gewählt wurde, muss es sofort in die `USED_EXERCISE_TOPICS.md` Datei eingetragen werden, um Dopplungen zu vermeiden. Füge das Thema in der Liste hinzu mit einem Hinweis auf die geplante Aufgabe.

**Schritt 1d: Thema-Konflikt-Behandlung**

Falls in den Exercise-Details bereits ein spezifisches Thema erwähnt wird:
- **Verfügbar**: Verwende das erwähnte Thema, wenn es noch nicht in `USED_EXERCISE_TOPICS.md` steht
- **Bereits verwendet**: Wähle ein neues, unbenutztes Thema aus der obigen Liste oder erfinde ein neues

### 2. Kategorie und Slug festlegen

**Schritt 2a: Kategorie bestimmen**

Bestimme zunächst die passende Kategorie für deine Aufgabe:

- **CodeSmells** (code-smells): Problematische Code-Patterns identifizieren und beheben
  - Beispiele: `long-method`, `feature-envy`, `data-clumps`, `large-class`
- **BasicRefactorings** (basic-refactorings): Grundlegende Refactoring-Techniken
  - Beispiele: `extract-method`, `extract-variable`, `inline-method`, `rename-method`
- **CleanCode** (clean-code): Clean Code Prinzipien anwenden
  - Beispiele: `srp-violation`, `dry-principle`, `magic-numbers`, `meaningful-names`
- **DomainDriven** (domain-driven): Domain-Driven Design Patterns
  - Beispiele: `anemic-model`, `repository-pattern`, `value-objects`, `factory-pattern`
- **LegacyModernization** (legacy-modernization): Legacy Code modernisieren
  - Beispiele: `legacy-refactoring`, `dependency-injection`, `test-introduction`

**Neue Kategorie erstellen?** Falls keine Kategorie passt, erstelle eine neue:
- **Format**: PascalCase für PHP, kebab-case für TypeScript/Python
- **Beispiel**: `PerformanceOptimization` (PHP) / `performance-optimization` (TS/Python)

**Schritt 2b: Slug festlegen**

**Format**: `kebab-case` ohne Nummern
**Beispiele**: 
- `long-method`, `feature-envy`, `data-clumps` (Code Smells)
- `extract-variable`, `inline-method` (Basic Refactorings)
- `srp-violation`, `dry-principle` (Clean Code)

### 3. Ordnerstruktur erstellen

```bash
# WICHTIG: Vom refactoring-exercises/ Hauptordner ausführen!

# PHP (PascalCase Konvention)
mkdir -p php/exercises/<PascalCaseKategorie>/<PascalCaseSlug>/{hints,solution}

# TypeScript (kebab-case Konvention)  
mkdir -p typescript/exercises/<kategorie>/<slug>/{src,tests,hints,solution}

# Python (kebab-case Konvention)
mkdir -p python/exercises/<kategorie>/<slug>/{src,tests,hints,solution}

# Beispiel für CodeSmells/Long Method:
# mkdir -p php/exercises/CodeSmells/LongMethod/{hints,solution}
# mkdir -p typescript/exercises/code-smells/long-method/{src,tests,hints,solution}
# mkdir -p python/exercises/code-smells/long-method/{src,tests,hints,solution}
```

**🐍 Python-spezifische __init__.py Files erstellen:**
```bash
# NACH der Ordnererstellung für Python immer ausführen:
touch python/exercises/<kategorie>/<slug>/src/__init__.py
touch python/exercises/<kategorie>/<slug>/tests/__init__.py

# Beispiel:
# touch python/exercises/code-smells/long-method/src/__init__.py
# touch python/exercises/code-smells/long-method/tests/__init__.py
```

**📁 Wichtige Unterschiede:**
- **PHP**: Direkte Dateien im Exercise-Ordner, PascalCase-Pfade
- **TypeScript/Python**: Separate `src/` und `tests/` Unterordner, kebab-case-Pfade

### 4. Aufgabenkonzept entwickeln und absegnen

**🚨 WICHTIG - Qualitätssicherung:**

**Schritt 4a: Konzept-Dialog**
1. **Aufgabe besprechen**: Idee, Ziel und Lerninhalt im Dialog erklären
2. **Fachliche Validierung**: Sicherstellen dass das Problem realistisch und lehrreich ist
3. **Scope definieren**: Umfang und Schwierigkeit festlegen

**Schritt 4b: Aufgabentext-Entwurf**
1. **Ersten Entwurf erstellen**: task.md mit allen Abschnitten verfassen
2. **Präsentation**: Vollständigen Text zur Begutachtung vorlegen
3. **Zustimmung einholen**: ✅ **NUR mit expliziter Zustimmung fortfahren!**
4. **Iterationen**: Bei Änderungswünschen überarbeiten und erneut präsentieren

**❌ Ohne Zustimmung des Aufgabentexts NICHT mit der Implementierung beginnen!**

### 5. task.md erstellen

**YAML-Frontmatter** (identisch in allen Sprachen):
```yaml
---
slug: your-slug-here
title: "Beschreibender Titel"
difficulty: beginner|intermediate|advanced
estimated_time: 30min
concepts: [extract-method, single-responsibility]
prerequisites: []  # Array von Slug-Namen
---
```

**Aufbau der Beschreibung**:
1. **Aufgabenstellung** - Was ist das Problem?
2. **Code-Smells** - Welche Smells sollen behoben werden?
3. **Was zu tun ist** - Konkrete Schritte
4. **Akzeptanzkriterien** - Messbare Erfolgskriterien
5. **Hinweise** - Tipps zum Vorgehen
6. **Tests ausführen** - Sprachspezifische Befehle
7. **Dateien** - Welche Dateien bearbeitet werden

**🇩🇪 WICHTIG - Sprache**: Alle Aufgabenbeschreibungen, Hinweise und Texte die Studenten lesen müssen auf Deutsch sein! Nur Quellcode, technische Fachbegriffe (wie "Long Method", "Extract Method") und Variablennamen bleiben auf Englisch.

### 6. Problem-Code erstellen

**Richtlinien**:
- **Realistisch**: Keine Toy-Examples, sondern realistische Geschäftslogik
- **Fokussiert**: Ein Hauptproblem pro Aufgabe
- **Testbar**: Vollständig durch Tests abgedeckt
- **Sprachspezifisch**: Nutze idiomatische Patterns

**PHP-Spezifika**:
- PSR-12 Code Style
- Type Declarations für alle Parameter/Returns
- `declare(strict_types=1);`
- Namespace: `RefactoringExercises\<Kategorie>\<Slug>`
- **Dateipfade**: kebab-case Slugs werden in PascalCase konvertiert (z.B. `long-method` → `LongMethod/`)
- **WICHTIG**: Kompatibilität zu PHP 8.3 (nicht höher) wegen Tool-Limitations (PHP-CS-Fixer)

**TypeScript-Spezifika**:
- Strict mode aktiviert
- Vollständige Interface-Definitionen
- Keine `any` Types
- Export/Import für Module

**Python-Spezifika**:
- Type Hints für alle Funktionen
- Dataclasses für strukturierte Daten
- PEP 8 compliant
- Docstrings für Klassen/Methoden
- **WICHTIG**: `__init__.py` Files in `src/` und `tests/` Ordnern erstellen
- **WICHTIG**: Korrekte Import-Struktur in Tests verwenden:
  ```python
  import sys
  from pathlib import Path
  
  # Add the src directory to Python path
  sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
  
  from your_module import YourClass
  ```

### 7. Tests schreiben

**Wichtige Prinzipien**:
- Tests definieren das erwartete Verhalten
- Müssen vor UND nach Refactoring grün sein
- Alle Edge-Cases abdecken
- Keine Implementation-Details testen

**Test-Kategorien**:
- **Happy Path**: Normale Anwendungsfälle
- **Edge Cases**: Grenzfälle
- **Error Cases**: Fehlerbehandlung
- **Integration**: Zusammenspiel der Komponenten

### 8. Hints erstellen

**Gestaffeltes System**:
- **hint-1.md**: Problem analysieren, Blöcke identifizieren
- **hint-2.md**: Erste Methode extrahieren
- **hint-3.md**: Weitere Refactorings, finale Struktur

**Aufbau pro Hint**:
```markdown
# Hint X: Kurzer Titel

## Was zu tun ist
Konkreter nächster Schritt

## Beispiel
```<sprache>
// Code-Beispiel der gewünschten Lösung
```

## Nächster Schritt
Was danach zu tun ist
```

### 9. README.md erstellen

**Template** (für jede Sprache anpassen):
```markdown
# <Aufgaben-Titel>

**Schwierigkeit**: <difficulty>  
**Geschätzte Zeit**: <estimated_time>  
**Konzepte**: <concepts>

## Schnellstart

1. **Tests ausführen**:
   ```bash
   # PHP (vom refactoring-exercises/ Ordner)
   cd php && vendor/bin/phpunit exercises/CodeSmells/<PascalCaseSlug>/
   
   # TypeScript (vom refactoring-exercises/ Ordner)  
   cd typescript && npm test -- --testPathPattern="<slug>"
   
   # Python (vom refactoring-exercises/ Ordner)
   cd python && source venv/bin/activate && pytest exercises/code-smells/<slug>/tests/ -v
   ```

2. **Code bearbeiten**: 
   - PHP: Dateien direkt im Exercise-Ordner
   - TypeScript/Python: Dateien in `src/` Unterordner

3. **Tests erneut ausführen** (müssen grün bleiben!)

## Ziel

<Kurze Zusammenfassung der Aufgabe>

## Hilfe

- Detaillierte Beschreibung: `task.md`
- Schrittweise Hinweise: `hints/`
```

### 10. Aufgabe testen und validieren

**WICHTIG**: Jede neue Aufgabe MUSS in allen drei Sprachen getestet werden, bevor sie als fertig gilt!

**Test-Kommandos** (vom refactoring-exercises/ Hauptordner ausführen):
```bash
# PHP - Tests und Code-Qualität prüfen
cd php && vendor/bin/phpunit exercises/CodeSmells/<PascalCaseSlug>/
cd php && vendor/bin/phpstan analyse exercises/CodeSmells/<PascalCaseSlug>/
cd php && vendor/bin/php-cs-fixer fix --dry-run --diff exercises/CodeSmells/<PascalCaseSlug>/

# TypeScript - Tests und Code-Qualität prüfen  
cd typescript && npm test -- --testPathPattern="exercises/code-smells/<slug>"
cd typescript && npm run lint
cd typescript && npm run format:check
cd typescript && npm run typecheck

# Python - Tests und Code-Qualität prüfen (mit venv)
cd python && source venv/bin/activate
cd python && pytest exercises/code-smells/<slug>/tests/ -v
cd python && black --check exercises/code-smells/<slug>/
cd python && source venv/bin/activate && ruff check exercises/code-smells/<slug>/
cd python && mypy exercises/code-smells/<slug>/src/
cd python && deactivate
```

**Qualitätssicherung - Checkliste vor Commit**:
- [ ] **Tests laufen erfolgreich in allen drei Sprachen** (OBLIGATORISCH!)
- [ ] **Aufgabe existiert in ALLEN drei Sprachen:** PHP, TypeScript UND Python (sicher ist sicher!)
- [ ] **Identische fachliche Logik** in allen drei Sprachen umgesetzt
- [ ] Code Style korrekt (alle Linter ohne Fehler)
- [ ] task.md vollständig und verständlich
- [ ] Hints führen zur Lösung
- [ ] Realistische Zeitschätzung
- [ ] Sprachspezifische Best Practices eingehalten
- [ ] Linux-Befehle zum Testen funktionieren

## Kategorien und Beispiele

### Code Smells
- `long-method` - Methoden aufteilen
- `large-class` - Klassen decomposieren
- `feature-envy` - Methoden verschieben
- `data-clumps` - Parameter-Objekte extrahieren
- `primitive-obsession` - Value Objects einführen

### Basic Refactorings
- `extract-method` - Methoden extrahieren
- `extract-variable` - Variablen extrahieren
- `inline-method` - Methoden einlinen
- `rename-method` - Methoden umbenennen
- `move-method` - Methoden verschieben

### Clean Code
- `srp-violation` - Single Responsibility Principle
- `dry-principle` - Don't Repeat Yourself
- `magic-numbers` - Konstanten extrahieren
- `long-parameter-list` - Parameter-Objekte

### Domain-Driven Design
- `anemic-model` - Domain Logic hinzufügen
- `repository-pattern` - Data Access abstrahieren
- `value-objects` - Primitive durch VOs ersetzen
- `factory-pattern` - Object Creation kapseln

## Beispiel: Long Method Aufgabe

Siehe `exercises/code-smells/long-method/` in allen drei Sprachen als Referenz-Implementierung.

**Wichtige Punkte**:
- Identische OrderProcessor-Logik in allen Sprachen
- Über 50 Zeilen in der Hauptmethode
- Mehrere logische Blöcke erkennbar
- Vollständige Test-Coverage
- Schrittweise Hints verfügbar

## 🔄 Workflow für neue Aufgaben

### 1. Vorbereitung und Setup
1. **Thema festlegen** (siehe Abschnitt 1 - USED_EXERCISE_TOPICS.md lesen und neues Thema wählen)
2. **Kategorie und Slug festlegen** (kebab-case, z.B. `long-method`)
3. **Ordnerstruktur anlegen** (siehe Abschnitt 3 - beachte Unterschiede zwischen Sprachen!)
4. **task.md mit Frontmatter erstellen** (in allen drei Sprachen identisch)

### 2. Code und Tests implementieren
5. **Problem-Code implementieren** (in allen drei Sprachen, identische Geschäftslogik)
6. **Tests schreiben** (müssen vor und nach Refactoring grün sein)
7. **README.md und Hints erstellen**

### 3. **🚨 OBLIGATORISCHE Validierung Original-Aufgaben**
8. **Alle Test-Kommandos ausführen** (siehe Abschnitt "Aufgabe testen und validieren")
9. **Code-Style prüfen** (alle Linter müssen grün sein)
**❌ Ohne erfolgreiche Tests in allen drei Sprachen ist die Aufgabe NICHT fertig!**

### 4. **Musterlösungen erstellen und testen**
1. Erstelle refactorierten Code in `solution/` Ordnern:
   - `OrderProcessorRefactored.php` (PHP)
   - `OrderProcessorRefactored.ts` (TypeScript)  
   - `order_processor_refactored.py` (Python)

2. **Automatische Test-Generierung** (empfohlen):
   ```bash
   # Generiert Solution-Tests automatisch aus Original-Tests
   ./generate_solution_tests.py
   ```
   **Vorteile:**
   - 100% identische Test-Logik (keine Duplikation)
   - Automatische Anpassung der Imports/Klassen-Namen
   - Garantiert konsistente Tests

3. **Alternative: Manuelle Test-Erstellung**
   - Kopiere Original-Test in `solution/` Ordner
   - **WICHTIG:** Test muss **exakt identisch** zum Original sein
   - Nur Import/Klassen-Namen ändern für Solution-Klasse

4. **Validierung der Setup:**
   ```bash
   # Prüft ob alle Solution-Tests vorhanden sind
   ./solution_tests_setup.sh
   ```

5. **🚨 OBLIGATORISCHE Validierung aller Musterlösungen:**
   ```bash
   # PHP - Solution-Tests ausführen
   cd php && vendor/bin/phpunit exercises/CodeSmells/<PascalCaseSlug>/solution/
   
   # TypeScript - Solution-Tests ausführen
   cd typescript && npm test -- --testPathPattern="solution"
   
   # Python - Solution-Tests ausführen 
   cd python && source venv/bin/activate && pytest exercises/code-smells/<slug>/solution/ -v
   ```
   **❌ Die Musterlösungen MÜSSEN alle Tests bestehen!**

### 5. Dokumentation vervollständigen
- README.md pro Aufgabe
- Hints erstellen
- Zeitschätzung validieren

### 6. Final Review und Abnahme
- [ ] **Vollständigkeit**: Aufgabe existiert in ALLEN drei Sprachen (PHP, TypeScript, Python)
- [ ] **Fachliche Konsistenz**: Identische Geschäftslogik in allen Sprachen
- [ ] **Original-Aufgaben**: Alle Tests grün in allen drei Sprachen
- [ ] **Musterlösungen**: Alle Tests grün in allen drei Sprachen  
- [ ] **Code-Style**: Alle Linter ohne Fehler
- [ ] **Dokumentation**: Vollständig und verständlich
- [ ] **Automatisierte Validierung**: `./solution_tests_setup.sh` erfolgreich
- [ ] **Cross-platform**: Linux-Befehle getestet
- [ ] **Ready für Commit**: Alle Kriterien erfüllt

### 7. Git Commit und Push

⚠️ **WICHTIG**: Alle folgenden Git-Befehle müssen im `refactoring-exercises/` Verzeichnis ausgeführt werden!

```bash
# WICHTIG: Zuerst ins richtige Verzeichnis wechseln!
cd /pfad/zum/projekt/refactoring-exercises

# 1. Sicherstellen dass main branch aktiv ist
git branch --show-current  # Sollte "main" anzeigen
git checkout main          # Falls nötig

# 2. Alle neuen Dateien hinzufügen (Solutions werden automatisch ignoriert)
git add .

# 3. Commit mit standardisierter Message
git commit -m "Added exercise <slug>"
# Beispiel: git commit -m "Added exercise long-method"

# 4. Zum Remote Repository pushen
git push origin main
```

**✅ Fertig!** Die neue Aufgabe ist jetzt verfügbar für alle Teilnehmer.

### Automatisierte Validierung

```bash
# 1. Musterlösungen erstellen und Tests generieren
./generate_solution_tests.py

# 2. Alle Solution-Tests validieren
./solution_tests_setup.sh

# 3. Alle Tests ausführen (Original + Solutions)
cd php && vendor/bin/phpunit exercises/
cd typescript && npm test
cd python && source venv/bin/activate && pytest exercises/ -v && deactivate
```

## Häufige Fehler vermeiden

1. **Tests zu spezifisch**: Testen Sie Verhalten, nicht Implementation
2. **Unrealistische Beispiele**: Verwenden Sie echte Geschäftslogik
3. **Zu viele Probleme**: Ein Hauptproblem pro Aufgabe
4. **Inkonsistente Sprachen**: Fachliche Logik muss identisch sein
5. **Schlechte Zeitschätzung**: Testen Sie mit echten Teilnehmern

## Review-Prozess

1. **Selbst-Review**: Checkliste durchgehen
2. **Peer-Review**: Von anderem Entwickler prüfen lassen
3. **Pilot-Test**: Mit echten Teilnehmern testen
4. **Iteration**: Basierend auf Feedback verbessern

## Versionierung

- Aufgaben in separatem Git-Repository verwalten
- Tags für Release-Versionen
- Changelog für wichtige Änderungen
- Backwards-Kompatibilität beachten