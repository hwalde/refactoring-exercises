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

interface User {
  id: string;
  username: string;
  email: string;
  password: string;
  roles: string[];
  createdAt: string;
  updatedAt: string;
  lastLogin: string | null;
  loginCount: number;
  status: 'active' | 'inactive' | 'suspended';
  emailVerified: boolean;
  profile: {
    firstName: string;
    lastName: string;
    avatar: string;
    bio: string;
  };
}

interface Session {
  token: string;
  userId: string;
  createdAt: string;
  expiresAt: string;
  ipAddress: string;
  userAgent: string;
}

interface Role {
  name: string;
  permissions: string[];
}

interface ActivityLog {
  userId: string;
  action: string;
  description: string;
  timestamp: string;
  ipAddress: string;
}

interface EmailItem {
  to: string;
  subject: string;
  message: string;
  queuedAt: string;
}

export class UserManager {
  private users: Map<string, User> = new Map();
  private sessions: Map<string, Session> = new Map();
  private roles: Map<string, Role> = new Map();
  private permissions: Map<string, string> = new Map();
  private activityLog: ActivityLog[] = [];
  private emailQueue: EmailItem[] = [];
  private emailEnabled: boolean = true;
  private loggingEnabled: boolean = true;

  constructor() {
    this.initializeDefaultRoles();
    this.initializeDefaultPermissions();
  }

  // ==== USER MANAGEMENT ====

  /**
   * Creates a new user with validation and email notification
   */
  createUser(
    username: string,
    email: string,
    password: string,
    roles: string[] = ['user']
  ): User {
    // Validate username
    if (!username || username.length < 3) {
      throw new Error('Username must be at least 3 characters long');
    }

    if (this.getUserByUsername(username) !== null) {
      throw new Error('Username already exists');
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      throw new Error('Invalid email address');
    }

    if (this.getUserByEmail(email) !== null) {
      throw new Error('Email already registered');
    }

    // Validate password
    if (password.length < 8) {
      throw new Error('Password must be at least 8 characters long');
    }

    if (
      !/[A-Z]/.test(password) ||
      !/[a-z]/.test(password) ||
      !/[0-9]/.test(password)
    ) {
      throw new Error(
        'Password must contain uppercase, lowercase, and numbers'
      );
    }

    // Validate roles
    for (const role of roles) {
      if (!this.roles.has(role)) {
        throw new Error(`Invalid role: ${role}`);
      }
    }

    // Hash password (simplified for demo)
    const hashedPassword = this.hashPassword(password);

    // Create user
    const user: User = {
      id: this.generateId(),
      username,
      email,
      password: hashedPassword,
      roles,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      lastLogin: null,
      loginCount: 0,
      status: 'active',
      emailVerified: false,
      profile: {
        firstName: '',
        lastName: '',
        avatar: '',
        bio: '',
      },
    };

    this.users.set(user.id, user);

    // Log activity
    this.logActivity(user.id, 'user_created', `User ${username} created`);

    // Send welcome email
    this.sendWelcomeEmail(email, username);

    return user;
  }

  /**
   * Updates user information with validation
   */
  updateUser(userId: string, data: Partial<User>): User {
    const user = this.getUserById(userId);
    if (!user) {
      throw new Error('User not found');
    }

    // Validate and update username
    if (data.username !== undefined) {
      if (!data.username || data.username.length < 3) {
        throw new Error('Username must be at least 3 characters long');
      }

      const existingUser = this.getUserByUsername(data.username);
      if (existingUser && existingUser.id !== userId) {
        throw new Error('Username already exists');
      }

      user.username = data.username;
    }

    // Validate and update email
    if (data.email !== undefined) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(data.email)) {
        throw new Error('Invalid email address');
      }

      const existingUser = this.getUserByEmail(data.email);
      if (existingUser && existingUser.id !== userId) {
        throw new Error('Email already registered');
      }

      const oldEmail = user.email;
      user.email = data.email;
      user.emailVerified = false;

      // Send email change notification
      this.sendEmailChangeNotification(oldEmail, data.email);
    }

    // Update password if provided
    if (data.password !== undefined) {
      if (data.password.length < 8) {
        throw new Error('Password must be at least 8 characters long');
      }

      if (
        !/[A-Z]/.test(data.password) ||
        !/[a-z]/.test(data.password) ||
        !/[0-9]/.test(data.password)
      ) {
        throw new Error(
          'Password must contain uppercase, lowercase, and numbers'
        );
      }

      user.password = this.hashPassword(data.password);
    }

    // Update roles if provided
    if (data.roles !== undefined) {
      for (const role of data.roles) {
        if (!this.roles.has(role)) {
          throw new Error(`Invalid role: ${role}`);
        }
      }
      user.roles = data.roles;
    }

    // Update profile data
    if (data.profile !== undefined) {
      user.profile = { ...user.profile, ...data.profile };
    }

    // Update status
    if (data.status !== undefined) {
      if (!['active', 'inactive', 'suspended'].includes(data.status)) {
        throw new Error('Invalid status');
      }
      user.status = data.status;
    }

    user.updatedAt = new Date().toISOString();
    this.users.set(userId, user);

    // Log activity
    this.logActivity(userId, 'user_updated', `User ${user.username} updated`);

    return user;
  }

  /**
   * Deletes a user and cleans up associated data
   */
  deleteUser(userId: string): boolean {
    const user = this.getUserById(userId);
    if (!user) {
      throw new Error('User not found');
    }

    // Log activity before deletion
    this.logActivity(userId, 'user_deleted', `User ${user.username} deleted`);

    // Send goodbye email
    this.sendGoodbyeEmail(user.email, user.username);

    // Clean up sessions
    this.cleanupUserSessions(userId);

    // Remove user
    this.users.delete(userId);

    return true;
  }

  // ==== AUTHENTICATION ====

  /**
   * Authenticates user and creates session
   */
  login(username: string, password: string): Session {
    const user = this.getUserByUsername(username);
    if (!user) {
      throw new Error('Invalid username or password');
    }

    if (user.status !== 'active') {
      throw new Error('Account is not active');
    }

    if (!this.verifyPassword(password, user.password)) {
      // Log failed login attempt
      this.logActivity(
        user.id,
        'login_failed',
        `Failed login attempt for ${username}`
      );
      throw new Error('Invalid username or password');
    }

    // Generate session token
    const sessionToken = this.generateSessionToken();
    const session: Session = {
      token: sessionToken,
      userId: user.id,
      createdAt: new Date().toISOString(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24 hours
      ipAddress: 'unknown', // Would be from request in real app
      userAgent: 'unknown', // Would be from request in real app
    };

    this.sessions.set(sessionToken, session);

    // Update user login info
    user.lastLogin = new Date().toISOString();
    user.loginCount++;
    this.users.set(user.id, user);

    // Log successful login
    this.logActivity(user.id, 'login_success', `User ${username} logged in`);

    // Send login notification email
    this.sendLoginNotificationEmail(
      user.email,
      user.username,
      session.ipAddress
    );

    return session;
  }

  /**
   * Validates session token and returns user data
   */
  validateSession(token: string): User | null {
    const session = this.sessions.get(token);
    if (!session) {
      return null;
    }

    // Check if session is expired
    if (new Date(session.expiresAt) < new Date()) {
      this.sessions.delete(token);
      return null;
    }

    const user = this.getUserById(session.userId);
    if (!user || user.status !== 'active') {
      this.sessions.delete(token);
      return null;
    }

    return user;
  }

  /**
   * Logs out user and destroys session
   */
  logout(token: string): boolean {
    const session = this.sessions.get(token);
    if (session) {
      const user = this.getUserById(session.userId);

      if (user) {
        this.logActivity(user.id, 'logout', `User ${user.username} logged out`);
      }

      this.sessions.delete(token);
      return true;
    }

    return false;
  }

  // ==== AUTHORIZATION ====

  /**
   * Checks if user has specific permission
   */
  hasPermission(userId: string, permission: string): boolean {
    const user = this.getUserById(userId);
    if (!user || user.status !== 'active') {
      return false;
    }

    for (const roleName of user.roles) {
      const role = this.roles.get(roleName);
      if (role && role.permissions.includes(permission)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Checks if user has specific role
   */
  hasRole(userId: string, roleName: string): boolean {
    const user = this.getUserById(userId);
    if (!user) {
      return false;
    }

    return user.roles.includes(roleName);
  }

  /**
   * Assigns role to user
   */
  assignRole(userId: string, roleName: string): boolean {
    if (!this.roles.has(roleName)) {
      throw new Error(`Invalid role: ${roleName}`);
    }

    const user = this.getUserById(userId);
    if (!user) {
      throw new Error('User not found');
    }

    if (!user.roles.includes(roleName)) {
      user.roles.push(roleName);
      this.users.set(userId, user);
      this.logActivity(
        userId,
        'role_assigned',
        `Role ${roleName} assigned to user ${user.username}`
      );
    }

    return true;
  }

  // ==== EMAIL OPERATIONS ====

  /**
   * Sends welcome email to new user
   */
  private sendWelcomeEmail(email: string, username: string): void {
    if (!this.emailEnabled) {
      return;
    }

    const subject = 'Welcome to our platform!';
    const message = `Hello ${username},\n\nWelcome to our platform! Your account has been created successfully.\n\nBest regards,\nThe Team`;

    this.queueEmail(email, subject, message);
  }

  /**
   * Sends email change notification
   */
  private sendEmailChangeNotification(
    oldEmail: string,
    newEmail: string
  ): void {
    if (!this.emailEnabled) {
      return;
    }

    const subject = 'Email address changed';
    const message = `Your email address has been changed from ${oldEmail} to ${newEmail}.\n\nIf you didn't make this change, please contact support immediately.`;

    this.queueEmail(oldEmail, subject, message);
    this.queueEmail(newEmail, subject, message);
  }

  /**
   * Sends login notification email
   */
  private sendLoginNotificationEmail(
    email: string,
    username: string,
    ipAddress: string
  ): void {
    if (!this.emailEnabled) {
      return;
    }

    const subject = 'New login detected';
    const message = `Hello ${username},\n\nA new login was detected from IP address: ${ipAddress}\n\nIf this wasn't you, please change your password immediately.`;

    this.queueEmail(email, subject, message);
  }

  /**
   * Sends goodbye email when user is deleted
   */
  private sendGoodbyeEmail(email: string, username: string): void {
    if (!this.emailEnabled) {
      return;
    }

    const subject = 'Account deleted';
    const message = `Hello ${username},\n\nYour account has been deleted. We're sorry to see you go!\n\nBest regards,\nThe Team`;

    this.queueEmail(email, subject, message);
  }

  /**
   * Queues email for sending
   */
  private queueEmail(to: string, subject: string, message: string): void {
    this.emailQueue.push({
      to,
      subject,
      message,
      queuedAt: new Date().toISOString(),
    });
  }

  // ==== ACTIVITY LOGGING ====

  /**
   * Logs user activity
   */
  private logActivity(
    userId: string,
    action: string,
    description: string
  ): void {
    if (!this.loggingEnabled) {
      return;
    }

    this.activityLog.push({
      userId,
      action,
      description,
      timestamp: new Date().toISOString(),
      ipAddress: 'unknown', // Would be from request in real app
    });
  }

  /**
   * Gets activity log for specific user
   */
  getUserActivityLog(userId: string): ActivityLog[] {
    return this.activityLog.filter(log => log.userId === userId);
  }

  // ==== HELPER METHODS ====

  getUserById(id: string): User | null {
    return this.users.get(id) || null;
  }

  getUserByUsername(username: string): User | null {
    for (const user of this.users.values()) {
      if (user.username === username) {
        return user;
      }
    }
    return null;
  }

  getUserByEmail(email: string): User | null {
    for (const user of this.users.values()) {
      if (user.email === email) {
        return user;
      }
    }
    return null;
  }

  getAllUsers(): User[] {
    return Array.from(this.users.values());
  }

  getUserCount(): number {
    return this.users.size;
  }

  private cleanupUserSessions(userId: string): void {
    for (const [token, session] of this.sessions.entries()) {
      if (session.userId === userId) {
        this.sessions.delete(token);
      }
    }
  }

  private initializeDefaultRoles(): void {
    this.roles.set('admin', {
      name: 'Administrator',
      permissions: [
        'user_create',
        'user_read',
        'user_update',
        'user_delete',
        'admin_panel',
      ],
    });

    this.roles.set('moderator', {
      name: 'Moderator',
      permissions: ['user_read', 'user_update', 'moderate_content'],
    });

    this.roles.set('user', {
      name: 'User',
      permissions: ['user_read', 'profile_update'],
    });
  }

  private initializeDefaultPermissions(): void {
    this.permissions.set('user_create', 'Create new users');
    this.permissions.set('user_read', 'View user information');
    this.permissions.set('user_update', 'Update user information');
    this.permissions.set('user_delete', 'Delete users');
    this.permissions.set('admin_panel', 'Access admin panel');
    this.permissions.set('moderate_content', 'Moderate user content');
    this.permissions.set('profile_update', 'Update own profile');
  }

  // Utility methods
  private generateId(): string {
    return Math.random().toString(36).substr(2, 9);
  }

  private generateSessionToken(): string {
    return Math.random().toString(36).substr(2, 32);
  }

  private hashPassword(password: string): string {
    // Simplified hashing for demo purposes
    return `hashed_${password}`;
  }

  private verifyPassword(password: string, hashedPassword: string): boolean {
    return hashedPassword === `hashed_${password}`;
  }

  // Configuration methods
  setEmailEnabled(enabled: boolean): void {
    this.emailEnabled = enabled;
  }

  setLoggingEnabled(enabled: boolean): void {
    this.loggingEnabled = enabled;
  }

  getEmailQueue(): EmailItem[] {
    return this.emailQueue;
  }

  getActivityLog(): ActivityLog[] {
    return this.activityLog;
  }
}
