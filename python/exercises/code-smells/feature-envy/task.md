---
slug: feature-envy
title: "Feature Envy - OrderCalculator refactorieren"
difficulty: advanced
estimated_time: 40min
concepts: [move-method, tell-dont-ask, feature-envy]
prerequisites: []
---

# Feature Envy - OrderCalculator refactorieren

## Aufgabenstellung

Die `OrderCalculator` Klasse zeigt das "Feature Envy" Code-Smell: Ihre Methoden nutzen hauptsächlich Daten und Methoden von anderen Objekten (`Order`, `Customer`, `Product`) anstatt ihrer eigenen Daten. Dies führt zu langen Getter-Ketten und verletzt das "Tell, don't ask" Prinzip.

Die Klasse berechnet verschiedene Aspekte von Bestellungen, aber die Logik gehört eigentlich zu den jeweiligen Domain-Objekten.

## Code-Smells

- **Feature Envy**: Methoden nutzen hauptsächlich Daten anderer Klassen
- **Getter Chains**: Lange Ketten von Getter-Aufrufen (`order.getCustomer().getType()`)
- **Misplaced Responsibility**: Geschäftslogik ist nicht dort wo die Daten sind

## Was zu tun ist

Verschiebe die Methoden von `OrderCalculator` zu den Klassen, deren Daten sie hauptsächlich verwenden:

1. **Kundenbezogene Berechnungen** → zu `Customer` Klasse verschieben
2. **Produktbezogene Berechnungen** → zu `Product` Klasse verschieben  
3. **Bestellbezogene Berechnungen** → zu `Order` Klasse verschieben
4. **OrderCalculator** sollte nur noch koordinieren, nicht mehr selbst rechnen

## Akzeptanzkriterien

- ✅ Alle bestehenden Tests bleiben grün
- ✅ Getter-Ketten sind eliminiert (`order.getCustomer().getType()` → `order.getCustomerType()`)
- ✅ "Tell, don't ask" Prinzip wird angewendet
- ✅ Geschäftslogik ist bei den entsprechenden Daten
- ✅ Public API der OrderCalculator bleibt funktional gleich
- ✅ Type Declarations bleiben vollständig erhalten

## Hinweise

- Verwende "Move Method" Refactoring um Methoden zu verschieben
- Erstelle neue Methoden in den Domain-Objekten die die Geschäftslogik kapseln
- Halte die OrderCalculator API kompatibel (Tests müssen grün bleiben)
- Eliminiere direkte Zugriffe auf Getter der eingebetteten Objekte

## Tests ausführen

```bash
# Python (vom refactoring-exercises/ Ordner)
cd python && source venv/bin/activate && pytest exercises/code-smells/feature-envy/tests/ -v

# Code-Style prüfen
cd python && black --check exercises/code-smells/feature-envy/
cd python && ruff check exercises/code-smells/feature-envy/
cd python && mypy exercises/code-smells/feature-envy/src/
```

## Dateien

- `src/order_calculator.py` - Die zu refactorierende Klasse (zeigt Feature Envy)
- `src/order.py` - Bestellung Domain-Objekt
- `src/customer.py` - Kunde Domain-Objekt  
- `src/product.py` - Produkt Domain-Objekt
- `tests/test_order_calculator.py` - Tests die grün bleiben müssen