# Hint 1: Problem erkennen und erste Schritte

## Was zu tun ist
Schaue dir die `MapMarker` Klasse genau an und identifiziere, welche Felder und Methoden zusammengehören:
- Welche Felder beschreiben die **Position** des Markers?
- Welche Methoden arbeiten **nur** mit Koordinaten-Daten?
- Welche Methoden gehören wirklich zum **Marker** selbst?

Denke daran: Eine Klasse sollte nur **eine Verantwortlichkeit** haben. Was sind die zwei verschiedenen Verantwortlichkeiten in der aktuellen `MapMarker` Klasse?

## Worauf achten
- Die `Coordinate` Klasse sollte **unveränderlich** (immutable) sein
- Koordinaten-Berechnungen gehören zur Koordinaten-Logik, nicht zur Marker-Logik
- Überlege, welche Informationen die neue `Coordinate` Klasse braucht
- Welche Validierungen könnten für Koordinaten sinnvoll sein?

## TypeScript-spezifische Überlegungen
- Nutze `readonly` Properties für unveränderliche Felder
- Definiere explizite Return-Types für alle Methoden
- Vermeide `any` Types - verwende konkrete Typen
- Überlege, ob ein Interface für Coordinate sinnvoll ist

## Nächster Schritt
Beginne mit der Erstellung einer einfachen `Coordinate` Klasse. Frage dich:
- Welche drei Felder braucht sie?
- Wie sollte der Konstruktor aussehen?
- Welche Getter-Methoden werden benötigt?
- Welche Methoden gehören zur Koordinaten-Logik?