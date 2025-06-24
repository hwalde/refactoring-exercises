# Hint 2: Refactoring durchführen

## Was zu tun ist
- Du hast die überflüssige Methode identifiziert - jetzt geht es ans Refactoring
- Ersetze jeden Aufruf von `isProductAvailable($productId)` durch `checkProductStock($productId)`
- Prüfe dabei jeden Aufruf einzeln: Ist die Bedeutung noch klar?
- Achte auf die Sichtbarkeit: Ist `checkProductStock()` für alle Aufrufer zugänglich?

## Worauf achten
- Alle Aufrufe der zu entfernenden Methode müssen ersetzt werden
- Die Funktionalität muss identisch bleiben
- Der Code sollte nach dem Refactoring lesbarer und direkter sein
- Private Methoden können nur innerhalb der gleichen Klasse aufgerufen werden

## Nächster Schritt
Führe die Tests aus, um sicherzustellen, dass deine Änderungen funktionieren. Wenn alle Tests grün sind, kannst du die überflüssige Methode entfernen. Was passiert, wenn du sie löschst?