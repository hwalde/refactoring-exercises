# Hint 2: Extrahiere Berechnungsmethoden

## Was zu tun ist

Nachdem du die Validierung extrahiert hast, konzentriere dich nun auf die Berechnungslogik. Diese kann in mehrere spezifische Methoden aufgeteilt werden.

## Methoden zu extrahieren

### 1. Subtotal-Berechnung
```typescript
private calculateSubtotal(items: OrderItem[]): number {
  // Summiere alle item.price * item.quantity
}
```

### 2. Rabatt-Berechnung
```typescript
private calculateDiscount(subtotal: number, customerType: string, isFirstOrder: boolean): number {
  // Verschiedene Rabattregeln basierend auf Kundenstatus
}
```

### 3. Steuer-Berechnung
```typescript
private calculateTax(subtotal: number, country: string): number {
  // Länder-spezifische Steuersätze anwenden
}
```

## Leitfragen zum Nachdenken

- Welche Parameter braucht jede Methode?
- Welche Rückgabetypen sind angemessen?
- Können Zwischenergebnisse wiederverwendet werden?
- Wie bleiben die Berechnungen nachvollziehbar?

## Worauf achten

### Typsicherheit
- Verwende spezifische TypeScript-Types für Parameter
- Nutze Union Types für begrenzte Wertebereiche (z.B. Länder)
- Definiere klare Rückgabetypen

### Fehlerbehandlung
- Berücksichtige ungültige Eingaben
- Verwende aussagekräftige Fehlermeldungen
- Stelle sicher, dass Berechnungen robust sind

### Lesbarkeit
- Verwende beschreibende Variablennamen
- Kommentiere komplexe Berechnungsregeln
- Halte die Methoden kurz und fokussiert

## Nächster Schritt

Nach dem Extrahieren der Berechnungsmethoden sollte deine `processOrder()` Methode deutlich kürzer und übersichtlicher werden. Der nächste Schritt ist die Extraktion der verbleibenden Logik (Order-Erstellung und Benachrichtigungen).