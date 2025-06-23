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
- **TypeScript**: Definiere ein `NotificationChannel` Interface mit gemeinsamen Methoden

### NotificationTemplates (Wie formatieren?)
- Wie werden die Inhalte für verschiedene Ereignisse erstellt?
- Welche Template-Engine oder Struktur ist sinnvoll?
- Wie können Templates wiederverwendet werden?
- **TypeScript**: Nutze Generic Types für typisierte Template-Parameter

### CustomerPreferences (Was möchte der Kunde?)
- Wie werden Kundenpräferenzen verwaltet und abgefragt?
- Welche Standardeinstellungen gibt es?
- Wie wird mit fehlenden Kontaktdaten umgegangen?
- **TypeScript**: Definiere einen `CustomerPreferences` Type mit optionalen Feldern

### NotificationCoordinator (Orchestrierung)
- Wie werden die einzelnen Services koordiniert?
- Welche einheitliche API wird nach außen angeboten?
- Wie wird die richtige Kombination von Kanälen gewählt?
- **TypeScript**: Implementiere als Facade mit klaren Interface-Boundaries

## TypeScript-spezifische Überlegungen

### Interface Design
```typescript
interface NotificationChannel<TData = unknown> {
  send(recipient: string, message: string, data?: TData): Promise<void>;
  isAvailable(customerId: string): boolean;
}
```

### Union Types für Ereignisse
- Definiere Union Types für verschiedene Notification-Events
- Nutze Discriminated Unions für typisierte Event-Data
- Implementiere Type Guards für Runtime-Validierung

### Dependency Injection Pattern
- Verwende Constructor Injection für Services
- Definiere abstrakte Interfaces, nicht konkrete Implementierungen
- Nutze Optional Dependencies für nicht-kritische Services

## Worauf achten
- **Single Responsibility**: Jede Klasse sollte nur einen Grund zur Änderung haben
- **Open/Closed Principle**: Neue Kanäle sollten ohne Änderung bestehender Klassen hinzufügbar sein
- **Dependency Direction**: Abhängigkeiten sollten nur in eine Richtung fließen
- **Interface Segregation**: Kleine, fokussierte Interfaces statt große monolithische
- **TypeScript Strict Mode**: Nutze strict type checking für bessere Code-Qualität

## Refactoring-Reihenfolge
1. **Extrahiere Notification Channels** zuerst (Email, SMS, Push Services)
2. **Extrahiere Template Logic** als zweites
3. **Extrahiere Customer Preferences** als drittes  
4. **Baue Facade/Coordinator** als letztes

## TypeScript-Features nutzen
- **Readonly Properties**: Für unveränderliche Datenstrukturen
- **Optional Chaining**: Für sichere Zugriffe auf möglicherweise undefined Werte
- **Nullish Coalescing**: Für Default-Werte
- **Template Literal Types**: Für typisierte String-Kombinationen

## Nächster Schritt
Beginne mit dem **Extract Class** Refactoring für den Email-Service. Überlege dir:
- Welche Methoden und Properties gehören zu Email-Versand?
- Welches Interface sollte der Email-Service haben?
- Wie kann der Service testbar und konfigurierbar gemacht werden?
- Wie können TypeScript Types helfen, Fehler zur Compile-Zeit zu vermeiden?

Denke daran: Mache **kleine Schritte** und teste nach jedem Schritt!