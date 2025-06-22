"""Tests for OrderProcessor - these tests must remain green after refactoring!"""

import pytest
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from order_processor import OrderProcessor


class TestOrderProcessor:
    """Test cases for OrderProcessor."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.processor = OrderProcessor()

    def test_process_simple_order(self) -> None:
        """Test processing a simple order without discounts."""
        order_data = {
            "customer_id": "cust_123",
            "items": [
                {
                    "product_id": "prod_1",
                    "quantity": 2,
                    "price": 25.0,
                },
                {
                    "product_id": "prod_2",
                    "quantity": 1,
                    "price": 50.0,
                },
            ],
            "shipping_address": {
                "country": "DE",
                "city": "Berlin",
                "zip": "10115",
            },
        }

        result = self.processor.process_order(order_data)

        assert result is not None
        assert result.id is not None
        assert result.customer_id == "cust_123"
        assert result.subtotal == 100.0
        assert result.discount == 0.0  # No discount for 100.0
        assert result.tax == 19.0  # 19% of 100.0
        assert result.total == 119.0
        assert result.status == "confirmed"

    def test_process_order_with_discount(self) -> None:
        """Test processing order with volume discount."""
        order_data = {
            "customer_id": "cust_456",
            "items": [
                {
                    "product_id": "prod_3",
                    "quantity": 1,
                    "price": 150.0,
                },
            ],
            "shipping_address": {
                "country": "DE",
                "city": "Munich",
                "zip": "80331",
            },
        }

        result = self.processor.process_order(order_data)

        assert result.subtotal == 150.0
        assert result.discount == 15.0  # 10% discount for orders > 100
        assert result.tax == 25.65  # 19% of (150 - 15)
        assert result.total == 160.65

    def test_process_premium_customer_order(self) -> None:
        """Test processing order for premium customer."""
        order_data = {
            "customer_id": "cust_premium",
            "customer_type": "premium",
            "items": [
                {
                    "product_id": "prod_4",
                    "quantity": 1,
                    "price": 200.0,
                },
            ],
            "shipping_address": {
                "country": "FR",
                "city": "Paris",
                "zip": "75001",
            },
        }

        result = self.processor.process_order(order_data)

        assert result.subtotal == 200.0
        assert result.discount == 30.0  # 10% + 5% premium discount
        assert result.tax == 34.0  # 20% FR tax of (200 - 30)
        assert result.total == 204.0

    def test_process_order_with_coupon(self) -> None:
        """Test processing order with coupon code."""
        order_data = {
            "customer_id": "cust_789",
            "coupon_code": "SAVE20",
            "items": [
                {
                    "product_id": "prod_5",
                    "quantity": 1,
                    "price": 100.0,
                },
            ],
            "shipping_address": {
                "country": "US",
                "city": "New York",
                "zip": "10001",
            },
        }

        result = self.processor.process_order(order_data)

        assert result.subtotal == 100.0
        assert result.discount == 20.0  # 20% coupon discount
        assert result.tax == 6.4  # 8% US tax of (100 - 20)
        assert result.total == 86.4

    def test_order_storage_and_notifications(self) -> None:
        """Test that orders are stored and notifications are sent."""
        order_data = {
            "customer_id": "cust_notify",
            "items": [
                {
                    "product_id": "prod_6",
                    "quantity": 1,
                    "price": 50.0,
                },
            ],
            "shipping_address": {
                "country": "DE",
                "city": "Hamburg",
                "zip": "20095",
            },
        }

        result = self.processor.process_order(order_data)

        # Check order is stored
        orders = self.processor.get_orders()
        assert len(orders) == 1
        assert orders[0] == result

        # Check customer notification
        notifications = self.processor.get_notifications()
        assert len(notifications) == 1
        assert notifications[0].type == "order_confirmation"
        assert notifications[0].customer_id == "cust_notify"
        assert notifications[0].order_id == result.id

    def test_high_value_order_notification(self) -> None:
        """Test that high value orders trigger admin notifications."""
        order_data = {
            "customer_id": "cust_big_spender",
            "items": [
                {
                    "product_id": "prod_expensive",
                    "quantity": 1,
                    "price": 600.0,
                },
            ],
            "shipping_address": {
                "country": "DE",
                "city": "Frankfurt",
                "zip": "60311",
            },
        }

        self.processor.process_order(order_data)

        notifications = self.processor.get_notifications()
        assert len(notifications) == 2  # Customer + Admin notification

        admin_notifications = [n for n in notifications if n.type == "high_value_order"]
        assert len(admin_notifications) == 1
        assert admin_notifications[0].total and admin_notifications[0].total > 500

    def test_validation_missing_customer_id(self) -> None:
        """Test validation for missing customer ID."""
        with pytest.raises(ValueError, match="Customer ID is required"):
            self.processor.process_order(
                {
                    "customer_id": "",
                    "items": [],
                    "shipping_address": {
                        "country": "DE",
                        "city": "Berlin",
                        "zip": "10115",
                    },
                }
            )

    def test_validation_empty_items(self) -> None:
        """Test validation for empty items list."""
        with pytest.raises(ValueError, match="Order must contain items"):
            self.processor.process_order(
                {
                    "customer_id": "cust_123",
                    "items": [],
                    "shipping_address": {
                        "country": "DE",
                        "city": "Berlin",
                        "zip": "10115",
                    },
                }
            )

    def test_maximum_discount_cap(self) -> None:
        """Test that discount is capped at 50% of subtotal."""
        order_data = {
            "customer_id": "cust_max_discount",
            "customer_type": "premium",
            "coupon_code": "SAVE20",
            "items": [
                {
                    "product_id": "prod_7",
                    "quantity": 1,
                    "price": 200.0,
                },
            ],
            "shipping_address": {
                "country": "DE",
                "city": "Berlin",
                "zip": "10115",
            },
        }

        result = self.processor.process_order(order_data)

        assert result.subtotal == 200.0
        assert result.discount == 70.0  # 35% of 200 (10% + 5% + 20%)
        assert result.discount <= 100.0  # Max 50% of subtotal
