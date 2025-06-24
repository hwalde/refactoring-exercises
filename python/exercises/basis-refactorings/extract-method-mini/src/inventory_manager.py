"""Inventory management system with report generation."""

from typing import Any


class InventoryManager:
    """Manages inventory items and generates reports.

    This class handles a collection of inventory items and provides
    functionality to generate statistical reports.
    """

    def __init__(self, items: list[dict[str, Any]]) -> None:
        """Initialize the inventory manager with a list of items.

        Args:
            items: List of dictionaries containing item data with 'active' boolean field.
        """
        self.items = items

    def generate_report(self) -> str:
        """Generate a comprehensive inventory report.

        Returns:
            Formatted string containing inventory statistics.
        """
        # Berechnungsblock - soll extrahiert werden
        active_items = 0
        total = len(self.items)

        for item in self.items:
            if item["active"]:
                active_items += 1

        if total > 0:
            percentage = round((active_items / total) * 100, 1)
            # Convert to int if it's a whole number (like 0.0, 100.0)
            if percentage == int(percentage):
                percentage = int(percentage)
        else:
            percentage = 0

        # Berichterstellung
        return (
            f"Inventory Report\n"
            f"Total items: {total}\n"
            f"Active items: {active_items}\n"
            f"Active percentage: {percentage}%"
        )
