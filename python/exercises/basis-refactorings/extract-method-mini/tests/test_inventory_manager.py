"""Tests for InventoryManager class."""

import sys
import unittest
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from inventory_manager import InventoryManager


class TestInventoryManager(unittest.TestCase):
    """Test cases for InventoryManager class."""

    def test_generate_report_with_all_active_items(self) -> None:
        """Test report generation when all items are active."""
        items = [
            {"name": "Item1", "active": True},
            {"name": "Item2", "active": True},
        ]

        manager = InventoryManager(items)
        report = manager.generate_report()

        self.assertIn("Total items: 2", report)
        self.assertIn("Active items: 2", report)
        self.assertIn("Active percentage: 100%", report)

    def test_generate_report_with_no_active_items(self) -> None:
        """Test report generation when no items are active."""
        items = [
            {"name": "Item1", "active": False},
            {"name": "Item2", "active": False},
        ]

        manager = InventoryManager(items)
        report = manager.generate_report()

        self.assertIn("Total items: 2", report)
        self.assertIn("Active items: 0", report)
        self.assertIn("Active percentage: 0%", report)

    def test_generate_report_with_mixed_items(self) -> None:
        """Test report generation with mixed active/inactive items."""
        items = [
            {"name": "Item1", "active": True},
            {"name": "Item2", "active": False},
            {"name": "Item3", "active": True},
        ]

        manager = InventoryManager(items)
        report = manager.generate_report()

        self.assertIn("Total items: 3", report)
        self.assertIn("Active items: 2", report)
        self.assertIn("Active percentage: 66.7%", report)

    def test_generate_report_with_empty_items(self) -> None:
        """Test report generation with empty item list."""
        items = []

        manager = InventoryManager(items)
        report = manager.generate_report()

        self.assertIn("Total items: 0", report)
        self.assertIn("Active items: 0", report)
        self.assertIn("Active percentage: 0%", report)


if __name__ == "__main__":
    unittest.main()
