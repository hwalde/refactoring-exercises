# Hint 3: Integration und Qualitätssicherung

## Was zu tun ist

### Schritt 1: EventManager refactorieren
- Ändere Methodensignaturen um Parameter Objects zu verwenden
- Entferne die ursprünglichen Validierungsmethoden (sie sind jetzt in den Parameter Objects)
- Nutze die Methoden der Parameter Objects für Business-Logik

### Schritt 2: Interface/Type-Definitionen anpassen
- Aktualisiere `Event`, `Venue`, `Notification` Interfaces
- Ersetze primitive Felder durch Parameter Objects
- Stelle sicher, dass alle Typen korrekt definiert sind

### Schritt 3: Methoden-Verhalten delegieren
Statt `EventManager` Logik:
```typescript
// Vorher: EventManager macht alles
if (!this.isValidCoordinates(lat1, lon1)) { ... }
const distance = this.calculateDistance(lat1, lon1, lat2, lon2);

// Nachher: Parameter Objects machen ihre eigene Logik
const distance = coord1.distanceTo(coord2);
```

## Leitfragen zum Nachdenken

### Code-Architektur
- Sind meine Parameter Objects wirklich unveränderlich?
- Haben alle Parameter Objects ihre eigene Validierung?
- Ist die Geschäftslogik richtig auf Parameter Objects verteilt?
- Sind die Methodensignaturen klarer und verständlicher geworden?

### Tell-Don't-Ask Prinzip
- Welche Logik kann ich von `EventManager` zu den Parameter Objects verschieben?
- Wo frage ich noch nach Daten, anstatt Verhalten zu delegieren?
- Sind meine Parameter Objects "dumme" Datencontainer oder enthalten sie Verhalten?

### Test-Kompatibilität
- Müssen die Original-Tests angepasst werden?
- Wie greife ich auf die Properties der Parameter Objects zu?
- Bleiben alle Assertions identisch?

## Worauf achten

### Häufige Fallstricke vermeiden
- **Leaky Abstractions**: Parameter Objects sollten ihre interne Struktur nicht preisgeben
- **Anemic Domain Model**: Parameter Objects sollten Verhalten haben, nicht nur Daten speichern
- **Überrefactoring**: Nicht jeden einzelnen Parameter in ein Object packen

### Performance-Überlegungen
- Parameter Objects werden öfter erstellt - ist das ein Problem?
- Sind Validierungen jetzt effizienter oder langsamer?
- Wird der Code durch die Objects verständlicher?

### TypeScript Best Practices
- Verwende Type Guards für Runtime-Validierung wenn nötig
- Nutze Union Types für begrenzte Wertebereiche
- Exponiere nur die notwendigen Properties und Methoden

## Nächster Schritt

### Finale Validierung
1. **Tests laufen**: Alle ursprünglichen Tests sollten weiterhin grün sein
2. **Code-Qualität**: Linter und TypeScript-Compiler sollten keine Fehler zeigen
3. **Lesbarkeit**: Sind die Methodensignaturen klarer geworden?
4. **Wartbarkeit**: Ist neue Funktionalität leichter hinzuzufügen?

### Qualitätsprüfung
- Haben alle Parameter Objects sinnvolle Methoden?
- Ist die Validierung konsistent und an der richtigen Stelle?
- Sind die Interfaces/Types klar und selbsterklärend?
- Würde ein neuer Entwickler den Code schneller verstehen?

### Reflexion
Welche Vorteile siehst du durch die Eliminierung der Data Clumps?
- Wartbarkeit
- Testbarkeit  
- Verständlichkeit
- Erweiterbarkeit