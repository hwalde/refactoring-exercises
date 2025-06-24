# Hint 2: Services extrahieren und strukturieren

## Was zu tun ist

Jetzt geht es an die systematische Extraktion der Services:

1. **Beginne mit dem ersten Service** - Wähle einen klar abgrenzbaren Bereich (z.B. Authentifizierung)
2. **Definiere ein Interface** - Was sind die öffentlichen Methoden dieses Services?
3. **Extrahiere schrittweise** - Verschiebe relevante Methoden und Daten in den neuen Service
4. **Teste nach jedem Schritt** - Sorge dafür, dass die Tests weiterhin grün bleiben

## Leitfragen zur Service-Extraktion

- **Welche Daten braucht dieser Service?** - Welche privaten Properties müssen mitwandern?
- **Welche Methoden gehören zusammen?** - Sowohl öffentliche als auch private Hilfsmethoden
- **Wie soll die Kommunikation aussehen?** - Welche Parameter werden übergeben? Welche Rückgabewerte?
- **Wo liegen die Grenzen?** - Was gehört definitiv NICHT in diesen Service?

## Strukturierungsansatz

Denke an diese Service-Bereiche:
- **Authentication Service**: Login, Passwort-Validierung, Account-Sperrung
- **Contact Service**: Persönliche Daten, Adressen, Telefonnummern
- **Marketing Service**: Präferenzen, Kampagnen, Kommunikationskanäle
- **Order History Service**: Bestellungen, Spending-History, Lifetime Value

## Worauf achten

- **Interface Design**: Jeder Service sollte ein klares Interface haben
- **Dependency Injection**: Die ursprüngliche `CustomerService` sollte die Services injiziert bekommen
- **Datenkapselung**: Jeder Service verwaltet nur seine eigenen Daten
- **Keine zirkulären Abhängigkeiten**: Services sollten nicht gegenseitig voneinander abhängen

## Nächster Schritt

Beginne mit einem Service und arbeite dich systematisch durch. Extrahiere nicht alles auf einmal - lieber einen Service nach dem anderen und dabei immer die Tests laufen lassen. Die ursprüngliche öffentliche API der `CustomerService` muss dabei unverändert bleiben.