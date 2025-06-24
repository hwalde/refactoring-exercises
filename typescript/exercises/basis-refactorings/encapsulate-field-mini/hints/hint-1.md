# Hint 1: Das Problem erkennen und erste Schritte

## Was zu tun ist

Schaue dir die aktuelle `User` Klasse genau an. Das `email` Feld ist derzeit öffentlich zugänglich. Das bedeutet, jeder Code kann direkten Zugriff darauf nehmen:

```typescript
const user = new User('John', 'john@example.com');
user.email = 'any-invalid-string'; // Das ist das Problem!
```

**Leitfragen zum Nachdenken:**
- Was passiert, wenn jemand `user.email = '';` setzt?
- Was passiert bei `user.email = 'not-an-email';`?
- Warum könnten andere Teile des Systems Probleme bekommen?
- Wie unterscheidet sich TypeScript's `private` von anderen Sprachen?

## Worauf achten

- **Datenintegrität**: E-Mail-Adressen haben bestimmte Formatregeln
- **Kapselung**: Private Felder schützen vor unkontrolliertem Zugriff zur Compile-Zeit
- **Validierung**: Geschäftsregeln sollten zentral durchgesetzt werden
- **TypeScript-Typsicherheit**: Nutze das Typsystem für bessere Validierung

## Nächster Schritt

Überlege dir, wie du das `email` Feld vor direktem Zugriff schützen kannst. In TypeScript machst du ein Feld `private`, um es zu kapseln. Aber was passiert dann mit dem Code, der das Feld liest oder schreibt? Welche Methoden brauchst du für kontrollierten Zugriff?