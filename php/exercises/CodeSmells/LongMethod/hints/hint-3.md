# Hinweis 3: Finale Struktur - Persistence und Benachrichtigungen

## Was zu tun ist
Extrahiere die letzten beiden Verantwortlichkeiten: Datenspeicherung und Benachrichtigungen.

## Verbleibende Blöcke
1. **Bestelldaten erstellen** (Zeilen 79-92): Order-Array zusammenstellen
2. **Bestellung speichern** (Zeile 95): In interne Liste einträgen  
3. **Benachrichtigungen senden** (Zeilen 97-116): Kunde und ggf. Admin informieren

## Deine finalen Methoden

```php
private function createOrderRecord(array $orderData, float $subtotal, float $discount, float $tax, float $total): array
{
    $orderId = uniqid('order_', true);
    
    return [
        'id' => $orderId,
        'customer_id' => $orderData['customer_id'],
        // ... weitere Felder
    ];
}

private function saveOrder(array $order): void
{
    $this->orders[$order['id']] = $order;
}

private function sendNotifications(array $order): void
{
    $this->sendCustomerNotification($order);
    
    if ($order['total'] > 500.0) {
        $this->sendHighValueOrderNotification($order);
    }
}
```

## Bonus-Tipp: Weitere Extraktion
Du kannst die Benachrichtigungslogiken noch weiter aufteilen:

```php
private function sendCustomerNotification(array $order): void
{
    // Kundenbenachrichtigung erstellen und versenden
}

private function sendHighValueOrderNotification(array $order): void  
{
    // Admin-Benachrichtigung für hohe Bestellwerte
}
```

## Das Endergebnis
Deine `processOrder()` Methode sollte jetzt nur noch etwa 12 Zeilen haben und sehr gut lesbar sein:

```php
public function processOrder(array $orderData): array
{
    $this->validateOrderData($orderData);
    
    $subtotal = $this->calculateSubtotal($orderData['items']);
    $discount = $this->calculateDiscount($subtotal, $orderData);
    $tax = $this->calculateTax($subtotal - $discount, $orderData['shipping_address']);
    $total = ($subtotal - $discount) + $tax;
    
    $order = $this->createOrderRecord($orderData, $subtotal, $discount, $tax, $total);
    $this->saveOrder($order);
    $this->sendNotifications($order);
    
    return $order;
}
```

Herzlichen Glückwunsch! Du hast erfolgreich eine Long Method refactoriert! 🎉