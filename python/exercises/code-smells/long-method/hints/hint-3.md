# Hint 3: Finale Struktur - Persistence und Benachrichtigungen

## Was zu tun ist

Extrahiere die letzten beiden Verantwortlichkeiten: Datenspeicherung und Benachrichtigungen.

## Verbleibende Blöcke

1. **Bestelldaten erstellen** (Zeilen ~72-95): Order-Objekt zusammenstellen
2. **Bestellung speichern** (Zeile ~97): In interne Liste eintragen
3. **Benachrichtigungen senden** (Zeilen ~99-120): Kunde und ggf. Admin informieren

## Deine finalen Methoden

```python
def _create_order_record(
    self, 
    order_data: OrderData, 
    subtotal: float, 
    discount: float, 
    tax: float, 
    total: float
) -> Order:
    """Create Order object from calculated values."""
    order_id = f"order_{uuid.uuid4().hex[:12]}"
    
    return Order(
        id=order_id,
        customer_id=order_data.customer_id,
        # ... weitere Felder setzen
    )

def _save_order(self, order: Order) -> None:
    """Save order to internal storage."""
    self._orders[order.id] = order

def _send_notifications(self, order: Order) -> None:
    """Send notifications for the order."""
    self._send_customer_notification(order)
    
    if order.total > 500.0:
        self._send_high_value_order_notification(order)
```

## Bonus-Tipp: Weitere Extraktion

Du kannst die Benachrichtigungslogiken noch weiter aufteilen:

```python
def _send_customer_notification(self, order: Order) -> None:
    """Send confirmation notification to customer."""
    # Kundenbenachrichtigung erstellen und versenden

def _send_high_value_order_notification(self, order: Order) -> None:
    """Send admin notification for high-value orders."""
    # Admin-Benachrichtigung für hohe Bestellwerte
```

## Das Endergebnis

Deine `process_order()` Methode sollte jetzt nur noch etwa 12 Zeilen haben und sehr gut lesbar sein:

```python
def process_order(self, order_data: OrderData) -> Order:
    """Process an order through validation, calculation, and notification."""
    self._validate_order_data(order_data)
    
    subtotal = self._calculate_subtotal(order_data.items)
    discount = self._calculate_discount(subtotal, order_data)
    tax = self._calculate_tax(subtotal - discount, order_data.shipping_address)
    total = (subtotal - discount) + tax
    
    order = self._create_order_record(order_data, subtotal, discount, tax, total)
    self._save_order(order)
    self._send_notifications(order)
    
    return order
```

## Qualitätsprüfung

Bevor du fertig bist, prüfe:

- **Sind alle Methoden fokussiert?** Jede Methode hat nur eine Verantwortlichkeit
- **Sind die Namen aussagekräftig?** Methodennamen beschreiben, was sie tun
- **Funktionieren die Tests noch?** Alle ursprünglichen Tests sollten grün bleiben
- **Ist der Code lesbarer geworden?** Die Hauptmethode ist wie eine Geschichte lesbar

Herzlichen Glückwunsch! Du hast erfolgreich eine Long Method refactoriert! 🎉