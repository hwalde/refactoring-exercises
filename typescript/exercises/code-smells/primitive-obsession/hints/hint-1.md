# Hint 1: Erkenne Primitive Obsession und plane deine Value Objects

## Was zu tun ist

- Durchsuche die `InvoiceGenerator` Klasse nach primitiven Typen (`string`, `number`), die eigentlich komplexe Domänen-Konzepte repräsentieren
- Frage dich bei jedem primitiven Typ: "Welche Geschäftsregeln und Validierungen gehören zu diesem Konzept?"
- Beginne mit Geldbeträgen, da diese die komplexesten Validierungsregeln haben
- Nutze TypeScript's strikte Typisierung für maximale Typsicherheit

## Erkennungsfragen für Primitive Obsession

**Für Geldbeträge:**
- Können Geldbeträge negativ sein?
- Welche Währungen sind erlaubt?
- Wie wird mit Rundung umgegangen?
- Dürfen verschiedene Währungen addiert werden?

**Für E-Mail-Adressen:**
- Welches Format muss eine gültige E-Mail haben?
- Soll es eine zentrale Validierung geben?
- Wie nutzt TypeScript die Typsicherheit für E-Mails?

**Für IDs (Kunden, Rechnungen):**
- Folgen die IDs einem bestimmten Format?
- Können IDs leer oder ungültig sein?
- Gibt es Unterschiede zwischen verschiedenen ID-Typen?
- Wie kann TypeScript verhindern, dass IDs verwechselt werden?

**Für Status-Werte:**
- Welche Status-Werte sind überhaupt erlaubt?
- Gibt es Regeln für Status-Übergänge?
- Wie können Union Types für Typsicherheit sorgen?

## Worauf achten

- **Tests zuerst verstehen**: Schaue dir die Tests an - sie zeigen dir das erwartete Verhalten
- **Schrittweise vorgehen**: Beginne mit einem Value Object, dann das nächste
- **Immutability**: Value Objects sollten unveränderlich sein (readonly Properties)
- **Aussagekräftige Namen**: Verwende Domänen-Sprache, nicht technische Begriffe
- **TypeScript Features nutzen**: Strikte Typisierung, Union Types, Type Guards

## Nächster Schritt

Beginne mit einem `Money` Value Object. Überlege dir zuerst: Welche Operationen braucht Geld? Wie soll die Validierung funktionieren? Welche TypeScript-Features helfen bei der Typsicherheit? Erst denken, dann implementieren!