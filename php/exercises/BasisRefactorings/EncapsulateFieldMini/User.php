<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\EncapsulateFieldMini;

/**
 * User class for managing user information in the system.
 *
 * This class currently has a public email field that can be accessed
 * and modified directly from outside the class, which leads to
 * data integrity issues.
 */
class User
{
    /**
     * The user's email address - currently public and unprotected.
     */
    public string $email;

    /**
     * The user's full name.
     */
    public string $name;

    /**
     * Creates a new User instance.
     */
    public function __construct(string $name, string $email)
    {
        $this->name = $name;
        $this->email = $email; // No validation here!
    }

    /**
     * Gets a formatted display name for the user.
     */
    public function getDisplayName(): string
    {
        return $this->name.' ('.$this->email.')';
    }

    /**
     * Checks if the user has a valid email domain for business use.
     */
    public function hasBusinessEmail(): bool
    {
        return str_contains($this->email, '@company.com');
    }

    /**
     * Gets the email domain.
     */
    public function getEmailDomain(): string
    {
        $parts = explode('@', $this->email);

        return $parts[1] ?? '';
    }

    /**
     * Gets the user's email address.
     */
    public function getEmail(): string
    {
        return $this->email;
    }

    /**
     * Sets the user's email address
     * Note: This method currently has no validation!
     */
    public function setEmail(string $email): void
    {
        $this->email = $email;
    }
}
