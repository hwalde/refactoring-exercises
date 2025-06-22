# Hinweis 2: Berechnungen extrahieren

## Was zu tun ist
Jetzt extrahieren wir die verschiedenen Berechnungslogiken in separate Methoden.

## Identifizierte Berechnungsblöcke
1. **Subtotal berechnen** (Zeilen 33-37): Summiert alle Item-Preise
2. **Rabatt berechnen** (Zeilen 39-53): Verschiedene Rabattregeln
3. **Steuer berechnen** (Zeilen 55-77): Länderspezifische Steuersätze

## Deine nächsten Schritte
Extrahiere diese drei Methoden:

```php
private function calculateSubtotal(array $items): float
{
    $subtotal = 0.0;
    foreach ($items as $item) {
        $subtotal += $item['price'] * $item['quantity'];
    }
    return $subtotal;
}

private function calculateDiscount(float $subtotal, array $orderData): float
{
    // Rabattlogik hier
}

private function calculateTax(float $taxableAmount, array $shippingAddress): float
{
    // Steuerberechnungslogik hier
}
```

## Tipp für die Steuerberechnung
Du kannst die Switch-Anweisung durch ein `match`-Expression ersetzen (PHP 8+):

```php
private function getTaxRateForCountry(string $country): float
{
    return match ($country) {
        'DE' => 0.19,
        'FR' => 0.20,
        'IT' => 0.22,
        'US' => 0.08,
        default => 0.19,
    };
}
```

## Nächster Schritt
Als letztes werden wir die Bestellungserstellung und Benachrichtigungen extrahieren.