# Hint 3: Integration und Qualitätsprüfung

## Was zu tun ist
Nachdem die `Coordinate` Klasse erstellt ist, integriere sie in die `MapMarker` Klasse:
- Ersetze die einzelnen Koordinaten-Felder durch ein `Coordinate`-Objekt
- Passe den Konstruktor an, um intern eine `Coordinate`-Instanz zu erstellen
- Delegiere Koordinaten-Operationen an das `Coordinate`-Objekt
- Stelle sicher, dass die öffentliche API unverändert bleibt

## Worauf achten
- **API-Kompatibilität**: Bestehende Tests dürfen nicht geändert werden
- **Delegation**: MapMarker-Methoden sollten Aufrufe an das Coordinate-Objekt weiterleiten
- **Konsistenz**: Alle Koordinaten-bezogenen Operationen sollten über das Coordinate-Objekt laufen
- **Performance**: Vermeide unnötige Objekt-Erstellungen in häufig genutzten Methoden

## Validierung der Lösung
- Laufen alle bestehenden Tests ohne Änderungen?
- Ist die `MapMarker` Klasse fokussierter und hat weniger Verantwortlichkeiten?
- Kann die `Coordinate` Klasse unabhängig verwendet und getestet werden?
- Folgt der Code den Python-Konventionen (PEP 8, Type Hints, Docstrings)?

## Finale Prüfung
- **Black**: Code-Formatierung prüfen
- **Ruff**: Linting-Regeln prüfen  
- **MyPy**: Type-Checking durchführen
- **Pytest**: Alle Tests erfolgreich ausführen

## Refactoring-Erfolgskriterien
- Single Responsibility Principle wird eingehalten
- Code ist wiederverwendbarer geworden
- Testbarkeit hat sich verbessert
- Keine Funktionalität wurde verloren oder verändert