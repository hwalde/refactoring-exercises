# Hint 1: Data Clumps identifizieren

## Was zu tun ist

### Schritt 1: Parameter-Gruppen analysieren
- Durchsuche die `EventManager.ts` nach Methoden mit vielen Parametern
- Markiere Parameter, die häufig zusammen auftreten
- Achte besonders auf Methoden wie `createEvent`, `updateEventTiming`, `registerVenue`

### Schritt 2: Wiederkehrende Muster erkennen
Suche nach diesen typischen Data Clump Mustern:
- **Zeitangaben**: Welche Parameter beschreiben immer gemeinsam einen Zeitpunkt?
- **Ortsangaben**: Welche Parameter beschreiben zusammen eine Adresse?
- **Kontaktdaten**: Welche Parameter gehören zu einer Person/Kontakt?
- **Koordinaten**: Welche Parameter beschreiben geografische Positionen?

### Leitfragen zum Nachdenken
- Welche Parameter treten in mindestens 3 verschiedenen Methoden zusammen auf?
- Wo wird dieselbe Validierung für Parameter-Gruppen wiederholt?
- Welche Parameter würden logisch zusammengehören, auch wenn sie getrennt validiert werden?

## Worauf achten

### Validierung beobachten
- Identifiziere private Methoden wie `isValidAddress()`, `isValidCoordinates()`, `isValidContact()`
- Diese Validierungen geben Hinweise auf natürliche Parameter-Gruppierungen
- Beachte, wo dieselben Validierungsregeln mehrfach angewendet werden

### Business-Logik verstehen
- DateTime-Parameter: Datum, Start-/Endzeit, Zeitzone
- Adressdaten: Straße, Stadt, Land, PLZ
- Koordinaten: Längen-/Breitengrad
- Kontaktinformationen: Name, E-Mail, Telefon

## Nächster Schritt

Erstelle eine Liste der identifizierten Data Clumps:
1. **Clump-Name**: Welche Parameter gehören zusammen
2. **Häufigkeit**: In wie vielen Methoden tritt diese Gruppe auf
3. **Validierung**: Welche Validierungslogik gehört dazu

Überlege dir bereits jetzt sinnvolle Namen für die zukünftigen Parameter Objects. Namen sollten das Domänenkonzept widerspiegeln (z.B. "DateTime" statt "TimeInfo").