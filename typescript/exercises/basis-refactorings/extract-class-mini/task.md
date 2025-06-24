# Extract Class Mini: MapMarker Koordinaten-Extraktion

## Aufgabenstellung
Das Team für Kartendienste hat eine `MapMarker` Klasse entwickelt, die zu viele Verantwortlichkeiten übernommen hat. Die Klasse verwaltet sowohl Marker-spezifische Eigenschaften als auch Koordinaten-Logik. Deine Aufgabe ist es, die Koordinaten-bezogene Funktionalität in eine separate `Coordinate` Klasse zu extrahieren.

## Problem(e)
Die `MapMarker` Klasse leidet unter **God Object**-Problemen:
- Koordinaten-Daten (`latitude`, `longitude`, `altitude`) sind direkt in der Marker-Klasse gespeichert
- Koordinaten-spezifische Methoden wie `moveTo()` und `distanceTo()` gehören logisch nicht zu einem Marker
- Die Klasse violiert das Single Responsibility Principle
- Code würde dupliziert werden, wenn andere Klassen ebenfalls Koordinaten benötigen

## Was zu tun ist
1. **Erstelle eine neue `Coordinate` Klasse** mit den Feldern `latitude`, `longitude`, `altitude`
2. **Verschiebe die Koordinaten-Methoden** `moveTo()` und `distanceTo()` in die `Coordinate` Klasse
3. **Refactoriere `MapMarker`** um ein `Coordinate` Objekt zu verwenden statt direkter Koordinaten-Felder
4. **Passe den Konstruktor an** um eine `Coordinate` Instanz zu akzeptieren oder zu erstellen
5. **Stelle sicher**, dass alle Tests weiterhin grün bleiben

## Akzeptanzkriterien
- [ ] Neue `Coordinate` Klasse mit `latitude`, `longitude`, `altitude` erstellt
- [ ] Methoden `moveTo()` und `distanceTo()` in `Coordinate` Klasse verschoben
- [ ] `MapMarker` verwendet `Coordinate` Objekt statt direkter Koordinaten-Felder
- [ ] Konstruktor von `MapMarker` angepasst
- [ ] Alle bestehenden Tests laufen durch
- [ ] Code folgt Single Responsibility Principle
- [ ] TypeScript strict mode konform
- [ ] Vollständige Interface-Definitionen ohne `any` Types

## Hinweise
- Beginne mit der Erstellung der `Coordinate` Klasse
- Verwende "Extract Class" Refactoring schrittweise
- Die `Coordinate` Klasse sollte unveränderlich (immutable) sein
- Nutze `readonly` Properties für Unveränderlichkeit
- Verwende explizite Return-Types für alle Methoden
- Teste nach jedem Schritt, dass die Funktionalität erhalten bleibt

## Tests ausführen
Vom typescript-Verzeichnis ausgehend:
```bash
npm test -- --testPathPattern="basis-refactorings/extract-class-mini"
```

## Dateien
- `src/MapMarker.ts` - Die zu refaktorierende Hauptklasse
- `tests/MapMarker.test.ts` - Tests, die das erwartete Verhalten definieren