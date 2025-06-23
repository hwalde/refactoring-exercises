# Hint 2: Erweitere dein Refactoring auf E-Mails und IDs

## Was zu tun ist

- Setze die Primitive Obsession-Beseitigung fort mit E-Mail-Adressen und ID-Typen
- Analysiere die bestehenden Validierungsregeln im Code - sie zeigen dir, welche Geschäftsregeln in die Value Objects gehören
- Schaue dir an, wie IDs im System generiert werden - das gibt dir Hinweise auf notwendige Hilfsmethoden

## Denkfragen für E-Mail-Validierung

- **Welche PHP-Funktion** eignet sich zur E-Mail-Validierung?
- **Wo im aktuellen Code** wird bereits E-Mail-Validierung gemacht?
- **Soll eine E-Mail-Adresse** nur lesbar sein oder braucht sie weitere Operationen?
- **Was passiert bei ungültigen E-Mails** - Exception werfen oder anders handhaben?

## Denkfragen für ID-Value Objects

**Für Kunden-IDs:**
- **Welche Validierung** macht der bestehende Code bereits?
- **Können Kunden-IDs leer sein?** Was sagen die Tests dazu?
- **Haben Kunden-IDs ein Format?** Untersuche die Testdaten!

**Für Rechnungs-IDs:**
- **Wie werden Rechnungs-IDs generiert?** Schaue dir die `nextInvoiceNumber` Logik an
- **Welches Format** haben die generierten IDs?
- **Braucht InvoiceId eine statische Factory-Methode** zum Generieren?

## Worauf achten

- **Validierung zentralisieren**: Was heute verstreut validiert wird, gehört in die Value Objects
- **Typsicherheit erhöhen**: Verschiedene ID-Typen dürfen nicht verwechselt werden
- **Tests als Spezifikation**: Die Tests zeigen dir das genaue erwartete Verhalten
- **Bestehende Exception-Messages**: Verwende die gleichen Fehlermeldungen wie im Original

## Nächster Schritt

Beginne mit `EmailAddress` - es ist das einfachste. Dann die ID-Typen. Überlege bei jeder Klasse: Welche Operationen brauche ich wirklich? Minimal, aber vollständig!