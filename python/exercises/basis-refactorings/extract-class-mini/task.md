# Extract Class Mini: MapMarker Koordinaten-Extraktion

## Aufgabenstellung
Das Team für Kartendienste hat eine `MapMarker` Klasse entwickelt, die zu viele Verantwortlichkeiten übernommen hat. Die Klasse verwaltet sowohl Marker-spezifische Eigenschaften als auch Koordinaten-Logik. Deine Aufgabe ist es, die Koordinaten-bezogene Funktionalität in eine separate `Coordinate` Klasse zu extrahieren.

## Problem(e)
Die `MapMarker` Klasse leidet unter **God Object**-Problemen:
- Koordinaten-Daten (`latitude`, `longitude`, `altitude`) sind direkt in der Marker-Klasse gespeichert
- Koordinaten-spezifische Methoden wie `move_to()` und `distance_to()` gehören logisch nicht zu einem Marker
- Die Klasse violiert das Single Responsibility Principle
- Code würde dupliziert werden, wenn andere Klassen ebenfalls Koordinaten benötigen

## Was zu tun ist
1. **Erstelle eine neue `Coordinate` Klasse** mit den Feldern `latitude`, `longitude`, `altitude`
2. **Verschiebe die Koordinaten-Methoden** `move_to()` und `distance_to()` in die `Coordinate` Klasse
3. **Refactoriere `MapMarker`** um ein `Coordinate` Objekt zu verwenden statt direkter Koordinaten-Felder
4. **Passe den Konstruktor an** um eine `Coordinate` Instanz zu akzeptieren oder zu erstellen
5. **Stelle sicher**, dass alle Tests weiterhin grün bleiben

## Akzeptanzkriterien
- [ ] Neue `Coordinate` Klasse mit `latitude`, `longitude`, `altitude` erstellt
- [ ] Methoden `move_to()` und `distance_to()` in `Coordinate` Klasse verschoben
- [ ] `MapMarker` verwendet `Coordinate` Objekt statt direkter Koordinaten-Felder
- [ ] Konstruktor von `MapMarker` angepasst
- [ ] Alle bestehenden Tests laufen durch
- [ ] Code folgt Single Responsibility Principle

## Hinweise
- Beginne mit der Erstellung der `Coordinate` Klasse
- Verwende "Extract Class" Refactoring schrittweise
- Die `Coordinate` Klasse sollte unveränderlich (immutable) sein
- Teste nach jedem Schritt, dass die Funktionalität erhalten bleibt
- Verwende Type Hints für alle Methoden und Parameter
- Folge PEP 8 Code Style Konventionen

## Tests ausführen
Vom python-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
source venv/bin/activate && pytest exercises/basic-refactorings/extract-class-mini/tests/ -v
```

**Unter Windows:**
```cmd
venv\Scripts\activate && pytest exercises\basic-refactorings\extract-class-mini\tests\ -v
```

## Dateien
- `src/map_marker.py` - Die zu refaktorierende Hauptklasse
- `tests/test_map_marker.py` - Tests, die das erwartete Verhalten definieren