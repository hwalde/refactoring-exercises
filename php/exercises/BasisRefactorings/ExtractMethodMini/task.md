# Extract Method Mini - Berechnungsblock extrahieren

## Aufgabenstellung
Extrahiere die Berechnung aus der `generateReport()` Methode in eine separate `calculateStatistics()` Methode.

## Problem
Die `generateReport()` Methode mischt Berichterstellung und Berechnungslogik.

## Was zu tun ist
1. Neue Methode `calculateStatistics()` erstellen
2. Berechnungsblock dorthin verschieben  
3. Ursprüngliche Methode anpassen

## Akzeptanzkriterien
- [x] Neue Methode `calculateStatistics()` existiert
- [x] Berechnet Summe und Prozentsatz korrekt
- [x] `generateReport()` nutzt die neue Methode
- [x] Alle Tests laufen erfolgreich

## Tests ausführen

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/BasisRefactorings/ExtractMethodMini/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\BasisRefactorings\ExtractMethodMini\
```

## Dateien
- `InventoryManager.php` - Hauptklasse bearbeiten
- `InventoryManagerTest.php` - Tests (nicht ändern)