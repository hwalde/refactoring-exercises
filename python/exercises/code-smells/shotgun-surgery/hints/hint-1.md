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

## Leitfragen zum Nachdenken
- Wenn du einen neuen Benachrichtigungskanal (z.B. Slack, WhatsApp) hinzufügen müsstest, wie viele Stellen müsstest du ändern?
- Welche Bereiche der Logik gehören wirklich zusammen?
- Was ist der Unterschied zwischen der **Entscheidung** eine Benachrichtigung zu senden und der **Implementierung** des Sendens?
- Welche Verantwortlichkeiten könnten in separate Klassen extrahiert werden?
- Wie könnten Python's **ABC (Abstract Base Classes)** helfen, um einheitliche Interfaces zu definieren?

## Python-spezifische Überlegungen
- Welche **Standard-Library-Module** könnten für Email-Versand verwendet werden? (smtplib, email)
- Wie könnte **typing.Protocol** helfen, um Interfaces zu definieren?
- Welche **dataclasses** oder **NamedTuple** könnten für strukturierte Daten sinnvoll sein?
- Wie könnte **functools** oder **itertools** helfen, Duplikation zu reduzieren?

## Nächster Schritt
Überlege dir eine Struktur mit separaten Klassen für:
- **Benachrichtigungs-Entscheidungen** (wann und was senden?)
- **Benachrichtigungs-Versand** (wie senden?)
- **Template-Erstellung** (wie formatieren?)
- **Kundenpräferenzen** (was möchte der Kunde?)

Denke daran: Das Ziel ist, dass Änderungen nur an **einer** Stelle gemacht werden müssen!