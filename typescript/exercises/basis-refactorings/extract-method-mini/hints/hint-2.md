# Hint 2: Parameter und Rückgabewerte

## Was zu tun ist

Jetzt planst du deine neue `calculateStatistics()`-Methode:

**Parameter:**
- Braucht die Methode Parameter oder kann sie auf `this.items` zugreifen?
- Sollte sie als `private` oder `public` deklariert werden?

**Rückgabewert:**
- Die Methode muss mehrere Werte zurückgeben: total, active, percentage
- TypeScript bietet verschiedene Möglichkeiten: Interface, Type, oder Objekt-Literal
- Definiere einen klaren Return-Type für bessere Typsicherheit

## Worauf achten

- TypeScript kann den Rückgabetyp inferieren, aber explizite Typen sind klarer
- Verwende sprechende Namen für die Rückgabewerte
- Die Rundung des Prozentsatzes sollte identisch zur ursprünglichen Implementierung bleiben
- Berücksichtige den Edge-Case mit leeren Items (Division durch Null)

## Nächster Schritt

Erstelle die Methodensignatur und denke über die Implementierung nach. Wie rufst du die neue Methode aus `generateReport()` auf und verwendest die zurückgegebenen Werte?