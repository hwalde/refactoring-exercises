# Inline Method Mini - ProductCatalogService

## Aufgabenstellung
Du arbeitest an einem E-Commerce-System und bist für die Wartung des `ProductCatalogService` verantwortlich. Der Service enthält eine überflüssige Methode `is_product_available()`, die lediglich die Methode `check_product_stock()` aufruft. Diese unnötige Zwischenmethode macht den Code komplizierter als nötig und soll durch Inline Method beseitigt werden.

## Problem(e)
- **Unnecessary Indirection**: Die `is_product_available()` Methode ruft nur `check_product_stock()` auf
- **Code Duplication**: Der Methodenname spiegelt bereits die Funktionalität von `check_product_stock()` wider  
- **Reduced Readability**: Entwickler müssen zusätzliche Methodenebenen durchgehen, um die eigentliche Logik zu verstehen

## Was zu tun ist
1. **Analysiere** die `is_product_available()` Methode und ihre Verwendung in der Klasse
2. **Identifiziere** alle Stellen, wo `is_product_available()` aufgerufen wird
3. **Ersetze** alle Aufrufe von `is_product_available()` durch direkte Aufrufe von `check_product_stock()`
4. **Entferne** die überflüssige `is_product_available()` Methode vollständig
5. **Verifiziere**, dass alle Tests weiterhin erfolgreich durchlaufen

## Akzeptanzkriterien
- [ ] Die Methode `is_product_available()` wurde vollständig entfernt
- [ ] Alle vorherigen Aufrufe von `is_product_available()` wurden durch direkte `check_product_stock()` Aufrufe ersetzt
- [ ] Der Code ist klarer und direkter ohne unnötige Methodenebenen
- [ ] Alle bestehenden Tests laufen erfolgreich durch
- [ ] Die Funktionalität des Services bleibt unverändert

## Hinweise
- Verwende die "Find Usages" Funktion deiner IDE, um alle Verwendungen von `is_product_available()` zu finden
- Prüfe, ob der Methodenname `check_product_stock()` aussagekräftig genug ist
- Achte darauf, dass keine Tests oder andere Klassen die zu entfernende Methode verwenden
- Bei Unsicherheiten: Schaue in die `/hints/` für gestaffelte Hilfestellungen

## Tests ausführen

**Unter Linux/macOS:**
```bash
source venv/bin/activate && pytest exercises/basis-refactorings/inline-method-mini/tests/ -v
```

**Unter Windows:**
```cmd
venv\Scripts\activate && pytest exercises\basis-refactorings\inline-method-mini\tests\ -v
```

## Dateien
- `product_catalog_service.py` - Hauptklasse mit der zu refactorierenden Logik
- `test_product_catalog_service.py` - Tests die das Verhalten definieren