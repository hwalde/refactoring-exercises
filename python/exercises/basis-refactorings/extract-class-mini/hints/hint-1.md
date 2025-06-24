# Hint 1: Verantwortlichkeiten identifizieren

## Was zu tun ist
Bevor du mit dem Refactoring beginnst, analysiere die `MapMarker` Klasse sorgfältig:
- Welche Daten und Methoden gehören zur **Koordinaten-Logik**?
- Welche Daten und Methoden gehören zur **Marker-spezifischen Logik**?
- Wo wird gegen das Single Responsibility Principle verstoßen?

## Worauf achten
- Die Klasse mischt zwei unterschiedliche Konzepte: Koordinaten und Marker-Eigenschaften
- Koordinaten-Methoden würden in anderen Klassen nützlich sein (Wiederverwendbarkeit)
- Testbarkeit: Koordinaten-Logik kann unabhängig getestet werden
- Änderungen an Koordinaten-Logik sollten nicht die Marker-Klasse betreffen

## Leitfragen
- Welche Felder gehören zusammen und repräsentieren ein eigenständiges Konzept?
- Welche Methoden operieren ausschließlich auf diesen zusammengehörigen Feldern?
- Wie würde sich die Klasse lesen, wenn sie nur eine Verantwortlichkeit hätte?

## Nächster Schritt
Entscheide dich für die Felder und Methoden, die in die neue `Coordinate` Klasse extrahiert werden sollen. Erstelle dann eine Liste der Methoden, die verschoben werden müssen.