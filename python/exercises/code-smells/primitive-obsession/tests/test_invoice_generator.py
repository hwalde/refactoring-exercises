"""
Tests for InvoiceGenerator class.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from invoice_generator import InvoiceGenerator


class TestInvoiceGenerator:
    """Test suite for InvoiceGenerator class."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.invoice_generator = InvoiceGenerator()

    def test_create_invoice_with_valid_data(self) -> None:
        """Test creating an invoice with valid data."""
        items = [
            {"name": "Product A", "price": 100.0, "quantity": 2},
            {"name": "Product B", "price": 50.5, "quantity": 1},
        ]

        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        assert invoice["id"] == "INV-000001"
        assert invoice["customerId"] == "CUST-001"
        assert invoice["customerEmail"] == "customer@example.com"
        assert invoice["totalAmount"] == 250.5
        assert invoice["currency"] == "EUR"
        assert invoice["status"] == "draft"
        assert len(invoice["items"]) == 2

    def test_create_invoice_with_different_currency(self) -> None:
        """Test creating an invoice with a different currency."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        invoice = self.invoice_generator.create_invoice(
            "CUST-002", "customer@example.com", items, "USD"
        )

        assert invoice["currency"] == "USD"

    def test_create_invoice_throws_exception_for_empty_customer_id(self) -> None:
        """Test that empty customer ID raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        with pytest.raises(ValueError, match="Customer ID cannot be empty"):
            self.invoice_generator.create_invoice("", "customer@example.com", items)

    def test_create_invoice_throws_exception_for_invalid_email(self) -> None:
        """Test that invalid email raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        with pytest.raises(ValueError, match="Invalid email format"):
            self.invoice_generator.create_invoice("CUST-001", "invalid-email", items)

    def test_create_invoice_throws_exception_for_empty_items(self) -> None:
        """Test that empty items list raises exception."""
        with pytest.raises(ValueError, match="Invoice must have at least one item"):
            self.invoice_generator.create_invoice(
                "CUST-001", "customer@example.com", []
            )

    def test_create_invoice_throws_exception_for_negative_price(self) -> None:
        """Test that negative price raises exception."""
        items = [{"name": "Product A", "price": -10.0, "quantity": 1}]

        with pytest.raises(ValueError, match="Item price cannot be negative"):
            self.invoice_generator.create_invoice(
                "CUST-001", "customer@example.com", items
            )

    def test_create_invoice_throws_exception_for_zero_quantity(self) -> None:
        """Test that zero quantity raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 0}]

        with pytest.raises(ValueError, match="Item quantity must be positive"):
            self.invoice_generator.create_invoice(
                "CUST-001", "customer@example.com", items
            )

    def test_invoice_number_increments_correctly(self) -> None:
        """Test that invoice numbers increment correctly."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        invoice1 = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )
        invoice2 = self.invoice_generator.create_invoice(
            "CUST-002", "customer2@example.com", items
        )

        assert invoice1["id"] == "INV-000001"
        assert invoice2["id"] == "INV-000002"

    def test_update_invoice_status_with_valid_transition(self) -> None:
        """Test updating invoice status with valid transition."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        self.invoice_generator.update_invoice_status(invoice["id"], "sent")
        updated_invoice = self.invoice_generator.get_invoice(invoice["id"])

        assert updated_invoice["status"] == "sent"

    def test_update_invoice_status_throws_exception_for_invalid_status(self) -> None:
        """Test that invalid status raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        with pytest.raises(ValueError, match="Invalid status"):
            self.invoice_generator.update_invoice_status(
                invoice["id"], "invalid-status"
            )

    def test_update_invoice_status_throws_exception_for_invalid_transition(
        self,
    ) -> None:
        """Test that invalid status transition raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        self.invoice_generator.update_invoice_status(invoice["id"], "sent")
        self.invoice_generator.update_invoice_status(invoice["id"], "paid")

        with pytest.raises(ValueError, match="Cannot transition from paid to draft"):
            self.invoice_generator.update_invoice_status(invoice["id"], "draft")

    def test_update_invoice_status_throws_exception_for_non_existent_invoice(
        self,
    ) -> None:
        """Test that updating non-existent invoice raises exception."""
        with pytest.raises(ValueError, match="Invoice not found"):
            self.invoice_generator.update_invoice_status("NON-EXISTENT", "sent")

    def test_get_invoice_returns_correct_invoice(self) -> None:
        """Test getting an invoice returns the correct one."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        retrieved_invoice = self.invoice_generator.get_invoice(invoice["id"])

        assert retrieved_invoice == invoice

    def test_get_invoice_returns_none_for_non_existent_invoice(self) -> None:
        """Test getting non-existent invoice returns None."""
        result = self.invoice_generator.get_invoice("NON-EXISTENT")

        assert result is None

    def test_get_invoices_by_customer(self) -> None:
        """Test getting invoices by customer."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        invoice1 = self.invoice_generator.create_invoice(
            "CUST-001", "customer1@example.com", items
        )
        invoice2 = self.invoice_generator.create_invoice(
            "CUST-002", "customer2@example.com", items
        )
        invoice3 = self.invoice_generator.create_invoice(
            "CUST-001", "customer1@example.com", items
        )

        customer_invoices = self.invoice_generator.get_invoices_by_customer("CUST-001")

        assert len(customer_invoices) == 2
        assert invoice1 in customer_invoices
        assert invoice3 in customer_invoices
        assert invoice2 not in customer_invoices

    def test_calculate_total_revenue_for_paid_invoices(self) -> None:
        """Test calculating total revenue for paid invoices."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        invoice1 = self.invoice_generator.create_invoice(
            "CUST-001", "customer1@example.com", items
        )
        self.invoice_generator.create_invoice(
            "CUST-002", "customer2@example.com", items
        )

        self.invoice_generator.update_invoice_status(invoice1["id"], "sent")
        self.invoice_generator.update_invoice_status(invoice1["id"], "paid")

        total_revenue = self.invoice_generator.calculate_total_revenue()

        assert total_revenue == 100.0

    def test_calculate_total_revenue_for_specific_currency(self) -> None:
        """Test calculating total revenue for specific currency."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]

        invoice1 = self.invoice_generator.create_invoice(
            "CUST-001", "customer1@example.com", items, "EUR"
        )
        invoice2 = self.invoice_generator.create_invoice(
            "CUST-002", "customer2@example.com", items, "USD"
        )

        self.invoice_generator.update_invoice_status(invoice1["id"], "sent")
        self.invoice_generator.update_invoice_status(invoice1["id"], "paid")
        self.invoice_generator.update_invoice_status(invoice2["id"], "sent")
        self.invoice_generator.update_invoice_status(invoice2["id"], "paid")

        eur_revenue = self.invoice_generator.calculate_total_revenue("EUR")
        usd_revenue = self.invoice_generator.calculate_total_revenue("USD")

        assert eur_revenue == 100.0
        assert usd_revenue == 100.0

    def test_add_discount_to_invoice(self) -> None:
        """Test adding a discount to an invoice."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        self.invoice_generator.add_discount_to_invoice(invoice["id"], 10.0)
        updated_invoice = self.invoice_generator.get_invoice(invoice["id"])

        assert updated_invoice["totalAmount"] == 90.0
        assert updated_invoice["discountPercentage"] == 10.0

    def test_add_discount_throws_exception_for_invalid_percentage(self) -> None:
        """Test that invalid discount percentage raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        with pytest.raises(
            ValueError, match="Discount percentage must be between 0 and 100"
        ):
            self.invoice_generator.add_discount_to_invoice(invoice["id"], -5.0)

    def test_add_discount_throws_exception_for_non_draft_invoice(self) -> None:
        """Test that adding discount to non-draft invoice raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        self.invoice_generator.update_invoice_status(invoice["id"], "sent")

        with pytest.raises(
            ValueError, match="Can only apply discount to draft invoices"
        ):
            self.invoice_generator.add_discount_to_invoice(invoice["id"], 10.0)

    def test_send_invoice_by_email(self) -> None:
        """Test sending an invoice by email."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        result = self.invoice_generator.send_invoice_by_email(
            invoice["id"], "sender@company.com"
        )
        updated_invoice = self.invoice_generator.get_invoice(invoice["id"])

        assert result is True
        assert updated_invoice["status"] == "sent"
        assert updated_invoice["sentFrom"] == "sender@company.com"
        assert "sentAt" in updated_invoice

    def test_send_invoice_throws_exception_for_invalid_email(self) -> None:
        """Test that invalid sender email raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        with pytest.raises(ValueError, match="Invalid sender email format"):
            self.invoice_generator.send_invoice_by_email(invoice["id"], "invalid-email")

    def test_send_invoice_throws_exception_for_non_draft_invoice(self) -> None:
        """Test that sending non-draft invoice raises exception."""
        items = [{"name": "Product A", "price": 100.0, "quantity": 1}]
        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        self.invoice_generator.update_invoice_status(invoice["id"], "sent")

        with pytest.raises(ValueError, match="Can only send draft invoices"):
            self.invoice_generator.send_invoice_by_email(
                invoice["id"], "sender@company.com"
            )

    def test_rounding_handled_correctly(self) -> None:
        """Test that rounding is handled correctly."""
        items = [
            {"name": "Product A", "price": 10.555, "quantity": 3},
            {"name": "Product B", "price": 20.999, "quantity": 2},
        ]

        invoice = self.invoice_generator.create_invoice(
            "CUST-001", "customer@example.com", items
        )

        assert invoice["totalAmount"] == 73.66
        assert invoice["items"][0]["price"] == 10.56
        assert invoice["items"][0]["total"] == 31.67
        assert invoice["items"][1]["price"] == 21.0
        assert invoice["items"][1]["total"] == 42.0
