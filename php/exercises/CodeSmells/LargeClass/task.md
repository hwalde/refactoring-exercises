---
slug: large-class
title: "Large Class - UserManager refactorieren"
difficulty: advanced
estimated_time: 45min
concepts: [extract-class, single-responsibility, code-smells]
prerequisites: []
---

# Large Class - UserManager refactorieren

## Aufgabenstellung

Die `UserManager` Klasse ist mit über 300 Zeilen Code zu groß geworden und übernimmt zu viele Verantwortlichkeiten. Sie kümmert sich gleichzeitig um:

- Benutzerverwaltung (CRUD-Operationen)
- Benutzerauthentifizierung
- Benutzerautorisierung
- E-Mail-Versendung
- Logging von Benutzeraktivitäten

Diese Vermischung verschiedener Verantwortlichkeiten macht die Klasse schwer zu verstehen, zu testen und zu warten.

## Code-Smells

- **Large Class**: Die Klasse ist über 300 Zeilen lang
- **Too Many Responsibilities**: Verletzt das Single Responsibility Principle
- **God Class**: Macht zu viele verschiedene Dinge gleichzeitig

## Was zu tun ist

Zerlege die `UserManager` Klasse in mehrere, fokussierte Klassen:

1. **UserManager** (Kernklasse): Koordiniert die anderen Services, max. 100 Zeilen
2. **UserRepository**: Kümmert sich um Datenpersistierung (CRUD)
3. **AuthenticationService**: Handhabt Login/Logout/Token-Validierung
4. **AuthorizationService**: Prüft Benutzerberechtigungen
5. **EmailService**: Versendet E-Mails an Benutzer
6. **UserActivityLogger**: Protokolliert Benutzeraktivitäten

## Akzeptanzkriterien

- ✅ Alle bestehenden Tests bleiben grün
- ✅ Die refactorierte `UserManager` Klasse hat maximal 100 Zeilen
- ✅ Jede neue Klasse hat eine klar definierte Verantwortlichkeit
- ✅ Dependency Injection wird für die Services verwendet
- ✅ Type Declarations bleiben vollständig erhalten
- ✅ Public API der UserManager Klasse bleibt unverändert

## Hinweise

- Beginne mit der Extraktion einer Klasse (z.B. `EmailService`)
- Verwende Constructor Injection für die Dependencies
- Halte die bestehende Public API der `UserManager` aufrecht
- Teste nach jeder Extraktion, dass alle Tests noch grün sind
- Die neuen Services sollten als separate Klassen definiert werden

## Tests ausführen

```bash
# PHP (vom refactoring-exercises/ Ordner)
cd php && vendor/bin/phpunit exercises/CodeSmells/LargeClass/

# Code-Style prüfen
cd php && vendor/bin/php-cs-fixer fix --dry-run --diff exercises/CodeSmells/LargeClass/
```

## Dateien

- `UserManager.php` - Die zu refactorierende Klasse
- `UserManagerTest.php` - Tests die grün bleiben müssen