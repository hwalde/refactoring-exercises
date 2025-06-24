# Hint 2: Service-Extraktion und Interface-Design

## Was zu tun ist

Jetzt ist es Zeit, die identifizierten Concerns in separate Service-Klassen zu extrahieren. Verwende das "Extract Class" Refactoring-Pattern schrittweise.

**Strategisches Vorgehen:**
- Beginne mit einem Concern und extrahiere alle zusammengehörigen Methoden und Daten
- Definiere klare Interfaces/Protocols für jeden Service
- Verwende Python's `typing.Protocol` für typisierte Contracts
- Implementiere Dependency Injection über Constructor Parameters

**Fragen zum Nachdenken:**
- Welche Methoden und Datenspeicher gehören zu jedem Service?
- Wie sollten die Services miteinander kommunizieren (falls nötig)?
- Welche öffentlichen Methoden braucht jeder Service?
- Wie kann ich sicherstellen, dass die ursprüngliche `CustomerService` API unverändert bleibt?

## Worauf achten

**Interface Design:**
- Jeder Service sollte ein klares, minimal nötiges Interface haben
- Verwende `typing.Protocol` statt ABC für Flexibilität
- Denke an zukünftige Erweiterbarkeit der Services
- Halte die Interfaces klein und fokussiert

**Service Responsibilities:**
- Ein Service für Authentifizierung: Login, Registrierung, Passwort-Management
- Ein Service für Kontakte: Adress- und Kontaktdatenverwaltung
- Ein Service für Marketing: Präferenzen, Kampagnen-Versand
- Ein Service für Orders: Bestellhistorie, Analytics, Lifetime Value

**Python-spezifische Überlegungen:**
- Type Hints für alle Service-Methoden
- Dataclasses für strukturierte Service-Parameter wenn sinnvoll
- Proper Error Handling zwischen Services

## Nächster Schritt

Beginne mit einem Service (z.B. Authentication) und extrahiere ihn vollständig, inklusive Interface und Implementierung. Teste, dass die ursprünglichen Tests noch laufen, bevor du zum nächsten Service gehst. Das "Divide and Conquer"-Prinzip hilft, Fehler früh zu erkennen.