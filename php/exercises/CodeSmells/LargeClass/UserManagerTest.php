<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\LargeClass;

use PHPUnit\Framework\TestCase;
use InvalidArgumentException;
use RuntimeException;

class UserManagerTest extends TestCase
{
    private UserManager $userManager;

    protected function setUp(): void
    {
        $this->userManager = new UserManager();
        // Disable email and logging for tests
        $this->userManager->setEmailEnabled(false);
        $this->userManager->setLoggingEnabled(false);
    }

    public function testCreateUserWithValidData(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $this->assertNotEmpty($user['id']);
        $this->assertEquals('testuser', $user['username']);
        $this->assertEquals('test@example.com', $user['email']);
        $this->assertEquals(['user'], $user['roles']);
        $this->assertEquals('active', $user['status']);
        $this->assertFalse($user['email_verified']);
        $this->assertEquals(0, $user['login_count']);
    }

    public function testCreateUserWithCustomRoles(): void
    {
        $user = $this->userManager->createUser('admin', 'admin@example.com', 'Password123', ['admin']);

        $this->assertEquals(['admin'], $user['roles']);
    }

    public function testCreateUserWithInvalidUsername(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Username must be at least 3 characters long');

        $this->userManager->createUser('ab', 'test@example.com', 'Password123');
    }

    public function testCreateUserWithDuplicateUsername(): void
    {
        $this->userManager->createUser('testuser', 'test1@example.com', 'Password123');

        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Username already exists');

        $this->userManager->createUser('testuser', 'test2@example.com', 'Password123');
    }

    public function testCreateUserWithInvalidEmail(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid email address');

        $this->userManager->createUser('testuser', 'invalid-email', 'Password123');
    }

    public function testCreateUserWithDuplicateEmail(): void
    {
        $this->userManager->createUser('user1', 'test@example.com', 'Password123');

        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Email already registered');

        $this->userManager->createUser('user2', 'test@example.com', 'Password123');
    }

    public function testCreateUserWithWeakPassword(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Password must be at least 8 characters long');

        $this->userManager->createUser('testuser', 'test@example.com', '123');
    }

    public function testCreateUserWithInvalidPasswordFormat(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Password must contain uppercase, lowercase, and numbers');

        $this->userManager->createUser('testuser', 'test@example.com', 'password');
    }

    public function testCreateUserWithInvalidRole(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid role: invalid');

        $this->userManager->createUser('testuser', 'test@example.com', 'Password123', ['invalid']);
    }

    public function testUpdateUserUsername(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $userId = $user['id'];

        $updatedUser = $this->userManager->updateUser($userId, ['username' => 'newusername']);

        $this->assertEquals('newusername', $updatedUser['username']);
    }

    public function testUpdateUserEmail(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $userId = $user['id'];

        $updatedUser = $this->userManager->updateUser($userId, ['email' => 'newemail@example.com']);

        $this->assertEquals('newemail@example.com', $updatedUser['email']);
        $this->assertFalse($updatedUser['email_verified']);
    }

    public function testUpdateUserWithInvalidUserId(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('User not found');

        $this->userManager->updateUser('invalid-id', ['username' => 'newusername']);
    }

    public function testDeleteUser(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $userId = $user['id'];

        $result = $this->userManager->deleteUser($userId);

        $this->assertTrue($result);
        $this->assertNull($this->userManager->getUserById($userId));
    }

    public function testDeleteUserWithInvalidId(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('User not found');

        $this->userManager->deleteUser('invalid-id');
    }

    public function testLogin(): void
    {
        $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $session = $this->userManager->login('testuser', 'Password123');

        $this->assertNotEmpty($session['token']);
        $this->assertNotEmpty($session['user_id']);
        $this->assertNotEmpty($session['created_at']);
        $this->assertNotEmpty($session['expires_at']);
    }

    public function testLoginWithInvalidUsername(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid username or password');

        $this->userManager->login('nonexistent', 'Password123');
    }

    public function testLoginWithInvalidPassword(): void
    {
        $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid username or password');

        $this->userManager->login('testuser', 'WrongPassword');
    }

    public function testLoginWithInactiveUser(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $this->userManager->updateUser($user['id'], ['status' => 'inactive']);

        $this->expectException(RuntimeException::class);
        $this->expectExceptionMessage('Account is not active');

        $this->userManager->login('testuser', 'Password123');
    }

    public function testValidateSession(): void
    {
        $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $session = $this->userManager->login('testuser', 'Password123');

        $user = $this->userManager->validateSession($session['token']);

        $this->assertNotNull($user);
        $this->assertEquals('testuser', $user['username']);
    }

    public function testValidateSessionWithInvalidToken(): void
    {
        $user = $this->userManager->validateSession('invalid-token');

        $this->assertNull($user);
    }

    public function testLogout(): void
    {
        $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $session = $this->userManager->login('testuser', 'Password123');

        $result = $this->userManager->logout($session['token']);

        $this->assertTrue($result);
        $this->assertNull($this->userManager->validateSession($session['token']));
    }

    public function testLogoutWithInvalidToken(): void
    {
        $result = $this->userManager->logout('invalid-token');

        $this->assertFalse($result);
    }

    public function testHasPermission(): void
    {
        $user = $this->userManager->createUser('admin', 'admin@example.com', 'Password123', ['admin']);

        $this->assertTrue($this->userManager->hasPermission($user['id'], 'user_create'));
        $this->assertFalse($this->userManager->hasPermission($user['id'], 'invalid_permission'));
    }

    public function testHasPermissionWithRegularUser(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $this->assertTrue($this->userManager->hasPermission($user['id'], 'user_read'));
        $this->assertFalse($this->userManager->hasPermission($user['id'], 'user_delete'));
    }

    public function testHasRole(): void
    {
        $user = $this->userManager->createUser('admin', 'admin@example.com', 'Password123', ['admin']);

        $this->assertTrue($this->userManager->hasRole($user['id'], 'admin'));
        $this->assertFalse($this->userManager->hasRole($user['id'], 'moderator'));
    }

    public function testAssignRole(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $result = $this->userManager->assignRole($user['id'], 'moderator');

        $this->assertTrue($result);
        $this->assertTrue($this->userManager->hasRole($user['id'], 'moderator'));
    }

    public function testAssignRoleWithInvalidRole(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid role: invalid');

        $this->userManager->assignRole($user['id'], 'invalid');
    }

    public function testAssignRoleWithInvalidUser(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('User not found');

        $this->userManager->assignRole('invalid-id', 'admin');
    }

    public function testGetUserById(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $retrievedUser = $this->userManager->getUserById($user['id']);

        $this->assertEquals($user, $retrievedUser);
    }

    public function testGetUserByIdWithInvalidId(): void
    {
        $user = $this->userManager->getUserById('invalid-id');

        $this->assertNull($user);
    }

    public function testGetUserByUsername(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $retrievedUser = $this->userManager->getUserByUsername('testuser');

        $this->assertEquals($user, $retrievedUser);
    }

    public function testGetUserByUsernameWithInvalidUsername(): void
    {
        $user = $this->userManager->getUserByUsername('nonexistent');

        $this->assertNull($user);
    }

    public function testGetUserByEmail(): void
    {
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $retrievedUser = $this->userManager->getUserByEmail('test@example.com');

        $this->assertEquals($user, $retrievedUser);
    }

    public function testGetUserByEmailWithInvalidEmail(): void
    {
        $user = $this->userManager->getUserByEmail('nonexistent@example.com');

        $this->assertNull($user);
    }

    public function testGetAllUsers(): void
    {
        $user1 = $this->userManager->createUser('user1', 'user1@example.com', 'Password123');
        $user2 = $this->userManager->createUser('user2', 'user2@example.com', 'Password123');

        $users = $this->userManager->getAllUsers();

        $this->assertCount(2, $users);
        $this->assertEquals([$user1, $user2], $users);
    }

    public function testGetUserCount(): void
    {
        $this->assertEquals(0, $this->userManager->getUserCount());

        $this->userManager->createUser('user1', 'user1@example.com', 'Password123');
        $this->assertEquals(1, $this->userManager->getUserCount());

        $this->userManager->createUser('user2', 'user2@example.com', 'Password123');
        $this->assertEquals(2, $this->userManager->getUserCount());
    }

    public function testEmailQueueWithEnabledEmail(): void
    {
        $this->userManager->setEmailEnabled(true);
        $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $emailQueue = $this->userManager->getEmailQueue();

        $this->assertCount(1, $emailQueue);
        $this->assertEquals('test@example.com', $emailQueue[0]['to']);
        $this->assertStringContainsString('Welcome', $emailQueue[0]['subject']);
    }

    public function testActivityLogWithEnabledLogging(): void
    {
        $this->userManager->setLoggingEnabled(true);
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');

        $activityLog = $this->userManager->getActivityLog();

        $this->assertCount(1, $activityLog);
        $this->assertEquals($user['id'], $activityLog[0]['user_id']);
        $this->assertEquals('user_created', $activityLog[0]['action']);
    }

    public function testGetUserActivityLog(): void
    {
        $this->userManager->setLoggingEnabled(true);
        $user1 = $this->userManager->createUser('user1', 'user1@example.com', 'Password123');
        $user2 = $this->userManager->createUser('user2', 'user2@example.com', 'Password123');

        $user1Log = $this->userManager->getUserActivityLog($user1['id']);

        $this->assertCount(1, $user1Log);
        $this->assertEquals($user1['id'], $user1Log[0]['user_id']);
    }

    public function testCompleteUserWorkflow(): void
    {
        // Create user
        $user = $this->userManager->createUser('testuser', 'test@example.com', 'Password123');
        $this->assertNotNull($user);

        // Login
        $session = $this->userManager->login('testuser', 'Password123');
        $this->assertNotNull($session);

        // Validate session
        $validatedUser = $this->userManager->validateSession($session['token']);
        $this->assertEquals($user['username'], $validatedUser['username']);

        // Check permissions
        $this->assertTrue($this->userManager->hasPermission($user['id'], 'user_read'));

        // Update user
        $updatedUser = $this->userManager->updateUser($user['id'], ['username' => 'updateduser']);
        $this->assertEquals('updateduser', $updatedUser['username']);

        // Logout
        $this->assertTrue($this->userManager->logout($session['token']));

        // Verify session is invalid
        $this->assertNull($this->userManager->validateSession($session['token']));
    }
}