# Hint 2: Implementiere Value Objects mit Validierung

## Was zu tun ist

- Erstelle separate Python-Dateien für jedes Value Object im `src/` Verzeichnis
- Verwende `@dataclass(frozen=True)` für Unveränderlichkeit
- Implementiere Validierung im `__post_init__` der Dataclass
- Stelle sicher, dass jedes Value Object eine `__str__` Methode hat

## Value Object Design-Prinzipien

**Money Value Object:**
- Welche Attribute braucht es? (Betrag, Währung)
- Wie validierst du negative Beträge?
- Wie rundest du korrekt auf 2 Dezimalstellen?
- Welche Arithmetik-Operationen sind sinnvoll?

**EmailAddress Value Object:**
- Wie validierst du das E-Mail-Format in Python?
- Ist ein einfacher Regex ausreichend oder brauchst du eine Bibliothek?
- Was passiert bei ungültigen E-Mails?

**ID Value Objects (CustomerId, InvoiceId):**
- Sollen die IDs bestimmte Präfixe haben?
- Wie lang dürfen sie sein?
- Sind alle ASCII-Zeichen erlaubt?

**InvoiceStatus Enum:**
- Verwende Python's `enum.Enum` für typsichere Status-Werte
- Wo definierst du die erlaubten Übergänge?
- Wie implementierst du die Übergangsvalidierung?

## Worauf achten

- **Aussagekräftige Exceptions**: Verwende spezifische Exception-Typen wie `ValueError`
- **Dokumentation**: Jedes Value Object braucht Docstrings
- **Type Hints**: Alle Parameter und Rückgabewerte typisieren
- **Equals und Hash**: `@dataclass(frozen=True)` generiert diese automatisch

## Nächster Schritt

Nachdem du 2-3 Value Objects erstellt hast, beginne mit dem Refactoring der `InvoiceGenerator` Klasse. Ersetze primitive Parameter durch deine Value Objects. Welche Methoden-Signaturen ändern sich dabei?