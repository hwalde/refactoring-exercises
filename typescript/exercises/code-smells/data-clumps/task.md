---
slug: data-clumps
title: "Data Clumps refactorieren"
difficulty: advanced
estimated_time: 45min
concepts: [data-clumps, parameter-object, value-objects, tell-dont-ask]
prerequisites: []
---

# Data Clumps refactorieren

## Aufgabenstellung

Du findest in dieser Aufgabe eine EventManager-Klasse, die für die Planung und Verwaltung von Veranstaltungen zuständig ist. Der Code funktioniert korrekt, leidet aber unter einem verbreiteten Code Smell: **Data Clumps**.

Data Clumps entstehen, wenn dieselben Gruppen von Parametern oder Daten immer wieder zusammen auftreten. Anstatt sie als separate Parameter zu behandeln, sollten sie in sinnvolle Objekte gekapselt werden.

## Code-Smells identifizieren

Analysiere den Code und identifiziere:

1. **Wiederkehrende Parameter-Gruppen**: Welche Parameter tauchen immer wieder zusammen auf?
2. **Fehlende Kapselung**: Welche Daten gehören logisch zusammen, sind aber nicht gruppiert?
3. **Validierung**: Wo wird dieselbe Validierung mehrfach durchgeführt?
4. **Logik-Verteilung**: Welche Logik gehört zu den Daten und sollte mit ihnen gekapselt werden?

## Was zu tun ist

1. **Identifiziere die Data Clumps**: Finde wiederkehrende Parameter-Gruppen
2. **Erstelle Parameter Objects**: Kapsele verwandte Daten in eigene Klassen
3. **Implementiere Validierung**: Verlagere Validierung in die neuen Klassen
4. **Nutze Tell-Don't-Ask**: Verschiebe Verhalten zu den Daten
5. **Refactoriere die Methodensignaturen**: Vereinfache durch Parameter Objects
6. **Stelle Unveränderlichkeit sicher**: Mache die neuen Objekte immutable

## Akzeptanzkriterien

- [ ] Alle wiederkehrenden Parameter-Gruppen sind in Parameter Objects gekapselt
- [ ] Die neuen Klassen enthalten die relevante Validierung
- [ ] Methodensignaturen sind durch Parameter Objects vereinfacht
- [ ] Alle Parameter Objects sind unveränderlich (immutable)
- [ ] Das Tell-Don't-Ask Prinzip wird angewendet
- [ ] Alle Tests bleiben grün

## Hinweise

- **Kandidaten für Parameter Objects**: Datum/Zeit-Kombinationen, Adressdaten, Koordinaten, Konfigurationsparameter
- **Unveränderlichkeit**: Verwende readonly Properties und keine Setter
- **Validierung**: Validiere die Daten bei der Objekterstellung
- **Verhalten**: Füge Methoden hinzu, die mit den Daten arbeiten
- **Schrittweise Refactoring**: Beginne mit einem Parameter Object und refactoriere schrittweise

## Tests ausführen

```bash
# TypeScript (vom refactoring-exercises/ Ordner)
cd typescript && npm test -- --testPathPattern="data-clumps"

# Zusätzliche Code-Qualitätsprüfungen
cd typescript && npm run lint
cd typescript && npm run format:check
cd typescript && npm run typecheck
```

## Dateien

- `src/EventManager.ts` - Die Hauptklasse mit Data Clumps
- `tests/EventManager.test.ts` - Tests die grün bleiben müssen