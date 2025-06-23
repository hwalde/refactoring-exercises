"""
Invoice generator with primitive obsession problems.
"""

import re
from datetime import datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def _round_money(amount: float) -> float:
    """Round money amount to 2 decimal places using commercial rounding."""
    return float(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


class InvoiceGenerator:
    """Generates and manages invoices for customers."""

    def __init__(self) -> None:
        """Initialize the invoice generator."""
        self.invoices: dict[str, dict[str, Any]] = {}
        self.next_invoice_number: int = 1

    def create_invoice(
        self,
        customer_id: str,
        customer_email: str,
        items: list[dict[str, Any]],
        currency: str = "EUR",
    ) -> dict[str, Any]:
        """
        Create a new invoice for a customer.

        Args:
            customer_id: The customer's ID
            customer_email: The customer's email address
            items: List of items with name, price, and quantity
            currency: The currency code (default: "EUR")

        Returns:
            Dictionary containing the created invoice

        Raises:
            ValueError: If validation fails
        """
        if not customer_id:
            raise ValueError("Customer ID cannot be empty")

        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", customer_email
        ):
            raise ValueError("Invalid email format")

        if not items:
            raise ValueError("Invoice must have at least one item")

        invoice_id = f"INV-{self.next_invoice_number:06d}"
        self.next_invoice_number += 1

        total_amount = 0.0
        processed_items = []

        for item in items:
            if not all(key in item for key in ["name", "price", "quantity"]):
                raise ValueError("Each item must have name, price, and quantity")

            if item["price"] < 0:
                raise ValueError("Item price cannot be negative")

            if item["quantity"] <= 0:
                raise ValueError("Item quantity must be positive")

            item_total = item["price"] * item["quantity"]
            total_amount += item_total

            processed_items.append(
                {
                    "name": item["name"],
                    "price": _round_money(item["price"]),
                    "quantity": item["quantity"],
                    "total": _round_money(item_total),
                }
            )

        now = datetime.now()
        due_date = now + timedelta(days=30)

        invoice = {
            "id": invoice_id,
            "customerId": customer_id,
            "customerEmail": customer_email,
            "items": processed_items,
            "totalAmount": _round_money(total_amount),
            "currency": currency,
            "status": "draft",
            "createdAt": now.strftime("%Y-%m-%d %H:%M:%S"),
            "dueDate": due_date.strftime("%Y-%m-%d"),
        }

        self.invoices[invoice_id] = invoice

        return invoice

    def update_invoice_status(self, invoice_id: str, new_status: str) -> None:
        """
        Update the status of an invoice.

        Args:
            invoice_id: The invoice ID
            new_status: The new status

        Raises:
            ValueError: If invoice not found or status transition invalid
        """
        if invoice_id not in self.invoices:
            raise ValueError("Invoice not found")

        allowed_statuses = ["draft", "sent", "paid", "overdue", "cancelled"]
        if new_status not in allowed_statuses:
            raise ValueError("Invalid status")

        current_status = self.invoices[invoice_id]["status"]

        valid_transitions = {
            "draft": ["sent", "cancelled"],
            "sent": ["paid", "overdue", "cancelled"],
            "paid": [],
            "overdue": ["paid", "cancelled"],
            "cancelled": [],
        }

        if new_status not in valid_transitions[current_status]:
            raise ValueError(f"Cannot transition from {current_status} to {new_status}")

        self.invoices[invoice_id]["status"] = new_status

    def get_invoice(self, invoice_id: str) -> dict[str, Any] | None:
        """
        Get an invoice by ID.

        Args:
            invoice_id: The invoice ID

        Returns:
            Invoice dictionary or None if not found
        """
        return self.invoices.get(invoice_id)

    def get_invoices_by_customer(self, customer_id: str) -> list[dict[str, Any]]:
        """
        Get all invoices for a specific customer.

        Args:
            customer_id: The customer ID

        Returns:
            List of invoices for the customer
        """
        customer_invoices = []
        for invoice in self.invoices.values():
            if invoice["customerId"] == customer_id:
                customer_invoices.append(invoice)
        return customer_invoices

    def calculate_total_revenue(self, currency: str = "EUR") -> float:
        """
        Calculate total revenue from paid invoices.

        Args:
            currency: The currency to calculate revenue for

        Returns:
            Total revenue amount
        """
        total = 0.0
        for invoice in self.invoices.values():
            if invoice["currency"] == currency and invoice["status"] == "paid":
                total += invoice["totalAmount"]
        return _round_money(total)

    def add_discount_to_invoice(
        self, invoice_id: str, discount_percentage: float
    ) -> None:
        """
        Add a discount to an invoice.

        Args:
            invoice_id: The invoice ID
            discount_percentage: Discount percentage (0-100)

        Raises:
            ValueError: If validation fails
        """
        if invoice_id not in self.invoices:
            raise ValueError("Invoice not found")

        if discount_percentage < 0 or discount_percentage > 100:
            raise ValueError("Discount percentage must be between 0 and 100")

        if self.invoices[invoice_id]["status"] != "draft":
            raise ValueError("Can only apply discount to draft invoices")

        discount_multiplier = 1 - (discount_percentage / 100)
        original_amount = self.invoices[invoice_id]["totalAmount"]
        discounted_amount = original_amount * discount_multiplier

        self.invoices[invoice_id]["totalAmount"] = _round_money(discounted_amount)
        self.invoices[invoice_id]["discountPercentage"] = discount_percentage

    def send_invoice_by_email(self, invoice_id: str, from_email: str) -> bool:
        """
        Send an invoice by email.

        Args:
            invoice_id: The invoice ID
            from_email: The sender's email address

        Returns:
            True if sent successfully

        Raises:
            ValueError: If validation fails
        """
        if invoice_id not in self.invoices:
            raise ValueError("Invoice not found")

        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", from_email
        ):
            raise ValueError("Invalid sender email format")

        invoice = self.invoices[invoice_id]
        if invoice["status"] != "draft":
            raise ValueError("Can only send draft invoices")

        self.invoices[invoice_id]["status"] = "sent"
        self.invoices[invoice_id]["sentAt"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.invoices[invoice_id]["sentFrom"] = from_email

        return True
