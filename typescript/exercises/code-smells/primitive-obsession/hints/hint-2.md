# Hint 2: Implementiere Value Objects mit TypeScript-Features

## Was zu tun ist

- Erstelle Value Object Klassen mit strikter Typisierung und Validierung im Konstruktor
- Nutze TypeScript's Union Types für begrenzte Wertebereiche wie Status
- Implementiere Type Guards für Runtime-Validierung
- Alle Value Objects sollten unveränderlich (readonly) und vergleichbar sein

## TypeScript-spezifische Implementierungshinweise

**Für Money Value Object:**
- Welche Properties braucht Money? Betrag und Währung getrennt?
- Wie implementierst du Rundungslogik konsistent?
- Welche Operationen sind sinnvoll? Addition, Multiplikation?
- Soll eine Currency-Enumeration oder Union Type verwendet werden?

**Für EmailAddress Value Object:**
- Regex-Pattern für E-Mail-Validierung definieren
- Private Validierungsmethoden für saubere Trennung
- Readonly Properties für Unveränderlichkeit

**Für ID Value Objects (CustomerId, InvoiceId):**
- Nominal Typing Pattern nutzen um IDs zu unterscheiden
- Format-Validierung im Konstruktor
- Wie unterscheidest du zur Compile-Zeit verschiedene ID-Typen?

**Für InvoiceStatus:**
- Union Type mit allen erlaubten Status-Werten
- Type Guards für Statusübergangs-Validierung
- Map oder Record für erlaubte Übergänge definieren

## Worauf achten

- **Validation vor State**: Alle Validierung im Konstruktor, niemals ungültige Instanzen
- **Readonly Properties**: Keine Setter, nur Getter für Unveränderlichkeit
- **Equals-Methoden**: Strukturelle Gleichheit implementieren
- **Fehlerbehandlung**: Aussagekräftige Error-Messages mit Kontext
- **Type Safety**: Nutze TypeScript's Compile-Time-Checks maximally

## Nächster Schritt

Implementiere die Value Objects Schritt für Schritt. Beginne mit der einfachsten Validierung und arbeite dich zu komplexeren vor. Status-Übergänge sind oft der komplexeste Teil - welche Datenstruktur hilft bei der Übergangsprüfung?