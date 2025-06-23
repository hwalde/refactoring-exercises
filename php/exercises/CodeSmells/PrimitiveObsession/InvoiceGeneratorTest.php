<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\PrimitiveObsession;

use PHPUnit\Framework\TestCase;

class InvoiceGeneratorTest extends TestCase
{
    private InvoiceGenerator $invoiceGenerator;

    protected function setUp(): void
    {
        $this->invoiceGenerator = new InvoiceGenerator();
    }

    public function testCreateInvoiceWithValidData(): void
    {
        $items = [
            ['name' => 'Product A', 'price' => 100.0, 'quantity' => 2],
            ['name' => 'Product B', 'price' => 50.5, 'quantity' => 1]
        ];

        $invoice = $this->invoiceGenerator->createInvoice(
            'CUST-001',
            'customer@example.com',
            $items
        );

        $this->assertSame('INV-000001', $invoice['id']);
        $this->assertSame('CUST-001', $invoice['customerId']);
        $this->assertSame('customer@example.com', $invoice['customerEmail']);
        $this->assertSame(250.5, $invoice['totalAmount']);
        $this->assertSame('EUR', $invoice['currency']);
        $this->assertSame('draft', $invoice['status']);
        $this->assertCount(2, $invoice['items']);
    }

    public function testCreateInvoiceWithDifferentCurrency(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];

        $invoice = $this->invoiceGenerator->createInvoice(
            'CUST-002',
            'customer@example.com',
            $items,
            'USD'
        );

        $this->assertSame('USD', $invoice['currency']);
    }

    public function testCreateInvoiceThrowsExceptionForEmptyCustomerId(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Customer ID cannot be empty');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $this->invoiceGenerator->createInvoice('', 'customer@example.com', $items);
    }

    public function testCreateInvoiceThrowsExceptionForInvalidEmail(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid email format');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $this->invoiceGenerator->createInvoice('CUST-001', 'invalid-email', $items);
    }

    public function testCreateInvoiceThrowsExceptionForEmptyItems(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invoice must have at least one item');

        $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', []);
    }

    public function testCreateInvoiceThrowsExceptionForNegativePrice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Item price cannot be negative');

        $items = [['name' => 'Product A', 'price' => -10.0, 'quantity' => 1]];
        $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);
    }

    public function testCreateInvoiceThrowsExceptionForZeroQuantity(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Item quantity must be positive');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 0]];
        $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);
    }

    public function testInvoiceNumberIncrementsCorrectly(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];

        $invoice1 = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);
        $invoice2 = $this->invoiceGenerator->createInvoice('CUST-002', 'customer2@example.com', $items);

        $this->assertSame('INV-000001', $invoice1['id']);
        $this->assertSame('INV-000002', $invoice2['id']);
    }

    public function testUpdateInvoiceStatusWithValidTransition(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'sent');
        $updatedInvoice = $this->invoiceGenerator->getInvoice($invoice['id']);

        $this->assertNotNull($updatedInvoice);
        $this->assertSame('sent', $updatedInvoice['status']);
    }

    public function testUpdateInvoiceStatusThrowsExceptionForInvalidStatus(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid status');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'invalid-status');
    }

    public function testUpdateInvoiceStatusThrowsExceptionForInvalidTransition(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Cannot transition from paid to draft');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'sent');
        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'paid');
        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'draft');
    }

    public function testUpdateInvoiceStatusThrowsExceptionForNonExistentInvoice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invoice not found');

        $this->invoiceGenerator->updateInvoiceStatus('NON-EXISTENT', 'sent');
    }

    public function testGetInvoiceReturnsCorrectInvoice(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $retrievedInvoice = $this->invoiceGenerator->getInvoice($invoice['id']);

        $this->assertSame($invoice, $retrievedInvoice);
    }

    public function testGetInvoiceReturnsNullForNonExistentInvoice(): void
    {
        $result = $this->invoiceGenerator->getInvoice('NON-EXISTENT');

        $this->assertNull($result);
    }

    public function testGetInvoicesByCustomer(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];

        $invoice1 = $this->invoiceGenerator->createInvoice('CUST-001', 'customer1@example.com', $items);
        $invoice2 = $this->invoiceGenerator->createInvoice('CUST-002', 'customer2@example.com', $items);
        $invoice3 = $this->invoiceGenerator->createInvoice('CUST-001', 'customer1@example.com', $items);

        $customerInvoices = $this->invoiceGenerator->getInvoicesByCustomer('CUST-001');

        $this->assertCount(2, $customerInvoices);
        $this->assertContains($invoice1, $customerInvoices);
        $this->assertContains($invoice3, $customerInvoices);
        $this->assertNotContains($invoice2, $customerInvoices);
    }

    public function testCalculateTotalRevenueForPaidInvoices(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];

        $invoice1 = $this->invoiceGenerator->createInvoice('CUST-001', 'customer1@example.com', $items);
        $invoice2 = $this->invoiceGenerator->createInvoice('CUST-002', 'customer2@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice1['id'], 'sent');
        $this->invoiceGenerator->updateInvoiceStatus($invoice1['id'], 'paid');

        $totalRevenue = $this->invoiceGenerator->calculateTotalRevenue();

        $this->assertSame(100.0, $totalRevenue);
    }

    public function testCalculateTotalRevenueForSpecificCurrency(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];

        $invoice1 = $this->invoiceGenerator->createInvoice('CUST-001', 'customer1@example.com', $items, 'EUR');
        $invoice2 = $this->invoiceGenerator->createInvoice('CUST-002', 'customer2@example.com', $items, 'USD');

        $this->invoiceGenerator->updateInvoiceStatus($invoice1['id'], 'sent');
        $this->invoiceGenerator->updateInvoiceStatus($invoice1['id'], 'paid');
        $this->invoiceGenerator->updateInvoiceStatus($invoice2['id'], 'sent');
        $this->invoiceGenerator->updateInvoiceStatus($invoice2['id'], 'paid');

        $eurRevenue = $this->invoiceGenerator->calculateTotalRevenue('EUR');
        $usdRevenue = $this->invoiceGenerator->calculateTotalRevenue('USD');

        $this->assertSame(100.0, $eurRevenue);
        $this->assertSame(100.0, $usdRevenue);
    }

    public function testAddDiscountToInvoice(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->addDiscountToInvoice($invoice['id'], 10.0);
        $updatedInvoice = $this->invoiceGenerator->getInvoice($invoice['id']);

        $this->assertNotNull($updatedInvoice);
        $this->assertSame(90.0, $updatedInvoice['totalAmount']);
        $this->assertSame(10.0, $updatedInvoice['discountPercentage']);
    }

    public function testAddDiscountThrowsExceptionForInvalidPercentage(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Discount percentage must be between 0 and 100');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->addDiscountToInvoice($invoice['id'], -5.0);
    }

    public function testAddDiscountThrowsExceptionForNonDraftInvoice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Can only apply discount to draft invoices');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'sent');
        $this->invoiceGenerator->addDiscountToInvoice($invoice['id'], 10.0);
    }

    public function testSendInvoiceByEmail(): void
    {
        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $result = $this->invoiceGenerator->sendInvoiceByEmail($invoice['id'], 'sender@company.com');
        $updatedInvoice = $this->invoiceGenerator->getInvoice($invoice['id']);

        $this->assertTrue($result);
        $this->assertNotNull($updatedInvoice);
        $this->assertSame('sent', $updatedInvoice['status']);
        $this->assertSame('sender@company.com', $updatedInvoice['sentFrom']);
        $this->assertArrayHasKey('sentAt', $updatedInvoice);
    }

    public function testSendInvoiceThrowsExceptionForInvalidEmail(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid sender email format');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->sendInvoiceByEmail($invoice['id'], 'invalid-email');
    }

    public function testSendInvoiceThrowsExceptionForNonDraftInvoice(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Can only send draft invoices');

        $items = [['name' => 'Product A', 'price' => 100.0, 'quantity' => 1]];
        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->invoiceGenerator->updateInvoiceStatus($invoice['id'], 'sent');
        $this->invoiceGenerator->sendInvoiceByEmail($invoice['id'], 'sender@company.com');
    }

    public function testRoundingHandledCorrectly(): void
    {
        $items = [
            ['name' => 'Product A', 'price' => 10.555, 'quantity' => 3],
            ['name' => 'Product B', 'price' => 20.999, 'quantity' => 2]
        ];

        $invoice = $this->invoiceGenerator->createInvoice('CUST-001', 'customer@example.com', $items);

        $this->assertSame(73.66, $invoice['totalAmount']);
        $this->assertSame(10.56, $invoice['items'][0]['price']);
        $this->assertSame(31.67, $invoice['items'][0]['total']);
        $this->assertSame(21.0, $invoice['items'][1]['price']);
        $this->assertSame(42.0, $invoice['items'][1]['total']);
    }
}