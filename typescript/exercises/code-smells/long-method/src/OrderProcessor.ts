interface OrderItem {
  product_id: string;
  quantity: number;
  price: number;
}

interface ShippingAddress {
  country: string;
  city: string;
  zip: string;
}

interface OrderData {
  customer_id: string;
  items: OrderItem[];
  shipping_address: ShippingAddress;
  customer_type?: 'premium' | 'regular';
  coupon_code?: string;
}

interface ProcessedOrder {
  id: string;
  customer_id: string;
  items: OrderItem[];
  subtotal: number;
  discount: number;
  tax: number;
  total: number;
  shipping_address: ShippingAddress;
  status: 'confirmed';
  created_at: string;
}

interface Notification {
  type: 'order_confirmation' | 'high_value_order';
  customer_id?: string;
  order_id: string;
  total?: number;
  message: string;
  sent_at: string;
}

export class OrderProcessor {
  private orders: Map<string, ProcessedOrder> = new Map();
  private notifications: Notification[] = [];

  public processOrder(orderData: OrderData): ProcessedOrder {
    // Validation block
    if (!orderData.customer_id || orderData.customer_id.trim() === '') {
      throw new Error('Customer ID is required');
    }
    if (
      !orderData.items ||
      !Array.isArray(orderData.items) ||
      orderData.items.length === 0
    ) {
      throw new Error('Order must contain items');
    }
    for (const item of orderData.items) {
      if (
        !item.product_id ||
        item.product_id.trim() === '' ||
        !item.quantity ||
        item.quantity <= 0
      ) {
        throw new Error('Invalid item data');
      }
      if (!item.price || item.price <= 0) {
        throw new Error('Invalid item price');
      }
    }
    if (!orderData.shipping_address || !orderData.shipping_address.country) {
      throw new Error('Shipping address is required');
    }

    // Calculate subtotal
    let subtotal = 0;
    for (const item of orderData.items) {
      subtotal += item.price * item.quantity;
    }

    // Apply discount logic
    let discount = 0;
    if (subtotal > 100) {
      discount = subtotal * 0.1; // 10% discount for orders over 100
    }
    if (orderData.customer_type === 'premium') {
      discount += subtotal * 0.05; // Additional 5% for premium customers
    }
    if (orderData.coupon_code === 'SAVE20') {
      discount += subtotal * 0.2; // 20% coupon discount
    }
    // Ensure discount doesn't exceed 50% of subtotal
    if (discount > subtotal * 0.5) {
      discount = subtotal * 0.5;
    }

    // Calculate tax
    let taxRate = 0.19; // 19% VAT default
    switch (orderData.shipping_address.country) {
      case 'DE':
        taxRate = 0.19;
        break;
      case 'FR':
        taxRate = 0.2;
        break;
      case 'IT':
        taxRate = 0.22;
        break;
      case 'US':
        taxRate = 0.08;
        break;
      default:
        taxRate = 0.19;
    }
    const discountedSubtotal = subtotal - discount;
    const tax = discountedSubtotal * taxRate;
    const total = discountedSubtotal + tax;

    // Create order record
    const orderId = `order_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const order: ProcessedOrder = {
      id: orderId,
      customer_id: orderData.customer_id,
      items: orderData.items,
      subtotal: Math.round(subtotal * 100) / 100,
      discount: Math.round(discount * 100) / 100,
      tax: Math.round(tax * 100) / 100,
      total: Math.round(total * 100) / 100,
      shipping_address: orderData.shipping_address,
      status: 'confirmed',
      created_at: new Date().toISOString(),
    };

    // Save order
    this.orders.set(orderId, order);

    // Send notifications
    const customerNotification: Notification = {
      type: 'order_confirmation',
      customer_id: orderData.customer_id,
      order_id: orderId,
      message: `Your order ${orderId} has been confirmed. Total: €${order.total.toFixed(2)}`,
      sent_at: new Date().toISOString(),
    };
    this.notifications.push(customerNotification);

    if (total > 500) {
      const adminNotification: Notification = {
        type: 'high_value_order',
        order_id: orderId,
        total: order.total,
        message: `High value order received: €${order.total.toFixed(2)}`,
        sent_at: new Date().toISOString(),
      };
      this.notifications.push(adminNotification);
    }

    return order;
  }

  public getOrders(): ProcessedOrder[] {
    return Array.from(this.orders.values());
  }

  public getNotifications(): Notification[] {
    return [...this.notifications];
  }
}
