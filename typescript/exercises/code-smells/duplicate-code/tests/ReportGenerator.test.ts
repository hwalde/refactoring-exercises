import { ReportGenerator } from '../src/ReportGenerator';

describe('ReportGenerator', () => {
  let reportGenerator: ReportGenerator;

  beforeEach(() => {
    reportGenerator = new ReportGenerator();
  });

  // Happy Path Tests for Sales Report
  describe('generateSalesReport', () => {
    test('should generate sales report with valid data', () => {
      const salesData = [
        { id: 1, amount: 100.5, customer: 'John Doe' },
        { id: 2, amount: 250.0, customer: 'Jane Smith' },
        { id: 3, amount: 75.25, customer: 'Bob Johnson' },
      ];

      const report = reportGenerator.generateSalesReport(salesData);

      expect(report).toContain('COMPANY SALES REPORT');
      expect(report).toContain('John Doe');
      expect(report).toContain('Jane Smith');
      expect(report).toContain('Bob Johnson');
      expect(report).toContain('Total Sales: $425.75');
      expect(report).toContain('Number of Sales: 3');
      expect(report).toContain('Average Sale: $141.92');
      expect(report).toContain('Highest Sale: $250.00');
      expect(report).toContain('Lowest Sale: $75.25');
      expect(report).toContain('ReportGenerator v1.0');
    });

    test('should generate sales report with single sale', () => {
      const salesData = [
        { id: 1, amount: 199.99, customer: 'Single Customer' },
      ];

      const report = reportGenerator.generateSalesReport(salesData);

      expect(report).toContain('Total Sales: $199.99');
      expect(report).toContain('Number of Sales: 1');
      expect(report).toContain('Average Sale: $199.99');
      expect(report).toContain('Highest Sale: $199.99');
      expect(report).toContain('Lowest Sale: $199.99');
    });

    test('should generate sales report with empty data', () => {
      const salesData: Array<{ id: number; amount: number; customer: string }> =
        [];

      const report = reportGenerator.generateSalesReport(salesData);

      expect(report).toContain('COMPANY SALES REPORT');
      expect(report).toContain('Total Sales: $0.00');
      expect(report).toContain('Number of Sales: 0');
      expect(report).toContain('Average Sale: $0.00');
      expect(report).toContain('Highest Sale: $0.00');
      expect(report).toContain('Lowest Sale: $0.00');
    });
  });

  // Happy Path Tests for Customer Report
  describe('generateCustomerReport', () => {
    test('should generate customer report with valid data', () => {
      const customerData = [
        { id: 101, name: 'Alice Cooper', totalSpent: 1500.0 },
        { id: 102, name: 'Bob Dylan', totalSpent: 2300.5 },
        { id: 103, name: 'Charlie Brown', totalSpent: 450.25 },
      ];

      const report = reportGenerator.generateCustomerReport(customerData);

      expect(report).toContain('COMPANY CUSTOMER REPORT');
      expect(report).toContain('Alice Cooper');
      expect(report).toContain('Bob Dylan');
      expect(report).toContain('Charlie Brown');
      expect(report).toContain('Total Revenue: $4250.75');
      expect(report).toContain('Number of Customers: 3');
      expect(report).toContain('Average Spent: $1416.92');
      expect(report).toContain('Top Customer Spent: $2300.50');
      expect(report).toContain('Lowest Customer Spent: $450.25');
      expect(report).toContain('ReportGenerator v1.0');
    });

    test('should generate customer report with single customer', () => {
      const customerData = [
        { id: 999, name: 'Solo Customer', totalSpent: 750.0 },
      ];

      const report = reportGenerator.generateCustomerReport(customerData);

      expect(report).toContain('Total Revenue: $750.00');
      expect(report).toContain('Number of Customers: 1');
      expect(report).toContain('Average Spent: $750.00');
      expect(report).toContain('Top Customer Spent: $750.00');
      expect(report).toContain('Lowest Customer Spent: $750.00');
    });

    test('should generate customer report with empty data', () => {
      const customerData: Array<{
        id: number;
        name: string;
        totalSpent: number;
      }> = [];

      const report = reportGenerator.generateCustomerReport(customerData);

      expect(report).toContain('COMPANY CUSTOMER REPORT');
      expect(report).toContain('Total Revenue: $0.00');
      expect(report).toContain('Number of Customers: 0');
      expect(report).toContain('Average Spent: $0.00');
      expect(report).toContain('Top Customer Spent: $0.00');
      expect(report).toContain('Lowest Customer Spent: $0.00');
    });
  });

  // Happy Path Tests for Product Report
  describe('generateProductReport', () => {
    test('should generate product report with valid data', () => {
      const productData = [
        { name: 'Laptop Pro', sku: 'LP001', revenue: 2400.0, unitsSold: 2 },
        { name: 'Mouse Wireless', sku: 'MW002', revenue: 150.0, unitsSold: 5 },
        { name: 'Keyboard RGB', sku: 'KR003', revenue: 450.0, unitsSold: 3 },
      ];

      const report = reportGenerator.generateProductReport(productData);

      expect(report).toContain('COMPANY PRODUCT REPORT');
      expect(report).toContain('Laptop Pro');
      expect(report).toContain('Mouse Wireless');
      expect(report).toContain('Keyboard RGB');
      expect(report).toContain('Total Product Revenue: $3000.00');
      expect(report).toContain('Number of Products: 3');
      expect(report).toContain('Average Product Revenue: $1000.00');
      expect(report).toContain('Top Product Revenue: $2400.00');
      expect(report).toContain('Lowest Product Revenue: $150.00');
      expect(report).toContain('ReportGenerator v1.0');
    });

    test('should generate product report with single product', () => {
      const productData = [
        { name: 'Single Product', sku: 'SP001', revenue: 299.99, unitsSold: 1 },
      ];

      const report = reportGenerator.generateProductReport(productData);

      expect(report).toContain('Total Product Revenue: $299.99');
      expect(report).toContain('Number of Products: 1');
      expect(report).toContain('Average Product Revenue: $299.99');
      expect(report).toContain('Top Product Revenue: $299.99');
      expect(report).toContain('Lowest Product Revenue: $299.99');
    });

    test('should generate product report with empty data', () => {
      const productData: Array<{
        name: string;
        sku: string;
        revenue: number;
        unitsSold: number;
      }> = [];

      const report = reportGenerator.generateProductReport(productData);

      expect(report).toContain('COMPANY PRODUCT REPORT');
      expect(report).toContain('Total Product Revenue: $0.00');
      expect(report).toContain('Number of Products: 0');
      expect(report).toContain('Average Product Revenue: $0.00');
      expect(report).toContain('Top Product Revenue: $0.00');
      expect(report).toContain('Lowest Product Revenue: $0.00');
    });
  });

  // Export Tests - Testing behavior, not implementation
  describe('exportReportToCsv', () => {
    test('should export report to CSV format', () => {
      const reportContent =
        'Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01';

      const result = reportGenerator.exportReportToCsv(
        reportContent,
        'sales_report'
      );

      expect(result).toContain('CSV Export completed successfully!');
      expect(result).toContain('sales_report_');
      expect(result).toContain('.csv');
      expect(result).toContain('Content size:');
      expect(result).toContain('bytes');
    });

    test('should export empty report to CSV format', () => {
      const reportContent = '';

      const result = reportGenerator.exportReportToCsv(
        reportContent,
        'empty_report'
      );

      expect(result).toContain('CSV Export completed successfully!');
      expect(result).toContain('empty_report_');
      expect(result).toContain('.csv');
    });
  });

  describe('exportReportToJson', () => {
    test('should export report to JSON format', () => {
      const reportContent =
        'Company Name: ACME Corp\nTotal Sales: $1000.00\nDate: 2024-01-01';

      const result = reportGenerator.exportReportToJson(
        reportContent,
        'sales_report'
      );

      expect(result).toContain('JSON Export completed successfully!');
      expect(result).toContain('sales_report_');
      expect(result).toContain('.json');
      expect(result).toContain('Content size:');
      expect(result).toContain('bytes');
    });

    test('should export empty report to JSON format', () => {
      const reportContent = '';

      const result = reportGenerator.exportReportToJson(
        reportContent,
        'empty_report'
      );

      expect(result).toContain('JSON Export completed successfully!');
      expect(result).toContain('empty_report_');
      expect(result).toContain('.json');
    });
  });

  // Integration Test: Generate report and export it
  describe('integration tests', () => {
    test('should generate and export sales report', () => {
      const salesData = [{ id: 1, amount: 500.0, customer: 'Test Customer' }];

      const report = reportGenerator.generateSalesReport(salesData);
      const csvResult = reportGenerator.exportReportToCsv(
        report,
        'integration_test'
      );
      const jsonResult = reportGenerator.exportReportToJson(
        report,
        'integration_test'
      );

      expect(report).toContain('Test Customer');
      expect(csvResult).toContain('CSV Export completed successfully!');
      expect(jsonResult).toContain('JSON Export completed successfully!');
    });

    test('should generate reports with proper headers and footers', () => {
      const salesData = [{ id: 1, amount: 100.0, customer: 'Test' }];
      const customerData = [{ id: 1, name: 'Test', totalSpent: 100.0 }];
      const productData = [
        { name: 'Test', sku: 'T001', revenue: 100.0, unitsSold: 1 },
      ];

      const salesReport = reportGenerator.generateSalesReport(salesData);
      const customerReport =
        reportGenerator.generateCustomerReport(customerData);
      const productReport = reportGenerator.generateProductReport(productData);

      // All reports should have generated timestamp
      expect(salesReport).toMatch(
        /Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/
      );
      expect(customerReport).toMatch(
        /Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/
      );
      expect(productReport).toMatch(
        /Generated on: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}/
      );

      // All reports should have footer
      expect(salesReport).toContain('ReportGenerator v1.0');
      expect(customerReport).toContain('ReportGenerator v1.0');
      expect(productReport).toContain('ReportGenerator v1.0');

      expect(salesReport).toContain('reports@company.com');
      expect(customerReport).toContain('reports@company.com');
      expect(productReport).toContain('reports@company.com');
    });
  });
});
