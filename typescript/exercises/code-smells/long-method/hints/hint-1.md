# Hint 1: Identifiziere die logischen Blöcke

## Was zu tun ist
Schau dir die `processOrder()` Methode genau an und identifiziere die verschiedenen logischen Abschnitte.

## Die Blöcke sind:
1. **Validierung** (Zeile ~15-30): Prüfung von customer_id, items, shipping_address
2. **Subtotal-Berechnung** (Zeile ~32-36): Summierung aller Artikel
3. **Rabatt-Berechnung** (Zeile ~38-50): Verschiedene Rabattregeln
4. **Steuer-Berechnung** (Zeile ~52-70): Länder-spezifische Steuersätze
5. **Order-Erstellung** (Zeile ~72-85): Order-Objekt zusammenbauen
6. **Speicherung** (Zeile ~87): In orders Map
7. **Benachrichtigungen** (Zeile ~89-110): Customer + Admin Notifications

## Nächster Schritt
Beginne mit dem ersten Block (Validierung) und extrahiere ihn in eine separate Methode namens `validateOrderData()`.

## Beispiel
```typescript
private validateOrderData(orderData: OrderData): void {
  // Validierungslogik hier hinein verschieben
}
```

## TypeScript Tipp
Nutze die vorhandenen Interfaces (`OrderData`, `OrderItem`, etc.) für bessere Typsicherheit.