# Hint 1: Identifiziere Feature Envy

## Was zu tun ist

Analysiere die `OrderCalculator` Methoden und identifiziere, welche Daten sie hauptsächlich verwenden. Feature Envy liegt vor, wenn eine Methode mehr Daten von anderen Objekten nutzt als von ihrem eigenen Objekt.

## Methoden mit Feature Envy

1. **Customer-bezogene Methoden**:
   - `calculateCustomerDiscount()` - nutzt hauptsächlich Customer-Daten
   - `calculateTaxRate()` - nutzt Customer-Typ
   - `isEligibleForFreeShipping()` - nutzt Customer-Typ und -Loyalität
   - `getCustomerPriorityLevel()` - nutzt Customer-Daten

2. **Product-bezogene Methoden**:
   - `calculateProductShippingCost()` - nutzt Product-Gewicht, Kategorie, etc.
   - `requiresSpecialHandling()` - nutzt Product-Eigenschaften

3. **Order-bezogene Methoden**:
   - `calculateOrderSubtotal()` - nutzt Order-Items
   - `calculateOrderWeight()` - nutzt Order-Items
   - `calculateShippingCost()` - nutzt Order-Daten
   - `hasSpecialHandlingItems()` - nutzt Order-Items

## Nächster Schritt

Beginne mit der Verschiebung von **Customer-bezogenen Methoden** zur `Customer` Klasse. Diese haben die klarste Zugehörigkeit.

Siehe `hint-2.md` für die konkrete Umsetzung.