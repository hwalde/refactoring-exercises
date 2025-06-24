# Hint 2: Koordinaten-Klasse implementieren und Integration planen

## Was zu tun ist
Nachdem du die Verantwortlichkeiten identifiziert hast, implementiere die `Coordinate` Klasse:
- Erstelle die Klasse mit den drei Koordinaten-Feldern
- Implementiere die koordinaten-spezifischen Methoden
- Denke an die Unveränderlichkeit der Klasse

Welche Methoden aus `MapMarker` arbeiten ausschließlich mit Koordinaten? Diese gehören in die neue Klasse!

## Worauf achten
- **Unveränderlichkeit**: Koordinaten sollten nach der Erstellung nicht mehr geändert werden können
- **Methoden-Signaturen**: Wie ändern sich die Parameter, wenn Methoden Coordinate-Objekte verwenden?
- **Factory-Pattern**: Soll `moveTo()` ein neues Coordinate-Objekt zurückgeben?
- **Konsistenz**: Alle koordinaten-bezogenen Operationen sollten durch die Coordinate-Klasse gehen

## TypeScript-spezifische Überlegungen
- Verwende `readonly` für alle Felder in der Coordinate-Klasse
- Überlege, ob `distanceTo()` ein anderes Coordinate-Objekt als Parameter nehmen soll
- Type Guards könnten für Koordinaten-Validierung nützlich sein
- Definiere klare Interfaces für die Coordinate-API

## Nächster Schritt
Beginne mit der schrittweisen Integration in `MapMarker`:
- Wie änderst du den Konstruktor?
- Welche Getter-Methoden delegieren an das Coordinate-Objekt?
- Wie behältst du die bestehende API bei, während du intern Coordinate verwendest?