---
slug: long-method
title: "Long Method Refactoring"
difficulty: beginner
estimated_time: 30min
concepts: [extract-method, single-responsibility]
prerequisites: []
---

# Long Method Refactoring

## Aufgabenstellung

Die Klasse `OrderProcessor` enthält eine sehr lange Methode `process_order()`, die zu viele Verantwortlichkeiten hat. Diese Methode ist schwer zu verstehen, zu testen und zu warten.

**Ziel**: Refactoriere die `process_order()` Methode durch Aufteilen in kleinere, fokussierte Methoden.

## Code-Smells die behoben werden sollen

1. **Long Method**: Die `process_order()` Methode ist über 50 Zeilen lang
2. **Multiple Responsibilities**: Validierung, Berechnung, Persistence und Benachrichtigung in einer Methode
3. **Poor Readability**: Verschachtelte Bedingungen und komplexe Logik

## Was zu tun ist

1. **Analysiere** die `process_order()` Methode und identifiziere logische Blöcke
2. **Extrahiere** separate Methoden für:
   - Bestellvalidierung
   - Rabattberechnung
   - Steuerberechnung
   - Bestellspeicherung
   - Benachrichtigungsversand
3. **Stelle sicher**, dass alle Tests weiterhin grün bleiben
4. **Achte auf** aussagekräftige Methodennamen und vollständige Type Hints

## Akzeptanzkriterien

- ✅ Alle bestehenden Tests laufen durch
- ✅ Die `process_order()` Methode ist maximal 15 Zeilen lang
- ✅ Jede extrahierte Methode hat eine einzige Verantwortlichkeit
- ✅ Methodennamen beschreiben klar, was die Methode tut
- ✅ Vollständige Type Hints beibehalten
- ✅ Code ist besser lesbar und verständlich

## Hinweise

- Beginne mit dem ersten logischen Block (Validierung)
- Verwende "Extract Method" Refactoring schrittweise
- Nutze Python-Features wie dataclasses und Enums
- Die Tests zeigen dir das erwartete Verhalten - ändere es nicht!
- Bei Unsicherheiten: Schaue in die `/hints/` für gestaffelte Hilfestellungen

## Tests ausführen

```bash
pytest exercises/code-smells/long-method/tests/
```

## Dateien

- `src/order_processor.py` - Klasse mit der langen Methode
- `tests/test_order_processor.py` - Tests die grün bleiben müssen