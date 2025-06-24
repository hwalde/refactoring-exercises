# Hint 2: Properties mit Validierung

## Was zu tun ist

Jetzt wo du das Attribut privat gemacht hast (`_email`), braucht der externe Code kontrollierte Zugriffsmethoden. In Python sind das typischerweise Properties mit `@property` und `@email.setter`.

**Leitfragen zum Nachdenken:**
- Was sollte die Property beim Lesen zurückgeben? (Ziemlich einfach!)
- Was sollte der Setter prüfen, bevor er den Wert setzt?
- Wo sollte die Validierungslogik stehen - im Setter, Constructor, oder beiden?

## Worauf achten

**E-Mail-Validierung**: 
- Was macht eine gültige E-Mail-Adresse aus?
- Welche einfachen Regeln kannst du implementieren?
- Python hat ein `email.utils` Modul - aber für diese Übung reicht es zu prüfen: nicht leer und enthält "@"

**Fehlerbehandlung**:
- Welche Exception-Klasse ist für ungültige Argumente geeignet?
- Was sollten aussagekräftige Fehlermeldungen enthalten?

## Nächster Schritt

Implementiere die Validierungslogik in einer separaten privaten Methode. Das macht den Code testbarer und wiederverwendbar. Wie kannst du sicherstellen, dass sowohl Constructor als auch Property-Setter dieselbe Validierung verwenden?