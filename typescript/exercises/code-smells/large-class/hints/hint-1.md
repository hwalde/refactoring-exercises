# Hint 1: Analysiere die Verantwortlichkeiten

## Was zu tun ist

Analysiere die `UserManager` Klasse und identifiziere die verschiedenen Verantwortlichkeiten. Die Klasse macht derzeit zu viele verschiedene Dinge gleichzeitig.

## Identifizierte Bereiche

1. **E-Mail-Operationen** - Methoden wie `sendWelcomeEmail()`, `sendEmailChangeNotification()`
2. **Activity Logging** - Methoden wie `logActivity()`, `getUserActivityLog()`
3. **Authentifizierung** - Methoden wie `login()`, `logout()`, `validateSession()`
4. **Autorisierung** - Methoden wie `hasPermission()`, `hasRole()`, `assignRole()`
5. **Benutzerverwaltung** - CRUD-Operationen für User

## Nächster Schritt

Beginne mit der Extraktion der **E-Mail-Funktionalität** in eine separate `EmailService` Klasse. Dies ist ein guter Startpunkt, da diese Funktionalität klar abgegrenzt ist und wenige Abhängigkeiten hat.

Siehe `hint-2.md` für die konkrete Umsetzung.