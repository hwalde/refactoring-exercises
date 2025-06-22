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

Die Klasse `OrderProcessor` enthält eine sehr lange Methode `processOrder()`, die zu viele Verantwortlichkeiten hat. Diese Methode ist schwer zu verstehen, zu testen und zu warten.

**Ziel**: Refactoriere die `processOrder()` Methode durch Aufteilen in kleinere, fokussierte Methoden.

## Code-Smells die behoben werden sollen

1. **Long Method**: Die `processOrder()` Methode ist über 50 Zeilen lang
2. **Multiple Responsibilities**: Validierung, Berechnung, Persistence und Benachrichtigung in einer Methode
3. **Poor Readability**: Verschachtelte Bedingungen und komplexe Logik

## Was zu tun ist

1. **Analysiere** die `processOrder()` Methode und identifiziere logische Blöcke
2. **Extrahiere** separate Methoden für:
   - Bestellvalidierung
   - Rabattberechnung
   - Steuerberechnung
   - Bestellspeicherung
   - Benachrichtigungsversand
3. **Stelle sicher**, dass alle Tests weiterhin grün bleiben
4. **Achte auf** aussagekräftige Methodennamen und TypeScript-Typen

## Akzeptanzkriterien

- ✅ Alle bestehenden Tests laufen durch
- ✅ Die `processOrder()` Methode ist maximal 15 Zeilen lang
- ✅ Jede extrahierte Methode hat eine einzige Verantwortlichkeit
- ✅ Methodennamen beschreiben klar, was die Methode tut
- ✅ Vollständige TypeScript-Typisierung beibehalten
- ✅ Code ist besser lesbar und verständlich

## Hinweise

- Beginne mit dem ersten logischen Block (Validierung)
- Verwende "Extract Method" Refactoring schrittweise
- Nutze TypeScript-Features wie Interfaces und Union Types
- Die Tests zeigen dir das erwartete Verhalten - ändere es nicht!
- Bei Unsicherheiten: Schaue in die `/hints/` für gestaffelte Hilfestellungen

## Tests ausführen

```bash
npm test exercises/code-smells/long-method/tests/
```

## Dateien

- `src/OrderProcessor.ts` - Klasse mit der langen Methode
- `tests/OrderProcessor.test.ts` - Tests die grün bleiben müssen