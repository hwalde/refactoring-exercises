# Hint 3: Weitere Extraktion und finale Struktur

## Was zu tun ist

Extraktiere die restlichen Services und strukturiere die finale Architektur.

## Services zu erstellen

1. **UserActivityLogger** - für Logging-Funktionalität
2. **AuthenticationService** - für Login/Logout/Session-Verwaltung  
3. **AuthorizationService** - für Berechtigungen und Rollen
4. **UserRepository** - für Datenpersistierung (CRUD)

## Finale UserManager Struktur

```php
class UserManager
{
    private UserRepository $userRepository;
    private AuthenticationService $authService;
    private AuthorizationService $authzService;
    private EmailService $emailService;
    private UserActivityLogger $activityLogger;

    public function __construct()
    {
        $this->userRepository = new UserRepository();
        $this->authService = new AuthenticationService();
        $this->authzService = new AuthorizationService();
        $this->emailService = new EmailService();
        $this->activityLogger = new UserActivityLogger();
    }

    public function createUser(string $username, string $email, string $password, array $roles = ['user']): array
    {
        // Validation bleibt hier
        // Delegiere an Services
        $user = $this->userRepository->create($username, $email, $password, $roles);
        $this->activityLogger->log($user['id'], 'user_created', "User {$username} created");
        $this->emailService->sendWelcomeEmail($email, $username);
        return $user;
    }

    // Andere Methoden delegieren an entsprechende Services...
}
```

## Wichtige Punkte

- Jede Service-Klasse hat eine klare Verantwortlichkeit
- UserManager koordiniert nur noch zwischen den Services  
- Public API bleibt unverändert (alle Tests bleiben grün)
- Verwende Constructor Injection für Dependencies

## Erfolgskontrolle

- UserManager hat maximal 100 Zeilen
- Alle Tests sind grün
- Code ist besser strukturiert und wartbar