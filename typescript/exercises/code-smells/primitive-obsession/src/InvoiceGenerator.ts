interface InvoiceItem {
  name: string;
  price: number;
  quantity: number;
  total?: number;
}

interface Invoice {
  id: string;
  customerId: string;
  customerEmail: string;
  items: InvoiceItem[];
  totalAmount: number;
  currency: string;
  status: string;
  createdAt: string;
  dueDate: string;
  discountPercentage?: number;
  sentAt?: string;
  sentFrom?: string;
}

export class InvoiceGenerator {
  private invoices: Map<string, Invoice> = new Map();
  private nextInvoiceNumber: number = 1;

  createInvoice(
    customerId: string,
    customerEmail: string,
    items: InvoiceItem[],
    currency: string = 'EUR'
  ): Invoice {
    if (!customerId.trim()) {
      throw new Error('Customer ID cannot be empty');
    }

    if (!this.isValidEmail(customerEmail)) {
      throw new Error('Invalid email format');
    }

    if (items.length === 0) {
      throw new Error('Invoice must have at least one item');
    }

    const invoiceId =
      'INV-' + this.nextInvoiceNumber.toString().padStart(6, '0');
    this.nextInvoiceNumber++;

    let totalAmount = 0;
    const processedItems: InvoiceItem[] = [];

    for (const item of items) {
      if (
        !item.name ||
        item.price === undefined ||
        item.quantity === undefined
      ) {
        throw new Error('Each item must have name, price, and quantity');
      }

      if (item.price < 0) {
        throw new Error('Item price cannot be negative');
      }

      if (item.quantity <= 0) {
        throw new Error('Item quantity must be positive');
      }

      const itemTotal = item.price * item.quantity;
      totalAmount += itemTotal;

      processedItems.push({
        name: item.name,
        price: Math.round(item.price * 100) / 100,
        quantity: item.quantity,
        total: Math.round(itemTotal * 100) / 100,
      });
    }

    const invoice: Invoice = {
      id: invoiceId,
      customerId,
      customerEmail,
      items: processedItems,
      totalAmount: Math.round(totalAmount * 100) / 100,
      currency,
      status: 'draft',
      createdAt: new Date().toISOString().slice(0, 19).replace('T', ' '),
      dueDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000)
        .toISOString()
        .slice(0, 10),
    };

    this.invoices.set(invoiceId, invoice);
    return invoice;
  }

  updateInvoiceStatus(invoiceId: string, newStatus: string): void {
    const invoice = this.invoices.get(invoiceId);
    if (!invoice) {
      throw new Error('Invoice not found');
    }

    const allowedStatuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled'];
    if (!allowedStatuses.includes(newStatus)) {
      throw new Error('Invalid status');
    }

    const currentStatus = invoice.status;

    const validTransitions: Record<string, string[]> = {
      draft: ['sent', 'cancelled'],
      sent: ['paid', 'overdue', 'cancelled'],
      paid: [],
      overdue: ['paid', 'cancelled'],
      cancelled: [],
    };

    if (!validTransitions[currentStatus]?.includes(newStatus)) {
      throw new Error(
        `Cannot transition from ${currentStatus} to ${newStatus}`
      );
    }

    invoice.status = newStatus;
  }

  getInvoice(invoiceId: string): Invoice | null {
    return this.invoices.get(invoiceId) || null;
  }

  getInvoicesByCustomer(customerId: string): Invoice[] {
    const customerInvoices: Invoice[] = [];
    for (const invoice of this.invoices.values()) {
      if (invoice.customerId === customerId) {
        customerInvoices.push(invoice);
      }
    }
    return customerInvoices;
  }

  calculateTotalRevenue(currency: string = 'EUR'): number {
    let total = 0;
    for (const invoice of this.invoices.values()) {
      if (invoice.currency === currency && invoice.status === 'paid') {
        total += invoice.totalAmount;
      }
    }
    return Math.round(total * 100) / 100;
  }

  addDiscountToInvoice(invoiceId: string, discountPercentage: number): void {
    const invoice = this.invoices.get(invoiceId);
    if (!invoice) {
      throw new Error('Invoice not found');
    }

    if (discountPercentage < 0 || discountPercentage > 100) {
      throw new Error('Discount percentage must be between 0 and 100');
    }

    if (invoice.status !== 'draft') {
      throw new Error('Can only apply discount to draft invoices');
    }

    const discountMultiplier = 1 - discountPercentage / 100;
    const originalAmount = invoice.totalAmount;
    const discountedAmount = originalAmount * discountMultiplier;

    invoice.totalAmount = Math.round(discountedAmount * 100) / 100;
    invoice.discountPercentage = discountPercentage;
  }

  sendInvoiceByEmail(invoiceId: string, fromEmail: string): boolean {
    const invoice = this.invoices.get(invoiceId);
    if (!invoice) {
      throw new Error('Invoice not found');
    }

    if (!this.isValidEmail(fromEmail)) {
      throw new Error('Invalid sender email format');
    }

    if (invoice.status !== 'draft') {
      throw new Error('Can only send draft invoices');
    }

    invoice.status = 'sent';
    invoice.sentAt = new Date().toISOString().slice(0, 19).replace('T', ' ');
    invoice.sentFrom = fromEmail;

    return true;
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}
