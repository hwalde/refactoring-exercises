# Encapsulate Field: E-Mail-Validierung durch Kapselung

## Aufgabenstellung

Du arbeitest an einem UserService-System, in dem Benutzerinformationen verwaltet werden. Die aktuelle `User` Klasse hat ein öffentliches `email` Attribut, das direkt von außen geändert werden kann. Dies führt zu Problemen, da ungültige E-Mail-Adressen gespeichert werden können, ohne dass eine Validierung stattfindet. Das System zeigt bereits Fehler bei der Datenpersistierung und bei E-Mail-Versendungen aufgrund von ungültigen E-Mail-Adressen.

## Problem(e)

Das öffentliche `email` Attribut in der `User` Klasse verletzt das Prinzip der Kapselung (Encapsulation) und führt zu folgenden Problemen:

1. **Fehlende Datenvalidierung**: E-Mail-Adressen können ohne Überprüfung gesetzt werden
2. **Direkter Zugriff auf interne Datenstrukturen**: Externe Klassen können das Attribut unkontrolliert ändern
3. **Schwierige Wartbarkeit**: Validierungslogik kann nicht zentral implementiert werden
4. **Potentielle Datenfehler**: Ungültige E-Mail-Adressen führen zu Fehlern in nachgelagerten Systemen

## Was zu tun ist

Refactoriere die `User` Klasse durch Implementierung des **Encapsulate Field** Refactorings:

1. **Mache das `email` Attribut privat** - Benenne es in `_email` um (Python Convention für private Attribute)
2. **Erstelle eine Property für den Lesezugriff** - Implementiere eine `email` Property mit Getter
3. **Erstelle einen Setter mit Validierung** - Implementiere einen Property-Setter mit E-Mail-Validierung
4. **Implementiere die Validierungslogik** - Prüfe, dass die E-Mail nicht leer ist und ein "@" Zeichen enthält
5. **Ergänze die Validierung im Constructor** - Stelle sicher, dass auch bei der Objekterstellung validiert wird
6. **Teste das Refactoring** - Überprüfe, dass alle bestehenden Tests weiterhin funktionieren

## Akzeptanzkriterien

- [ ] Das `_email` Attribut ist privat und nicht mehr direkt zugänglich
- [ ] Eine `email` Property ermöglicht das Lesen der E-Mail-Adresse
- [ ] Der Property-Setter ermöglicht das kontrollierte Setzen mit Validierung
- [ ] Die Validierung prüft auf nicht-leere Strings und das Vorhandensein von "@"
- [ ] Aussagekräftige Fehlermeldungen werden bei ungültigen E-Mails geworfen
- [ ] Der Constructor verwendet ebenfalls die Validierung
- [ ] Alle bestehenden Tests laufen erfolgreich durch
- [ ] Der Code ist sauberer und besser gekapselt

## Hinweise

- Verwende Python Properties (`@property` und `@email.setter`) für elegante Kapselung
- Verwende `ValueError` für ungültige E-Mail-Adressen
- Die Validierung sollte beschreibende Nachrichten enthalten
- Denke daran, dass der Constructor die Property verwenden sollte
- Die Tests zeigen dir das erwartete Verhalten - ändere die externe API nicht unnötig!

## Tests ausführen

Vom python-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
source venv/bin/activate && pytest exercises/basis-refactorings/encapsulate-field-mini/tests/ -v
```

**Unter Windows:**
```cmd
venv\Scripts\activate && pytest exercises\basis-refactorings\encapsulate-field-mini\tests\ -v
```

## Dateien

- `user.py` - Die zu refactorierende Benutzer-Klasse
- `test_user.py` - Tests für die User-Klasse (dürfen nicht verändert werden)