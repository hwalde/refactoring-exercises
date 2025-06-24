# Hint 2: Getter und Setter mit Validierung

## Was zu tun ist

Jetzt wo du das Feld privat gemacht hast, braucht der externe Code kontrollierte Zugriffsmethoden. In PHP sind das typischerweise `getXxx()` und `setXxx()` Methoden.

**Leitfragen zum Nachdenken:**
- Was sollte der Getter zurückgeben? (Ziemlich einfach!)
- Was sollte der Setter prüfen, bevor er den Wert setzt?
- Wo sollte die Validierungslogik stehen - im Setter, Constructor, oder beiden?

## Worauf achten

**E-Mail-Validierung**: 
- Was macht eine gültige E-Mail-Adresse aus?
- Welche einfachen Regeln kannst du implementieren?
- PHP hat eine eingebaute `filter_var()` Funktion - aber für diese Übung reicht es zu prüfen: nicht leer und enthält "@"

**Fehlerbehandlung**:
- Welche Exception-Klasse ist für ungültige Argumente geeignet?
- Was sollten aussagekräftige Fehlermeldungen enthalten?

## Nächster Schritt

Implementiere die Validierungslogik in einer separaten private Methode. Das macht den Code testbarer und wiederverwendbar. Wie kannst du sicherstellen, dass sowohl Constructor als auch Setter dieselbe Validierung verwenden?