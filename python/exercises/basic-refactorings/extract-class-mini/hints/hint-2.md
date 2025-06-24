# Hint 2: Die Coordinate Klasse erstellen

## Was zu tun ist
Beginne mit der Erstellung der `Coordinate` Klasse als separaten Baustein:
- Identifiziere die drei Koordinaten-Felder, die extrahiert werden sollen
- Überlege dir, welche Methoden ausschließlich auf Koordinaten operieren
- Entscheide, wie die Klasse **unveränderlich (immutable)** gestaltet werden kann

## Worauf achten
- **Immutability**: Die Coordinate Klasse sollte nach der Erstellung nicht mehr verändert werden
- **Type Hints**: Alle Parameter und Rückgabewerte sollten typisiert sein
- **Methodensignaturen**: Überlege, ob Methoden Koordinaten-Objekte oder einzelne Werte als Parameter nehmen sollen
- **Geschäftslogik**: Die Haversine-Formel für Entfernungsberechnung muss erhalten bleiben

## Leitfragen für die Coordinate Klasse
- Soll `move_to()` eine neue Coordinate-Instanz zurückgeben oder die bestehende ändern?
- Wie können Methoden wie `distance_to()` eleganter mit Coordinate-Objekten arbeiten?
- Welche Validierung benötigen Koordinaten-Werte (Breitengrad: -90 bis 90, Längengrad: -180 bis 180)?
- Wie bleibt die öffentliche API der MapMarker-Klasse unverändert?

## Nächster Schritt
Erstelle die `Coordinate` Klasse in einer separaten Datei. Teste sie isoliert, bevor du die `MapMarker` Klasse anpasst. Denke daran: Die bestehenden Tests müssen weiterhin funktionieren!