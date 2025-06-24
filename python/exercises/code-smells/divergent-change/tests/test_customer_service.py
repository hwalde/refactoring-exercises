"""Test suite for CustomerService with divergent change issues."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from customer_service import CustomerService


class TestCustomerService:
    """Test cases for CustomerService functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures before each test method."""
        self.customer_service = CustomerService()

    def test_register_customer(self) -> None:
        """Test successful customer registration."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        assert isinstance(customer_id, int)
        assert customer_id > 0

    def test_register_customer_with_invalid_email(self) -> None:
        """Test customer registration with invalid email."""
        with pytest.raises(ValueError, match="Invalid email format"):
            self.customer_service.register_customer(
                "invalid-email", "password123", "John", "Doe"
            )

    def test_register_customer_with_short_password(self) -> None:
        """Test customer registration with password too short."""
        with pytest.raises(ValueError, match="Password must be at least 8 characters"):
            self.customer_service.register_customer(
                "john.doe@example.com", "123", "John", "Doe"
            )

    def test_register_customer_with_empty_names(self) -> None:
        """Test customer registration with empty names."""
        with pytest.raises(ValueError, match="First name and last name are required"):
            self.customer_service.register_customer(
                "john.doe@example.com", "password123", "", "Doe"
            )

    def test_register_customer_with_duplicate_email(self) -> None:
        """Test customer registration with duplicate email."""
        self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(ValueError, match="Customer with this email already exists"):
            self.customer_service.register_customer(
                "john.doe@example.com", "password456", "Jane", "Smith"
            )

    def test_authenticate_customer_success(self) -> None:
        """Test successful customer authentication."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        authenticated_id = self.customer_service.authenticate_customer(
            "john.doe@example.com", "password123"
        )

        assert authenticated_id == customer_id

    def test_authenticate_customer_with_wrong_password(self) -> None:
        """Test customer authentication with wrong password."""
        self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        result = self.customer_service.authenticate_customer(
            "john.doe@example.com", "wrongpassword"
        )

        assert result is None

    def test_authenticate_customer_with_nonexistent_email(self) -> None:
        """Test customer authentication with non-existent email."""
        result = self.customer_service.authenticate_customer(
            "nonexistent@example.com", "password123"
        )

        assert result is None

    def test_account_locking_after_failed_attempts(self) -> None:
        """Test account locking after multiple failed login attempts."""
        self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        # Make 3 failed attempts
        for _ in range(3):
            self.customer_service.authenticate_customer(
                "john.doe@example.com", "wrongpassword"
            )

        with pytest.raises(
            RuntimeError,
            match="Account is temporarily locked due to too many failed attempts",
        ):
            self.customer_service.authenticate_customer(
                "john.doe@example.com", "password123"
            )

    def test_update_contact_information(self) -> None:
        """Test updating customer contact information."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        self.customer_service.update_contact_information(
            customer_id, "Johnny", "Doe-Smith", "+1234567890"
        )

        profile = self.customer_service.get_customer_profile(customer_id)
        assert profile["personal"]["first_name"] == "Johnny"
        assert profile["personal"]["last_name"] == "Doe-Smith"
        assert profile["personal"]["phone"] == "+1234567890"

    def test_update_contact_information_with_invalid_phone(self) -> None:
        """Test updating contact information with invalid phone number."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(ValueError, match="Invalid phone number format"):
            self.customer_service.update_contact_information(
                customer_id, "Johnny", "Doe-Smith", "invalid-phone"
            )

    def test_update_contact_information_for_nonexistent_customer(self) -> None:
        """Test updating contact information for non-existent customer."""
        with pytest.raises(ValueError, match="Customer not found"):
            self.customer_service.update_contact_information(
                999, "Johnny", "Doe-Smith", "+1234567890"
            )

    def test_add_customer_address(self) -> None:
        """Test adding customer address."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        address_id = self.customer_service.add_customer_address(
            customer_id, "123 Main St", "New York", "10001", "USA", True
        )

        assert isinstance(address_id, int)
        assert address_id > 0

        profile = self.customer_service.get_customer_profile(customer_id)
        assert len(profile["addresses"]) == 1
        assert profile["addresses"][address_id]["is_default"] is True

    def test_add_multiple_addresses(self) -> None:
        """Test adding multiple addresses with default handling."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        address1_id = self.customer_service.add_customer_address(
            customer_id, "123 Main St", "New York", "10001", "USA"
        )

        address2_id = self.customer_service.add_customer_address(
            customer_id, "456 Oak Ave", "Los Angeles", "90210", "USA", True
        )

        profile = self.customer_service.get_customer_profile(customer_id)
        assert len(profile["addresses"]) == 2
        assert profile["addresses"][address1_id]["is_default"] is False
        assert profile["addresses"][address2_id]["is_default"] is True

    def test_add_address_with_missing_fields(self) -> None:
        """Test adding address with missing required fields."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(ValueError, match="All address fields are required"):
            self.customer_service.add_customer_address(
                customer_id, "", "New York", "10001", "USA"
            )

    def test_update_marketing_preferences(self) -> None:
        """Test updating customer marketing preferences."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        self.customer_service.update_marketing_preferences(
            customer_id, False, True, False, ["sms", "mail"]
        )

        profile = self.customer_service.get_customer_profile(customer_id)
        marketing = profile["marketing"]

        assert marketing["email_marketing"] is False
        assert marketing["sms_marketing"] is True
        assert marketing["push_notifications"] is False
        assert marketing["preferred_channels"] == ["sms", "mail"]

    def test_update_marketing_preferences_with_invalid_channel(self) -> None:
        """Test updating marketing preferences with invalid channel."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(ValueError, match="Invalid marketing channel: invalid"):
            self.customer_service.update_marketing_preferences(
                customer_id, True, False, True, ["email", "invalid"]
            )

    def test_send_marketing_campaign_success(self) -> None:
        """Test sending marketing campaign successfully."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        result = self.customer_service.send_marketing_campaign(
            customer_id, "Special Offer", "Check out our latest deals!", "email"
        )

        assert result is True

    def test_send_marketing_campaign_with_opt_out(self) -> None:
        """Test sending marketing campaign with customer opted out."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        self.customer_service.update_marketing_preferences(
            customer_id, False, False, False, []
        )

        result = self.customer_service.send_marketing_campaign(
            customer_id, "Special Offer", "Check out our latest deals!", "email"
        )

        assert result is False

    def test_send_marketing_campaign_with_unsupported_channel(self) -> None:
        """Test sending marketing campaign with unsupported channel."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(
            ValueError, match="Unsupported marketing channel: carrier-pigeon"
        ):
            self.customer_service.send_marketing_campaign(
                customer_id,
                "Special Offer",
                "Check out our latest deals!",
                "carrier-pigeon",
            )

    def test_record_purchase(self) -> None:
        """Test recording a customer purchase."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        items = [
            {"name": "Product A", "price": 29.99, "quantity": 2},
            {"name": "Product B", "price": 15.50, "quantity": 1},
        ]

        order_id = self.customer_service.record_purchase(customer_id, items, 75.48)

        assert isinstance(order_id, int)
        assert order_id > 0

    def test_record_purchase_with_empty_items(self) -> None:
        """Test recording purchase with empty items list."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        with pytest.raises(ValueError, match="Purchase must contain at least one item"):
            self.customer_service.record_purchase(customer_id, [], 0.0)

    def test_record_purchase_with_invalid_amount(self) -> None:
        """Test recording purchase with invalid amount."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        items = [{"name": "Product A", "price": 29.99, "quantity": 1}]

        with pytest.raises(ValueError, match="Total amount must be positive"):
            self.customer_service.record_purchase(customer_id, items, -10.0)

    def test_get_customer_spending_history(self) -> None:
        """Test getting customer spending history."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        items1 = [{"name": "Product A", "price": 29.99, "quantity": 1}]
        items2 = [{"name": "Product B", "price": 15.50, "quantity": 2}]

        self.customer_service.record_purchase(customer_id, items1, 29.99)
        self.customer_service.record_purchase(customer_id, items2, 31.00)

        history = self.customer_service.get_customer_spending_history(customer_id)

        assert len(history) == 2
        assert history[0]["amount"] == 31.00  # Most recent first
        assert history[1]["amount"] == 29.99

    def test_get_customer_spending_history_for_customer_without_orders(self) -> None:
        """Test getting spending history for customer without orders."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        history = self.customer_service.get_customer_spending_history(customer_id)

        assert len(history) == 0

    def test_calculate_customer_lifetime_value(self) -> None:
        """Test calculating customer lifetime value."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        items1 = [{"name": "Product A", "price": 29.99, "quantity": 1}]
        items2 = [{"name": "Product B", "price": 15.50, "quantity": 2}]

        self.customer_service.record_purchase(customer_id, items1, 29.99)
        self.customer_service.record_purchase(customer_id, items2, 31.00)

        lifetime_value = self.customer_service.calculate_customer_lifetime_value(
            customer_id
        )

        assert abs(lifetime_value - 60.99) < 0.01

    def test_calculate_customer_lifetime_value_for_customer_without_orders(
        self,
    ) -> None:
        """Test calculating lifetime value for customer without orders."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        lifetime_value = self.customer_service.calculate_customer_lifetime_value(
            customer_id
        )

        assert lifetime_value == 0.0

    def test_get_customer_profile(self) -> None:
        """Test getting complete customer profile."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        self.customer_service.update_contact_information(
            customer_id, "Johnny", "Doe", "+1234567890"
        )
        self.customer_service.add_customer_address(
            customer_id, "123 Main St", "New York", "10001", "USA"
        )
        self.customer_service.record_purchase(
            customer_id, [{"name": "Product A", "price": 29.99}], 29.99
        )

        profile = self.customer_service.get_customer_profile(customer_id)

        assert "personal" in profile
        assert "addresses" in profile
        assert "marketing" in profile
        assert "order_history" in profile
        assert "lifetime_value" in profile

        assert profile["personal"]["first_name"] == "Johnny"
        assert profile["personal"]["email"] == "john.doe@example.com"
        assert len(profile["addresses"]) == 1
        assert len(profile["order_history"]) == 1
        assert profile["lifetime_value"] == 29.99

    def test_get_customer_profile_for_nonexistent_customer(self) -> None:
        """Test getting profile for non-existent customer."""
        with pytest.raises(ValueError, match="Customer not found"):
            self.customer_service.get_customer_profile(999)

    def test_methods_for_nonexistent_customer(self) -> None:
        """Test various methods with non-existent customer."""
        nonexistent_id = 999

        with pytest.raises(ValueError):
            self.customer_service.update_contact_information(
                nonexistent_id, "John", "Doe", "+1234567890"
            )

    def test_default_marketing_preferences_on_registration(self) -> None:
        """Test default marketing preferences are set on registration."""
        customer_id = self.customer_service.register_customer(
            "john.doe@example.com", "password123", "John", "Doe"
        )

        profile = self.customer_service.get_customer_profile(customer_id)
        marketing = profile["marketing"]

        assert marketing["email_marketing"] is True
        assert marketing["sms_marketing"] is False
        assert marketing["push_notifications"] is True
        assert marketing["preferred_channels"] == ["email"]
