# Divergent Change - Trennung von Verantwortlichkeiten

## Aufgabenstellung

Du arbeitest an einem E-Commerce-System und hast eine `CustomerService` Klasse geerbt, die über die Jahre gewachsen ist. Diese Klasse verwaltet alle Aspekte rund um Kunden - von der Registrierung über die Kontaktdatenverwaltung bis hin zu Marketing-Aktionen und Bestellhistorie. Das Problem: Die Klasse ändert sich ständig aus verschiedenen Gründen.

## Problem(e)

Die `CustomerService` Klasse leidet unter **Divergent Change** - einem Code Smell, bei dem eine Klasse häufig aus verschiedenen, unabhängigen Gründen geändert werden muss:

1. **Multiple Änderungsgründe**: Die Klasse muss geändert werden bei Änderungen an Authentifizierungslogik, Marketing-Features, Adressverwaltung oder Bestellhistorie
2. **Violation des Single Responsibility Principle**: Eine Klasse hat zu viele Verantwortlichkeiten
3. **Hohe Kopplung**: Verschiedene Concerns sind miteinander vermischt
4. **Schwer testbar**: Tests müssen viele unabhängige Bereiche abdecken
5. **Riskante Änderungen**: Eine Änderung in einem Bereich kann ungewollt andere Bereiche beeinflussen

## Was zu tun ist

Refactoriere die `CustomerService` Klasse durch systematische Trennung der Verantwortlichkeiten:

1. **Analysiere** die `CustomerService` Klasse und identifiziere verschiedene Concerns/Verantwortlichkeiten
2. **Identifiziere** mindestens 3-4 verschiedene Änderungsgründe in der Klasse
3. **Extrahiere** separate Service-Klassen für jeden identifizierten Concern:
   - Authentifizierung und Account-Verwaltung
   - Kontaktdaten und Adressverwaltung  
   - Marketing und Kommunikation
   - Bestellhistorie und Kaufverhalten
4. **Definiere** klare Interfaces für jeden Service
5. **Implementiere** Dependency Injection in der ursprünglichen `CustomerService` Klasse
6. **Stelle sicher**, dass die ursprüngliche API nach außen unverändert bleibt

## Akzeptanzkriterien

- [ ] Die ursprüngliche `CustomerService` Klasse hat maximal 50 Zeilen Code
- [ ] Mindestens 3 separate Service-Klassen wurden extrahiert
- [ ] Jede Service-Klasse hat eine einzige, klar definierte Verantwortlichkeit
- [ ] Alle Services haben saubere, interface-basierte Contracts
- [ ] Die ursprüngliche öffentliche API der `CustomerService` bleibt unverändert
- [ ] Dependency Injection wird verwendet (kein `new` in der `CustomerService`)
- [ ] Alle bestehenden Tests laufen weiterhin durch
- [ ] Jeder Service kann unabhängig getestet werden
- [ ] Zirkuläre Abhängigkeiten zwischen Services sind vermieden

## Hinweise

- Beginne mit der Identifikation der verschiedenen Änderungsgründe - schreibe sie auf!
- Nutze das "Extract Class" Refactoring schrittweise, nicht alles auf einmal
- Achte auf Methoden, die zusammengehörige Daten verwenden - diese gehören oft in denselben Service
- Die bestehenden Tests zeigen dir, welche Funktionalität erhalten bleiben muss
- Verwende aussagekräftige Namen für die neuen Service-Klassen (z.B. `CustomerAuthenticationService`, `CustomerContactService`)
- Dependency Injection kann über Constructor Injection implementiert werden

## Tests ausführen

Vom php-Verzeichnis ausgehend:

**Unter Linux/macOS:**
```bash
vendor/bin/phpunit exercises/CodeSmells/DivergentChange/
```

**Unter Windows:**
```cmd
vendor\bin\phpunit.bat exercises\CodeSmells\DivergentChange\
```

## Dateien

- `CustomerService.php` - Die zu refactorierende Klasse
- `CustomerServiceTest.php` - Tests für die Funktionalität
- `hints/` - Gestaffelte Hinweise zum Vorgehen
- `solution/` - Musterlösung mit refactoriertem Code