"""
User class for managing user information in the system.

This class currently has a public email attribute that can be accessed
and modified directly from outside the class, which leads to
data integrity issues.
"""


class User:
    """User class for managing user information in the system.

    This class currently has a public email attribute that can be accessed
    and modified directly from outside the class, which leads to
    data integrity issues.
    """

    def __init__(self, name: str, email: str) -> None:
        """Creates a new User instance.

        Args:
            name: The user's full name
            email: The user's email address
        """
        self.name: str = name
        self.email: str = email  # No validation here!

    def get_display_name(self) -> str:
        """Gets a formatted display name for the user.

        Returns:
            Formatted string with name and email
        """
        return f"{self.name} ({self.email})"

    def has_business_email(self) -> bool:
        """Checks if the user has a valid email domain for business use.

        Returns:
            True if email contains @company.com domain
        """
        return "@company.com" in self.email

    def get_email_domain(self) -> str:
        """Gets the email domain.

        Returns:
            The domain part of the email address
        """
        parts = self.email.split("@")
        return parts[1] if len(parts) > 1 else ""

    def get_email(self) -> str:
        """Gets the user's email address.

        Returns:
            The user's email address
        """
        return self.email

    def set_email(self, email: str) -> None:
        """Sets the user's email address.

        Note: This method currently has no validation!

        Args:
            email: The new email address
        """
        self.email = email
