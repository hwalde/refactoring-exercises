# Primitive Obsession - InvoiceGenerator

## Aufgabenstellung

Du arbeitest an einem Rechnungsverarbeitungssystem, das Rechnungen für Kunden erstellt. Die aktuelle `InvoiceGenerator` Klasse leidet unter dem Code Smell **Primitive Obsession** - sie verwendet primitive Datentypen (strings, numbers) für komplexe Geschäftskonzepte wie Geldbeträge, E-Mail-Adressen, Kunden-IDs und Rechnungsstatus.

## Problem(e)

Die `InvoiceGenerator` Klasse weist folgende Probleme auf:

1. **Primitive Obsession**: Geldbeträge werden als einfache Zahlen (float) gespeichert, ohne Währungsinformation oder Rundungslogik
2. **Fehlende Validierung**: E-Mail-Adressen werden als Strings behandelt, ohne Formatvalidierung
3. **Unsichere Typisierung**: Kunden-IDs und Rechnungs-IDs sind einfache Strings, die verwechselt werden können
4. **Magische Strings**: Status-Werte werden als Strings gespeichert, ohne Typsicherheit oder erlaubte Werte zu definieren
5. **Verteilte Validierung**: Geschäftsregeln sind über den Code verstreut, statt in den entsprechenden Domänen-Objekten gekapselt

## Was zu tun ist

Refactoriere die `InvoiceGenerator` Klasse durch das Erstellen von Value Objects für alle primitiven Domänen-Konzepte:

1. **Analysiere** die aktuelle Implementierung und identifiziere alle primitiven Typen, die Domänen-Konzepte repräsentieren
2. **Erstelle Value Objects** für:
   - `Money` (Geldbetrag mit Währung und Rundungslogik)
   - `EmailAddress` (E-Mail-Adresse mit Formatvalidierung)
   - `CustomerId` (Kunden-ID mit Validierung)
   - `InvoiceId` (Rechnungs-ID mit Formatvorgaben)
   - `InvoiceStatus` (Status-Enum mit erlaubten Übergängen)
3. **Implementiere Validierung** in den Konstruktoren der Value Objects
4. **Ersetze** alle Verwendungen der primitiven Typen durch die neuen Value Objects
5. **Stelle sicher**, dass alle Value Objects unveränderlich (immutable) sind

## Akzeptanzkriterien

- [ ] Alle primitiven Typen für Domänen-Konzepte wurden durch Value Objects ersetzt
- [ ] `Money` Value Object mit Währungsunterstützung und korrekter Rundung implementiert
- [ ] `EmailAddress` Value Object mit Formatvalidierung (gültiges E-Mail-Format) implementiert
- [ ] `CustomerId` und `InvoiceId` Value Objects mit entsprechender Validierung implementiert
- [ ] `InvoiceStatus` als typsichere Enumeration mit erlaubten Werten implementiert
- [ ] Alle Value Objects sind unveränderlich (immutable)
- [ ] Validierung ist in den Konstruktoren der Value Objects implementiert
- [ ] Alle bestehenden Tests laufen weiterhin erfolgreich durch
- [ ] Code ist besser lesbar und typsicher
- [ ] Keine magischen Strings oder Zahlen mehr im Code

## Hinweise

- Beginne mit dem `Money` Value Object, da es die komplexeste Validierung benötigt
- Verwende Enums oder konstante Werte für `InvoiceStatus` mit erlaubten Statusübergängen
- E-Mail-Validierung kann mit regulären Ausdrücken oder PHPs `filter_var()` Funktion erfolgen
- Value Objects sollten `equals()` Methoden implementieren (PHP hat keine `hashCode()`)
- Alle Value Objects müssen unveränderlich sein - keine Setter-Methoden!
- Bei Validierungsfehlern sollten aussagekräftige Exceptions geworfen werden
- Die Tests zeigen dir das erwartete Verhalten - ändere es nicht!

## Tests ausführen

Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/CodeSmells/PrimitiveObsession/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\CodeSmells\PrimitiveObsession\
```

## Dateien

- `InvoiceGenerator.php` - Die Hauptklasse mit Primitive Obsession Problem
- `InvoiceGeneratorTest.php` - Tests die das gewünschte Verhalten definieren