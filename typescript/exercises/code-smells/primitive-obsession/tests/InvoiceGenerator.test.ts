import { InvoiceGenerator } from '../src/InvoiceGenerator';

describe('InvoiceGenerator', () => {
  let invoiceGenerator: InvoiceGenerator;

  beforeEach(() => {
    invoiceGenerator = new InvoiceGenerator();
  });

  test('createInvoiceWithValidData', () => {
    const items = [
      { name: 'Product A', price: 100.0, quantity: 2 },
      { name: 'Product B', price: 50.5, quantity: 1 },
    ];

    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    expect(invoice.id).toBe('INV-000001');
    expect(invoice.customerId).toBe('CUST-001');
    expect(invoice.customerEmail).toBe('customer@example.com');
    expect(invoice.totalAmount).toBe(250.5);
    expect(invoice.currency).toBe('EUR');
    expect(invoice.status).toBe('draft');
    expect(invoice.items).toHaveLength(2);
  });

  test('createInvoiceWithDifferentCurrency', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    const invoice = invoiceGenerator.createInvoice(
      'CUST-002',
      'customer@example.com',
      items,
      'USD'
    );

    expect(invoice.currency).toBe('USD');
  });

  test('createInvoiceThrowsExceptionForEmptyCustomerId', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    expect(() => {
      invoiceGenerator.createInvoice('', 'customer@example.com', items);
    }).toThrow('Customer ID cannot be empty');
  });

  test('createInvoiceThrowsExceptionForInvalidEmail', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    expect(() => {
      invoiceGenerator.createInvoice('CUST-001', 'invalid-email', items);
    }).toThrow('Invalid email format');
  });

  test('createInvoiceThrowsExceptionForEmptyItems', () => {
    expect(() => {
      invoiceGenerator.createInvoice('CUST-001', 'customer@example.com', []);
    }).toThrow('Invoice must have at least one item');
  });

  test('createInvoiceThrowsExceptionForNegativePrice', () => {
    const items = [{ name: 'Product A', price: -10.0, quantity: 1 }];

    expect(() => {
      invoiceGenerator.createInvoice('CUST-001', 'customer@example.com', items);
    }).toThrow('Item price cannot be negative');
  });

  test('createInvoiceThrowsExceptionForZeroQuantity', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 0 }];

    expect(() => {
      invoiceGenerator.createInvoice('CUST-001', 'customer@example.com', items);
    }).toThrow('Item quantity must be positive');
  });

  test('invoiceNumberIncrementsCorrectly', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    const invoice1 = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );
    const invoice2 = invoiceGenerator.createInvoice(
      'CUST-002',
      'customer2@example.com',
      items
    );

    expect(invoice1.id).toBe('INV-000001');
    expect(invoice2.id).toBe('INV-000002');
  });

  test('updateInvoiceStatusWithValidTransition', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    invoiceGenerator.updateInvoiceStatus(invoice.id, 'sent');
    const updatedInvoice = invoiceGenerator.getInvoice(invoice.id);

    expect(updatedInvoice?.status).toBe('sent');
  });

  test('updateInvoiceStatusThrowsExceptionForInvalidStatus', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    expect(() => {
      invoiceGenerator.updateInvoiceStatus(invoice.id, 'invalid-status');
    }).toThrow('Invalid status');
  });

  test('updateInvoiceStatusThrowsExceptionForInvalidTransition', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    invoiceGenerator.updateInvoiceStatus(invoice.id, 'sent');
    invoiceGenerator.updateInvoiceStatus(invoice.id, 'paid');

    expect(() => {
      invoiceGenerator.updateInvoiceStatus(invoice.id, 'draft');
    }).toThrow('Cannot transition from paid to draft');
  });

  test('updateInvoiceStatusThrowsExceptionForNonExistentInvoice', () => {
    expect(() => {
      invoiceGenerator.updateInvoiceStatus('NON-EXISTENT', 'sent');
    }).toThrow('Invoice not found');
  });

  test('getInvoiceReturnsCorrectInvoice', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    const retrievedInvoice = invoiceGenerator.getInvoice(invoice.id);

    expect(retrievedInvoice).toEqual(invoice);
  });

  test('getInvoiceReturnsNullForNonExistentInvoice', () => {
    const result = invoiceGenerator.getInvoice('NON-EXISTENT');

    expect(result).toBeNull();
  });

  test('getInvoicesByCustomer', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    const invoice1 = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer1@example.com',
      items
    );
    const invoice2 = invoiceGenerator.createInvoice(
      'CUST-002',
      'customer2@example.com',
      items
    );
    const invoice3 = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer1@example.com',
      items
    );

    const customerInvoices = invoiceGenerator.getInvoicesByCustomer('CUST-001');

    expect(customerInvoices).toHaveLength(2);
    expect(customerInvoices).toContain(invoice1);
    expect(customerInvoices).toContain(invoice3);
    expect(customerInvoices).not.toContain(invoice2);
  });

  test('calculateTotalRevenueForPaidInvoices', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    const invoice1 = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer1@example.com',
      items
    );
    invoiceGenerator.createInvoice('CUST-002', 'customer2@example.com', items);

    invoiceGenerator.updateInvoiceStatus(invoice1.id, 'sent');
    invoiceGenerator.updateInvoiceStatus(invoice1.id, 'paid');

    const totalRevenue = invoiceGenerator.calculateTotalRevenue();

    expect(totalRevenue).toBe(100.0);
  });

  test('calculateTotalRevenueForSpecificCurrency', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];

    const invoice1 = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer1@example.com',
      items,
      'EUR'
    );
    const invoice2 = invoiceGenerator.createInvoice(
      'CUST-002',
      'customer2@example.com',
      items,
      'USD'
    );

    invoiceGenerator.updateInvoiceStatus(invoice1.id, 'sent');
    invoiceGenerator.updateInvoiceStatus(invoice1.id, 'paid');
    invoiceGenerator.updateInvoiceStatus(invoice2.id, 'sent');
    invoiceGenerator.updateInvoiceStatus(invoice2.id, 'paid');

    const eurRevenue = invoiceGenerator.calculateTotalRevenue('EUR');
    const usdRevenue = invoiceGenerator.calculateTotalRevenue('USD');

    expect(eurRevenue).toBe(100.0);
    expect(usdRevenue).toBe(100.0);
  });

  test('addDiscountToInvoice', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    invoiceGenerator.addDiscountToInvoice(invoice.id, 10.0);
    const updatedInvoice = invoiceGenerator.getInvoice(invoice.id);

    expect(updatedInvoice?.totalAmount).toBe(90.0);
    expect(updatedInvoice?.discountPercentage).toBe(10.0);
  });

  test('addDiscountThrowsExceptionForInvalidPercentage', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    expect(() => {
      invoiceGenerator.addDiscountToInvoice(invoice.id, -5.0);
    }).toThrow('Discount percentage must be between 0 and 100');
  });

  test('addDiscountThrowsExceptionForNonDraftInvoice', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    invoiceGenerator.updateInvoiceStatus(invoice.id, 'sent');

    expect(() => {
      invoiceGenerator.addDiscountToInvoice(invoice.id, 10.0);
    }).toThrow('Can only apply discount to draft invoices');
  });

  test('sendInvoiceByEmail', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    const result = invoiceGenerator.sendInvoiceByEmail(
      invoice.id,
      'sender@company.com'
    );
    const updatedInvoice = invoiceGenerator.getInvoice(invoice.id);

    expect(result).toBe(true);
    expect(updatedInvoice?.status).toBe('sent');
    expect(updatedInvoice?.sentFrom).toBe('sender@company.com');
    expect(updatedInvoice?.sentAt).toBeDefined();
  });

  test('sendInvoiceThrowsExceptionForInvalidEmail', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    expect(() => {
      invoiceGenerator.sendInvoiceByEmail(invoice.id, 'invalid-email');
    }).toThrow('Invalid sender email format');
  });

  test('sendInvoiceThrowsExceptionForNonDraftInvoice', () => {
    const items = [{ name: 'Product A', price: 100.0, quantity: 1 }];
    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    invoiceGenerator.updateInvoiceStatus(invoice.id, 'sent');

    expect(() => {
      invoiceGenerator.sendInvoiceByEmail(invoice.id, 'sender@company.com');
    }).toThrow('Can only send draft invoices');
  });

  test('roundingHandledCorrectly', () => {
    const items = [
      { name: 'Product A', price: 10.555, quantity: 3 },
      { name: 'Product B', price: 20.999, quantity: 2 },
    ];

    const invoice = invoiceGenerator.createInvoice(
      'CUST-001',
      'customer@example.com',
      items
    );

    expect(invoice.totalAmount).toBe(73.66);
    expect(invoice.items[0]!.price).toBe(10.56);
    expect(invoice.items[0]!.total).toBe(31.67);
    expect(invoice.items[1]!.price).toBe(21.0);
    expect(invoice.items[1]!.total).toBe(42.0);
  });
});
