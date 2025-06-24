"""
Product Catalog Service for E-Commerce System

This module contains the ProductCatalogService class which manages product catalogs,
availability checks, and product recommendations.
"""

from typing import Any


class ProductCatalogService:
    """
    Service class for managing product catalogs and availability checks.

    Handles product stock management, availability checks, and product recommendations
    for an e-commerce system.
    """

    def __init__(self) -> None:
        """
        Initialize the ProductCatalogService with sample product data.
        """
        self.products: dict[str, dict[str, Any]] = {
            "laptop-001": {"name": "Business Laptop", "stock": 15, "price": 899.99},
            "phone-002": {"name": "Smartphone Pro", "stock": 0, "price": 699.99},
            "tablet-003": {"name": "Tablet Air", "stock": 8, "price": 399.99},
            "monitor-004": {"name": '27" Monitor', "stock": 3, "price": 299.99},
            "keyboard-005": {
                "name": "Mechanical Keyboard",
                "stock": 25,
                "price": 129.99,
            },
        }

    def get_available_products(self) -> dict[str, dict[str, Any]]:
        """
        Get all products that are currently available in stock.

        Returns:
            Dict[str, Dict[str, Any]]: Dictionary of available products with their details.
        """
        available_products = {}

        for product_id, product in self.products.items():
            if self.is_product_available(product_id):
                available_products[product_id] = product

        return available_products

    def get_product_recommendations(self, category: str) -> list[dict[str, Any]]:
        """
        Get product recommendations for a specific category.

        Args:
            category (str): The product category to filter by.

        Returns:
            List[Dict[str, Any]]: List of recommended products matching the category.
        """
        recommendations = []

        for product_id, product in self.products.items():
            if category in product_id and self.is_product_available(product_id):
                recommendations.append(
                    {
                        "id": product_id,
                        "name": product["name"],
                        "price": product["price"],
                    }
                )

        return recommendations

    def can_add_to_cart(self, product_id: str, quantity: int) -> bool:
        """
        Check if a specific quantity of a product can be added to the cart.

        Args:
            product_id (str): The ID of the product to check.
            quantity (int): The desired quantity to add.

        Returns:
            bool: True if the product can be added in the requested quantity, False otherwise.
        """
        if not self.is_product_available(product_id):
            return False

        return int(self.products[product_id]["stock"]) >= quantity

    def _check_product_stock(self, product_id: str) -> bool:
        """
        Check if a product has stock available.

        Args:
            product_id (str): The ID of the product to check.

        Returns:
            bool: True if the product exists and has stock > 0, False otherwise.
        """
        if product_id not in self.products:
            return False

        return int(self.products[product_id]["stock"]) > 0

    def get_product_details(self, product_id: str) -> dict[str, Any] | None:
        """
        Get detailed information about a specific product.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            Optional[Dict[str, Any]]: Product details if found, None otherwise.
        """
        if product_id not in self.products:
            return None

        return self.products[product_id]

    # This is the unnecessary wrapper method that should be inlined
    def is_product_available(self, product_id: str) -> bool:
        """
        Check if a product is available (unnecessary wrapper method).

        This method is a simple wrapper around _check_product_stock() and should be inlined.

        Args:
            product_id (str): The ID of the product to check.

        Returns:
            bool: True if the product is available, False otherwise.
        """
        return self._check_product_stock(product_id)
