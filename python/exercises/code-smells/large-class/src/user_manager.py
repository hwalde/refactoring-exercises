"""
UserManager handles all user-related operations

This class demonstrates the "Large Class" code smell by having too many responsibilities:
- User management (CRUD operations)
- Authentication
- Authorization
- Email sending
- Activity logging
"""

import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass
class User:
    id: str
    username: str
    email: str
    password: str
    roles: list[str]
    created_at: str
    updated_at: str
    last_login: str | None
    login_count: int
    status: str
    email_verified: bool
    profile: dict[str, str] = field(
        default_factory=lambda: {
            "first_name": "",
            "last_name": "",
            "avatar": "",
            "bio": "",
        }
    )


@dataclass
class Session:
    token: str
    user_id: str
    created_at: str
    expires_at: str
    ip_address: str
    user_agent: str


@dataclass
class Role:
    name: str
    permissions: list[str]


@dataclass
class ActivityLog:
    user_id: str
    action: str
    description: str
    timestamp: str
    ip_address: str


@dataclass
class EmailItem:
    to: str
    subject: str
    message: str
    queued_at: str


class UserManager:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.sessions: dict[str, Session] = {}
        self.roles: dict[str, Role] = {}
        self.permissions: dict[str, str] = {}
        self.activity_log: list[ActivityLog] = []
        self.email_queue: list[EmailItem] = []
        self.email_enabled: bool = True
        self.logging_enabled: bool = True

        self._initialize_default_roles()
        self._initialize_default_permissions()

    # ==== USER MANAGEMENT ====

    def create_user(
        self, username: str, email: str, password: str, roles: list[str] = None
    ) -> User:
        """Creates a new user with validation and email notification"""
        if roles is None:
            roles = ["user"]

        # Validate username
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")

        if self.get_user_by_username(username) is not None:
            raise ValueError("Username already exists")

        # Validate email
        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email address")

        if self.get_user_by_email(email) is not None:
            raise ValueError("Email already registered")

        # Validate password
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not (
            re.search(r"[A-Z]", password)
            and re.search(r"[a-z]", password)
            and re.search(r"[0-9]", password)
        ):
            raise ValueError("Password must contain uppercase, lowercase, and numbers")

        # Validate roles
        for role in roles:
            if role not in self.roles:
                raise ValueError(f"Invalid role: {role}")

        # Hash password
        hashed_password = self._hash_password(password)

        # Create user
        user = User(
            id=str(uuid.uuid4()),
            username=username,
            email=email,
            password=hashed_password,
            roles=roles,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            last_login=None,
            login_count=0,
            status="active",
            email_verified=False,
        )

        self.users[user.id] = user

        # Log activity
        self._log_activity(user.id, "user_created", f"User {username} created")

        # Send welcome email
        self._send_welcome_email(email, username)

        return user

    def update_user(self, user_id: str, data: dict[str, Any]) -> User:
        """Updates user information with validation"""
        user = self.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        # Validate and update username
        if "username" in data:
            if not data["username"] or len(data["username"]) < 3:
                raise ValueError("Username must be at least 3 characters long")

            existing_user = self.get_user_by_username(data["username"])
            if existing_user is not None and existing_user.id != user_id:
                raise ValueError("Username already exists")

            user.username = data["username"]

        # Validate and update email
        if "email" in data:
            email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
            if not re.match(email_pattern, data["email"]):
                raise ValueError("Invalid email address")

            existing_user = self.get_user_by_email(data["email"])
            if existing_user is not None and existing_user.id != user_id:
                raise ValueError("Email already registered")

            old_email = user.email
            user.email = data["email"]
            user.email_verified = False

            # Send email change notification
            self._send_email_change_notification(old_email, data["email"])

        # Update password if provided
        if "password" in data:
            if len(data["password"]) < 8:
                raise ValueError("Password must be at least 8 characters long")

            if not (
                re.search(r"[A-Z]", data["password"])
                and re.search(r"[a-z]", data["password"])
                and re.search(r"[0-9]", data["password"])
            ):
                raise ValueError(
                    "Password must contain uppercase, lowercase, and numbers"
                )

            user.password = self._hash_password(data["password"])

        # Update roles if provided
        if "roles" in data:
            for role in data["roles"]:
                if role not in self.roles:
                    raise ValueError(f"Invalid role: {role}")
            user.roles = data["roles"]

        # Update profile data
        if "profile" in data:
            user.profile.update(data["profile"])

        # Update status
        if "status" in data:
            if data["status"] not in ["active", "inactive", "suspended"]:
                raise ValueError("Invalid status")
            user.status = data["status"]

        user.updated_at = datetime.now().isoformat()
        self.users[user_id] = user

        # Log activity
        self._log_activity(user_id, "user_updated", f"User {user.username} updated")

        return user

    def delete_user(self, user_id: str) -> bool:
        """Deletes a user and cleans up associated data"""
        user = self.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        # Log activity before deletion
        self._log_activity(user_id, "user_deleted", f"User {user.username} deleted")

        # Send goodbye email
        self._send_goodbye_email(user.email, user.username)

        # Clean up sessions
        self._cleanup_user_sessions(user_id)

        # Remove user
        del self.users[user_id]

        return True

    # ==== AUTHENTICATION ====

    def login(self, username: str, password: str) -> Session:
        """Authenticates user and creates session"""
        user = self.get_user_by_username(username)
        if user is None:
            raise ValueError("Invalid username or password")

        if user.status != "active":
            raise RuntimeError("Account is not active")

        if not self._verify_password(password, user.password):
            # Log failed login attempt
            self._log_activity(
                user.id, "login_failed", f"Failed login attempt for {username}"
            )
            raise ValueError("Invalid username or password")

        # Generate session token
        session_token = self._generate_session_token()
        session = Session(
            token=session_token,
            user_id=user.id,
            created_at=datetime.now().isoformat(),
            expires_at=(datetime.now() + timedelta(hours=24)).isoformat(),
            ip_address="unknown",  # Would be from request in real app
            user_agent="unknown",  # Would be from request in real app
        )

        self.sessions[session_token] = session

        # Update user login info
        user.last_login = datetime.now().isoformat()
        user.login_count += 1
        self.users[user.id] = user

        # Log successful login
        self._log_activity(user.id, "login_success", f"User {username} logged in")

        # Send login notification email
        self._send_login_notification_email(
            user.email, user.username, session.ip_address
        )

        return session

    def validate_session(self, token: str) -> User | None:
        """Validates session token and returns user data"""
        if token not in self.sessions:
            return None

        session = self.sessions[token]

        # Check if session is expired
        if datetime.fromisoformat(session.expires_at) < datetime.now():
            del self.sessions[token]
            return None

        user = self.get_user_by_id(session.user_id)
        if user is None or user.status != "active":
            del self.sessions[token]
            return None

        return user

    def logout(self, token: str) -> bool:
        """Logs out user and destroys session"""
        if token in self.sessions:
            session = self.sessions[token]
            user = self.get_user_by_id(session.user_id)

            if user is not None:
                self._log_activity(
                    user.id, "logout", f"User {user.username} logged out"
                )

            del self.sessions[token]
            return True

        return False

    # ==== AUTHORIZATION ====

    def has_permission(self, user_id: str, permission: str) -> bool:
        """Checks if user has specific permission"""
        user = self.get_user_by_id(user_id)
        if user is None or user.status != "active":
            return False

        for role_name in user.roles:
            if role_name in self.roles:
                role = self.roles[role_name]
                if permission in role.permissions:
                    return True

        return False

    def has_role(self, user_id: str, role_name: str) -> bool:
        """Checks if user has specific role"""
        user = self.get_user_by_id(user_id)
        if user is None:
            return False

        return role_name in user.roles

    def assign_role(self, user_id: str, role_name: str) -> bool:
        """Assigns role to user"""
        if role_name not in self.roles:
            raise ValueError(f"Invalid role: {role_name}")

        user = self.get_user_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        if role_name not in user.roles:
            user.roles.append(role_name)
            self.users[user_id] = user
            self._log_activity(
                user_id,
                "role_assigned",
                f"Role {role_name} assigned to user {user.username}",
            )

        return True

    # ==== EMAIL OPERATIONS ====

    def _send_welcome_email(self, email: str, username: str) -> None:
        """Sends welcome email to new user"""
        if not self.email_enabled:
            return

        subject = "Welcome to our platform!"
        message = f"Hello {username},\n\nWelcome to our platform! Your account has been created successfully.\n\nBest regards,\nThe Team"

        self._queue_email(email, subject, message)

    def _send_email_change_notification(self, old_email: str, new_email: str) -> None:
        """Sends email change notification"""
        if not self.email_enabled:
            return

        subject = "Email address changed"
        message = f"Your email address has been changed from {old_email} to {new_email}.\n\nIf you didn't make this change, please contact support immediately."

        self._queue_email(old_email, subject, message)
        self._queue_email(new_email, subject, message)

    def _send_login_notification_email(
        self, email: str, username: str, ip_address: str
    ) -> None:
        """Sends login notification email"""
        if not self.email_enabled:
            return

        subject = "New login detected"
        message = f"Hello {username},\n\nA new login was detected from IP address: {ip_address}\n\nIf this wasn't you, please change your password immediately."

        self._queue_email(email, subject, message)

    def _send_goodbye_email(self, email: str, username: str) -> None:
        """Sends goodbye email when user is deleted"""
        if not self.email_enabled:
            return

        subject = "Account deleted"
        message = f"Hello {username},\n\nYour account has been deleted. We're sorry to see you go!\n\nBest regards,\nThe Team"

        self._queue_email(email, subject, message)

    def _queue_email(self, to: str, subject: str, message: str) -> None:
        """Queues email for sending"""
        self.email_queue.append(
            EmailItem(
                to=to,
                subject=subject,
                message=message,
                queued_at=datetime.now().isoformat(),
            )
        )

    # ==== ACTIVITY LOGGING ====

    def _log_activity(self, user_id: str, action: str, description: str) -> None:
        """Logs user activity"""
        if not self.logging_enabled:
            return

        self.activity_log.append(
            ActivityLog(
                user_id=user_id,
                action=action,
                description=description,
                timestamp=datetime.now().isoformat(),
                ip_address="unknown",  # Would be from request in real app
            )
        )

    def get_user_activity_log(self, user_id: str) -> list[ActivityLog]:
        """Gets activity log for specific user"""
        return [log for log in self.activity_log if log.user_id == user_id]

    # ==== HELPER METHODS ====

    def get_user_by_id(self, user_id: str) -> User | None:
        """Gets user by ID"""
        return self.users.get(user_id)

    def get_user_by_username(self, username: str) -> User | None:
        """Gets user by username"""
        for user in self.users.values():
            if user.username == username:
                return user
        return None

    def get_user_by_email(self, email: str) -> User | None:
        """Gets user by email"""
        for user in self.users.values():
            if user.email == email:
                return user
        return None

    def get_all_users(self) -> list[User]:
        """Gets all users"""
        return list(self.users.values())

    def get_user_count(self) -> int:
        """Gets user count"""
        return len(self.users)

    def _cleanup_user_sessions(self, user_id: str) -> None:
        """Cleans up sessions for a user"""
        tokens_to_remove = []
        for token, session in self.sessions.items():
            if session.user_id == user_id:
                tokens_to_remove.append(token)

        for token in tokens_to_remove:
            del self.sessions[token]

    def _initialize_default_roles(self) -> None:
        """Initializes default roles"""
        self.roles = {
            "admin": Role(
                name="Administrator",
                permissions=[
                    "user_create",
                    "user_read",
                    "user_update",
                    "user_delete",
                    "admin_panel",
                ],
            ),
            "moderator": Role(
                name="Moderator",
                permissions=["user_read", "user_update", "moderate_content"],
            ),
            "user": Role(name="User", permissions=["user_read", "profile_update"]),
        }

    def _initialize_default_permissions(self) -> None:
        """Initializes default permissions"""
        self.permissions = {
            "user_create": "Create new users",
            "user_read": "View user information",
            "user_update": "Update user information",
            "user_delete": "Delete users",
            "admin_panel": "Access admin panel",
            "moderate_content": "Moderate user content",
            "profile_update": "Update own profile",
        }

    # Utility methods
    def _generate_id(self) -> str:
        """Generates a unique ID"""
        return str(uuid.uuid4())

    def _generate_session_token(self) -> str:
        """Generates a session token"""
        return str(uuid.uuid4()).replace("-", "")

    def _hash_password(self, password: str) -> str:
        """Hashes a password (simplified for demo)"""
        return f"hashed_{password}"

    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifies a password against its hash"""
        return hashed_password == f"hashed_{password}"

    # Configuration methods
    def set_email_enabled(self, enabled: bool) -> None:
        """Sets email enabled state"""
        self.email_enabled = enabled

    def set_logging_enabled(self, enabled: bool) -> None:
        """Sets logging enabled state"""
        self.logging_enabled = enabled

    def get_email_queue(self) -> list[EmailItem]:
        """Gets email queue"""
        return self.email_queue

    def get_activity_log(self) -> list[ActivityLog]:
        """Gets activity log"""
        return self.activity_log
