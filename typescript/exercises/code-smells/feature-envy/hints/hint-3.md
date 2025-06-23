# Hint 3: Finale Refactoring-Struktur

## Was zu tun ist

Vervollständige das Refactoring durch Verschieben der restlichen Methoden und erstelle eine saubere Architektur.

## Product-Methoden verschieben

```php
// In Product.php hinzufügen:
public function calculateShippingCost(int $quantity): float
{
    $weight = $this->getWeight();
    $isFragile = $this->isFragile();
    $category = $this->getCategory();

    $baseCost = $weight * $quantity * 0.5;

    // Kategorie-spezifische Kosten...
    // Fragile-Zuschlag...
    
    return round($baseCost, 2);
}

public function requiresSpecialHandling(): bool
{
    return $this->isFragile() || 
           $this->getWeight() > 20.0 || 
           $this->getCategory() === 'electronics';
}
```

## Order-Methoden verschieben

```php
// In Order.php hinzufügen:
public function calculateSubtotal(): float
{
    $subtotal = 0.0;
    foreach ($this->getItems() as $item) {
        $subtotal += $item['product']->getPrice() * $item['quantity'];
    }
    return round($subtotal, 2);
}

public function calculateWeight(): float
{
    $totalWeight = 0.0;
    foreach ($this->getItems() as $item) {
        $totalWeight += $item['product']->getWeight() * $item['quantity'];
    }
    return round($totalWeight, 2);
}

public function hasSpecialHandlingItems(): bool
{
    foreach ($this->getItems() as $item) {
        if ($item['product']->requiresSpecialHandling()) {
            return true;
        }
    }
    return false;
}
```

## Finale OrderCalculator Struktur

```php
class OrderCalculator
{
    public function calculateTotal(Order $order): array
    {
        // Delegiert an die Domain-Objekte
        $subtotal = $order->calculateSubtotal();
        $discount = $order->getCustomer()->calculateDiscount();
        $taxRate = $order->getCustomer()->getTaxRate();
        // ... koordiniert nur noch die Berechnungen
    }
}
```

## Erfolgskontrolle

- ✅ Alle Tests bleiben grün
- ✅ OrderCalculator koordiniert nur noch, rechnet nicht mehr selbst
- ✅ Geschäftslogik ist bei den entsprechenden Daten
- ✅ "Tell, don't ask" Prinzip wird angewendet
- ✅ Getter-Ketten sind eliminiert