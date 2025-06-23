# Hint 3: Refactoriere InvoiceGenerator und optimiere Type Safety

## Was zu tun ist

- Ersetze alle primitiven Parameter und Rückkehrwerte durch Value Objects
- Passe Interface-Definitionen an um Value Objects zu verwenden
- Nutze TypeScript's Inference und Type Guards für bessere Entwicklererfahrung
- Teste alle Edge Cases und Validierungsregeln

## Integration der Value Objects

**InvoiceGenerator Refactoring:**
- Welche Method-Signaturen müssen angepasst werden?
- Wie ändern sich die Interface-Definitionen für Invoice und InvoiceItem?
- Wo musst du Value Objects erstellen vs. primitive Werte verwenden?
- Sollen die Tests unverändert bleiben oder Value Objects direkt verwenden?

**Fehlerbehandlung optimieren:**
- Value Objects werfen ihre eigenen spezifischen Fehler
- InvoiceGenerator sollte diese weiterleiten oder wrappen?
- Wie bleibt der Exception-Kontext erhalten?

**Type Safety maximieren:**
- Generic Constraints für Currency-spezifische Operationen?
- Branded Types um ID-Verwechslung zur Compile-Time zu verhindern?
- Exhaustive Checking für Union Types?

## Worauf achten

- **Backward Compatibility**: Tests sollten weiterhin funktionieren
- **Performance**: Value Object Erstellung nicht in Loops
- **Memory**: Immutable Objects können Memory-Overhead haben
- **Consistency**: Alle primitiven Domänen-Konzepte sollten ersetzt sein
- **Domain Logic**: Business Rules gehören in die Value Objects, nicht in InvoiceGenerator

## Qualitätsprüfung

- **Compile-Time Checks**: Nutzt TypeScript alle verfügbaren Type-Checks?
- **Runtime Validation**: Sind alle Geschäftsregeln in Value Objects gekapselt?
- **Test Coverage**: Funktionieren alle ursprünglichen Tests weiterhin?
- **Code Readability**: Ist der Code verständlicher und weniger fehleranfällig?
- **Maintainability**: Sind neue Features einfacher hinzuzufügen?

## Finalisierung

Prüfe ob alle magischen Strings und Zahlen eliminiert wurden. Sind Validierungen konsistent und zentral? Nutzt der Code TypeScript's Stärken optimal aus?