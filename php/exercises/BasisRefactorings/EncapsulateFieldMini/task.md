# Encapsulate Field: E-Mail-Validierung durch Kapselung

## Aufgabenstellung

Du arbeitest an einem UserService-System, in dem Benutzerinformationen verwaltet werden. Die aktuelle `User` Klasse hat ein öffentliches `$email` Feld, das direkt von außen geändert werden kann. Dies führt zu Problemen, da ungültige E-Mail-Adressen gespeichert werden können, ohne dass eine Validierung stattfindet. Das System zeigt bereits Fehler bei der Datenpersistierung und bei E-Mail-Versendungen aufgrund von ungültigen E-Mail-Adressen.

## Problem(e)

Das öffentliche `$email` Feld in der `User` Klasse verletzt das Prinzip der Kapselung (Encapsulation) und führt zu folgenden Problemen:

1. **Fehlende Datenvalidierung**: E-Mail-Adressen können ohne Überprüfung gesetzt werden
2. **Direkter Zugriff auf interne Datenstrukturen**: Externe Klassen können das Feld unkontrolliert ändern
3. **Schwierige Wartbarkeit**: Validierungslogik kann nicht zentral implementiert werden
4. **Potentielle Datenfehler**: Ungültige E-Mail-Adressen führen zu Fehlern in nachgelagerten Systemen

## Was zu tun ist

Refactoriere die `User` Klasse durch Implementierung des **Encapsulate Field** Refactorings:

1. **Mache das `$email` Feld privat** - Benenne es in `$email` um und markiere es als private
2. **Erstelle einen Getter** - Implementiere eine `getEmail()` Methode für den Lesezugriff
3. **Erstelle einen Setter mit Validierung** - Implementiere eine `setEmail(string $email)` Methode mit E-Mail-Validierung
4. **Implementiere die Validierungslogik** - Prüfe, dass die E-Mail nicht leer ist und ein "@" Zeichen enthält
5. **Ergänze die Validierung im Constructor** - Stelle sicher, dass auch bei der Objekterstellung validiert wird
6. **Teste das Refactoring** - Überprüfe, dass alle bestehenden Tests weiterhin funktionieren

## Akzeptanzkriterien

- [ ] Das `$email` Feld ist privat und nicht mehr direkt zugänglich
- [ ] Ein Getter `getEmail()` ermöglicht das Lesen der E-Mail-Adresse
- [ ] Ein Setter `setEmail(string $email)` ermöglicht das kontrollierte Setzen mit Validierung
- [ ] Die Validierung prüft auf nicht-leere Strings und das Vorhandensein von "@"
- [ ] Aussagekräftige Fehlermeldungen werden bei ungültigen E-Mails geworfen
- [ ] Der Constructor verwendet ebenfalls die Validierung
- [ ] Alle bestehenden Tests laufen erfolgreich durch
- [ ] Der Code ist sauberer und besser gekapselt

## Hinweise

- Beginne mit dem Markieren des Feldes als private
- Verwende `InvalidArgumentException` für ungültige E-Mail-Adressen
- Die Validierung sollte beschreibende Nachrichten enthalten
- Denke daran, dass der Constructor möglicherweise angepasst werden muss
- Die Tests zeigen dir das erwartete Verhalten - ändere die externe API nicht unnötig!

## Tests ausführen

Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/BasisRefactorings/EncapsulateFieldMini/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\BasisRefactorings\EncapsulateFieldMini\
```

## Dateien

- `User.php` - Die zu refactorierende Benutzer-Klasse
- `UserTest.php` - Tests für die User-Klasse (dürfen nicht verändert werden)