"""
OrderCalculator demonstrates Feature Envy code smell

This module shows "Feature Envy" by having methods that use data and methods
from other objects (Order, Customer, Product) more than their own data.
The business logic should be moved closer to the data it operates on.
"""

from typing import Dict, Any
from customer import Customer
from product import Product
from order import Order


class OrderCalculator:
    """
    OrderCalculator demonstrates Feature Envy code smell

    This class shows "Feature Envy" by having methods that use data and methods
    from other objects (Order, Customer, Product) more than their own data.
    The business logic should be moved closer to the data it operates on.
    """

    def __init__(self):
        # This class has minimal state of its own
        self.tax_rates = {"standard": 0.20, "premium": 0.15, "vip": 0.10}

        self.shipping_rates = {"standard": 5.99, "express": 12.99}

    def calculate_customer_discount(self, order: Order) -> float:
        """
        Feature Envy: This method uses mostly Customer data
        Should be moved to Customer class

        Args:
            order: The order containing customer information

        Returns:
            The discount rate as a float (0.0-1.0)
        """
        customer = order.get_customer()
        customer_type = customer.get_type()
        loyalty_years = customer.get_loyalty_years()

        # Complex customer-specific discount logic
        if customer_type == "vip":
            return 0.15 + min(loyalty_years * 0.01, 0.10)  # Up to 25% for VIP

        if customer_type == "premium":
            return 0.10 + min(loyalty_years * 0.005, 0.05)  # Up to 15% for Premium

        if customer_type == "standard":
            if loyalty_years >= 5:
                return 0.05  # 5% for loyal standard customers
            if loyalty_years >= 2:
                return 0.02  # 2% for somewhat loyal customers

        return 0.0  # No discount for new standard customers

    def calculate_product_shipping_cost(self, product: Product, quantity: int) -> float:
        """
        Feature Envy: This method uses mostly Product data
        Should be moved to Product class

        Args:
            product: The product to calculate shipping for
            quantity: The quantity of products

        Returns:
            The shipping cost for the product
        """
        weight = product.get_weight()
        is_fragile = product.is_fragile()
        category = product.get_category()

        base_cost = weight * quantity * 0.5

        # Category-specific shipping costs
        if category == "electronics":
            base_cost *= 1.2  # Electronics have higher shipping costs
        elif category == "books":
            base_cost *= 0.8  # Books have lower shipping costs
        elif category == "furniture":
            base_cost *= 2.0  # Furniture is expensive to ship

        # Fragile items cost more to ship
        if is_fragile:
            base_cost *= 1.5

        return round(base_cost, 2)

    def calculate_order_subtotal(self, order: Order) -> float:
        """
        Feature Envy: This method uses mostly Order data
        Should be moved to Order class

        Args:
            order: The order to calculate subtotal for

        Returns:
            The subtotal of the order
        """
        subtotal = 0.0
        items = order.get_items()

        for item in items:
            product = item.product
            quantity = item.quantity
            product_price = product.get_price()

            subtotal += product_price * quantity

        return round(subtotal, 2)

    def calculate_order_weight(self, order: Order) -> float:
        """
        Feature Envy: This method uses mostly Order and Product data
        Could be moved to Order class

        Args:
            order: The order to calculate weight for

        Returns:
            The total weight of the order
        """
        total_weight = 0.0
        items = order.get_items()

        for item in items:
            product = item.product
            quantity = item.quantity
            product_weight = product.get_weight()

            total_weight += product_weight * quantity

        return round(total_weight, 2)

    def calculate_tax_rate(self, order: Order) -> float:
        """
        Feature Envy: This method mostly uses data from Customer (via Order)
        Should be moved to Customer class

        Args:
            order: The order containing customer information

        Returns:
            The tax rate for the customer
        """
        customer_type = order.get_customer().get_type()

        return self.tax_rates.get(customer_type, self.tax_rates["standard"])

    def calculate_shipping_cost(self, order: Order) -> float:
        """
        Feature Envy: Uses Order data and shipping logic
        Could be moved to Order class

        Args:
            order: The order to calculate shipping for

        Returns:
            The total shipping cost for the order
        """
        total_shipping_cost = 0.0
        is_express = order.is_express()
        items = order.get_items()

        # Base shipping cost
        base_rate = (
            self.shipping_rates["express"]
            if is_express
            else self.shipping_rates["standard"]
        )
        total_shipping_cost += base_rate

        # Add per-product shipping costs
        for item in items:
            product = item.product
            quantity = item.quantity

            product_shipping_cost = self.calculate_product_shipping_cost(
                product, quantity
            )
            total_shipping_cost += product_shipping_cost

        return round(total_shipping_cost, 2)

    def calculate_total(self, order: Order) -> Dict[str, Any]:
        """
        Main calculation method - coordinates other calculations
        This method should remain in OrderCalculator as it coordinates everything

        Args:
            order: The order to calculate totals for

        Returns:
            Dictionary containing all calculated values
        """
        subtotal = self.calculate_order_subtotal(order)
        discount = self.calculate_customer_discount(order)
        discount_amount = subtotal * discount
        subtotal_after_discount = subtotal - discount_amount

        tax_rate = self.calculate_tax_rate(order)
        tax_amount = subtotal_after_discount * tax_rate

        shipping_cost = self.calculate_shipping_cost(order)

        total = subtotal_after_discount + tax_amount + shipping_cost

        return {
            "subtotal": subtotal,
            "discount_rate": discount,
            "discount_amount": round(discount_amount, 2),
            "subtotal_after_discount": round(subtotal_after_discount, 2),
            "tax_rate": tax_rate,
            "tax_amount": round(tax_amount, 2),
            "shipping_cost": shipping_cost,
            "total": round(total, 2),
            "weight": self.calculate_order_weight(order),
        }

    def is_eligible_for_free_shipping(self, order: Order) -> bool:
        """
        Feature Envy: Uses mostly Customer data
        Should be moved to Customer class

        Args:
            order: The order to check for free shipping eligibility

        Returns:
            True if eligible for free shipping, False otherwise
        """
        customer = order.get_customer()
        customer_type = customer.get_type()
        subtotal = self.calculate_order_subtotal(order)

        # VIP customers get free shipping on orders over 50
        if customer_type == "vip" and subtotal >= 50.0:
            return True

        # Premium customers get free shipping on orders over 75
        if customer_type == "premium" and subtotal >= 75.0:
            return True

        # Standard customers get free shipping on orders over 100
        if customer_type == "standard" and subtotal >= 100.0:
            return True

        return False

    def requires_special_handling(self, product: Product) -> bool:
        """
        Feature Envy: Uses mostly Product data
        Should be moved to Product class

        Args:
            product: The product to check for special handling requirements

        Returns:
            True if product requires special handling, False otherwise
        """
        return (
            product.is_fragile()
            or product.get_weight() > 20.0
            or product.get_category() == "electronics"
        )

    def has_special_handling_items(self, order: Order) -> bool:
        """
        Feature Envy: Uses mostly Order and Product data
        Could be moved to Order class

        Args:
            order: The order to check for special handling items

        Returns:
            True if order contains items requiring special handling, False otherwise
        """
        items = order.get_items()

        for item in items:
            product = item.product
            if self.requires_special_handling(product):
                return True

        return False

    def get_customer_priority_level(self, order: Order) -> str:
        """
        Feature Envy: Uses mostly Customer data (via Order)
        Should be moved to Customer class

        Args:
            order: The order containing customer information

        Returns:
            The priority level as a string ('high', 'medium', 'low')
        """
        customer = order.get_customer()
        customer_type = customer.get_type()
        loyalty_years = customer.get_loyalty_years()

        if customer_type == "vip":
            return "high"

        if customer_type == "premium":
            return "medium"

        if customer_type == "standard" and loyalty_years >= 5:
            return "medium"

        return "low"
