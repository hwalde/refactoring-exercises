"""
Tests for ProductCatalogService

This module contains unit tests for the ProductCatalogService class to verify
its behavior and functionality.
"""

import sys
import unittest
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from product_catalog_service import ProductCatalogService


class TestProductCatalogService(unittest.TestCase):
    """Test cases for ProductCatalogService class."""

    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        self.service = ProductCatalogService()

    def test_get_available_products_returns_only_products_with_stock(self) -> None:
        """Test that get_available_products returns only products with stock > 0."""
        available_products = self.service.get_available_products()

        self.assertEqual(len(available_products), 4)
        self.assertIn("laptop-001", available_products)
        self.assertIn("tablet-003", available_products)
        self.assertIn("monitor-004", available_products)
        self.assertIn("keyboard-005", available_products)
        self.assertNotIn("phone-002", available_products)

    def test_get_available_products_returns_correct_product_data(self) -> None:
        """Test that get_available_products returns correct product information."""
        available_products = self.service.get_available_products()

        self.assertEqual(available_products["laptop-001"]["name"], "Business Laptop")
        self.assertEqual(available_products["laptop-001"]["stock"], 15)
        self.assertEqual(available_products["laptop-001"]["price"], 899.99)

    def test_get_product_recommendations_filters_available_products_by_category(
        self,
    ) -> None:
        """Test that product recommendations filter by category and availability."""
        laptop_recommendations = self.service.get_product_recommendations("laptop")

        self.assertEqual(len(laptop_recommendations), 1)
        self.assertEqual(laptop_recommendations[0]["id"], "laptop-001")
        self.assertEqual(laptop_recommendations[0]["name"], "Business Laptop")
        self.assertEqual(laptop_recommendations[0]["price"], 899.99)

    def test_get_product_recommendations_excludes_out_of_stock_products(self) -> None:
        """Test that product recommendations exclude out-of-stock products."""
        phone_recommendations = self.service.get_product_recommendations("phone")

        self.assertEqual(len(phone_recommendations), 0)

    def test_get_product_recommendations_returns_multiple_matching_products(
        self,
    ) -> None:
        """Test that product recommendations return multiple products when available."""
        keyboard_recommendations = self.service.get_product_recommendations("keyboard")

        self.assertEqual(len(keyboard_recommendations), 1)
        self.assertEqual(keyboard_recommendations[0]["id"], "keyboard-005")

    def test_get_product_recommendations_returns_empty_array_for_unknown_category(
        self,
    ) -> None:
        """Test that unknown categories return empty recommendations."""
        unknown_recommendations = self.service.get_product_recommendations("unknown")

        self.assertEqual(len(unknown_recommendations), 0)

    def test_can_add_to_cart_returns_true_for_available_product_with_sufficient_stock(
        self,
    ) -> None:
        """Test that can_add_to_cart returns True for available products with sufficient stock."""
        can_add = self.service.can_add_to_cart("laptop-001", 5)

        self.assertTrue(can_add)

    def test_can_add_to_cart_returns_false_for_unavailable_product(self) -> None:
        """Test that can_add_to_cart returns False for unavailable products."""
        can_add = self.service.can_add_to_cart("phone-002", 1)

        self.assertFalse(can_add)

    def test_can_add_to_cart_returns_false_for_insufficient_stock(self) -> None:
        """Test that can_add_to_cart returns False when requested quantity exceeds stock."""
        can_add = self.service.can_add_to_cart("monitor-004", 5)

        self.assertFalse(can_add)

    def test_can_add_to_cart_returns_false_for_nonexistent_product(self) -> None:
        """Test that can_add_to_cart returns False for non-existent products."""
        can_add = self.service.can_add_to_cart("nonexistent-999", 1)

        self.assertFalse(can_add)

    def test_can_add_to_cart_returns_true_for_exact_stock_amount(self) -> None:
        """Test that can_add_to_cart returns True when requesting exact stock amount."""
        can_add = self.service.can_add_to_cart("monitor-004", 3)

        self.assertTrue(can_add)

    def test_get_product_details_returns_correct_data_for_existing_product(
        self,
    ) -> None:
        """Test that get_product_details returns correct data for existing products."""
        product_details = self.service.get_product_details("tablet-003")

        self.assertIsInstance(product_details, dict)
        self.assertEqual(product_details["name"], "Tablet Air")
        self.assertEqual(product_details["stock"], 8)
        self.assertEqual(product_details["price"], 399.99)

    def test_get_product_details_returns_none_for_nonexistent_product(self) -> None:
        """Test that get_product_details returns None for non-existent products."""
        product_details = self.service.get_product_details("nonexistent-999")

        self.assertIsNone(product_details)

    def test_get_product_details_works_for_out_of_stock_product(self) -> None:
        """Test that get_product_details works for out-of-stock products."""
        product_details = self.service.get_product_details("phone-002")

        self.assertIsInstance(product_details, dict)
        self.assertEqual(product_details["name"], "Smartphone Pro")
        self.assertEqual(product_details["stock"], 0)
        self.assertEqual(product_details["price"], 699.99)


if __name__ == "__main__":
    unittest.main()
