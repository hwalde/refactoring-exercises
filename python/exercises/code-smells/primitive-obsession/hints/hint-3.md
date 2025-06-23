# Hint 3: Refactoring abschließen und Qualität sicherstellen

## Was zu tun ist

- Ersetze alle primitiven Parameter in der `InvoiceGenerator` Klasse durch Value Objects
- Aktualisiere alle Methoden-Signaturen mit den neuen Typen
- Stelle sicher, dass die Validierung aus der `InvoiceGenerator` Klasse in die Value Objects verschoben wurde
- Führe die Tests aus um zu prüfen, ob das Verhalten gleich geblieben ist

## Refactoring-Checkliste

**Parameter-Ersetzung:**
- `customer_id: str` → `customer_id: CustomerId`
- `customer_email: str` → `customer_email: EmailAddress`
- `currency: str` → wird Teil des `Money` Value Objects
- `new_status: str` → `new_status: InvoiceStatus`

**Return-Typ Anpassungen:**
- Sollen Methoden weiterhin Dictionaries zurückgeben oder eigene Datenstrukturen?
- Wie behandelst du die Kompatibilität mit bestehenden Tests?

**Validierung verschieben:**
- Entferne alle Validierungs-if-Statements aus `InvoiceGenerator`
- Die Value Objects sollten jetzt für die Validierung zuständig sein
- Welche Exceptions werfen die Value Objects bei ungültigen Werten?

## Worauf achten

- **Tests bleiben grün**: Nach jedem Refactoring-Schritt sollten die Tests weiterhin bestehen
- **Schrittweise Änderungen**: Refactoriere eine Methode nach der anderen
- **Backwards-Kompatibilität**: Die Test-Schnittstelle sollte gleich bleiben
- **Clean Code**: Ist der Code jetzt lesbarer und typsicherer geworden?

## Qualitätsprüfung

**Führe folgende Validierungen durch:**
- Laufen alle Tests? (`pytest`)
- Ist der Code formatiert? (`black`)
- Keine Linter-Warnungen? (`ruff`)
- Type-Checking erfolgreich? (`mypy`)

**Frage dich abschließend:**
- Sind alle "magischen Strings" und Zahlen verschwunden?
- Ist die Geschäftslogik jetzt in den richtigen Klassen gekapselt?
- Würde ein neuer Entwickler den Code schneller verstehen?

## Nächster Schritt

Nachdem alle Tests grün sind, betrachte die Lösung kritisch: Wo könntest du noch weitere Verbesserungen vornehmen? Gibt es weitere Code Smells die du entdeckst?