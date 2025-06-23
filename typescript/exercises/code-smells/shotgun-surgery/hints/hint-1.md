# Hint 1: Problem erkennen und analysieren

## Was zu tun ist
- **Analysiere die bestehende NotificationService Klasse** und identifiziere die verschiedenen Bereiche der Benachrichtigungslogik
- **Erkenne das Muster**: Wo wird ähnliche Logik für Email, SMS und Push-Notifications wiederholt?
- **Finde die Inkonsistenzen**: Welche unterschiedlichen Ansätze werden für ähnliche Aufgaben verwendet?

## Worauf achten
- **Verschiedene Domänen vermischt**: Order, Payment, Customer Service, Promotional - jeder Bereich hat seine eigenen Regeln
- **Duplikation der Versandlogik**: Email/SMS/Push-Logik wird in jeder Methode neu implementiert
- **Inkonsistente Header-Behandlung**: Manche Emails haben Headers, andere nicht
- **Verschiedene Template-Ansätze**: Mal Templates, mal direkte String-Erstellung
- **Verstreute Kundenlogik**: Präferenzen werden überall abgefragt

## TypeScript-spezifische Probleme
- **Lose Typisierung der Data-Parameter**: `Record<string, unknown>` ist zu unspezifisch
- **Fehlende Union Types**: Notification-Types könnten besser typisiert werden
- **Keine Interface-Trennung**: Alle Notification-Kanäle verwenden dieselben Methoden
- **Vermischte Concerns**: Business Logic und Infrastructure Code sind nicht getrennt

## Leitfragen zum Nachdenken
- Wenn du ein neues Benachrichtigungskanal (z.B. Slack, WhatsApp) hinzufügen müsstest, wie viele Stellen müsstest du ändern?
- Welche Bereiche der Logik gehören wirklich zusammen?
- Was ist der Unterschied zwischen der **Entscheidung** eine Benachrichtigung zu senden und der **Implementierung** des Sendens?
- Welche Verantwortlichkeiten könnten in separate Klassen extrahiert werden?
- Wie können TypeScript Interfaces helfen, die verschiedenen Concerns zu trennen?

## Nächster Schritt
Überlege dir eine Struktur mit separaten Klassen für:
- **Benachrichtigungs-Entscheidungen** (wann und was senden?)
- **Benachrichtigungs-Versand** (wie senden?)
- **Template-Erstellung** (wie formatieren?)
- **Kundenpräferenzen** (was möchte der Kunde?)

Denke dabei an TypeScript-Features:
- **Interface Segregation**: Kleine, fokussierte Interfaces statt große monolithische
- **Union Types**: Für begrenzte Wertebereiche (NotificationType, UpdateType)
- **Generic Constraints**: Für typisierte Template-Parameter

Denke daran: Das Ziel ist, dass Änderungen nur an **einer** Stelle gemacht werden müssen!