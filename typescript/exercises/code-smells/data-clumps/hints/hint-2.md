# Hint 2: Parameter Objects erstellen

## Was zu tun ist

### Schritt 1: Parameter Object Klassen definieren
Erstelle für jeden identifizierten Data Clump eine eigene Klasse:
- **Unveränderlichkeit**: Verwende `readonly` Properties
- **Konstruktor-Validierung**: Validiere alle Parameter im Konstruktor
- **Fehlerbehandlung**: Wirf aussagekräftige Fehlermeldungen

### Schritt 2: Validierung kapseln
- Verschiebe die Validierungslogik aus `EventManager` in die Parameter Objects
- Beispiel: `isValidAddress()` Logik gehört in die `Address` Klasse
- Jedes Parameter Object sollte sich selbst validieren

### Schritt 3: Verhalten hinzufügen (Tell-Don't-Ask)
Überlege welche Methoden zu den Daten gehören:
- **DateTime**: Zeitbereichs-Prüfungen, Zeitzone-Konvertierung
- **Coordinates**: Distanz-Berechnungen
- **Address**: Formatierung, Gleichheits-Prüfungen
- **Contact**: Kontakt-Formatierung

## Leitfragen zum Nachdenken

### Für jedes Parameter Object:
- Welche Konstruktor-Parameter brauche ich?
- Welche Validierungsregeln gehören hierher?
- Welche Methoden arbeiten hauptsächlich mit diesen Daten?
- Wie kann ich Unveränderlichkeit sicherstellen?

### TypeScript-Spezifische Überlegungen:
- Brauche ich Union Types für begrenzte Wertebereiche?
- Wo kann ich Type Guards für Runtime-Validierung einsetzen?
- Welche Properties sollten `readonly` sein?
- Wie strukturiere ich Exports/Imports?

## Worauf achten

### Schrittweise Refactoring
- Beginne mit einem Parameter Object (z.B. dem einfachsten)
- Teste nach jeder Änderung
- Refactoriere eine Methode nach der anderen
- Stelle sicher, dass Tests weiterhin grün bleiben

### Unveränderlichkeit sicherstellen
```typescript
// Guter Ansatz - readonly Properties
class ParameterObject {
  constructor(
    public readonly prop1: string,
    public readonly prop2: number
  ) {
    // Validierung hier
  }
}
```

### Validierung konsolidieren
- Sammle alle Validierungsregeln für eine Datengruppe in einem Ort
- Verwende private Methoden für komplexere Validierung
- Gib spezifische Fehlermeldungen zurück

## Nächster Schritt

Erstelle zunächst eine Parameter Object Klasse und teste sie isoliert:
1. Definiere die Klasse mit Konstruktor und readonly Properties
2. Implementiere die Validierung
3. Schreibe einen einfachen Test für die Validierung
4. Erst dann beginne mit der Integration in `EventManager`

Welches Parameter Object würdest du zuerst implementieren und warum?