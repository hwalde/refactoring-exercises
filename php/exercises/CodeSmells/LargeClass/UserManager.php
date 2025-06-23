<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\LargeClass;

use InvalidArgumentException;
use RuntimeException;

/**
 * UserManager handles all user-related operations
 * 
 * This class demonstrates the "Large Class" code smell by having too many responsibilities:
 * - User management (CRUD operations)
 * - Authentication
 * - Authorization
 * - Email sending
 * - Activity logging
 */
class UserManager
{
    private array $users = [];
    private array $sessions = [];
    private array $roles = [];
    private array $activityLog = [];
    private array $emailQueue = [];
    private bool $emailEnabled = true;
    private bool $loggingEnabled = true;

    public function __construct()
    {
        $this->initializeDefaultRoles();
        $this->initializeDefaultPermissions();
    }

    // ==== USER MANAGEMENT ====

    /**
     * Creates a new user with validation and email notification
     */
    public function createUser(string $username, string $email, string $password, array $roles = ['user']): array
    {
        // Validate username
        if (empty($username) || strlen($username) < 3) {
            throw new InvalidArgumentException('Username must be at least 3 characters long');
        }

        if ($this->getUserByUsername($username) !== null) {
            throw new InvalidArgumentException('Username already exists');
        }

        // Validate email
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            throw new InvalidArgumentException('Invalid email address');
        }

        if ($this->getUserByEmail($email) !== null) {
            throw new InvalidArgumentException('Email already registered');
        }

        // Validate password
        if (strlen($password) < 8) {
            throw new InvalidArgumentException('Password must be at least 8 characters long');
        }

        if (!preg_match('/[A-Z]/', $password) || !preg_match('/[a-z]/', $password) || !preg_match('/[0-9]/', $password)) {
            throw new InvalidArgumentException('Password must contain uppercase, lowercase, and numbers');
        }

        // Validate roles
        foreach ($roles as $role) {
            if (!isset($this->roles[$role])) {
                throw new InvalidArgumentException("Invalid role: {$role}");
            }
        }

        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

        // Create user
        $user = [
            'id' => uniqid(),
            'username' => $username,
            'email' => $email,
            'password' => $hashedPassword,
            'roles' => $roles,
            'created_at' => date('Y-m-d H:i:s'),
            'updated_at' => date('Y-m-d H:i:s'),
            'last_login' => null,
            'login_count' => 0,
            'status' => 'active',
            'email_verified' => false,
            'profile' => [
                'first_name' => '',
                'last_name' => '',
                'avatar' => '',
                'bio' => ''
            ]
        ];

        $this->users[$user['id']] = $user;

        // Log activity
        $this->logActivity($user['id'], 'user_created', "User {$username} created");

        // Send welcome email
        $this->sendWelcomeEmail($email, $username);

        return $user;
    }

    /**
     * Updates user information with validation
     */
    public function updateUser(string $userId, array $data): array
    {
        $user = $this->getUserById($userId);
        if ($user === null) {
            throw new InvalidArgumentException('User not found');
        }

        // Validate and update username
        if (isset($data['username'])) {
            if (empty($data['username']) || strlen($data['username']) < 3) {
                throw new InvalidArgumentException('Username must be at least 3 characters long');
            }
            
            $existingUser = $this->getUserByUsername($data['username']);
            if ($existingUser !== null && $existingUser['id'] !== $userId) {
                throw new InvalidArgumentException('Username already exists');
            }
            
            $user['username'] = $data['username'];
        }

        // Validate and update email
        if (isset($data['email'])) {
            if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
                throw new InvalidArgumentException('Invalid email address');
            }
            
            $existingUser = $this->getUserByEmail($data['email']);
            if ($existingUser !== null && $existingUser['id'] !== $userId) {
                throw new InvalidArgumentException('Email already registered');
            }
            
            $oldEmail = $user['email'];
            $user['email'] = $data['email'];
            $user['email_verified'] = false;
            
            // Send email change notification
            $this->sendEmailChangeNotification($oldEmail, $data['email']);
        }

        // Update password if provided
        if (isset($data['password'])) {
            if (strlen($data['password']) < 8) {
                throw new InvalidArgumentException('Password must be at least 8 characters long');
            }
            
            if (!preg_match('/[A-Z]/', $data['password']) || !preg_match('/[a-z]/', $data['password']) || !preg_match('/[0-9]/', $data['password'])) {
                throw new InvalidArgumentException('Password must contain uppercase, lowercase, and numbers');
            }
            
            $user['password'] = password_hash($data['password'], PASSWORD_BCRYPT, ['cost' => 12]);
        }

        // Update roles if provided
        if (isset($data['roles'])) {
            foreach ($data['roles'] as $role) {
                if (!isset($this->roles[$role])) {
                    throw new InvalidArgumentException("Invalid role: {$role}");
                }
            }
            $user['roles'] = $data['roles'];
        }

        // Update profile data
        if (isset($data['profile'])) {
            $user['profile'] = array_merge($user['profile'], $data['profile']);
        }

        // Update status
        if (isset($data['status'])) {
            if (!in_array($data['status'], ['active', 'inactive', 'suspended'])) {
                throw new InvalidArgumentException('Invalid status');
            }
            $user['status'] = $data['status'];
        }

        $user['updated_at'] = date('Y-m-d H:i:s');
        $this->users[$userId] = $user;

        // Log activity
        $this->logActivity($userId, 'user_updated', "User {$user['username']} updated");

        return $user;
    }

    /**
     * Deletes a user and cleans up associated data
     */
    public function deleteUser(string $userId): bool
    {
        $user = $this->getUserById($userId);
        if ($user === null) {
            throw new InvalidArgumentException('User not found');
        }

        // Log activity before deletion
        $this->logActivity($userId, 'user_deleted', "User {$user['username']} deleted");

        // Send goodbye email
        $this->sendGoodbyeEmail($user['email'], $user['username']);

        // Clean up sessions
        $this->cleanupUserSessions($userId);

        // Remove user
        unset($this->users[$userId]);

        return true;
    }

    // ==== AUTHENTICATION ====

    /**
     * Authenticates user and creates session
     */
    public function login(string $username, string $password): array
    {
        $user = $this->getUserByUsername($username);
        if ($user === null) {
            throw new InvalidArgumentException('Invalid username or password');
        }

        if ($user['status'] !== 'active') {
            throw new RuntimeException('Account is not active');
        }

        if (!password_verify($password, $user['password'])) {
            // Log failed login attempt
            $this->logActivity($user['id'], 'login_failed', "Failed login attempt for {$username}");
            throw new InvalidArgumentException('Invalid username or password');
        }

        // Generate session token
        $sessionToken = bin2hex(random_bytes(32));
        $session = [
            'token' => $sessionToken,
            'user_id' => $user['id'],
            'created_at' => date('Y-m-d H:i:s'),
            'expires_at' => date('Y-m-d H:i:s', strtotime('+24 hours')),
            'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown',
            'user_agent' => $_SERVER['HTTP_USER_AGENT'] ?? 'unknown'
        ];

        $this->sessions[$sessionToken] = $session;

        // Update user login info
        $this->users[$user['id']]['last_login'] = date('Y-m-d H:i:s');
        $this->users[$user['id']]['login_count']++;

        // Log successful login
        $this->logActivity($user['id'], 'login_success', "User {$username} logged in");

        // Send login notification email
        $this->sendLoginNotificationEmail($user['email'], $user['username'], $session['ip_address']);

        return $session;
    }

    /**
     * Validates session token and returns user data
     */
    public function validateSession(string $token): ?array
    {
        if (!isset($this->sessions[$token])) {
            return null;
        }

        $session = $this->sessions[$token];
        
        // Check if session is expired
        if (strtotime($session['expires_at']) < time()) {
            unset($this->sessions[$token]);
            return null;
        }

        $user = $this->getUserById($session['user_id']);
        if ($user === null || $user['status'] !== 'active') {
            unset($this->sessions[$token]);
            return null;
        }

        return $user;
    }

    /**
     * Logs out user and destroys session
     */
    public function logout(string $token): bool
    {
        if (isset($this->sessions[$token])) {
            $session = $this->sessions[$token];
            $user = $this->getUserById($session['user_id']);
            
            if ($user !== null) {
                $this->logActivity($user['id'], 'logout', "User {$user['username']} logged out");
            }
            
            unset($this->sessions[$token]);
            return true;
        }

        return false;
    }

    // ==== AUTHORIZATION ====

    /**
     * Checks if user has specific permission
     */
    public function hasPermission(string $userId, string $permission): bool
    {
        $user = $this->getUserById($userId);
        if ($user === null || $user['status'] !== 'active') {
            return false;
        }

        foreach ($user['roles'] as $roleName) {
            if (isset($this->roles[$roleName])) {
                $role = $this->roles[$roleName];
                if (in_array($permission, $role['permissions'])) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Checks if user has specific role
     */
    public function hasRole(string $userId, string $roleName): bool
    {
        $user = $this->getUserById($userId);
        if ($user === null) {
            return false;
        }

        return in_array($roleName, $user['roles']);
    }

    /**
     * Assigns role to user
     */
    public function assignRole(string $userId, string $roleName): bool
    {
        if (!isset($this->roles[$roleName])) {
            throw new InvalidArgumentException("Invalid role: {$roleName}");
        }

        $user = $this->getUserById($userId);
        if ($user === null) {
            throw new InvalidArgumentException('User not found');
        }

        if (!in_array($roleName, $user['roles'])) {
            $this->users[$userId]['roles'][] = $roleName;
            $this->logActivity($userId, 'role_assigned', "Role {$roleName} assigned to user {$user['username']}");
        }

        return true;
    }

    // ==== EMAIL OPERATIONS ====

    /**
     * Sends welcome email to new user
     */
    private function sendWelcomeEmail(string $email, string $username): void
    {
        if (!$this->emailEnabled) {
            return;
        }

        $subject = 'Welcome to our platform!';
        $message = "Hello {$username},\n\nWelcome to our platform! Your account has been created successfully.\n\nBest regards,\nThe Team";

        $this->queueEmail($email, $subject, $message);
    }

    /**
     * Sends email change notification
     */
    private function sendEmailChangeNotification(string $oldEmail, string $newEmail): void
    {
        if (!$this->emailEnabled) {
            return;
        }

        $subject = 'Email address changed';
        $message = "Your email address has been changed from {$oldEmail} to {$newEmail}.\n\nIf you didn't make this change, please contact support immediately.";

        $this->queueEmail($oldEmail, $subject, $message);
        $this->queueEmail($newEmail, $subject, $message);
    }

    /**
     * Sends login notification email
     */
    private function sendLoginNotificationEmail(string $email, string $username, string $ipAddress): void
    {
        if (!$this->emailEnabled) {
            return;
        }

        $subject = 'New login detected';
        $message = "Hello {$username},\n\nA new login was detected from IP address: {$ipAddress}\n\nIf this wasn't you, please change your password immediately.";

        $this->queueEmail($email, $subject, $message);
    }

    /**
     * Sends goodbye email when user is deleted
     */
    private function sendGoodbyeEmail(string $email, string $username): void
    {
        if (!$this->emailEnabled) {
            return;
        }

        $subject = 'Account deleted';
        $message = "Hello {$username},\n\nYour account has been deleted. We're sorry to see you go!\n\nBest regards,\nThe Team";

        $this->queueEmail($email, $subject, $message);
    }

    /**
     * Queues email for sending
     */
    private function queueEmail(string $to, string $subject, string $message): void
    {
        $this->emailQueue[] = [
            'to' => $to,
            'subject' => $subject,
            'message' => $message,
            'queued_at' => date('Y-m-d H:i:s')
        ];
    }

    // ==== ACTIVITY LOGGING ====

    /**
     * Logs user activity
     */
    private function logActivity(string $userId, string $action, string $description): void
    {
        if (!$this->loggingEnabled) {
            return;
        }

        $this->activityLog[] = [
            'user_id' => $userId,
            'action' => $action,
            'description' => $description,
            'timestamp' => date('Y-m-d H:i:s'),
            'ip_address' => $_SERVER['REMOTE_ADDR'] ?? 'unknown'
        ];
    }

    /**
     * Gets activity log for specific user
     */
    public function getUserActivityLog(string $userId): array
    {
        return array_filter($this->activityLog, function($log) use ($userId) {
            return $log['user_id'] === $userId;
        });
    }

    // ==== HELPER METHODS ====

    public function getUserById(string $id): ?array
    {
        return $this->users[$id] ?? null;
    }

    public function getUserByUsername(string $username): ?array
    {
        foreach ($this->users as $user) {
            if ($user['username'] === $username) {
                return $user;
            }
        }
        return null;
    }

    public function getUserByEmail(string $email): ?array
    {
        foreach ($this->users as $user) {
            if ($user['email'] === $email) {
                return $user;
            }
        }
        return null;
    }

    public function getAllUsers(): array
    {
        return array_values($this->users);
    }

    public function getUserCount(): int
    {
        return count($this->users);
    }

    private function cleanupUserSessions(string $userId): void
    {
        foreach ($this->sessions as $token => $session) {
            if ($session['user_id'] === $userId) {
                unset($this->sessions[$token]);
            }
        }
    }

    private function initializeDefaultRoles(): void
    {
        $this->roles = [
            'admin' => [
                'name' => 'Administrator',
                'permissions' => ['user_create', 'user_read', 'user_update', 'user_delete', 'admin_panel']
            ],
            'moderator' => [
                'name' => 'Moderator',
                'permissions' => ['user_read', 'user_update', 'moderate_content']
            ],
            'user' => [
                'name' => 'User',
                'permissions' => ['user_read', 'profile_update']
            ]
        ];
    }

    private function initializeDefaultPermissions(): void
    {
        // Available permissions for reference
        // 'user_create' => 'Create new users',
        // 'user_read' => 'View user information',  
        // 'user_update' => 'Update user information',
        // 'user_delete' => 'Delete users',
        // 'admin_panel' => 'Access admin panel',
        // 'moderate_content' => 'Moderate user content',
        // 'profile_update' => 'Update own profile'
    }

    // Configuration methods
    public function setEmailEnabled(bool $enabled): void
    {
        $this->emailEnabled = $enabled;
    }

    public function setLoggingEnabled(bool $enabled): void
    {
        $this->loggingEnabled = $enabled;
    }

    public function getEmailQueue(): array
    {
        return $this->emailQueue;
    }

    public function getActivityLog(): array
    {
        return $this->activityLog;
    }
}