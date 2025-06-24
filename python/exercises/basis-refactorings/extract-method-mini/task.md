# Extract Method Mini - Berechnungsblock extrahieren

## Aufgabenstellung
Extrahiere die Berechnung aus der `generate_report()` Methode in eine separate `calculate_statistics()` Methode.

## Problem
Die `generate_report()` Methode mischt Berichterstellung und Berechnungslogik.

## Was zu tun ist
1. Neue Methode `calculate_statistics()` erstellen
2. Berechnungsblock dorthin verschieben  
3. Ursprüngliche Methode anpassen

## Akzeptanzkriterien
- [x] Neue Methode `calculate_statistics()` existiert
- [x] Berechnet Summe und Prozentsatz korrekt
- [x] `generate_report()` nutzt die neue Methode
- [x] Alle Tests laufen erfolgreich

## Hinweise
- Python verwendet snake_case für Methodennamen
- Type Hints für alle Parameter und Rückgabewerte verwenden
- Die neue Methode kann `private` sein (beginnt mit `_`)

## Tests ausführen

**Unter Linux/macOS:**
```bash
source venv/bin/activate && pytest exercises/basis-refactorings/extract-method-mini/tests/ -v
```

**Unter Windows:**
```cmd
venv\Scripts\activate && pytest exercises\basis-refactorings\extract-method-mini\tests\ -v
```

## Dateien
- `inventory_manager.py` - Hauptklasse bearbeiten
- `test_inventory_manager.py` - Tests (nicht ändern)