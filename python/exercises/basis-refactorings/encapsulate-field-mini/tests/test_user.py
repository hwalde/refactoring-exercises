"""Tests for the User class."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import unittest

from user import User


class TestUser(unittest.TestCase):
    """Test cases for the User class."""

    def test_can_create_user_with_valid_email(self) -> None:
        """Test that a user can be created with a valid email."""
        user = User("John Doe", "john@example.com")

        self.assertEqual("John Doe", user.name)
        self.assertEqual("john@example.com", user.get_email())

    def test_can_get_display_name(self) -> None:
        """Test that display name is formatted correctly."""
        user = User("Jane Smith", "jane@company.com")

        self.assertEqual("Jane Smith (jane@company.com)", user.get_display_name())

    def test_can_detect_business_email(self) -> None:
        """Test that business email detection works correctly."""
        business_user = User("Bob Manager", "bob@company.com")
        external_user = User("Alice Client", "alice@external.com")

        self.assertTrue(business_user.has_business_email())
        self.assertFalse(external_user.has_business_email())

    def test_can_get_email_domain(self) -> None:
        """Test that email domain extraction works correctly."""
        user = User("Tom Developer", "tom@example.org")

        self.assertEqual("example.org", user.get_email_domain())

    def test_can_set_email_after_creation(self) -> None:
        """Test that email can be changed after user creation."""
        user = User("Sarah Tester", "sarah@old.com")

        user.set_email("sarah@new.com")

        self.assertEqual("sarah@new.com", user.get_email())

    def test_currently_allows_empty_email(self) -> None:
        """Test that demonstrates current problematic behavior.

        After refactoring, this should raise an exception.
        """
        user = User("Invalid User", "")

        self.assertEqual("", user.get_email())

    def test_currently_allows_email_without_at_symbol(self) -> None:
        """Test that demonstrates current problematic behavior.

        After refactoring, this should raise an exception.
        """
        user = User("Invalid User", "notanemail")

        self.assertEqual("notanemail", user.get_email())

    def test_currently_allows_setting_empty_email(self) -> None:
        """Test that demonstrates current problematic behavior.

        After refactoring, this should raise an exception.
        """
        user = User("Valid User", "valid@email.com")

        user.set_email("")

        self.assertEqual("", user.get_email())

    def test_currently_allows_setting_email_without_at_symbol(self) -> None:
        """Test that demonstrates current problematic behavior.

        After refactoring, this should raise an exception.
        """
        user = User("Valid User", "valid@email.com")

        user.set_email("invalid-email")

        self.assertEqual("invalid-email", user.get_email())

    def test_can_set_valid_email_after_creation(self) -> None:
        """Test that valid email can be set and affects display name."""
        user = User("Change User", "old@domain.com")

        user.set_email("new@domain.com")

        self.assertEqual("new@domain.com", user.get_email())
        self.assertEqual("Change User (new@domain.com)", user.get_display_name())

    def test_email_domain_works_after_email_change(self) -> None:
        """Test that email domain extraction works after email change."""
        user = User("Domain User", "user@first.com")

        user.set_email("user@second.org")

        self.assertEqual("second.org", user.get_email_domain())

    def test_business_email_detection_works_after_email_change(self) -> None:
        """Test that business email detection works after email change."""
        user = User("Business User", "user@external.com")
        self.assertFalse(user.has_business_email())

        user.set_email("user@company.com")
        self.assertTrue(user.has_business_email())


if __name__ == "__main__":
    unittest.main()
