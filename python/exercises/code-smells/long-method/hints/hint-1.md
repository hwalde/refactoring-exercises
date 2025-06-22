# Hint 1: Identifiziere die logischen Blöcke

## Was zu tun ist
Schau dir die `process_order()` Methode genau an und identifiziere die verschiedenen logischen Abschnitte.

## Die Blöcke sind:
1. **Validierung** (Zeile ~15-30): Prüfung von customer_id, items, shipping_address
2. **Subtotal-Berechnung** (Zeile ~32-36): Summierung aller Artikel
3. **Rabatt-Berechnung** (Zeile ~38-50): Verschiedene Rabattregeln
4. **Steuer-Berechnung** (Zeile ~52-70): Länder-spezifische Steuersätze
5. **Order-Erstellung** (Zeile ~72-95): Order-Objekt zusammenbauen
6. **Speicherung** (Zeile ~97): In _orders Dict
7. **Benachrichtigungen** (Zeile ~99-120): Customer + Admin Notifications

## Nächster Schritt
Beginne mit dem ersten Block (Validierung) und extrahiere ihn in eine separate Methode namens `_validate_order_data()`.

## Beispiel
```python
def _validate_order_data(self, order_data: OrderData) -> None:
    """Validate order data and raise ValueError if invalid."""
    # Validierungslogik hier hinein verschieben
```

## Python Tipp
Nutze die vorhandenen Type Hints und dataclasses für bessere Struktur.