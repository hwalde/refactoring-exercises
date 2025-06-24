# Hint 3: Integration abschließen und Tests grün halten

## Was zu tun ist
Du hast die `Coordinate` Klasse erstellt - jetzt geht es um die saubere Integration in `MapMarker`:
- Passe den `MapMarker` Konstruktor an, um intern ein Coordinate-Objekt zu erstellen
- Refactoriere die bestehenden Methoden, um das Coordinate-Objekt zu verwenden
- Stelle sicher, dass die äußere API unverändert bleibt

## Worauf achten
- **API-Kompatibilität**: Alle bestehenden Tests müssen weiterhin grün bleiben
- **Delegation**: Getter-Methoden sollten an das Coordinate-Objekt delegieren
- **Objekt-Erstellung**: Bei `moveTo()` und `distanceTo()` temporäre Coordinate-Objekte erstellen
- **Konsistenz**: Alle Koordinaten-Zugriffe sollten über das Coordinate-Objekt laufen

## TypeScript-spezifische Überlegungen
- Nutze die Unveränderlichkeit der Coordinate-Klasse für bessere Typsicherheit
- Vermeide Type-Assertions - lass TypeScript die Typen inferieren
- Überlege, ob private Hilfsmethoden für Coordinate-Erstellung sinnvoll sind
- Stelle sicher, dass alle Return-Types explizit definiert sind

## Qualitätsprüfung
Nach der Refactorierung:
- Laufen alle Tests noch durch?
- Ist die Verantwortlichkeiten-Trennung klar erkennbar?
- Könnte die Coordinate-Klasse in anderen Kontexten wiederverwendet werden?
- Folgt der Code TypeScript-Best-Practices?

## Nächster Schritt
Führe die Tests aus und validiere, dass das Refactoring erfolgreich war:
- Alle Tests grün?
- Lint-Checks bestanden?
- Type-Checks ohne Fehler?