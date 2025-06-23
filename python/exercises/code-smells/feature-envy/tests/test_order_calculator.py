import sys
from pathlib import Path

import pytest

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from order_calculator import OrderCalculator
from customer import Customer
from product import Product
from order import Order, OrderItem


class TestOrderCalculator:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.calculator = OrderCalculator()
        
        self.standard_customer = Customer('1', 'John Doe', 'john@example.com', 'standard', 1)
        self.premium_customer = Customer('2', 'Jane Smith', 'jane@example.com', 'premium', 3)
        self.vip_customer = Customer('3', 'Bob Wilson', 'bob@example.com', 'vip', 5)
        
        self.book = Product('book1', 'Programming Book', 29.99, 'books', 0.5, False)
        self.electronics = Product('phone1', 'Smartphone', 699.99, 'electronics', 0.2, True)
        self.furniture = Product('chair1', 'Office Chair', 199.99, 'furniture', 15.0, False)

    def test_calculate_customer_discount_for_standard_customer(self):
        """Test customer discount for standard customer."""
        order = Order('1', self.standard_customer, [], 'Address')
        
        discount = self.calculator.calculate_customer_discount(order)
        
        assert discount == 0.0

    def test_calculate_customer_discount_for_standard_loyal_customer(self):
        """Test customer discount for loyal standard customer."""
        loyal_customer = Customer('4', 'Loyal Customer', 'loyal@example.com', 'standard', 5)
        order = Order('1', loyal_customer, [], 'Address')
        
        discount = self.calculator.calculate_customer_discount(order)
        
        assert discount == 0.05

    def test_calculate_customer_discount_for_premium_customer(self):
        """Test customer discount for premium customer."""
        order = Order('1', self.premium_customer, [], 'Address')
        
        discount = self.calculator.calculate_customer_discount(order)
        
        assert discount == 0.115  # 0.10 + (3 * 0.005)

    def test_calculate_customer_discount_for_vip_customer(self):
        """Test customer discount for VIP customer."""
        order = Order('1', self.vip_customer, [], 'Address')
        
        discount = self.calculator.calculate_customer_discount(order)
        
        assert discount == 0.20  # 0.15 + (5 * 0.01)

    def test_calculate_product_shipping_cost_for_book(self):
        """Test product shipping cost for book."""
        cost = self.calculator.calculate_product_shipping_cost(self.book, 2)
        
        # weight(0.5) * quantity(2) * base(0.5) * book_modifier(0.8) = 0.4
        assert cost == 0.40

    def test_calculate_product_shipping_cost_for_electronics(self):
        """Test product shipping cost for electronics."""
        cost = self.calculator.calculate_product_shipping_cost(self.electronics, 1)
        
        # weight(0.2) * quantity(1) * base(0.5) * electronics_modifier(1.2) * fragile_modifier(1.5) = 0.18
        assert cost == 0.18

    def test_calculate_product_shipping_cost_for_furniture(self):
        """Test product shipping cost for furniture."""
        cost = self.calculator.calculate_product_shipping_cost(self.furniture, 1)
        
        # weight(15.0) * quantity(1) * base(0.5) * furniture_modifier(2.0) = 15.0
        assert cost == 15.0

    def test_calculate_order_subtotal(self):
        """Test order subtotal calculation."""
        items = [
            OrderItem(self.book, 2),
            OrderItem(self.electronics, 1)
        ]
        order = Order('1', self.standard_customer, items, 'Address')
        
        subtotal = self.calculator.calculate_order_subtotal(order)
        
        # (29.99 * 2) + (699.99 * 1) = 59.98 + 699.99 = 759.97
        assert subtotal == 759.97

    def test_calculate_order_weight(self):
        """Test order weight calculation."""
        items = [
            OrderItem(self.book, 2),
            OrderItem(self.furniture, 1)
        ]
        order = Order('1', self.standard_customer, items, 'Address')
        
        weight = self.calculator.calculate_order_weight(order)
        
        # (0.5 * 2) + (15.0 * 1) = 1.0 + 15.0 = 16.0
        assert weight == 16.0

    def test_calculate_tax_rate_for_standard_customer(self):
        """Test tax rate for standard customer."""
        order = Order('1', self.standard_customer, [], 'Address')
        
        tax_rate = self.calculator.calculate_tax_rate(order)
        
        assert tax_rate == 0.20

    def test_calculate_tax_rate_for_premium_customer(self):
        """Test tax rate for premium customer."""
        order = Order('1', self.premium_customer, [], 'Address')
        
        tax_rate = self.calculator.calculate_tax_rate(order)
        
        assert tax_rate == 0.15

    def test_calculate_tax_rate_for_vip_customer(self):
        """Test tax rate for VIP customer."""
        order = Order('1', self.vip_customer, [], 'Address')
        
        tax_rate = self.calculator.calculate_tax_rate(order)
        
        assert tax_rate == 0.10

    def test_calculate_shipping_cost_standard(self):
        """Test standard shipping cost calculation."""
        items = [OrderItem(self.book, 1)]
        order = Order('1', self.standard_customer, items, 'Address', False)
        
        shipping_cost = self.calculator.calculate_shipping_cost(order)
        
        # Base rate(5.99) + book shipping(0.5 * 1 * 0.5 * 0.8) = 5.99 + 0.2 = 6.19
        assert shipping_cost == 6.19

    def test_calculate_shipping_cost_express(self):
        """Test express shipping cost calculation."""
        items = [OrderItem(self.book, 1)]
        order = Order('1', self.standard_customer, items, 'Address', True)
        
        shipping_cost = self.calculator.calculate_shipping_cost(order)
        
        # Base rate(12.99) + book shipping(0.2) = 13.19
        assert shipping_cost == 13.19

    def test_calculate_total(self):
        """Test total calculation without discount."""
        items = [OrderItem(self.book, 2)]
        order = Order('1', self.standard_customer, items, 'Address')
        
        result = self.calculator.calculate_total(order)
        
        assert result['subtotal'] == 59.98
        assert result['discount_rate'] == 0.0
        assert result['discount_amount'] == 0.0
        assert result['subtotal_after_discount'] == 59.98
        assert result['tax_rate'] == 0.20
        assert result['tax_amount'] == 12.0  # 59.98 * 0.20 rounded
        assert result['shipping_cost'] == 6.39  # 5.99 + 0.4
        assert result['total'] == 78.37  # 59.98 + 12.0 + 6.39
        assert result['weight'] == 1.0

    def test_calculate_total_with_discount(self):
        """Test total calculation with discount."""
        items = [OrderItem(self.book, 2)]
        order = Order('1', self.premium_customer, items, 'Address')
        
        result = self.calculator.calculate_total(order)
        
        assert result['subtotal'] == 59.98
        assert result['discount_rate'] == 0.115
        assert result['discount_amount'] == 6.90
        assert result['subtotal_after_discount'] == 53.08
        assert result['tax_rate'] == 0.15
        assert result['tax_amount'] == 7.96
        assert result['total'] == 67.43

    def test_is_eligible_for_free_shipping_standard_customer(self):
        """Test free shipping eligibility for standard customer."""
        items = [OrderItem(self.electronics, 1)]  # 699.99 > 100
        order = Order('1', self.standard_customer, items, 'Address')
        
        is_eligible = self.calculator.is_eligible_for_free_shipping(order)
        
        assert is_eligible is True

    def test_is_eligible_for_free_shipping_standard_customer_not_eligible(self):
        """Test free shipping eligibility for standard customer not eligible."""
        items = [OrderItem(self.book, 2)]  # 59.98 < 100
        order = Order('1', self.standard_customer, items, 'Address')
        
        is_eligible = self.calculator.is_eligible_for_free_shipping(order)
        
        assert is_eligible is False

    def test_is_eligible_for_free_shipping_premium_customer(self):
        """Test free shipping eligibility for premium customer."""
        items = [OrderItem(self.furniture, 1)]  # 199.99 > 75
        order = Order('1', self.premium_customer, items, 'Address')
        
        is_eligible = self.calculator.is_eligible_for_free_shipping(order)
        
        assert is_eligible is True

    def test_is_eligible_for_free_shipping_vip_customer(self):
        """Test free shipping eligibility for VIP customer."""
        items = [OrderItem(self.book, 2)]  # 59.98 > 50
        order = Order('1', self.vip_customer, items, 'Address')
        
        is_eligible = self.calculator.is_eligible_for_free_shipping(order)
        
        assert is_eligible is True

    def test_requires_special_handling_for_fragile_product(self):
        """Test special handling requirement for fragile product."""
        requires_special_handling = self.calculator.requires_special_handling(self.electronics)
        
        assert requires_special_handling is True  # fragile and electronics

    def test_requires_special_handling_for_heavy_product(self):
        """Test special handling requirement for heavy product."""
        heavy_product = Product('heavy1', 'Heavy Item', 99.99, 'other', 25.0, False)
        requires_special_handling = self.calculator.requires_special_handling(heavy_product)
        
        assert requires_special_handling is True  # weight > 20

    def test_requires_special_handling_for_normal_product(self):
        """Test special handling requirement for normal product."""
        requires_special_handling = self.calculator.requires_special_handling(self.book)
        
        assert requires_special_handling is False

    def test_has_special_handling_items(self):
        """Test detection of special handling items in order."""
        items = [
            OrderItem(self.book, 1),
            OrderItem(self.electronics, 1)  # fragile
        ]
        order = Order('1', self.standard_customer, items, 'Address')
        
        has_special_handling = self.calculator.has_special_handling_items(order)
        
        assert has_special_handling is True

    def test_has_no_special_handling_items(self):
        """Test detection of no special handling items in order."""
        items = [OrderItem(self.book, 2)]
        order = Order('1', self.standard_customer, items, 'Address')
        
        has_special_handling = self.calculator.has_special_handling_items(order)
        
        assert has_special_handling is False

    def test_get_customer_priority_level_for_vip(self):
        """Test customer priority level for VIP."""
        order = Order('1', self.vip_customer, [], 'Address')
        
        priority = self.calculator.get_customer_priority_level(order)
        
        assert priority == 'high'

    def test_get_customer_priority_level_for_premium(self):
        """Test customer priority level for premium."""
        order = Order('1', self.premium_customer, [], 'Address')
        
        priority = self.calculator.get_customer_priority_level(order)
        
        assert priority == 'medium'

    def test_get_customer_priority_level_for_loyal_standard(self):
        """Test customer priority level for loyal standard."""
        loyal_customer = Customer('5', 'Loyal Standard', 'loyal@example.com', 'standard', 5)
        order = Order('1', loyal_customer, [], 'Address')
        
        priority = self.calculator.get_customer_priority_level(order)
        
        assert priority == 'medium'

    def test_get_customer_priority_level_for_new_standard(self):
        """Test customer priority level for new standard."""
        order = Order('1', self.standard_customer, [], 'Address')
        
        priority = self.calculator.get_customer_priority_level(order)
        
        assert priority == 'low'

    def test_complete_order_workflow(self):
        """Test complete order workflow integration."""
        items = [
            OrderItem(self.book, 2),
            OrderItem(self.electronics, 1)
        ]
        order = Order('1', self.vip_customer, items, 'Address', True)
        
        # Test various calculations work together
        total = self.calculator.calculate_total(order)
        assert total['total'] > 0
        
        is_eligible = self.calculator.is_eligible_for_free_shipping(order)
        assert is_eligible is True  # VIP with high-value order
        
        has_special_handling = self.calculator.has_special_handling_items(order)
        assert has_special_handling is True  # Electronics is fragile
        
        priority = self.calculator.get_customer_priority_level(order)
        assert priority == 'high'  # VIP customer