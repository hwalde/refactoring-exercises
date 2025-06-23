# Hint 2: Extraktiere EmailService

## Was zu tun ist

Erstelle eine neue `EmailService` Klasse und verschiebe alle E-Mail-bezogenen Methoden dorthin.

## Beispiel

```php
<?php

namespace RefactoringExercises\CodeSmells\LargeClass;

class EmailService
{
    private array $emailQueue = [];
    private bool $enabled = true;

    public function sendWelcomeEmail(string $email, string $username): void
    {
        if (!$this->enabled) {
            return;
        }

        $subject = 'Welcome to our platform!';
        $message = "Hello {$username},\n\nWelcome to our platform! Your account has been created successfully.\n\nBest regards,\nThe Team";

        $this->queueEmail($email, $subject, $message);
    }

    // Weitere E-Mail-Methoden...

    public function setEnabled(bool $enabled): void
    {
        $this->enabled = $enabled;
    }

    public function getEmailQueue(): array
    {
        return $this->emailQueue;
    }

    private function queueEmail(string $to, string $subject, string $message): void
    {
        $this->emailQueue[] = [
            'to' => $to,
            'subject' => $subject,
            'message' => $message,
            'queued_at' => date('Y-m-d H:i:s')
        ];
    }
}
```

## Integration in UserManager

```php
class UserManager
{
    private EmailService $emailService;

    public function __construct()
    {
        $this->emailService = new EmailService();
        // ...
    }

    public function setEmailEnabled(bool $enabled): void
    {
        $this->emailService->setEnabled($enabled);
    }

    public function getEmailQueue(): array
    {
        return $this->emailService->getEmailQueue();
    }
}
```

## Nächster Schritt

Extraktiere die **Logging-Funktionalität** in eine `UserActivityLogger` Klasse (siehe `hint-3.md`).