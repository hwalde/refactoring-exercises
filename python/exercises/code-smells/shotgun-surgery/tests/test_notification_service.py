"""Tests for NotificationService class."""

import sys
from pathlib import Path

import pytest

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notification_service import NotificationService


class TestNotificationService:
    """Test suite for NotificationService class."""

    def setup_method(self):
        """Setup method called before each test."""
        self.notification_service = NotificationService()

    def teardown_method(self):
        """Teardown method called after each test."""
        self.notification_service.clear_notifications()

    def test_send_order_confirmation(self):
        """Test order confirmation notifications are sent correctly."""
        customer_id = "customer_123"
        order_data = {
            "order_id": "ORDER_001",
            "total": "99.99",
            "items": [{"name": "Test Product", "quantity": 2, "price": "49.99"}],
        }

        self.notification_service.send_order_confirmation(customer_id, order_data)

        notifications = self.notification_service.get_sent_notifications()
        assert len(notifications) > 0

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "Order Confirmation #ORDER_001"
        assert "ORDER_001" in email_notifications[0]["body"]
        assert "€99.99" in email_notifications[0]["body"]

        # Should send SMS for customers who prefer SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "ORDER_001" in sms_notifications[0]["message"]
        assert "€99.99" in sms_notifications[0]["message"]

        # Should send push notification for app users
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
        assert push_notifications[0]["message"] == "Your order has been confirmed!"
        assert push_notifications[0]["data"]["type"] == "order_confirmation"
        assert push_notifications[0]["data"]["order_id"] == "ORDER_001"

    def test_send_order_confirmation_no_sms_for_customer_no_sms(self):
        """Test that customers who don't want SMS don't receive SMS."""
        customer_id = "customer_no_sms"
        order_data = {"order_id": "ORDER_002", "total": "149.99", "items": []}

        self.notification_service.send_order_confirmation(customer_id, order_data)

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1

        # Should NOT send SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 0

        # Should send push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1

    def test_send_order_shipped(self):
        """Test order shipped notifications with tracking information."""
        customer_id = "customer_456"
        shipping_data = {
            "order_id": "ORDER_003",
            "tracking_number": "TRACK123456",
            "expected_delivery": "2024-01-15",
        }

        self.notification_service.send_order_shipped(customer_id, shipping_data)

        notifications = self.notification_service.get_sent_notifications()
        assert len(notifications) > 0

        # Should send email with tracking info
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "Your Order Has Shipped!"
        assert "ORDER_003" in email_notifications[0]["body"]
        assert "TRACK123456" in email_notifications[0]["body"]
        assert "2024-01-15" in email_notifications[0]["body"]

        # Should send SMS with tracking
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "TRACK123456" in sms_notifications[0]["message"]

        # Should send push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
        assert push_notifications[0]["message"] == "Package on the way!"
        assert push_notifications[0]["data"]["type"] == "shipping_update"
        assert push_notifications[0]["data"]["tracking_number"] == "TRACK123456"

    def test_send_payment_confirmation(self):
        """Test payment confirmation notifications."""
        customer_id = "customer_789"
        payment_data = {
            "order_id": "ORDER_004",
            "amount": 299.99,
            "method": "Credit Card",
            "transaction_id": "TXN_12345",
        }

        self.notification_service.send_payment_confirmation(customer_id, payment_data)

        # Should send email with special headers
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert (
            email_notifications[0]["subject"] == "Payment Received - Order #ORDER_004"
        )
        assert "€299.99" in email_notifications[0]["body"]
        assert "Credit Card" in email_notifications[0]["body"]
        assert "TXN_12345" in email_notifications[0]["body"]
        assert "headers" in email_notifications[0]
        assert email_notifications[0]["headers"]["X-Payment-Notification"] == "true"
        assert email_notifications[0]["headers"]["X-Transaction-ID"] == "TXN_12345"

        # Should NOT send SMS for low-value payments
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 0

    def test_send_payment_confirmation_high_value(self):
        """Test payment confirmation for high-value payments includes SMS."""
        customer_id = "customer_999"
        payment_data = {
            "order_id": "ORDER_005",
            "amount": 750.00,
            "method": "PayPal",
            "transaction_id": "TXN_67890",
        }

        self.notification_service.send_payment_confirmation(customer_id, payment_data)

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1

        # Should send SMS for high-value payments
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "€750" in sms_notifications[0]["message"]
        assert "ORDER_005" in sms_notifications[0]["message"]

    def test_send_payment_failed(self):
        """Test urgent notifications for failed payments."""
        customer_id = "customer_abc"
        payment_data = {"order_id": "ORDER_006", "failure_reason": "Insufficient funds"}

        self.notification_service.send_payment_failed(customer_id, payment_data)

        # Should send urgent email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert (
            email_notifications[0]["subject"]
            == "URGENT: Payment Failed - Order #ORDER_006"
        )
        assert "Insufficient funds" in email_notifications[0]["body"]
        assert "headers" in email_notifications[0]
        assert email_notifications[0]["headers"]["X-Priority"] == "1"
        assert email_notifications[0]["headers"]["X-MSMail-Priority"] == "High"

        # Should always send SMS for failed payments
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "ORDER_006" in sms_notifications[0]["message"]

        # Should send high priority push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
        assert push_notifications[0]["message"] == "Payment Issue - Action Required"
        assert push_notifications[0]["data"]["type"] == "payment_failed"
        assert push_notifications[0]["data"]["priority"] == "high"

    def test_send_account_update_profile_updated(self):
        """Test account update notifications for profile updates."""
        customer_id = "customer_def"
        data = {"field": "name", "old_value": "John", "new_value": "John Doe"}

        self.notification_service.send_account_update(
            customer_id, "profile_updated", data
        )

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "Profile Updated Successfully"

        # Should send SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert sms_notifications[0]["message"] == "Profile updated"

    def test_send_account_update_email_verified(self):
        """Test account update notifications for email verification."""
        customer_id = "customer_ghi"
        data = {"email": "customer@example.com"}

        self.notification_service.send_account_update(
            customer_id, "email_verified", data
        )

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "Email Address Verified"

        # Should NOT send SMS for email verification
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 0

    def test_send_account_update_invalid_type(self):
        """Test that invalid update types raise appropriate exceptions."""
        customer_id = "customer_jkl"
        data = {}

        with pytest.raises(ValueError) as exc_info:
            self.notification_service.send_account_update(
                customer_id, "invalid_type", data
            )

        assert "Unknown update type: invalid_type" in str(exc_info.value)

    def test_send_welcome_messages(self):
        """Test welcome message series for new customers."""
        customer_id = "customer_mno"
        customer_data = {
            "name": "Jane Smith",
            "mobile": "+49123456789",
            "mobile_app": True,
        }

        self.notification_service.send_welcome_messages(customer_id, customer_data)

        # Should send welcome email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "Welcome to Our Store!"
        assert "Jane Smith" in email_notifications[0]["body"]

        # Should send welcome SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "Jane Smith" in sms_notifications[0]["message"]

        # Should send push notification for app setup
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
        assert push_notifications[0]["data"]["type"] == "welcome"
        assert push_notifications[0]["data"]["setup_notifications"] is True

    def test_send_promotional_offer(self):
        """Test promotional offer notifications."""
        customer_id = "customer_pqr"
        offer_data = {
            "title": "50% Off Sale",
            "description": "Get 50% off all items this weekend only!",
            "code": "SAVE50",
            "valid_until": "2024-01-31",
            "campaign_id": "CAMP_001",
        }

        self.notification_service.send_promotional_offer(customer_id, offer_data)

        # Should send promotional email with special headers
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1
        assert email_notifications[0]["subject"] == "🎉 Special Offer: 50% Off Sale"
        assert "SAVE50" in email_notifications[0]["body"]
        assert "2024-01-31" in email_notifications[0]["body"]
        assert "headers" in email_notifications[0]
        assert email_notifications[0]["headers"]["X-Campaign-ID"] == "CAMP_001"
        assert email_notifications[0]["headers"]["X-Offer-Code"] == "SAVE50"

        # Should send promotional SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1
        assert "SAVE50" in sms_notifications[0]["message"]

        # Should send promotional push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
        assert push_notifications[0]["message"] == "50% Off Sale"
        assert push_notifications[0]["data"]["type"] == "promotion"
        assert push_notifications[0]["data"]["offer_code"] == "SAVE50"

    def test_get_notifications_by_customer(self):
        """Test filtering notifications by customer."""
        customer_id1 = "customer_111"
        customer_id2 = "customer_222"

        # Send notifications for first customer
        self.notification_service.send_order_confirmation(
            customer_id1, {"order_id": "ORDER_111", "total": "50.00", "items": []}
        )

        # Send notifications for second customer
        self.notification_service.send_order_confirmation(
            customer_id2, {"order_id": "ORDER_222", "total": "75.00", "items": []}
        )

        customer1_notifications = (
            self.notification_service.get_notifications_by_customer(customer_id1)
        )
        customer2_notifications = (
            self.notification_service.get_notifications_by_customer(customer_id2)
        )

        # Each customer should have 3 notifications (email, sms, push)
        assert len(customer1_notifications) == 3
        assert len(customer2_notifications) == 3

        # Check that notifications are correctly filtered
        for notification in customer1_notifications:
            assert notification["customer_id"] == customer_id1

        for notification in customer2_notifications:
            assert notification["customer_id"] == customer_id2

    def test_get_notifications_by_type(self):
        """Test filtering notifications by type."""
        customer_id = "customer_333"

        # Send multiple different types of notifications
        self.notification_service.send_order_confirmation(
            customer_id, {"order_id": "ORDER_333", "total": "100.00", "items": []}
        )

        self.notification_service.send_payment_confirmation(
            customer_id,
            {
                "order_id": "ORDER_333",
                "amount": 100.00,
                "method": "Credit Card",
                "transaction_id": "TXN_333",
            },
        )

        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        push_notifications = self.notification_service.get_notifications_by_type("push")

        # Should have 2 emails (order confirmation + payment confirmation)
        assert len(email_notifications) == 2
        # Should have 1 SMS (order confirmation only, payment was under 500)
        assert len(sms_notifications) == 1
        # Should have 1 push (order confirmation only)
        assert len(push_notifications) == 1

        # Verify types are correct
        for notification in email_notifications:
            assert notification["type"] == "email"
        for notification in sms_notifications:
            assert notification["type"] == "sms"
        for notification in push_notifications:
            assert notification["type"] == "push"

    def test_clear_notifications(self):
        """Test clearing all notifications."""
        customer_id = "customer_444"

        # Send some notifications
        self.notification_service.send_order_confirmation(
            customer_id, {"order_id": "ORDER_444", "total": "25.00", "items": []}
        )

        assert len(self.notification_service.get_sent_notifications()) > 0

        # Clear notifications
        self.notification_service.clear_notifications()

        assert len(self.notification_service.get_sent_notifications()) == 0

    def test_no_sms_for_customer_without_phone(self):
        """Test that customers without phone numbers don't receive SMS."""
        customer_id = "customer_no_phone"

        self.notification_service.send_order_confirmation(
            customer_id, {"order_id": "ORDER_NO_PHONE", "total": "100.00", "items": []}
        )

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1

        # Should NOT send SMS (no phone number)
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 0

        # Should send push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1

    def test_no_push_for_customer_without_app(self):
        """Test that customers without mobile app don't receive push notifications."""
        customer_id = "customer_no_app"

        self.notification_service.send_order_confirmation(
            customer_id, {"order_id": "ORDER_NO_APP", "total": "100.00", "items": []}
        )

        # Should send email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1

        # Should send SMS
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 1

        # Should NOT send push notification (no app)
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 0

    def test_no_promo_sms_for_opted_out_customer(self):
        """Test that customers who opted out of promotions don't receive promo SMS."""
        customer_id = "customer_no_promo"
        offer_data = {
            "title": "Test Offer",
            "description": "Test description",
            "code": "TEST123",
            "valid_until": "2024-12-31",
            "campaign_id": "TEST_CAMP",
        }

        self.notification_service.send_promotional_offer(customer_id, offer_data)

        # Should send promotional email
        email_notifications = self.notification_service.get_notifications_by_type(
            "email"
        )
        assert len(email_notifications) == 1

        # Should NOT send promotional SMS (opted out)
        sms_notifications = self.notification_service.get_notifications_by_type("sms")
        assert len(sms_notifications) == 0

        # Should send push notification
        push_notifications = self.notification_service.get_notifications_by_type("push")
        assert len(push_notifications) == 1
