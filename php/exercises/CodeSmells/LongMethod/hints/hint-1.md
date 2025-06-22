# Hinweis 1: Validierung extrahieren

## Was zu tun ist
Beginne mit dem ersten logischen Block - der Validierung der Eingabedaten.

## Analyse der aktuellen Methode
Die `processOrder()` Methode beginnt mit einem großen Validierungsblock (Zeilen 14-31). Dieser Block:
- Prüft ob `customer_id` vorhanden ist
- Validiert das `items` Array 
- Prüft jedes einzelne Item
- Validiert die Versandadresse

## Dein erster Schritt
Extrahiere eine neue Methode `validateOrderData(array $orderData): void`

## Beispiel
```php
private function validateOrderData(array $orderData): void
{
    if (empty($orderData['customer_id'])) {
        throw new \InvalidArgumentException('Customer ID is required');
    }
    
    // ... weitere Validierungen
}
```

## Warum das hilft
- Die Hauptmethode wird sofort kürzer und übersichtlicher
- Die Validierungslogik ist klar abgegrenzt
- Der Code wird leichter zu testen

## Nächster Schritt
Nach der Validierung kommt die Berechnung des Subtotals - das wird unser nächster Refactoring-Schritt sein.