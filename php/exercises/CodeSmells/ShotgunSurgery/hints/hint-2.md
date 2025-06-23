# Hint 2: Refactoring-Strategie entwickeln

## Was zu tun ist
- **Wende das Extract Class Pattern** an, um zusammengehörige Logik zu gruppieren
- **Nutze das Facade Pattern**, um eine einheitliche Schnittstelle zu schaffen
- **Implementiere Dependency Injection**, um lose Kopplung zu erreichen
- **Extrahiere Value Objects** für wiederverwendbare Konzepte

## Konzeptuelle Klassen-Aufteilung
Denke an diese Separierung der Verantwortlichkeiten:

### NotificationChannels (Wie senden?)
- Welche Kanäle gibt es für den Versand? (Email, SMS, Push)
- Wie wird jeder Kanal konfiguriert und verwendet?
- Welche gemeinsamen Interfaces können definiert werden?

### NotificationTemplates (Wie formatieren?)
- Wie werden die Inhalte für verschiedene Ereignisse erstellt?
- Welche Template-Engine oder Struktur ist sinnvoll?
- Wie können Templates wiederverwendet werden?

### CustomerPreferences (Was möchte der Kunde?)
- Wie werden Kundenpräferenzen verwaltet und abgefragt?
- Welche Standardeinstellungen gibt es?
- Wie wird mit fehlenden Kontaktdaten umgegangen?

### NotificationCoordinator (Orchestrierung)
- Wie werden die einzelnen Services koordiniert?
- Welche einheitliche API wird nach außen angeboten?
- Wie wird die richtige Kombination von Kanälen gewählt?

## Worauf achten
- **Single Responsibility**: Jede Klasse sollte nur einen Grund zur Änderung haben
- **Open/Closed Principle**: Neue Kanäle sollten ohne Änderung bestehender Klassen hinzufügbar sein
- **Dependency Direction**: Abhängigkeiten sollten nur in eine Richtung fließen
- **Interface Segregation**: Kleine, fokussierte Interfaces statt große monolithische

## Refactoring-Reihenfolge
1. **Extrahiere Notification Channels** zuerst (Email, SMS, Push Services)
2. **Extrahiere Template Logic** als zweites
3. **Extrahiere Customer Preferences** als drittes  
4. **Baue Facade/Coordinator** als letztes

## Nächster Schritt
Beginne mit dem **Extract Class** Refactoring für den Email-Service. Überlege dir:
- Welche Methoden und Properties gehören zu Email-Versand?
- Welches Interface sollte der Email-Service haben?
- Wie kann der Service testbar und konfigurierbar gemacht werden?

Denke daran: Mache **kleine Schritte** und teste nach jedem Schritt!