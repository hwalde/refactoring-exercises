"""
Tests for ReportGenerator class.

This test suite ensures that the ReportGenerator works correctly both before
and after refactoring. All tests focus on behavior, not implementation details.
"""

import re
import sys
import unittest
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):
    """Test cases for ReportGenerator functionality."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.report_generator = ReportGenerator()

    # Happy Path Tests for Sales Report
    def test_generate_sales_report_with_valid_data(self) -> None:
        """Test sales report generation with valid data."""
        sales_data = [
            {"id": 1, "amount": 100.50, "customer": "John Doe"},
            {"id": 2, "amount": 250.00, "customer": "Jane Smith"},
            {"id": 3, "amount": 75.25, "customer": "Bob Johnson"},
        ]

        report = self.report_generator.generate_sales_report(sales_data)

        self.assertIn("COMPANY SALES REPORT", report)
        self.assertIn("John Doe", report)
        self.assertIn("Jane Smith", report)
        self.assertIn("Bob Johnson", report)
        self.assertIn("Total Sales: $425.75", report)
        self.assertIn("Number of Sales: 3", report)
        self.assertIn("Average Sale: $141.92", report)
        self.assertIn("Highest Sale: $250.00", report)
        self.assertIn("Lowest Sale: $75.25", report)
        self.assertIn("ReportGenerator v1.0", report)

    def test_generate_sales_report_with_single_sale(self) -> None:
        """Test sales report generation with single sale."""
        sales_data = [{"id": 1, "amount": 199.99, "customer": "Single Customer"}]

        report = self.report_generator.generate_sales_report(sales_data)

        self.assertIn("Total Sales: $199.99", report)
        self.assertIn("Number of Sales: 1", report)
        self.assertIn("Average Sale: $199.99", report)
        self.assertIn("Highest Sale: $199.99", report)
        self.assertIn("Lowest Sale: $199.99", report)

    # Edge Case: Empty Sales Data
    def test_generate_sales_report_with_empty_data(self) -> None:
        """Test sales report generation with empty data."""
        sales_data = []

        report = self.report_generator.generate_sales_report(sales_data)

        self.assertIn("COMPANY SALES REPORT", report)
        self.assertIn("Total Sales: $0.00", report)
        self.assertIn("Number of Sales: 0", report)
        self.assertIn("Average Sale: $0.00", report)
        self.assertIn("Highest Sale: $0.00", report)
        self.assertIn("Lowest Sale: $0.00", report)

    # Happy Path Tests for Customer Report
    def test_generate_customer_report_with_valid_data(self) -> None:
        """Test customer report generation with valid data."""
        customer_data = [
            {"id": 101, "name": "Alice Cooper", "totalSpent": 1500.00},
            {"id": 102, "name": "Bob Dylan", "totalSpent": 2300.50},
            {"id": 103, "name": "Charlie Brown", "totalSpent": 450.25},
        ]

        report = self.report_generator.generate_customer_report(customer_data)

        self.assertIn("COMPANY CUSTOMER REPORT", report)
        self.assertIn("Alice Cooper", report)
        self.assertIn("Bob Dylan", report)
        self.assertIn("Charlie Brown", report)
        self.assertIn("Total Revenue: $4250.75", report)
        self.assertIn("Number of Customers: 3", report)
        self.assertIn("Average Spent: $1416.92", report)
        self.assertIn("Top Customer Spent: $2300.50", report)
        self.assertIn("Lowest Customer Spent: $450.25", report)
        self.assertIn("ReportGenerator v1.0", report)

    def test_generate_customer_report_with_single_customer(self) -> None:
        """Test customer report generation with single customer."""
        customer_data = [{"id": 999, "name": "Solo Customer", "totalSpent": 750.00}]

        report = self.report_generator.generate_customer_report(customer_data)

        self.assertIn("Total Revenue: $750.00", report)
        self.assertIn("Number of Customers: 1", report)
        self.assertIn("Average Spent: $750.00", report)
        self.assertIn("Top Customer Spent: $750.00", report)
        self.assertIn("Lowest Customer Spent: $750.00", report)

    # Edge Case: Empty Customer Data
    def test_generate_customer_report_with_empty_data(self) -> None:
        """Test customer report generation with empty data."""
        customer_data = []

        report = self.report_generator.generate_customer_report(customer_data)

        self.assertIn("COMPANY CUSTOMER REPORT", report)
        self.assertIn("Total Revenue: $0.00", report)
        self.assertIn("Number of Customers: 0", report)
        self.assertIn("Average Spent: $0.00", report)
        self.assertIn("Top Customer Spent: $0.00", report)
        self.assertIn("Lowest Customer Spent: $0.00", report)

    # Happy Path Tests for Product Report
    def test_generate_product_report_with_valid_data(self) -> None:
        """Test product report generation with valid data."""
        product_data = [
            {"name": "Laptop Pro", "sku": "LP001", "revenue": 2400.00, "unitsSold": 2},
            {
                "name": "Mouse Wireless",
                "sku": "MW002",
                "revenue": 150.00,
                "unitsSold": 5,
            },
            {"name": "Keyboard RGB", "sku": "KR003", "revenue": 450.00, "unitsSold": 3},
        ]

        report = self.report_generator.generate_product_report(product_data)

        self.assertIn("COMPANY PRODUCT REPORT", report)
        self.assertIn("Laptop Pro", report)
        self.assertIn("Mouse Wireless", report)
        self.assertIn("Keyboard RGB", report)
        self.assertIn("Total Product Revenue: $3000.00", report)
        self.assertIn("Number of Products: 3", report)
        self.assertIn("Average Product Revenue: $1000.00", report)
        self.assertIn("Top Product Revenue: $2400.00", report)
        self.assertIn("Lowest Product Revenue: $150.00", report)
        self.assertIn("ReportGenerator v1.0", report)

    def test_generate_product_report_with_single_product(self) -> None:
        """Test product report generation with single product."""
        product_data = [
            {
                "name": "Single Product",
                "sku": "SP001",
                "revenue": 299.99,
                "unitsSold": 1,
            }
        ]

        report = self.report_generator.generate_product_report(product_data)

        self.assertIn("Total Product Revenue: $299.99", report)
        self.assertIn("Number of Products: 1", report)
        self.assertIn("Average Product Revenue: $299.99", report)
        self.assertIn("Top Product Revenue: $299.99", report)
        self.assertIn("Lowest Product Revenue: $299.99", report)

    # Edge Case: Empty Product Data
    def test_generate_product_report_with_empty_data(self) -> None:
        """Test product report generation with empty data."""
        product_data = []

        report = self.report_generator.generate_product_report(product_data)

        self.assertIn("COMPANY PRODUCT REPORT", report)
        self.assertIn("Total Product Revenue: $0.00", report)
        self.assertIn("Number of Products: 0", report)
        self.assertIn("Average Product Revenue: $0.00", report)
        self.assertIn("Top Product Revenue: $0.00", report)
        self.assertIn("Lowest Product Revenue: $0.00", report)

    # Export Tests - Testing behavior, not implementation
    def test_export_report_to_csv(self) -> None:
        """Test CSV export functionality."""
        report_content = (
            "Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01"
        )

        result = self.report_generator.export_report_to_csv(
            report_content, "sales_report"
        )

        self.assertIn("CSV Export completed successfully!", result)
        self.assertIn("sales_report_", result)
        self.assertIn(".csv", result)
        self.assertIn("Content size:", result)
        self.assertIn("bytes", result)

    def test_export_report_to_json(self) -> None:
        """Test JSON export functionality."""
        report_content = (
            "Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01"
        )

        result = self.report_generator.export_report_to_json(
            report_content, "sales_report"
        )

        self.assertIn("JSON Export completed successfully!", result)
        self.assertIn("sales_report_", result)
        self.assertIn(".json", result)
        self.assertIn("Content size:", result)
        self.assertIn("bytes", result)

    def test_export_report_to_csv_with_empty_content(self) -> None:
        """Test CSV export with empty content."""
        report_content = ""

        result = self.report_generator.export_report_to_csv(
            report_content, "empty_report"
        )

        self.assertIn("CSV Export completed successfully!", result)
        self.assertIn("empty_report_", result)
        self.assertIn(".csv", result)

    def test_export_report_to_json_with_empty_content(self) -> None:
        """Test JSON export with empty content."""
        report_content = ""

        result = self.report_generator.export_report_to_json(
            report_content, "empty_report"
        )

        self.assertIn("JSON Export completed successfully!", result)
        self.assertIn("empty_report_", result)
        self.assertIn(".json", result)

    # Integration Test: Generate report and export it
    def test_generate_and_export_sales_report(self) -> None:
        """Test integration of report generation and export."""
        sales_data = [{"id": 1, "amount": 500.00, "customer": "Test Customer"}]

        report = self.report_generator.generate_sales_report(sales_data)
        csv_result = self.report_generator.export_report_to_csv(
            report, "integration_test"
        )
        json_result = self.report_generator.export_report_to_json(
            report, "integration_test"
        )

        self.assertIn("Test Customer", report)
        self.assertIn("CSV Export completed successfully!", csv_result)
        self.assertIn("JSON Export completed successfully!", json_result)

    # Test that all reports contain proper headers and footers
    def test_all_reports_contain_proper_headers_and_footers(self) -> None:
        """Test that all reports have consistent headers and footers."""
        sales_data = [{"id": 1, "amount": 100.00, "customer": "Test"}]
        customer_data = [{"id": 1, "name": "Test", "totalSpent": 100.00}]
        product_data = [
            {"name": "Test", "sku": "T001", "revenue": 100.00, "unitsSold": 1}
        ]

        sales_report = self.report_generator.generate_sales_report(sales_data)
        customer_report = self.report_generator.generate_customer_report(customer_data)
        product_report = self.report_generator.generate_product_report(product_data)

        # All reports should have generated timestamp
        timestamp_pattern = r"Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        self.assertRegex(sales_report, timestamp_pattern)
        self.assertRegex(customer_report, timestamp_pattern)
        self.assertRegex(product_report, timestamp_pattern)

        # All reports should have footer
        self.assertIn("ReportGenerator v1.0", sales_report)
        self.assertIn("ReportGenerator v1.0", customer_report)
        self.assertIn("ReportGenerator v1.0", product_report)

        self.assertIn("reports@company.com", sales_report)
        self.assertIn("reports@company.com", customer_report)
        self.assertIn("reports@company.com", product_report)


if __name__ == "__main__":
    unittest.main()
