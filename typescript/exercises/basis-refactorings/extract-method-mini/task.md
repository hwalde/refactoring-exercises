# Extract Method Mini - TypeScript

## Aufgabenstellung

Du hast eine `InventoryManager`-Klasse, die einen Bericht über das Inventar generiert. Die `generateReport()`-Methode mischt dabei zwei Verantwortlichkeiten: die Berechnung der Statistiken und die Formatierung des Berichts.

## Problem(e)

- **Long Method**: Die `generateReport()`-Methode ist zu lang und macht zu viele Dinge
- **Mixed Responsibilities**: Berechnung und Formatierung sind in einer Methode vermischt
- **Schlechte Testbarkeit**: Die Berechnungslogik kann nicht isoliert getestet werden

## Was zu tun ist

Extrahiere die Berechnungslogik aus der `generateReport()`-Methode in eine separate `calculateStatistics()`-Methode:

1. **Identifiziere** den Berechnungsblock in `generateReport()`
2. **Erstelle** eine neue private Methode `calculateStatistics()`
3. **Verschiebe** die Berechnungslogik in die neue Methode
4. **Passe** die `generateReport()`-Methode an, um die neue Methode zu verwenden
5. **Stelle sicher**, dass alle Tests weiterhin erfolgreich laufen

## Akzeptanzkriterien

- ✅ Eine neue Methode `calculateStatistics()` existiert
- ✅ Die Methode berechnet korrekt die Summe und den Prozentsatz
- ✅ Die `generateReport()`-Methode verwendet die neue Methode
- ✅ Alle Tests laufen erfolgreich durch
- ✅ Das Verhalten der Klasse bleibt unverändert
- ✅ TypeScript-Code ist typsicher und verwendet keine `any`-Types

## Hinweise

- Die neue Methode sollte `private` sein, da sie nur intern verwendet wird
- Überlege dir, welche Parameter die Methode benötigt und was sie zurückgeben soll
- TypeScript ermöglicht es dir, ein Interface für den Rückgabewert zu definieren
- Nutze explizite Return-Types für bessere Typsicherheit

## Tests ausführen

Vom typescript-Verzeichnis ausgehend:
```bash
npm test -- --testPathPattern="basis-refactorings/extract-method-mini"
```

## Dateien

- `src/InventoryManager.ts` - Die Hauptklasse, die refactoriert werden soll
- `tests/InventoryManager.test.ts` - Tests (nicht ändern!)
- `hints/` - Schrittweise Hinweise zur Lösung