# Hint 2: Berechnungen extrahieren

## Was zu tun ist

Jetzt extrahiere die verschiedenen Berechnungslogiken in separate Methoden.

## Identifizierte Berechnungsblöcke

1. **Subtotal berechnen** (Zeilen ~32-36): Summiert alle Item-Preise
2. **Rabatt berechnen** (Zeilen ~38-50): Verschiedene Rabattregeln
3. **Steuer berechnen** (Zeilen ~52-70): Länderspezifische Steuersätze

## Deine nächsten Schritte

Extrahiere diese drei Methoden:

```python
def _calculate_subtotal(self, items: list[dict[str, Any]]) -> float:
    """Calculate subtotal from order items."""
    subtotal = 0.0
    for item in items:
        subtotal += item['price'] * item['quantity']
    return subtotal

def _calculate_discount(self, subtotal: float, order_data: OrderData) -> float:
    """Calculate discount based on order value and rules."""
    # Rabattlogik hier verschieben

def _calculate_tax(self, taxable_amount: float, shipping_address: dict[str, str]) -> float:
    """Calculate tax based on shipping address."""
    # Steuerberechnungslogik hier verschieben
```

## Tipp für die Steuerberechnung

Du kannst die if-elif Kette durch ein Dictionary oder eine separate Methode ersetzen:

```python
def _get_tax_rate_for_country(self, country: str) -> float:
    """Get tax rate for given country."""
    tax_rates = {
        'DE': 0.19,
        'FR': 0.20,
        'IT': 0.22,
        'US': 0.08,
    }
    return tax_rates.get(country, 0.19)  # Default to German tax rate
```

## Python-Tipps

- Nutze Type Hints für alle Parameter und Rückgabewerte
- Verwende aussagekräftige Variable-Namen
- Behalte die Dataclass-Struktur bei für bessere Typensicherheit

## Nächster Schritt

Als letztes werden wir die Bestellungserstellung und Benachrichtigungen extrahieren.