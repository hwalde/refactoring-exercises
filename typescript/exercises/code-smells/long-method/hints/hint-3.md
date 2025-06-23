# Hint 3: Finale Schritte und Qualitätssicherung

## Was zu tun ist

Du hast bereits Validierung und Berechnungen extrahiert. Jetzt geht es um die finalen Schritte: Order-Erstellung, Speicherung und Benachrichtigungen.

## Verbleibende Methoden extrahieren

### 1. Order-Erstellung
```typescript
private createOrderObject(
  orderData: OrderData, 
  subtotal: number, 
  discountAmount: number, 
  taxAmount: number
): Order {
  // Order-Objekt mit allen berechneten Werten erstellen
}
```

### 2. Order-Speicherung
```typescript
private saveOrder(order: Order): void {
  // Order in der orders Map speichern
}
```

### 3. Benachrichtigungen
```typescript
private sendNotifications(order: Order): void {
  // Customer und Admin über neue Bestellung informieren
}
```

## Finale processOrder() Methode

Die refactorierte `processOrder()` Methode sollte nun nur noch koordinieren:

```typescript
processOrder(orderData: OrderData): Order {
  this.validateOrderData(orderData);
  
  const subtotal = this.calculateSubtotal(orderData.items);
  const discountAmount = this.calculateDiscount(/* ... */);
  const taxAmount = this.calculateTax(/* ... */);
  
  const order = this.createOrderObject(/* ... */);
  this.saveOrder(order);
  this.sendNotifications(order);
  
  return order;
}
```

## Qualitätsprüfung

### Code-Metriken
- `processOrder()` sollte maximal 15 Zeilen haben
- Jede extrahierte Methode sollte eine klare Verantwortlichkeit haben
- Methodennamen sollten selbsterklärend sein

### TypeScript Best Practices
- Alle Parameter und Rückgabetypen explizit typisiert
- Verwendung von Interfaces für komplexe Datenstrukturen
- Konsistente Fehlerbehandlung

### Testbarkeit
- Jede extrahierte Methode ist theoretisch einzeln testbar
- Die Logik ist in kleinere, überschaubare Einheiten aufgeteilt
- Abhängigkeiten sind klar erkennbar

## Reflexion

### Vorteile des Refactoring
- **Lesbarkeit**: Jede Methode hat einen klaren Zweck
- **Wartbarkeit**: Änderungen können isoliert vorgenommen werden
- **Testbarkeit**: Kleinere Methoden sind einfacher zu testen
- **Wiederverwendbarkeit**: Einzelne Berechnungen können anderweitig genutzt werden

### Lernziele erreicht?
- Verstehst du, warum lange Methoden problematisch sind?
- Kannst du logische Blöcke in Code identifizieren?
- Weißt du, wie man Methoden sinnvoll extrahiert?
- Sind dir die Vorteile des "Extract Method" Refactoring klar?

## Nächster Schritt

Führe alle Tests aus und stelle sicher, dass sie grün bleiben. Überprüfe, ob deine Lösung alle Akzeptanzkriterien erfüllt. Falls nicht, iteriere über deine Extraktion bis alle Anforderungen erfüllt sind.