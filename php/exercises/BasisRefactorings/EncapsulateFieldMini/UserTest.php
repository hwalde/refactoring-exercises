<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\EncapsulateFieldMini;

use PHPUnit\Framework\TestCase;

/**
 * @internal
 *
 * @coversNothing
 */
final class UserTest extends TestCase
{
    public function testCanCreateUserWithValidEmail(): void
    {
        $user = new User('John Doe', 'john@example.com');

        $this->assertSame('John Doe', $user->name);
        $this->assertSame('john@example.com', $user->getEmail());
    }

    public function testCanGetDisplayName(): void
    {
        $user = new User('Jane Smith', 'jane@company.com');

        $this->assertSame('Jane Smith (jane@company.com)', $user->getDisplayName());
    }

    public function testCanDetectBusinessEmail(): void
    {
        $businessUser = new User('Bob Manager', 'bob@company.com');
        $externalUser = new User('Alice Client', 'alice@external.com');

        $this->assertTrue($businessUser->hasBusinessEmail());
        $this->assertFalse($externalUser->hasBusinessEmail());
    }

    public function testCanGetEmailDomain(): void
    {
        $user = new User('Tom Developer', 'tom@example.org');

        $this->assertSame('example.org', $user->getEmailDomain());
    }

    public function testCanSetEmailAfterCreation(): void
    {
        $user = new User('Sarah Tester', 'sarah@old.com');

        $user->setEmail('sarah@new.com');

        $this->assertSame('sarah@new.com', $user->getEmail());
    }

    public function testCurrentlyAllowsEmptyEmail(): void
    {
        // This test demonstrates the current problematic behavior
        // After refactoring, this should throw an exception
        $user = new User('Invalid User', '');

        $this->assertSame('', $user->getEmail());
    }

    public function testCurrentlyAllowsEmailWithoutAtSymbol(): void
    {
        // This test demonstrates the current problematic behavior
        // After refactoring, this should throw an exception
        $user = new User('Invalid User', 'notanemail');

        $this->assertSame('notanemail', $user->getEmail());
    }

    public function testCurrentlyAllowsSettingEmptyEmail(): void
    {
        // This test demonstrates the current problematic behavior
        // After refactoring, this should throw an exception
        $user = new User('Valid User', 'valid@email.com');

        $user->setEmail('');

        $this->assertSame('', $user->getEmail());
    }

    public function testCurrentlyAllowsSettingEmailWithoutAtSymbol(): void
    {
        // This test demonstrates the current problematic behavior
        // After refactoring, this should throw an exception
        $user = new User('Valid User', 'valid@email.com');

        $user->setEmail('invalid-email');

        $this->assertSame('invalid-email', $user->getEmail());
    }

    public function testCanSetValidEmailAfterCreation(): void
    {
        $user = new User('Change User', 'old@domain.com');

        $user->setEmail('new@domain.com');

        $this->assertSame('new@domain.com', $user->getEmail());
        $this->assertSame('Change User (new@domain.com)', $user->getDisplayName());
    }

    public function testEmailDomainWorksAfterEmailChange(): void
    {
        $user = new User('Domain User', 'user@first.com');

        $user->setEmail('user@second.org');

        $this->assertSame('second.org', $user->getEmailDomain());
    }

    public function testBusinessEmailDetectionWorksAfterEmailChange(): void
    {
        $user = new User('Business User', 'user@external.com');
        $this->assertFalse($user->hasBusinessEmail());

        $user->setEmail('user@company.com');
        $this->assertTrue($user->hasBusinessEmail());
    }
}
