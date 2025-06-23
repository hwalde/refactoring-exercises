import sys
from pathlib import Path

import pytest

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_manager import UserManager


class TestUserManager:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.user_manager = UserManager()
        # Disable email and logging for tests
        self.user_manager.set_email_enabled(False)
        self.user_manager.set_logging_enabled(False)

    def test_create_user_with_valid_data(self):
        """Test creating a user with valid data."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.roles == ["user"]
        assert user.status == "active"
        assert user.email_verified is False
        assert user.login_count == 0

    def test_create_user_with_custom_roles(self):
        """Test creating a user with custom roles."""
        user = self.user_manager.create_user(
            "admin", "admin@example.com", "Password123", ["admin"]
        )

        assert user.roles == ["admin"]

    def test_create_user_with_invalid_username(self):
        """Test creating a user with invalid username."""
        with pytest.raises(
            ValueError, match="Username must be at least 3 characters long"
        ):
            self.user_manager.create_user("ab", "test@example.com", "Password123")

    def test_create_user_with_duplicate_username(self):
        """Test creating a user with duplicate username."""
        self.user_manager.create_user("testuser", "test1@example.com", "Password123")

        with pytest.raises(ValueError, match="Username already exists"):
            self.user_manager.create_user(
                "testuser", "test2@example.com", "Password123"
            )

    def test_create_user_with_invalid_email(self):
        """Test creating a user with invalid email."""
        with pytest.raises(ValueError, match="Invalid email address"):
            self.user_manager.create_user("testuser", "invalid-email", "Password123")

    def test_create_user_with_duplicate_email(self):
        """Test creating a user with duplicate email."""
        self.user_manager.create_user("user1", "test@example.com", "Password123")

        with pytest.raises(ValueError, match="Email already registered"):
            self.user_manager.create_user("user2", "test@example.com", "Password123")

    def test_create_user_with_weak_password(self):
        """Test creating a user with weak password."""
        with pytest.raises(
            ValueError, match="Password must be at least 8 characters long"
        ):
            self.user_manager.create_user("testuser", "test@example.com", "123")

    def test_create_user_with_invalid_password_format(self):
        """Test creating a user with invalid password format."""
        with pytest.raises(
            ValueError, match="Password must contain uppercase, lowercase, and numbers"
        ):
            self.user_manager.create_user("testuser", "test@example.com", "password")

    def test_create_user_with_invalid_role(self):
        """Test creating a user with invalid role."""
        with pytest.raises(ValueError, match="Invalid role: invalid"):
            self.user_manager.create_user(
                "testuser", "test@example.com", "Password123", ["invalid"]
            )

    def test_update_user_username(self):
        """Test updating user username."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        updated_user = self.user_manager.update_user(
            user.id, {"username": "newusername"}
        )

        assert updated_user.username == "newusername"

    def test_update_user_email(self):
        """Test updating user email."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        updated_user = self.user_manager.update_user(
            user.id, {"email": "newemail@example.com"}
        )

        assert updated_user.email == "newemail@example.com"
        assert updated_user.email_verified is False

    def test_update_user_with_invalid_user_id(self):
        """Test updating user with invalid user ID."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.update_user("invalid-id", {"username": "newusername"})

    def test_delete_user(self):
        """Test deleting a user."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        result = self.user_manager.delete_user(user.id)

        assert result is True
        assert self.user_manager.get_user_by_id(user.id) is None

    def test_delete_user_with_invalid_id(self):
        """Test deleting user with invalid ID."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.delete_user("invalid-id")

    def test_login(self):
        """Test user login."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")

        session = self.user_manager.login("testuser", "Password123")

        assert session.token is not None
        assert session.user_id is not None
        assert session.created_at is not None
        assert session.expires_at is not None

    def test_login_with_invalid_username(self):
        """Test login with invalid username."""
        with pytest.raises(ValueError, match="Invalid username or password"):
            self.user_manager.login("nonexistent", "Password123")

    def test_login_with_invalid_password(self):
        """Test login with invalid password."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")

        with pytest.raises(ValueError, match="Invalid username or password"):
            self.user_manager.login("testuser", "WrongPassword")

    def test_login_with_inactive_user(self):
        """Test login with inactive user."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )
        self.user_manager.update_user(user.id, {"status": "inactive"})

        with pytest.raises(RuntimeError, match="Account is not active"):
            self.user_manager.login("testuser", "Password123")

    def test_validate_session(self):
        """Test session validation."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        session = self.user_manager.login("testuser", "Password123")

        user = self.user_manager.validate_session(session.token)

        assert user is not None
        assert user.username == "testuser"

    def test_validate_session_with_invalid_token(self):
        """Test session validation with invalid token."""
        user = self.user_manager.validate_session("invalid-token")

        assert user is None

    def test_logout(self):
        """Test user logout."""
        self.user_manager.create_user("testuser", "test@example.com", "Password123")
        session = self.user_manager.login("testuser", "Password123")

        result = self.user_manager.logout(session.token)

        assert result is True
        assert self.user_manager.validate_session(session.token) is None

    def test_logout_with_invalid_token(self):
        """Test logout with invalid token."""
        result = self.user_manager.logout("invalid-token")

        assert result is False

    def test_has_permission(self):
        """Test permission checking."""
        user = self.user_manager.create_user(
            "admin", "admin@example.com", "Password123", ["admin"]
        )

        assert self.user_manager.has_permission(user.id, "user_create") is True
        assert self.user_manager.has_permission(user.id, "invalid_permission") is False

    def test_has_permission_with_regular_user(self):
        """Test permission checking with regular user."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        assert self.user_manager.has_permission(user.id, "user_read") is True
        assert self.user_manager.has_permission(user.id, "user_delete") is False

    def test_has_role(self):
        """Test role checking."""
        user = self.user_manager.create_user(
            "admin", "admin@example.com", "Password123", ["admin"]
        )

        assert self.user_manager.has_role(user.id, "admin") is True
        assert self.user_manager.has_role(user.id, "moderator") is False

    def test_assign_role(self):
        """Test role assignment."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        result = self.user_manager.assign_role(user.id, "moderator")

        assert result is True
        assert self.user_manager.has_role(user.id, "moderator") is True

    def test_assign_role_with_invalid_role(self):
        """Test role assignment with invalid role."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        with pytest.raises(ValueError, match="Invalid role: invalid"):
            self.user_manager.assign_role(user.id, "invalid")

    def test_assign_role_with_invalid_user(self):
        """Test role assignment with invalid user."""
        with pytest.raises(ValueError, match="User not found"):
            self.user_manager.assign_role("invalid-id", "admin")

    def test_get_user_by_id(self):
        """Test getting user by ID."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        retrieved_user = self.user_manager.get_user_by_id(user.id)

        assert retrieved_user == user

    def test_get_user_by_id_with_invalid_id(self):
        """Test getting user by invalid ID."""
        user = self.user_manager.get_user_by_id("invalid-id")

        assert user is None

    def test_get_user_by_username(self):
        """Test getting user by username."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        retrieved_user = self.user_manager.get_user_by_username("testuser")

        assert retrieved_user == user

    def test_get_user_by_username_with_invalid_username(self):
        """Test getting user by invalid username."""
        user = self.user_manager.get_user_by_username("nonexistent")

        assert user is None

    def test_get_user_by_email(self):
        """Test getting user by email."""
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        retrieved_user = self.user_manager.get_user_by_email("test@example.com")

        assert retrieved_user == user

    def test_get_user_by_email_with_invalid_email(self):
        """Test getting user by invalid email."""
        user = self.user_manager.get_user_by_email("nonexistent@example.com")

        assert user is None

    def test_get_all_users(self):
        """Test getting all users."""
        user1 = self.user_manager.create_user(
            "user1", "user1@example.com", "Password123"
        )
        user2 = self.user_manager.create_user(
            "user2", "user2@example.com", "Password123"
        )

        users = self.user_manager.get_all_users()

        assert len(users) == 2
        assert user1 in users
        assert user2 in users

    def test_get_user_count(self):
        """Test getting user count."""
        assert self.user_manager.get_user_count() == 0

        self.user_manager.create_user("user1", "user1@example.com", "Password123")
        assert self.user_manager.get_user_count() == 1

        self.user_manager.create_user("user2", "user2@example.com", "Password123")
        assert self.user_manager.get_user_count() == 2

    def test_email_queue_with_enabled_email(self):
        """Test email queue when email is enabled."""
        self.user_manager.set_email_enabled(True)
        self.user_manager.create_user("testuser", "test@example.com", "Password123")

        email_queue = self.user_manager.get_email_queue()

        assert len(email_queue) == 1
        assert email_queue[0].to == "test@example.com"
        assert "Welcome" in email_queue[0].subject

    def test_activity_log_with_enabled_logging(self):
        """Test activity log when logging is enabled."""
        self.user_manager.set_logging_enabled(True)
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )

        activity_log = self.user_manager.get_activity_log()

        assert len(activity_log) == 1
        assert activity_log[0].user_id == user.id
        assert activity_log[0].action == "user_created"

    def test_get_user_activity_log(self):
        """Test getting user activity log."""
        self.user_manager.set_logging_enabled(True)
        user1 = self.user_manager.create_user(
            "user1", "user1@example.com", "Password123"
        )
        user2 = self.user_manager.create_user(
            "user2", "user2@example.com", "Password123"
        )

        user1_log = self.user_manager.get_user_activity_log(user1.id)

        assert len(user1_log) == 1
        assert user1_log[0].user_id == user1.id

    def test_complete_user_workflow(self):
        """Test complete user workflow."""
        # Create user
        user = self.user_manager.create_user(
            "testuser", "test@example.com", "Password123"
        )
        assert user is not None

        # Login
        session = self.user_manager.login("testuser", "Password123")
        assert session is not None

        # Validate session
        validated_user = self.user_manager.validate_session(session.token)
        assert validated_user.username == user.username

        # Check permissions
        assert self.user_manager.has_permission(user.id, "user_read") is True

        # Update user
        updated_user = self.user_manager.update_user(
            user.id, {"username": "updateduser"}
        )
        assert updated_user.username == "updateduser"

        # Logout
        assert self.user_manager.logout(session.token) is True

        # Verify session is invalid
        assert self.user_manager.validate_session(session.token) is None
