# Hint 1: Problem erkennen und Verantwortlichkeiten identifizieren

## Was zu tun ist

Analysiere die `CustomerService` Klasse gründlich und identifiziere die verschiedenen Änderungsgründe. Divergent Change bedeutet, dass eine Klasse aus verschiedenen, unabhängigen Gründen geändert werden muss.

**Fragen zum Nachdenken:**
- Welche verschiedenen Bereiche der Geschäftslogik sind in der Klasse vermischt?
- Wann müsste die Klasse geändert werden, wenn sich Authentifizierungsregeln ändern?
- Wann müsste sie geändert werden, wenn sich Marketing-Kanäle ändern?
- Wann müsste sie geändert werden, wenn sich die Adressverwaltung ändert?
- Wann müsste sie geändert werden, wenn sich Bestellungsregeln ändern?

**Tipp:** Schaue dir die Methoden in der Klasse an und gruppiere sie gedanklich. Welche Methoden arbeiten mit ähnlichen Daten oder haben verwandte Verantwortlichkeiten?

## Worauf achten

- **Single Responsibility Principle**: Jede Klasse sollte nur einen Grund zur Änderung haben
- **Cohesion**: Zusammengehörige Funktionalitäten sollten gruppiert werden
- **Separation of Concerns**: Verschiedene Geschäftsbereiche sollten getrennt werden

**Identifiziere mindestens 4 verschiedene Concerns:**
1. Was gehört zur Authentifizierung und Account-Verwaltung?
2. Was gehört zur Kontaktdaten- und Adressverwaltung?
3. Was gehört zum Marketing und zur Kommunikation?
4. Was gehört zur Bestellhistorie und Analytics?

## Nächster Schritt

Bevor du mit dem Refactoring beginnst, erstelle eine Liste oder Notizen mit den identifizierten Concerns. Notiere dir auch, welche Methoden zu welchem Concern gehören. Das wird dir beim nächsten Schritt helfen, wenn du die Services extrahierst.