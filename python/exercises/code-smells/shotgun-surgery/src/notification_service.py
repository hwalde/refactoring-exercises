"""
NotificationService demonstrates the Shotgun Surgery code smell.

This class contains notification logic that's scattered across different domains.
When we need to add a new notification channel or change notification behavior,
we have to modify code in multiple places, making maintenance difficult.

The notification logic here should be centralized and organized better.
"""

import uuid
from datetime import datetime
from typing import Any


class NotificationService:
    """
    A service class that demonstrates the Shotgun Surgery code smell.

    This class contains notification logic scattered across different domains
    (order, payment, customer service, promotional) making it difficult to maintain
    and extend. Each type of notification has different patterns and inconsistent
    approaches to handling emails, SMS, and push notifications.
    """

    def __init__(self) -> None:
        """Initialize the NotificationService with default configurations."""
        self.sent_notifications: list[dict[str, Any]] = []

        # Configuration scattered across different domains
        self.email_config: dict[str, Any] = {
            "smtp_host": "mail.example.com",
            "smtp_port": 587,
            "username": "notifications@example.com",
        }
        self.sms_config: dict[str, Any] = {
            "provider": "TwilioSMS",
            "api_key": "fake_api_key",
        }
        self.push_config: dict[str, Any] = {"firebase_key": "fake_firebase_key"}

    # ORDER-RELATED NOTIFICATIONS (scattered in different methods)

    def send_order_confirmation(
        self, customer_id: str, order_data: dict[str, Any]
    ) -> None:
        """
        Send order confirmation notifications via multiple channels.

        This method demonstrates scattered logic by handling email, SMS, and push
        notifications in a single method with different patterns for each.

        Args:
            customer_id: The customer identifier
            order_data: Dictionary containing order details
        """
        # Email notification
        email_subject = f"Order Confirmation #{order_data['order_id']}"
        email_body = self._build_order_confirmation_email_body(order_data)
        self._send_email(customer_id, email_subject, email_body)

        # SMS notification if customer prefers SMS
        if self._customer_prefers_sms(customer_id):
            sms_message = f"Order #{order_data['order_id']} confirmed. Total: €{order_data['total']}"
            self._send_sms(customer_id, sms_message)

        # Push notification for mobile app users
        if self._customer_has_mobile_app(customer_id):
            push_message = "Your order has been confirmed!"
            self._send_push_notification(
                customer_id,
                push_message,
                {"type": "order_confirmation", "order_id": order_data["order_id"]},
            )

    def send_order_shipped(
        self, customer_id: str, shipping_data: dict[str, Any]
    ) -> None:
        """
        Send order shipped notifications with tracking information.

        Args:
            customer_id: The customer identifier
            shipping_data: Dictionary containing shipping details
        """
        # Email with tracking info
        email_subject = "Your Order Has Shipped!"
        email_body = f"""Your order #{shipping_data['order_id']} has been shipped.
Tracking Number: {shipping_data['tracking_number']}
Expected Delivery: {shipping_data['expected_delivery']}"""
        self._send_email(customer_id, email_subject, email_body)

        # SMS with short tracking info
        if self._customer_prefers_sms(customer_id):
            sms_message = f"Order shipped! Track: {shipping_data['tracking_number']}"
            self._send_sms(customer_id, sms_message)

        # Push notification
        if self._customer_has_mobile_app(customer_id):
            self._send_push_notification(
                customer_id,
                "Package on the way!",
                {
                    "type": "shipping_update",
                    "tracking_number": shipping_data["tracking_number"],
                },
            )

    # PAYMENT-RELATED NOTIFICATIONS (scattered logic)

    def send_payment_confirmation(
        self, customer_id: str, payment_data: dict[str, Any]
    ) -> None:
        """
        Send payment confirmation with different email format for payments.

        Args:
            customer_id: The customer identifier
            payment_data: Dictionary containing payment details
        """
        # Different email format for payments
        email_subject = f"Payment Received - Order #{payment_data['order_id']}"
        email_body = f"""Thank you for your payment!

Amount: €{payment_data['amount']}
Payment Method: {payment_data['method']}
Transaction ID: {payment_data['transaction_id']}"""

        # Add payment-specific email headers
        email_headers = {
            "X-Payment-Notification": "true",
            "X-Transaction-ID": payment_data["transaction_id"],
        }
        self._send_email_with_headers(
            customer_id, email_subject, email_body, email_headers
        )

        # SMS for high-value payments
        if payment_data["amount"] > 500.0:
            sms_message = f"Payment of €{payment_data['amount']} confirmed for order #{payment_data['order_id']}"
            self._send_sms(customer_id, sms_message)

    def send_payment_failed(
        self, customer_id: str, payment_data: dict[str, Any]
    ) -> None:
        """
        Send urgent notifications for failed payments.

        Args:
            customer_id: The customer identifier
            payment_data: Dictionary containing payment failure details
        """
        # Urgent email notification
        email_subject = f"URGENT: Payment Failed - Order #{payment_data['order_id']}"
        email_body = f"""Your payment could not be processed.

Reason: {payment_data['failure_reason']}
Please update your payment method to complete your order."""

        urgent_headers = {"X-Priority": "1", "X-MSMail-Priority": "High"}
        self._send_email_with_headers(
            customer_id, email_subject, email_body, urgent_headers
        )

        # Always send SMS for failed payments
        sms_message = f"Payment failed for order #{payment_data['order_id']}. Please check your payment method."
        self._send_sms(customer_id, sms_message)

        # Push notification with high priority
        if self._customer_has_mobile_app(customer_id):
            self._send_push_notification(
                customer_id,
                "Payment Issue - Action Required",
                {
                    "type": "payment_failed",
                    "order_id": payment_data["order_id"],
                    "priority": "high",
                },
            )

    # CUSTOMER SERVICE NOTIFICATIONS (different patterns again)

    def send_account_update(
        self, customer_id: str, update_type: str, data: dict[str, Any]
    ) -> None:
        """
        Send account update notifications using template-based approach.

        Args:
            customer_id: The customer identifier
            update_type: Type of account update
            data: Update-specific data

        Raises:
            ValueError: If update_type is not recognized
        """
        templates = {
            "profile_updated": {
                "email_subject": "Profile Updated Successfully",
                "email_body": "Your profile has been updated.",
                "sms_message": "Profile updated",
            },
            "password_changed": {
                "email_subject": "Password Changed",
                "email_body": "Your password has been changed successfully.",
                "sms_message": "Password changed",
            },
            "email_verified": {
                "email_subject": "Email Address Verified",
                "email_body": "Your email address has been verified.",
                "sms_message": None,  # No SMS for email verification
            },
        }

        if update_type not in templates:
            raise ValueError(f"Unknown update type: {update_type}")

        template = templates[update_type]

        # Send email
        self._send_email(customer_id, template["email_subject"], template["email_body"])

        # Send SMS if template has SMS message
        if template["sms_message"] and self._customer_prefers_sms(customer_id):
            self._send_sms(customer_id, template["sms_message"])

    def send_welcome_messages(
        self, customer_id: str, customer_data: dict[str, Any]
    ) -> None:
        """
        Send welcome message series to new customers.

        Args:
            customer_id: The customer identifier
            customer_data: Dictionary containing customer details
        """
        # Welcome email series
        welcome_email_subject = "Welcome to Our Store!"
        welcome_email_body = f"""Dear {customer_data['name']},

Welcome to our online store! We're excited to have you."""
        self._send_email(customer_id, welcome_email_subject, welcome_email_body)

        # SMS welcome if customer provided mobile
        if customer_data.get("mobile"):
            welcome_sms = f"Welcome {customer_data['name']}! Thanks for joining us."
            self._send_sms(customer_id, welcome_sms)

        # Setup push notifications
        if customer_data.get("mobile_app"):
            self._send_push_notification(
                customer_id,
                "Welcome! Get notified about deals and orders.",
                {"type": "welcome", "setup_notifications": True},
            )

    # PROMOTIONAL NOTIFICATIONS (yet another different approach)

    def send_promotional_offer(
        self, customer_id: str, offer_data: dict[str, Any]
    ) -> None:
        """
        Send promotional offers with different styling and tracking.

        Args:
            customer_id: The customer identifier
            offer_data: Dictionary containing offer details
        """
        # Promotional emails have different styling and tracking
        promo_subject = f"🎉 Special Offer: {offer_data['title']}"
        promo_body = self._build_promo_email_body(offer_data)

        promo_headers = {
            "X-Campaign-ID": offer_data["campaign_id"],
            "X-Offer-Code": offer_data["code"],
            "List-Unsubscribe": "<mailto:unsubscribe@example.com>",
        }
        self._send_email_with_headers(
            customer_id, promo_subject, promo_body, promo_headers
        )

        # SMS promos are shorter and different
        if self._customer_accepts_promo_sms(customer_id):
            promo_sms = f"🎁 {offer_data['title']} - Use code {offer_data['code']}. Reply STOP to opt out."
            self._send_sms(customer_id, promo_sms)

        # Push notifications for app users
        if self._customer_has_mobile_app(customer_id):
            self._send_push_notification(
                customer_id,
                offer_data["title"],
                {
                    "type": "promotion",
                    "offer_code": offer_data["code"],
                    "campaign_id": offer_data["campaign_id"],
                },
            )

    # LOW-LEVEL NOTIFICATION METHODS (implementation details mixed with business logic)

    def _send_email(self, customer_id: str, subject: str, body: str) -> None:
        """Send email notification (internal method)."""
        customer_email = self._get_customer_email(customer_id)

        # Simulate email sending
        notification = {
            "id": f"email_{uuid.uuid4().hex[:8]}",
            "type": "email",
            "customer_id": customer_id,
            "recipient": customer_email,
            "subject": subject,
            "body": body,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "sent",
        }

        self.sent_notifications.append(notification)

    def _send_email_with_headers(
        self, customer_id: str, subject: str, body: str, headers: dict[str, str]
    ) -> None:
        """Send email notification with custom headers (internal method)."""
        customer_email = self._get_customer_email(customer_id)

        notification = {
            "id": f"email_{uuid.uuid4().hex[:8]}",
            "type": "email",
            "customer_id": customer_id,
            "recipient": customer_email,
            "subject": subject,
            "body": body,
            "headers": headers,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "sent",
        }

        self.sent_notifications.append(notification)

    def _send_sms(self, customer_id: str, message: str) -> None:
        """Send SMS notification (internal method)."""
        customer_phone = self._get_customer_phone(customer_id)

        if not customer_phone:
            return  # Skip if no phone number

        notification = {
            "id": f"sms_{uuid.uuid4().hex[:8]}",
            "type": "sms",
            "customer_id": customer_id,
            "recipient": customer_phone,
            "message": message,
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "sent",
        }

        self.sent_notifications.append(notification)

    def _send_push_notification(
        self, customer_id: str, message: str, data: dict[str, Any] | None = None
    ) -> None:
        """Send push notification (internal method)."""
        device_token = self._get_customer_device_token(customer_id)

        if not device_token:
            return  # Skip if no device token

        notification = {
            "id": f"push_{uuid.uuid4().hex[:8]}",
            "type": "push",
            "customer_id": customer_id,
            "device_token": device_token,
            "message": message,
            "data": data or {},
            "sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "sent",
        }

        self.sent_notifications.append(notification)

    # HELPER METHODS (scattered customer preference logic)

    def _customer_prefers_sms(self, customer_id: str) -> bool:
        """Check if customer prefers SMS notifications."""
        # Simulate customer preference lookup
        return customer_id != "customer_no_sms"

    def _customer_has_mobile_app(self, customer_id: str) -> bool:
        """Check if customer has mobile app installed."""
        return customer_id != "customer_no_app"

    def _customer_accepts_promo_sms(self, customer_id: str) -> bool:
        """Check if customer accepts promotional SMS."""
        return customer_id != "customer_no_promo" and self._customer_prefers_sms(
            customer_id
        )

    def _get_customer_email(self, customer_id: str) -> str:
        """Get customer email address."""
        # Simulate customer email lookup
        return f"customer.{customer_id}@example.com"

    def _get_customer_phone(self, customer_id: str) -> str | None:
        """Get customer phone number."""
        if customer_id == "customer_no_phone":
            return None
        return "+49123456789"

    def _get_customer_device_token(self, customer_id: str) -> str | None:
        """Get customer device token for push notifications."""
        if customer_id == "customer_no_app":
            return None
        return f"device_token_for_{customer_id}"

    # EMAIL TEMPLATE BUILDERS (mixed with business logic)

    def _build_order_confirmation_email_body(self, order_data: dict[str, Any]) -> str:
        """Build email body for order confirmation."""
        body = """Dear Customer,

Thank you for your order!

Order Details:
"""
        body += f"Order ID: {order_data['order_id']}\n"
        body += f"Total: €{order_data['total']}\n"
        body += "Items:\n"

        for item in order_data["items"]:
            body += f"- {item['name']} (Qty: {item['quantity']}) - €{item['price']}\n"

        body += "\nYour order will be processed within 1-2 business days.\n"
        body += "\nBest regards,\nYour Online Store"

        return body

    def _build_promo_email_body(self, offer_data: dict[str, Any]) -> str:
        """Build email body for promotional offers."""
        body = f"""🎉 Special Offer Just for You! 🎉

{offer_data['title']}

{offer_data['description']}

Use code: {offer_data['code']}
Valid until: {offer_data['valid_until']}

Shop now and save!

To unsubscribe from promotional emails, click here."""

        return body

    # PUBLIC API METHODS

    def get_sent_notifications(self) -> list[dict[str, Any]]:
        """Get all sent notifications."""
        return self.sent_notifications

    def get_notifications_by_type(self, notification_type: str) -> list[dict[str, Any]]:
        """Get notifications filtered by type."""
        return [n for n in self.sent_notifications if n["type"] == notification_type]

    def get_notifications_by_customer(self, customer_id: str) -> list[dict[str, Any]]:
        """Get notifications filtered by customer."""
        return [n for n in self.sent_notifications if n["customer_id"] == customer_id]

    def clear_notifications(self) -> None:
        """Clear all sent notifications."""
        self.sent_notifications = []
