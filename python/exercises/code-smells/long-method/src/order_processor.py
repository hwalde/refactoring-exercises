"""Order processing with a very long method that needs refactoring."""

import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal, TypedDict


class CustomerType(Enum):
    REGULAR = "regular"
    PREMIUM = "premium"


@dataclass
class OrderItem:
    product_id: str
    quantity: int
    price: float


@dataclass
class ShippingAddress:
    country: str
    city: str
    zip: str


class OrderData(TypedDict):
    customer_id: str
    items: list[dict[str, any]]
    shipping_address: dict[str, str]
    customer_type: str | None
    coupon_code: str | None


@dataclass
class ProcessedOrder:
    id: str
    customer_id: str
    items: list[OrderItem]
    subtotal: float
    discount: float
    tax: float
    total: float
    shipping_address: ShippingAddress
    status: Literal["confirmed"]
    created_at: str


@dataclass
class Notification:
    type: Literal["order_confirmation", "high_value_order"]
    customer_id: str | None
    order_id: str
    total: float | None
    message: str
    sent_at: str


class OrderProcessor:
    """Processes orders with validation, calculations, and notifications."""

    def __init__(self) -> None:
        self._orders: dict[str, ProcessedOrder] = {}
        self._notifications: list[Notification] = []

    def process_order(self, order_data: OrderData) -> ProcessedOrder:
        """Process an order - this method is too long and needs refactoring!"""

        # Validation block
        if not order_data.get("customer_id") or not order_data["customer_id"].strip():
            raise ValueError("Customer ID is required")

        if (
            not order_data.get("items")
            or not isinstance(order_data["items"], list)
            or len(order_data["items"]) == 0
        ):
            raise ValueError("Order must contain items")

        for item in order_data["items"]:
            if (
                not item.get("product_id")
                or not item["product_id"].strip()
                or not item.get("quantity")
                or item["quantity"] <= 0
            ):
                raise ValueError("Invalid item data")
            if not item.get("price") or item["price"] <= 0:
                raise ValueError("Invalid item price")

        if not order_data.get("shipping_address") or not order_data[
            "shipping_address"
        ].get("country"):
            raise ValueError("Shipping address is required")

        # Calculate subtotal
        subtotal = 0.0
        for item in order_data["items"]:
            subtotal += item["price"] * item["quantity"]

        # Apply discount logic
        discount = 0.0
        if subtotal > 100.0:
            discount = subtotal * 0.1  # 10% discount for orders over 100

        if order_data.get("customer_type") == "premium":
            discount += subtotal * 0.05  # Additional 5% for premium customers

        if order_data.get("coupon_code") == "SAVE20":
            discount += subtotal * 0.2  # 20% coupon discount

        # Ensure discount doesn't exceed 50% of subtotal
        if discount > subtotal * 0.5:
            discount = subtotal * 0.5

        # Calculate tax
        tax_rate = 0.19  # 19% VAT default
        country = order_data["shipping_address"]["country"]

        if country == "DE":
            tax_rate = 0.19
        elif country == "FR":
            tax_rate = 0.20
        elif country == "IT":
            tax_rate = 0.22
        elif country == "US":
            tax_rate = 0.08
        else:
            tax_rate = 0.19

        discounted_subtotal = subtotal - discount
        tax = discounted_subtotal * tax_rate
        total = discounted_subtotal + tax

        # Create order record
        order_id = f"order_{uuid.uuid4().hex[:12]}"

        items = [
            OrderItem(
                product_id=item["product_id"],
                quantity=item["quantity"],
                price=item["price"],
            )
            for item in order_data["items"]
        ]

        shipping_address = ShippingAddress(
            country=order_data["shipping_address"]["country"],
            city=order_data["shipping_address"]["city"],
            zip=order_data["shipping_address"]["zip"],
        )

        order = ProcessedOrder(
            id=order_id,
            customer_id=order_data["customer_id"],
            items=items,
            subtotal=round(subtotal, 2),
            discount=round(discount, 2),
            tax=round(tax, 2),
            total=round(total, 2),
            shipping_address=shipping_address,
            status="confirmed",
            created_at=datetime.now().isoformat(),
        )

        # Save order
        self._orders[order_id] = order

        # Send notifications
        customer_notification = Notification(
            type="order_confirmation",
            customer_id=order_data["customer_id"],
            order_id=order_id,
            total=None,
            message=f"Your order {order_id} has been confirmed. Total: €{order.total:.2f}",
            sent_at=datetime.now().isoformat(),
        )
        self._notifications.append(customer_notification)

        if total > 500.0:
            admin_notification = Notification(
                type="high_value_order",
                customer_id=None,
                order_id=order_id,
                total=order.total,
                message=f"High value order received: €{order.total:.2f}",
                sent_at=datetime.now().isoformat(),
            )
            self._notifications.append(admin_notification)

        return order

    def get_orders(self) -> list[ProcessedOrder]:
        """Get all processed orders."""
        return list(self._orders.values())

    def get_notifications(self) -> list[Notification]:
        """Get all notifications."""
        return self._notifications.copy()
