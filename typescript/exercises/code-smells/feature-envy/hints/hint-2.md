# Hint 2: Verschiebe Customer-bezogene Methoden

## Was zu tun ist

Verschiebe die Customer-bezogenen Methoden von `OrderCalculator` zur `Customer` Klasse.

## Beispiel: calculateCustomerDiscount()

```php
// In Customer.php hinzufügen:
public function calculateDiscount(): float
{
    $customerType = $this->getType();
    $loyaltyYears = $this->getLoyaltyYears();

    if ($customerType === 'vip') {
        return 0.15 + min($loyaltyYears * 0.01, 0.10);
    }

    if ($customerType === 'premium') {
        return 0.10 + min($loyaltyYears * 0.005, 0.05);
    }

    if ($customerType === 'standard') {
        if ($loyaltyYears >= 5) {
            return 0.05;
        }
        if ($loyaltyYears >= 2) {
            return 0.02;
        }
    }

    return 0.0;
}
```

## Anpassung in OrderCalculator

```php
// In OrderCalculator.php:
public function calculateCustomerDiscount(Order $order): float
{
    return $order->getCustomer()->calculateDiscount();
}
```

## Weitere Methoden

Verschiebe auch:
- `calculateTaxRate()` → `Customer::getTaxRate()`
- `isEligibleForFreeShipping()` → `Customer::isEligibleForFreeShipping(float $orderValue)`
- `getCustomerPriorityLevel()` → `Customer::getPriorityLevel()`

## Nächster Schritt

Verschiebe **Product-bezogene Methoden** zur `Product` Klasse (siehe `hint-3.md`).