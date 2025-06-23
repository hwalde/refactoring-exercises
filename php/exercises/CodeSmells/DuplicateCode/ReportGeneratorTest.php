<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\DuplicateCode;

use PHPUnit\Framework\TestCase;

final class ReportGeneratorTest extends TestCase
{
    private ReportGenerator $reportGenerator;

    protected function setUp(): void
    {
        $this->reportGenerator = new ReportGenerator();
    }

    // Happy Path Tests for Sales Report
    public function testGenerateSalesReportWithValidData(): void
    {
        $salesData = [
            ['id' => 1, 'amount' => 100.50, 'customer' => 'John Doe'],
            ['id' => 2, 'amount' => 250.00, 'customer' => 'Jane Smith'],
            ['id' => 3, 'amount' => 75.25, 'customer' => 'Bob Johnson']
        ];

        $report = $this->reportGenerator->generateSalesReport($salesData);

        $this->assertStringContainsString('COMPANY SALES REPORT', $report);
        $this->assertStringContainsString('John Doe', $report);
        $this->assertStringContainsString('Jane Smith', $report);
        $this->assertStringContainsString('Bob Johnson', $report);
        $this->assertStringContainsString('Total Sales: $425.75', $report);
        $this->assertStringContainsString('Number of Sales: 3', $report);
        $this->assertStringContainsString('Average Sale: $141.92', $report);
        $this->assertStringContainsString('Highest Sale: $250.00', $report);
        $this->assertStringContainsString('Lowest Sale: $75.25', $report);
        $this->assertStringContainsString('ReportGenerator v1.0', $report);
    }

    public function testGenerateSalesReportWithSingleSale(): void
    {
        $salesData = [
            ['id' => 1, 'amount' => 199.99, 'customer' => 'Single Customer']
        ];

        $report = $this->reportGenerator->generateSalesReport($salesData);

        $this->assertStringContainsString('Total Sales: $199.99', $report);
        $this->assertStringContainsString('Number of Sales: 1', $report);
        $this->assertStringContainsString('Average Sale: $199.99', $report);
        $this->assertStringContainsString('Highest Sale: $199.99', $report);
        $this->assertStringContainsString('Lowest Sale: $199.99', $report);
    }

    // Edge Case: Empty Sales Data
    public function testGenerateSalesReportWithEmptyData(): void
    {
        $salesData = [];

        $report = $this->reportGenerator->generateSalesReport($salesData);

        $this->assertStringContainsString('COMPANY SALES REPORT', $report);
        $this->assertStringContainsString('Total Sales: $0.00', $report);
        $this->assertStringContainsString('Number of Sales: 0', $report);
        $this->assertStringContainsString('Average Sale: $0.00', $report);
        $this->assertStringContainsString('Highest Sale: $0.00', $report);
        $this->assertStringContainsString('Lowest Sale: $0.00', $report);
    }

    // Happy Path Tests for Customer Report
    public function testGenerateCustomerReportWithValidData(): void
    {
        $customerData = [
            ['id' => 101, 'name' => 'Alice Cooper', 'totalSpent' => 1500.00],
            ['id' => 102, 'name' => 'Bob Dylan', 'totalSpent' => 2300.50],
            ['id' => 103, 'name' => 'Charlie Brown', 'totalSpent' => 450.25]
        ];

        $report = $this->reportGenerator->generateCustomerReport($customerData);

        $this->assertStringContainsString('COMPANY CUSTOMER REPORT', $report);
        $this->assertStringContainsString('Alice Cooper', $report);
        $this->assertStringContainsString('Bob Dylan', $report);
        $this->assertStringContainsString('Charlie Brown', $report);
        $this->assertStringContainsString('Total Revenue: $4250.75', $report);
        $this->assertStringContainsString('Number of Customers: 3', $report);
        $this->assertStringContainsString('Average Spent: $1416.92', $report);
        $this->assertStringContainsString('Top Customer Spent: $2300.50', $report);
        $this->assertStringContainsString('Lowest Customer Spent: $450.25', $report);
        $this->assertStringContainsString('ReportGenerator v1.0', $report);
    }

    public function testGenerateCustomerReportWithSingleCustomer(): void
    {
        $customerData = [
            ['id' => 999, 'name' => 'Solo Customer', 'totalSpent' => 750.00]
        ];

        $report = $this->reportGenerator->generateCustomerReport($customerData);

        $this->assertStringContainsString('Total Revenue: $750.00', $report);
        $this->assertStringContainsString('Number of Customers: 1', $report);
        $this->assertStringContainsString('Average Spent: $750.00', $report);
        $this->assertStringContainsString('Top Customer Spent: $750.00', $report);
        $this->assertStringContainsString('Lowest Customer Spent: $750.00', $report);
    }

    // Edge Case: Empty Customer Data
    public function testGenerateCustomerReportWithEmptyData(): void
    {
        $customerData = [];

        $report = $this->reportGenerator->generateCustomerReport($customerData);

        $this->assertStringContainsString('COMPANY CUSTOMER REPORT', $report);
        $this->assertStringContainsString('Total Revenue: $0.00', $report);
        $this->assertStringContainsString('Number of Customers: 0', $report);
        $this->assertStringContainsString('Average Spent: $0.00', $report);
        $this->assertStringContainsString('Top Customer Spent: $0.00', $report);
        $this->assertStringContainsString('Lowest Customer Spent: $0.00', $report);
    }

    // Happy Path Tests for Product Report
    public function testGenerateProductReportWithValidData(): void
    {
        $productData = [
            ['name' => 'Laptop Pro', 'sku' => 'LP001', 'revenue' => 2400.00, 'unitsSold' => 2],
            ['name' => 'Mouse Wireless', 'sku' => 'MW002', 'revenue' => 150.00, 'unitsSold' => 5],
            ['name' => 'Keyboard RGB', 'sku' => 'KR003', 'revenue' => 450.00, 'unitsSold' => 3]
        ];

        $report = $this->reportGenerator->generateProductReport($productData);

        $this->assertStringContainsString('COMPANY PRODUCT REPORT', $report);
        $this->assertStringContainsString('Laptop Pro', $report);
        $this->assertStringContainsString('Mouse Wireless', $report);
        $this->assertStringContainsString('Keyboard RGB', $report);
        $this->assertStringContainsString('Total Product Revenue: $3000.00', $report);
        $this->assertStringContainsString('Number of Products: 3', $report);
        $this->assertStringContainsString('Average Product Revenue: $1000.00', $report);
        $this->assertStringContainsString('Top Product Revenue: $2400.00', $report);
        $this->assertStringContainsString('Lowest Product Revenue: $150.00', $report);
        $this->assertStringContainsString('ReportGenerator v1.0', $report);
    }

    public function testGenerateProductReportWithSingleProduct(): void
    {
        $productData = [
            ['name' => 'Single Product', 'sku' => 'SP001', 'revenue' => 299.99, 'unitsSold' => 1]
        ];

        $report = $this->reportGenerator->generateProductReport($productData);

        $this->assertStringContainsString('Total Product Revenue: $299.99', $report);
        $this->assertStringContainsString('Number of Products: 1', $report);
        $this->assertStringContainsString('Average Product Revenue: $299.99', $report);
        $this->assertStringContainsString('Top Product Revenue: $299.99', $report);
        $this->assertStringContainsString('Lowest Product Revenue: $299.99', $report);
    }

    // Edge Case: Empty Product Data
    public function testGenerateProductReportWithEmptyData(): void
    {
        $productData = [];

        $report = $this->reportGenerator->generateProductReport($productData);

        $this->assertStringContainsString('COMPANY PRODUCT REPORT', $report);
        $this->assertStringContainsString('Total Product Revenue: $0.00', $report);
        $this->assertStringContainsString('Number of Products: 0', $report);
        $this->assertStringContainsString('Average Product Revenue: $0.00', $report);
        $this->assertStringContainsString('Top Product Revenue: $0.00', $report);
        $this->assertStringContainsString('Lowest Product Revenue: $0.00', $report);
    }

    // Export Tests - Testing behavior, not implementation
    public function testExportReportToCsv(): void
    {
        $reportContent = "Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01";
        
        $result = $this->reportGenerator->exportReportToCsv($reportContent, 'sales_report');

        $this->assertStringContainsString('CSV Export completed successfully!', $result);
        $this->assertStringContainsString('sales_report_', $result);
        $this->assertStringContainsString('.csv', $result);
        $this->assertStringContainsString('Content size:', $result);
        $this->assertStringContainsString('bytes', $result);
    }

    public function testExportReportToJson(): void
    {
        $reportContent = "Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01";
        
        $result = $this->reportGenerator->exportReportToJson($reportContent, 'sales_report');

        $this->assertStringContainsString('JSON Export completed successfully!', $result);
        $this->assertStringContainsString('sales_report_', $result);
        $this->assertStringContainsString('.json', $result);
        $this->assertStringContainsString('Content size:', $result);
        $this->assertStringContainsString('bytes', $result);
    }

    public function testExportReportToCsvWithEmptyContent(): void
    {
        $reportContent = "";
        
        $result = $this->reportGenerator->exportReportToCsv($reportContent, 'empty_report');

        $this->assertStringContainsString('CSV Export completed successfully!', $result);
        $this->assertStringContainsString('empty_report_', $result);
        $this->assertStringContainsString('.csv', $result);
    }

    public function testExportReportToJsonWithEmptyContent(): void
    {
        $reportContent = "";
        
        $result = $this->reportGenerator->exportReportToJson($reportContent, 'empty_report');

        $this->assertStringContainsString('JSON Export completed successfully!', $result);
        $this->assertStringContainsString('empty_report_', $result);
        $this->assertStringContainsString('.json', $result);
    }

    // Integration Test: Generate report and export it
    public function testGenerateAndExportSalesReport(): void
    {
        $salesData = [
            ['id' => 1, 'amount' => 500.00, 'customer' => 'Test Customer']
        ];

        $report = $this->reportGenerator->generateSalesReport($salesData);
        $csvResult = $this->reportGenerator->exportReportToCsv($report, 'integration_test');
        $jsonResult = $this->reportGenerator->exportReportToJson($report, 'integration_test');

        $this->assertStringContainsString('Test Customer', $report);
        $this->assertStringContainsString('CSV Export completed successfully!', $csvResult);
        $this->assertStringContainsString('JSON Export completed successfully!', $jsonResult);
    }

    // Test that all reports contain proper headers and footers
    public function testAllReportsContainProperHeadersAndFooters(): void
    {
        $salesData = [['id' => 1, 'amount' => 100.00, 'customer' => 'Test']];
        $customerData = [['id' => 1, 'name' => 'Test', 'totalSpent' => 100.00]];
        $productData = [['name' => 'Test', 'sku' => 'T001', 'revenue' => 100.00, 'unitsSold' => 1]];

        $salesReport = $this->reportGenerator->generateSalesReport($salesData);
        $customerReport = $this->reportGenerator->generateCustomerReport($customerData);
        $productReport = $this->reportGenerator->generateProductReport($productData);

        // All reports should have generated timestamp
        $this->assertMatchesRegularExpression('/Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/', $salesReport);
        $this->assertMatchesRegularExpression('/Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/', $customerReport);
        $this->assertMatchesRegularExpression('/Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/', $productReport);

        // All reports should have footer
        $this->assertStringContainsString('ReportGenerator v1.0', $salesReport);
        $this->assertStringContainsString('ReportGenerator v1.0', $customerReport);
        $this->assertStringContainsString('ReportGenerator v1.0', $productReport);

        $this->assertStringContainsString('reports@company.com', $salesReport);
        $this->assertStringContainsString('reports@company.com', $customerReport);
        $this->assertStringContainsString('reports@company.com', $productReport);
    }
}