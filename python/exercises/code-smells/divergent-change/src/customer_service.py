"""Customer service module with divergent change code smell."""

import hashlib
import re
from datetime import datetime, timedelta
from typing import Any


class CustomerService:
    """Service managing all customer-related operations (with divergent change issues)."""

    def __init__(self) -> None:
        """Initialize customer service with empty storage."""
        self._customers: dict[int, dict[str, Any]] = {}
        self._login_attempts: dict[str, list[datetime]] = {}
        self._marketing_preferences: dict[int, dict[str, Any]] = {}
        self._order_history: dict[int, dict[int, dict[str, Any]]] = {}
        self._addresses: dict[int, dict[int, dict[str, Any]]] = {}

    def register_customer(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> int:
        """Register a new customer in the system.

        Args:
            email: Customer's email address
            password: Customer's password (min 8 characters)
            first_name: Customer's first name
            last_name: Customer's last name

        Returns:
            The ID of the newly registered customer

        Raises:
            ValueError: If input validation fails
        """
        if not self._is_valid_email(email):
            raise ValueError("Invalid email format")

        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")

        if not first_name or not last_name:
            raise ValueError("First name and last name are required")

        for customer in self._customers.values():
            if customer["email"] == email:
                raise ValueError("Customer with this email already exists")

        customer_id = len(self._customers) + 1
        self._customers[customer_id] = {
            "id": customer_id,
            "email": email,
            "password": self._hash_password(password),
            "first_name": first_name,
            "last_name": last_name,
            "phone": None,
            "status": "active",
            "created_at": datetime.now(),
            "last_login": None,
        }

        self._marketing_preferences[customer_id] = {
            "email_marketing": True,
            "sms_marketing": False,
            "push_notifications": True,
            "preferred_channels": ["email"],
        }

        return customer_id

    def authenticate_customer(self, email: str, password: str) -> int | None:
        """Authenticate a customer by email and password.

        Args:
            email: Customer's email address
            password: Customer's password

        Returns:
            Customer ID if authentication successful, None otherwise

        Raises:
            RuntimeError: If account is locked due to failed attempts
        """
        customer = self._find_customer_by_email(email)

        if not customer:
            self._record_failed_login_attempt(email)
            return None

        if self._is_account_locked(customer["id"]):
            raise RuntimeError(
                "Account is temporarily locked due to too many failed attempts"
            )

        if not self._verify_password(password, customer["password"]):
            self._record_failed_login_attempt(email)
            return None

        self._clear_failed_login_attempts(customer["id"])
        self._update_last_login(customer["id"])

        return customer["id"]

    def update_contact_information(
        self, customer_id: int, first_name: str, last_name: str, phone: str
    ) -> None:
        """Update customer's contact information.

        Args:
            customer_id: Customer's ID
            first_name: Updated first name
            last_name: Updated last name
            phone: Updated phone number

        Raises:
            ValueError: If customer not found or validation fails
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if not first_name or not last_name:
            raise ValueError("First name and last name are required")

        if phone and not self._is_valid_phone(phone):
            raise ValueError("Invalid phone number format")

        self._customers[customer_id]["first_name"] = first_name
        self._customers[customer_id]["last_name"] = last_name
        self._customers[customer_id]["phone"] = phone

    def add_customer_address(
        self,
        customer_id: int,
        street: str,
        city: str,
        zip_code: str,
        country: str,
        is_default: bool = False,
    ) -> int:
        """Add a new address for a customer.

        Args:
            customer_id: Customer's ID
            street: Street address
            city: City name
            zip_code: ZIP/postal code
            country: Country name
            is_default: Whether this should be the default address

        Returns:
            The ID of the newly created address

        Raises:
            ValueError: If customer not found or validation fails
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if not all([street, city, zip_code, country]):
            raise ValueError("All address fields are required")

        if customer_id not in self._addresses:
            self._addresses[customer_id] = {}

        address_id = len(self._addresses[customer_id]) + 1

        if is_default:
            for address in self._addresses[customer_id].values():
                address["is_default"] = False

        self._addresses[customer_id][address_id] = {
            "id": address_id,
            "street": street,
            "city": city,
            "zip_code": zip_code,
            "country": country,
            "is_default": is_default or len(self._addresses[customer_id]) == 0,
        }

        return address_id

    def update_marketing_preferences(
        self,
        customer_id: int,
        email_marketing: bool,
        sms_marketing: bool,
        push_notifications: bool,
        preferred_channels: list[str],
    ) -> None:
        """Update customer's marketing preferences.

        Args:
            customer_id: Customer's ID
            email_marketing: Allow email marketing
            sms_marketing: Allow SMS marketing
            push_notifications: Allow push notifications
            preferred_channels: List of preferred marketing channels

        Raises:
            ValueError: If customer not found or invalid channels provided
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        valid_channels = ["email", "sms", "push", "mail"]
        for channel in preferred_channels:
            if channel not in valid_channels:
                raise ValueError(f"Invalid marketing channel: {channel}")

        self._marketing_preferences[customer_id] = {
            "email_marketing": email_marketing,
            "sms_marketing": sms_marketing,
            "push_notifications": push_notifications,
            "preferred_channels": preferred_channels,
        }

    def send_marketing_campaign(
        self, customer_id: int, subject: str, content: str, channel: str
    ) -> bool:
        """Send marketing campaign to customer.

        Args:
            customer_id: Customer's ID
            subject: Campaign subject
            content: Campaign content
            channel: Marketing channel to use

        Returns:
            True if campaign was sent, False if customer opted out

        Raises:
            ValueError: If customer not found or invalid channel
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if customer_id not in self._marketing_preferences:
            return False

        preferences = self._marketing_preferences[customer_id]

        if channel == "email":
            if (
                not preferences["email_marketing"]
                or "email" not in preferences["preferred_channels"]
            ):
                return False
        elif channel == "sms":
            if (
                not preferences["sms_marketing"]
                or "sms" not in preferences["preferred_channels"]
            ):
                return False
        elif channel == "push":
            if (
                not preferences["push_notifications"]
                or "push" not in preferences["preferred_channels"]
            ):
                return False
        else:
            raise ValueError(f"Unsupported marketing channel: {channel}")

        return True

    def record_purchase(
        self, customer_id: int, items: list[dict[str, Any]], total_amount: float
    ) -> int:
        """Record a customer purchase.

        Args:
            customer_id: Customer's ID
            items: List of purchased items
            total_amount: Total purchase amount

        Returns:
            The ID of the created order

        Raises:
            ValueError: If customer not found or validation fails
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if not items:
            raise ValueError("Purchase must contain at least one item")

        if total_amount <= 0:
            raise ValueError("Total amount must be positive")

        if customer_id not in self._order_history:
            self._order_history[customer_id] = {}

        order_id = len(self._order_history[customer_id]) + 1
        self._order_history[customer_id][order_id] = {
            "id": order_id,
            "items": items,
            "total_amount": total_amount,
            "order_date": datetime.now(),
            "status": "completed",
        }

        return order_id

    def get_customer_spending_history(self, customer_id: int) -> list[dict[str, Any]]:
        """Get customer's spending history.

        Args:
            customer_id: Customer's ID

        Returns:
            List of spending history entries, sorted by date (newest first)

        Raises:
            ValueError: If customer not found
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if customer_id not in self._order_history:
            return []

        history = []
        for order in self._order_history[customer_id].values():
            history.append(
                {
                    "order_id": order["id"],
                    "amount": order["total_amount"],
                    "date": order["order_date"],
                    "item_count": len(order["items"]),
                }
            )

        history.sort(key=lambda x: x["date"], reverse=True)
        return history

    def calculate_customer_lifetime_value(self, customer_id: int) -> float:
        """Calculate customer's lifetime value.

        Args:
            customer_id: Customer's ID

        Returns:
            Total amount spent by customer

        Raises:
            ValueError: If customer not found
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        if customer_id not in self._order_history:
            return 0.0

        total_spent = 0.0
        for order in self._order_history[customer_id].values():
            total_spent += order["total_amount"]

        return total_spent

    def get_customer_profile(self, customer_id: int) -> dict[str, Any]:
        """Get complete customer profile.

        Args:
            customer_id: Customer's ID

        Returns:
            Dictionary containing all customer information

        Raises:
            ValueError: If customer not found
        """
        if customer_id not in self._customers:
            raise ValueError("Customer not found")

        customer = self._customers[customer_id]

        return {
            "personal": {
                "id": customer["id"],
                "first_name": customer["first_name"],
                "last_name": customer["last_name"],
                "email": customer["email"],
                "phone": customer["phone"],
                "status": customer["status"],
            },
            "addresses": self._addresses.get(customer_id, {}),
            "marketing": self._marketing_preferences.get(customer_id),
            "order_history": self.get_customer_spending_history(customer_id),
            "lifetime_value": self.calculate_customer_lifetime_value(customer_id),
        }

    def _find_customer_by_email(self, email: str) -> dict[str, Any] | None:
        """Find customer by email address."""
        for customer in self._customers.values():
            if customer["email"] == email:
                return customer
        return None

    def _record_failed_login_attempt(self, email: str) -> None:
        """Record a failed login attempt for an email."""
        if email not in self._login_attempts:
            self._login_attempts[email] = []
        self._login_attempts[email].append(datetime.now())

    def _is_account_locked(self, customer_id: int) -> bool:
        """Check if account is locked due to failed login attempts."""
        customer = self._customers[customer_id]
        email = customer["email"]

        if email not in self._login_attempts:
            return False

        recent_attempts = [
            attempt
            for attempt in self._login_attempts[email]
            if attempt > datetime.now() - timedelta(minutes=15)
        ]

        return len(recent_attempts) >= 3

    def _clear_failed_login_attempts(self, customer_id: int) -> None:
        """Clear failed login attempts for a customer."""
        customer = self._customers[customer_id]
        email = customer["email"]
        if email in self._login_attempts:
            del self._login_attempts[email]

    def _update_last_login(self, customer_id: int) -> None:
        """Update customer's last login timestamp."""
        self._customers[customer_id]["last_login"] = datetime.now()

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone number format."""
        pattern = r"^\+?[1-9]\d{1,14}$"
        return re.match(pattern, phone) is not None

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return self._hash_password(password) == hashed
