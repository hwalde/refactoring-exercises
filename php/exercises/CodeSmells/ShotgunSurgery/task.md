# Shotgun Surgery Refactoring

## Aufgabenstellung

Du arbeitest an einem E-Commerce System, das unter dem **Shotgun Surgery** Code Smell leidet. Benachrichtigungslogik ist über mehrere Klassen verstreut (`OrderController`, `PaymentProcessor`, `ShippingManager`, `CustomerService`). Jede Änderung an den Benachrichtigungen erfordert Anpassungen in 4-6 verschiedenen Klassen.

## Problem(e)

Das System weist folgende Probleme auf:

- **Verstreute Logik**: Benachrichtigungslogik ist über mehrere Klassen verteilt
- **Multiple Änderungspunkte**: Jede Änderung an den Benachrichtigungen erfordert Anpassungen in vielen Klassen
- **Duplikation**: Ähnliche Benachrichtigungslogik wird in verschiedenen Klassen wiederholt
- **Schwierige Erweiterung**: Neue Benachrichtigungskanäle erfordern Änderungen in allen betroffenen Klassen
- **Inkonsistenz**: Benachrichtigungsformate und -verhalten sind zwischen den Klassen inkonsistent

## Was zu tun ist

Refactoriere die verstreute Benachrichtigungslogik durch Zentralisierung:

1. **Analysiere** die bestehenden Klassen und identifiziere alle Stellen mit Benachrichtigungslogik
2. **Erstelle** eine zentrale `NotificationService` Klasse, die alle Benachrichtigungstypen verwaltet
3. **Extrahiere** die Benachrichtigungslogik aus den verschiedenen Klassen mit **Move Method**
4. **Konsolidiere** ähnliche Benachrichtigungsmethoden und eliminiere Duplikation
5. **Implementiere** ein **Facade Pattern**, um eine einheitliche Schnittstelle für alle Benachrichtigungen zu schaffen
6. **Refactoriere** die ursprünglichen Klassen, so dass sie den neuen `NotificationService` verwenden
7. **Bereinige** die Abhängigkeiten und stelle sicher, dass die Trennung der Verantwortlichkeiten klar ist

## Akzeptanzkriterien

- [ ] Eine zentrale `NotificationService` Klasse existiert und verwaltet alle Benachrichtigungslogik
- [ ] Alle ursprünglichen Klassen verwenden den `NotificationService` statt eigene Benachrichtigungslogik
- [ ] Duplikate in der Benachrichtigungslogik sind eliminiert
- [ ] Eine einheitliche Schnittstelle für alle Benachrichtigungstypen ist implementiert
- [ ] Neue Benachrichtigungskanäle können durch Änderung nur einer Klasse hinzugefügt werden
- [ ] Alle bestehenden Tests laufen weiterhin durch
- [ ] Die Klassen haben klar getrennte Verantwortlichkeiten ohne Benachrichtigungslogik

## Hinweise

- Beginne mit der Identifikation aller Stellen, wo Benachrichtigungslogik vorhanden ist
- Verwende **Extract Method** und **Move Method** schrittweise, um die Logik zu zentralisieren
- Das **Facade Pattern** hilft dabei, eine saubere und einheitliche Schnittstelle zu schaffen
- Achte darauf, dass die Abhängigkeiten nur in eine Richtung fließen (andere Klassen → NotificationService)
- Die Tests zeigen dir das erwartete Verhalten - ändere es nicht!
- Bei Unsicherheiten: Schaue in die `/hints/` für gestaffelte Hilfestellungen

## Tests ausführen

Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/CodeSmells/ShotgunSurgery/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\CodeSmells\ShotgunSurgery\
```

## Dateien

Du wirst folgende Dateien bearbeiten:
- `NotificationService.php` - Die Hauptklasse mit verstreuter Benachrichtigungslogik
- `NotificationServiceTest.php` - Tests für die Klasse