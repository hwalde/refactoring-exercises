# Guide: Refactoring-Aufgaben erstellen

Dieser Guide erklärt, wie neue Refactoring-Aufgaben in den Projekten erstellt werden.

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

### 1. Slug festlegen

**Format**: `kebab-case` ohne Nummern
**Beispiele**: 
- `long-method`, `feature-envy`, `data-clumps` (Code Smells)
- `extract-variable`, `inline-method` (Basic Refactorings)
- `srp-violation`, `dry-principle` (Clean Code)

### 2. Ordnerstruktur erstellen

```bash
# Für alle drei Sprachen
mkdir -p php/exercises/code-smells/<slug>/{src,tests,hints,solution}
mkdir -p typescript/exercises/code-smells/<slug>/{src,tests,hints,solution}
mkdir -p python/exercises/code-smells/<slug>/{src,tests,hints,solution}
```

### 3. task.md erstellen

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

### 4. Problem-Code erstellen

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

### 5. Tests schreiben

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

### 6. Hints erstellen

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

### 7. README.md erstellen

**Template**:
```markdown
# <Aufgaben-Titel>

**Schwierigkeit**: <difficulty>  
**Geschätzte Zeit**: <estimated_time>  
**Konzepte**: <concepts>

## Schnellstart

1. Tests ausführen: `<test-command>`
2. Code in `src/` bearbeiten
3. Tests erneut ausführen

## Ziel

<Kurze Zusammenfassung der Aufgabe>

## Hilfe

- Detaillierte Beschreibung: `task.md`
- Schrittweise Hinweise: `hints/`
```

### 8. Aufgabe testen und validieren

**WICHTIG**: Jede neue Aufgabe MUSS in allen drei Sprachen getestet werden, bevor sie als fertig gilt!

**Test-Kommandos für Linux/macOS**:
```bash
# PHP - Tests ausführen
cd php && vendor/bin/phpunit exercises/CodeSmells/<PascalCaseSlug>/
cd php && vendor/bin/phpstan analyse
cd php && vendor/bin/php-cs-fixer fix --dry-run --diff

# TypeScript - Tests ausführen  
cd typescript && npm test exercises/code-smells/<slug>/tests/
cd typescript && npm run lint
cd typescript && npm run format:check

# Python - Tests ausführen (mit venv)
cd python && source venv/bin/activate && pytest exercises/code-smells/<slug>/tests/
cd python && source venv/bin/activate && black --check .
cd python && source venv/bin/activate && ruff check .
cd python && source venv/bin/activate && mypy exercises/code-smells/<slug>/src/
```

**Qualitätssicherung - Checkliste vor Commit**:
- [ ] **Tests laufen erfolgreich in allen drei Sprachen** (OBLIGATORISCH!)
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

## Workflow für neue Aufgaben

### 1. Aufgabe erstellen
1. Slug festlegen (kebab-case)
2. Ordnerstruktur anlegen
3. task.md mit Frontmatter erstellen
4. Code in allen drei Sprachen implementieren
5. Tests für alle Sprachen schreiben

### 2. **OBLIGATORISCH: Vollständige Validierung**
Führe alle Test-Kommandos aus dem Abschnitt "Aufgabe testen und validieren" aus.
**Ohne erfolgreiche Tests in allen drei Sprachen ist die Aufgabe NICHT fertig!**

### 3. **Musterlösungen erstellen und testen**
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

5. **Teste alle Musterlösungen:**
   ```bash
   # PHP
   cd php && vendor/bin/phpunit exercises/
   
   # TypeScript
   cd typescript && npm test
   
   # Python
   cd python && source venv/bin/activate && pytest exercises/ -v
   ```
**Die Musterlösungen MÜSSEN alle Tests bestehen!**

### 3. Dokumentation vervollständigen
- README.md pro Aufgabe
- Hints erstellen
- Zeitschätzung validieren

### 4. Final Review
- Alle Checklisten-Punkte abgehakt
- Cross-platform getestet (Linux-Befehle)
- Ready für Commit

### Automatisierte Validierung
```bash
# Alle Sprachen testen
./scripts/test-all-exercises.sh

# Spezifische Aufgabe
./scripts/test-exercise.sh <slug>
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