import { UserManager } from '../src/UserManager';

describe('UserManager', () => {
  let userManager: UserManager;

  beforeEach(() => {
    userManager = new UserManager();
    // Disable email and logging for tests
    userManager.setEmailEnabled(false);
    userManager.setLoggingEnabled(false);
  });

  describe('User Creation', () => {
    test('should create user with valid data', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      expect(user.id).toBeDefined();
      expect(user.username).toBe('testuser');
      expect(user.email).toBe('test@example.com');
      expect(user.roles).toEqual(['user']);
      expect(user.status).toBe('active');
      expect(user.emailVerified).toBe(false);
      expect(user.loginCount).toBe(0);
    });

    test('should create user with custom roles', () => {
      const user = userManager.createUser(
        'admin',
        'admin@example.com',
        'Password123',
        ['admin']
      );

      expect(user.roles).toEqual(['admin']);
    });

    test('should throw error for invalid username', () => {
      expect(() => {
        userManager.createUser('ab', 'test@example.com', 'Password123');
      }).toThrow('Username must be at least 3 characters long');
    });

    test('should throw error for duplicate username', () => {
      userManager.createUser('testuser', 'test1@example.com', 'Password123');

      expect(() => {
        userManager.createUser('testuser', 'test2@example.com', 'Password123');
      }).toThrow('Username already exists');
    });

    test('should throw error for invalid email', () => {
      expect(() => {
        userManager.createUser('testuser', 'invalid-email', 'Password123');
      }).toThrow('Invalid email address');
    });

    test('should throw error for duplicate email', () => {
      userManager.createUser('user1', 'test@example.com', 'Password123');

      expect(() => {
        userManager.createUser('user2', 'test@example.com', 'Password123');
      }).toThrow('Email already registered');
    });

    test('should throw error for weak password', () => {
      expect(() => {
        userManager.createUser('testuser', 'test@example.com', '123');
      }).toThrow('Password must be at least 8 characters long');
    });

    test('should throw error for invalid password format', () => {
      expect(() => {
        userManager.createUser('testuser', 'test@example.com', 'password');
      }).toThrow('Password must contain uppercase, lowercase, and numbers');
    });

    test('should throw error for invalid role', () => {
      expect(() => {
        userManager.createUser('testuser', 'test@example.com', 'Password123', [
          'invalid',
        ]);
      }).toThrow('Invalid role: invalid');
    });
  });

  describe('User Updates', () => {
    test('should update user username', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const updatedUser = userManager.updateUser(user.id, {
        username: 'newusername',
      });

      expect(updatedUser.username).toBe('newusername');
    });

    test('should update user email', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const updatedUser = userManager.updateUser(user.id, {
        email: 'newemail@example.com',
      });

      expect(updatedUser.email).toBe('newemail@example.com');
      expect(updatedUser.emailVerified).toBe(false);
    });

    test('should throw error for invalid user id', () => {
      expect(() => {
        userManager.updateUser('invalid-id', { username: 'newusername' });
      }).toThrow('User not found');
    });
  });

  describe('User Deletion', () => {
    test('should delete user', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const result = userManager.deleteUser(user.id);

      expect(result).toBe(true);
      expect(userManager.getUserById(user.id)).toBeNull();
    });

    test('should throw error for invalid user id', () => {
      expect(() => {
        userManager.deleteUser('invalid-id');
      }).toThrow('User not found');
    });
  });

  describe('Authentication', () => {
    test('should login user', () => {
      userManager.createUser('testuser', 'test@example.com', 'Password123');

      const session = userManager.login('testuser', 'Password123');

      expect(session.token).toBeDefined();
      expect(session.userId).toBeDefined();
      expect(session.createdAt).toBeDefined();
      expect(session.expiresAt).toBeDefined();
    });

    test('should throw error for invalid username', () => {
      expect(() => {
        userManager.login('nonexistent', 'Password123');
      }).toThrow('Invalid username or password');
    });

    test('should throw error for invalid password', () => {
      userManager.createUser('testuser', 'test@example.com', 'Password123');

      expect(() => {
        userManager.login('testuser', 'WrongPassword');
      }).toThrow('Invalid username or password');
    });

    test('should throw error for inactive user', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );
      userManager.updateUser(user.id, { status: 'inactive' });

      expect(() => {
        userManager.login('testuser', 'Password123');
      }).toThrow('Account is not active');
    });

    test('should validate session', () => {
      userManager.createUser('testuser', 'test@example.com', 'Password123');
      const session = userManager.login('testuser', 'Password123');

      const user = userManager.validateSession(session.token);

      expect(user).not.toBeNull();
      expect(user!.username).toBe('testuser');
    });

    test('should return null for invalid session token', () => {
      const user = userManager.validateSession('invalid-token');

      expect(user).toBeNull();
    });

    test('should logout user', () => {
      userManager.createUser('testuser', 'test@example.com', 'Password123');
      const session = userManager.login('testuser', 'Password123');

      const result = userManager.logout(session.token);

      expect(result).toBe(true);
      expect(userManager.validateSession(session.token)).toBeNull();
    });

    test('should return false for invalid logout token', () => {
      const result = userManager.logout('invalid-token');

      expect(result).toBe(false);
    });
  });

  describe('Authorization', () => {
    test('should check user permissions', () => {
      const user = userManager.createUser(
        'admin',
        'admin@example.com',
        'Password123',
        ['admin']
      );

      expect(userManager.hasPermission(user.id, 'user_create')).toBe(true);
      expect(userManager.hasPermission(user.id, 'invalid_permission')).toBe(
        false
      );
    });

    test('should check regular user permissions', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      expect(userManager.hasPermission(user.id, 'user_read')).toBe(true);
      expect(userManager.hasPermission(user.id, 'user_delete')).toBe(false);
    });

    test('should check user roles', () => {
      const user = userManager.createUser(
        'admin',
        'admin@example.com',
        'Password123',
        ['admin']
      );

      expect(userManager.hasRole(user.id, 'admin')).toBe(true);
      expect(userManager.hasRole(user.id, 'moderator')).toBe(false);
    });

    test('should assign role to user', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const result = userManager.assignRole(user.id, 'moderator');

      expect(result).toBe(true);
      expect(userManager.hasRole(user.id, 'moderator')).toBe(true);
    });

    test('should throw error for invalid role assignment', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      expect(() => {
        userManager.assignRole(user.id, 'invalid');
      }).toThrow('Invalid role: invalid');
    });

    test('should throw error for invalid user role assignment', () => {
      expect(() => {
        userManager.assignRole('invalid-id', 'admin');
      }).toThrow('User not found');
    });
  });

  describe('User Retrieval', () => {
    test('should get user by id', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const retrievedUser = userManager.getUserById(user.id);

      expect(retrievedUser).toEqual(user);
    });

    test('should return null for invalid user id', () => {
      const user = userManager.getUserById('invalid-id');

      expect(user).toBeNull();
    });

    test('should get user by username', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const retrievedUser = userManager.getUserByUsername('testuser');

      expect(retrievedUser).toEqual(user);
    });

    test('should return null for invalid username', () => {
      const user = userManager.getUserByUsername('nonexistent');

      expect(user).toBeNull();
    });

    test('should get user by email', () => {
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const retrievedUser = userManager.getUserByEmail('test@example.com');

      expect(retrievedUser).toEqual(user);
    });

    test('should return null for invalid email', () => {
      const user = userManager.getUserByEmail('nonexistent@example.com');

      expect(user).toBeNull();
    });

    test('should get all users', () => {
      const user1 = userManager.createUser(
        'user1',
        'user1@example.com',
        'Password123'
      );
      const user2 = userManager.createUser(
        'user2',
        'user2@example.com',
        'Password123'
      );

      const users = userManager.getAllUsers();

      expect(users).toHaveLength(2);
      expect(users).toEqual([user1, user2]);
    });

    test('should get user count', () => {
      expect(userManager.getUserCount()).toBe(0);

      userManager.createUser('user1', 'user1@example.com', 'Password123');
      expect(userManager.getUserCount()).toBe(1);

      userManager.createUser('user2', 'user2@example.com', 'Password123');
      expect(userManager.getUserCount()).toBe(2);
    });
  });

  describe('Email and Logging', () => {
    test('should queue emails when enabled', () => {
      userManager.setEmailEnabled(true);
      userManager.createUser('testuser', 'test@example.com', 'Password123');

      const emailQueue = userManager.getEmailQueue();

      expect(emailQueue).toHaveLength(1);
      expect(emailQueue[0]?.to).toBe('test@example.com');
      expect(emailQueue[0]?.subject).toContain('Welcome');
    });

    test('should log activities when enabled', () => {
      userManager.setLoggingEnabled(true);
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );

      const activityLog = userManager.getActivityLog();

      expect(activityLog).toHaveLength(1);
      expect(activityLog[0]?.userId).toBe(user.id);
      expect(activityLog[0]?.action).toBe('user_created');
    });

    test('should get user activity log', () => {
      userManager.setLoggingEnabled(true);
      const user1 = userManager.createUser(
        'user1',
        'user1@example.com',
        'Password123'
      );
      userManager.createUser('user2', 'user2@example.com', 'Password123');

      const user1Log = userManager.getUserActivityLog(user1.id);

      expect(user1Log).toHaveLength(1);
      expect(user1Log[0]?.userId).toBe(user1.id);
    });
  });

  describe('Complete User Workflow', () => {
    test('should handle complete user workflow', () => {
      // Create user
      const user = userManager.createUser(
        'testuser',
        'test@example.com',
        'Password123'
      );
      expect(user).toBeDefined();

      // Login
      const session = userManager.login('testuser', 'Password123');
      expect(session).toBeDefined();

      // Validate session
      const validatedUser = userManager.validateSession(session.token);
      expect(validatedUser!.username).toBe(user.username);

      // Check permissions
      expect(userManager.hasPermission(user.id, 'user_read')).toBe(true);

      // Update user
      const updatedUser = userManager.updateUser(user.id, {
        username: 'updateduser',
      });
      expect(updatedUser.username).toBe('updateduser');

      // Logout
      expect(userManager.logout(session.token)).toBe(true);

      // Verify session is invalid
      expect(userManager.validateSession(session.token)).toBeNull();
    });
  });
});
