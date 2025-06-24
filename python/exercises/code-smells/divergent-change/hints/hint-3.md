# Hint 3: Integration und Qualitätssicherung

## Was zu tun ist

Du bist fast fertig! Jetzt geht es darum, alle Services sauber zu integrieren und die Qualität zu sichern. Die ursprüngliche `CustomerService` sollte jetzt hauptsächlich als Facade fungieren, die Calls an die spezialisierten Services delegiert.

**Integration der Services:**
- Die `CustomerService` sollte die Service-Instanzen über Dependency Injection erhalten
- Jeder öffentliche Aufruf wird an den entsprechenden Service weitergeleitet
- Die ursprüngliche API bleibt vollständig erhalten
- Keine Geschäftslogik mehr in der `CustomerService` - nur noch Delegation

**Fragen zum Nachdenken:**
- Sind alle Services über ihre Interfaces ansprechbar?
- Bleibt die öffentliche API der `CustomerService` unverändert?
- Können Services unabhängig getestet werden?
- Gibt es zirkuläre Abhängigkeiten zwischen Services?
- Ist der Code nach den Änderungen noch type-safe?

## Worauf achten

**Dependency Injection:**
- Services werden über Constructor Parameter injiziert
- Default-Implementierungen können bereitgestellt werden
- Services sind austauschbar durch ihre Interfaces
- Keine `new`/direkte Instanziierung in der `CustomerService`

**Testing Strategy:**
- Originale Tests sollten weiterhin grün sein
- Jeder Service kann isoliert getestet werden
- Mock-Objects können für Service-Dependencies verwendet werden
- Integration Tests für die Facade-Funktionalität

**Code Quality Checks:**
- Laufen alle Tests weiterhin?
- Ist der Code PEP 8 konform? (black, ruff)
- Sind alle Type Hints korrekt? (mypy)
- Hat die `CustomerService` weniger als 50 Zeilen?
- Sind die Services wirklich unabhängig?

## Nächster Schritt

Führe alle Qualitätsprüfungen durch:
1. Tests laufen lassen
2. Code-Style prüfen
3. Type Checking durchführen
4. Akzeptanzkriterien aus der Task-Beschreibung abgleichen

Wenn alles grün ist, hast du erfolgreich das Divergent Change Problem gelöst und saubere, fokussierte Services erstellt!