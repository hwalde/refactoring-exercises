# Hint 2: Getter und Setter mit Validierung

## Was zu tun ist

Jetzt wo du das Feld privat gemacht hast, braucht der externe Code kontrollierte Zugriffsmethoden. In TypeScript sind das typischerweise `getXxx()` und `setXxx()` Methoden mit expliziten Return-Types.

**Leitfragen zum Nachdenken:**
- Was sollte der Getter zurückgeben? (Ziemlich einfach!)
- Was sollte der Setter prüfen, bevor er den Wert setzt?
- Wo sollte die Validierungslogik stehen - im Setter, Constructor, oder beiden?
- Welche TypeScript-spezifischen Error-Types sind geeignet?

## Worauf achten

**E-Mail-Validierung**: 
- Was macht eine gültige E-Mail-Adresse aus?
- Welche einfachen Regeln kannst du implementieren?
- Für diese Übung reicht es zu prüfen: nicht leer und enthält "@"

**Fehlerbehandlung in TypeScript**:
- Welche Error-Klasse ist für ungültige Argumente geeignet?
- Was sollten aussagekräftige Fehlermeldungen enthalten?
- Wie stellst du sicher, dass Errors zur Compile-Zeit typsicher sind?

**Type Safety**:
- Verwende explizite Return-Types für alle Methoden
- Keine `any` Types - nutze spezifische String-Typen
- Stelle sicher, dass alle Parameter vollständig typisiert sind

## Nächster Schritt

Implementiere die Validierungslogik in einer separaten private Methode. Das macht den Code testbarer und wiederverwendbar. Wie kannst du sicherstellen, dass sowohl Constructor als auch Setter dieselbe Validierung verwenden?