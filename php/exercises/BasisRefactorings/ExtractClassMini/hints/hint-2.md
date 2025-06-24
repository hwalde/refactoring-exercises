# Hint 2: Methoden verschieben und Klassen koppeln

## Was zu tun ist
Nachdem du die `Coordinate` Klasse erstellt hast, identifiziere welche Methoden von `MapMarker` eigentlich zur Koordinaten-Logik gehören:
- Welche Methoden arbeiten nur mit `latitude`, `longitude` und `altitude`?
- Wie können diese Methoden in die `Coordinate` Klasse verschoben werden?
- Welche Methodensignaturen müssen angepasst werden?

Denke über die Beziehung zwischen den Klassen nach:
- Soll `MapMarker` eine `Coordinate` **haben** (Komposition)?
- Wie rufst du dann Koordinaten-Methoden auf?

## Worauf achten
- Die `moveTo()` Methode muss eine neue `Coordinate` Instanz erstellen (wegen Immutability)
- Die `distanceTo()` Methode sollte eine andere `Coordinate` als Parameter akzeptieren
- Die `MapMarker` Klasse muss angepasst werden, um die neue Struktur zu verwenden
- Vergiss nicht die Methoden `getFormattedCoordinates()` und `isAtSameLocation()`

## Nächster Schritt
Verschiebe die Koordinaten-Methoden schrittweise:
1. Kopiere zuerst die Methoden in die `Coordinate` Klasse
2. Passe die Methodensignaturen an
3. Ändere `MapMarker` um die neuen Methoden zu verwenden
4. Entferne die alten Methoden aus `MapMarker`