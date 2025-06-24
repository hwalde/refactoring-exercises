# Hint 3: Qualitätsprüfung und Vollständigkeit

## Was zu tun ist

Du solltest jetzt eine `User` Klasse haben mit:
- Einem privaten `$email` Feld
- Einer `getEmail()` Methode
- Einer `setEmail()` Methode mit Validierung
- Validierung im Constructor

**Leitfragen zur Selbstprüfung:**
- Laufen alle Tests erfolgreich durch?
- Werden ungültige E-Mails sowohl im Constructor als auch im Setter abgefangen?
- Sind die Fehlermeldungen aussagekräftig?
- Funktionieren alle bestehenden Funktionen wie `getDisplayName()` und `hasBusinessEmail()` noch?

## Worauf achten

**Code-Qualität prüfen:**
- Sind deine Fehlermeldungen hilfreich für Entwickler?
- Hast du alle Edge-Cases abgedeckt?
- Ist der Code noch lesbar und verständlich?

**Testing-Aspekte:**
- Schaue dir die Tests an, die vorher "problematisches Verhalten" gezeigt haben
- Nach deinem Refactoring sollten diese Tests fehlschlagen - das ist gut!
- Die Tests zeigen, dass deine Validierung funktioniert

## Nächster Schritt

Führe die Tests aus und prüfe, ob alle grün sind. Wenn nicht, analysiere die Fehlermeldungen. Oft zeigen sie dir genau, was noch zu tun ist. 

Überlege auch: Ist das `$email` Feld jetzt wirklich privat? Kann externer Code es noch direkt ändern?