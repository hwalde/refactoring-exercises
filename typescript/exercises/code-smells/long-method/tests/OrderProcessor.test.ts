import { OrderProcessor } from '../src/OrderProcessor';

describe('OrderProcessor', () => {
  let processor: OrderProcessor;

  beforeEach(() => {
    processor = new OrderProcessor();
  });

  test('should process simple order', () => {
    const orderData = {
      customer_id: 'cust_123',
      items: [
        {
          product_id: 'prod_1',
          quantity: 2,
          price: 25.0,
        },
        {
          product_id: 'prod_2',
          quantity: 1,
          price: 50.0,
        },
      ],
      shipping_address: {
        country: 'DE',
        city: 'Berlin',
        zip: '10115',
      },
    };

    const result = processor.processOrder(orderData);

    expect(result).toBeDefined();
    expect(result.id).toBeDefined();
    expect(result.customer_id).toBe('cust_123');
    expect(result.subtotal).toBe(100.0);
    expect(result.discount).toBe(0.0); // No discount for 100.0
    expect(result.tax).toBe(19.0); // 19% of 100.0
    expect(result.total).toBe(119.0);
    expect(result.status).toBe('confirmed');
  });

  test('should process order with discount', () => {
    const orderData = {
      customer_id: 'cust_456',
      items: [
        {
          product_id: 'prod_3',
          quantity: 1,
          price: 150.0,
        },
      ],
      shipping_address: {
        country: 'DE',
        city: 'Munich',
        zip: '80331',
      },
    };

    const result = processor.processOrder(orderData);

    expect(result.subtotal).toBe(150.0);
    expect(result.discount).toBe(15.0); // 10% discount for orders > 100
    expect(result.tax).toBe(25.65); // 19% of (150 - 15)
    expect(result.total).toBe(160.65);
  });

  test('should process premium customer order', () => {
    const orderData = {
      customer_id: 'cust_premium',
      customer_type: 'premium' as const,
      items: [
        {
          product_id: 'prod_4',
          quantity: 1,
          price: 200.0,
        },
      ],
      shipping_address: {
        country: 'FR',
        city: 'Paris',
        zip: '75001',
      },
    };

    const result = processor.processOrder(orderData);

    expect(result.subtotal).toBe(200.0);
    expect(result.discount).toBe(30.0); // 10% + 5% premium discount
    expect(result.tax).toBe(34.0); // 20% FR tax of (200 - 30)
    expect(result.total).toBe(204.0);
  });

  test('should process order with coupon', () => {
    const orderData = {
      customer_id: 'cust_789',
      coupon_code: 'SAVE20',
      items: [
        {
          product_id: 'prod_5',
          quantity: 1,
          price: 100.0,
        },
      ],
      shipping_address: {
        country: 'US',
        city: 'New York',
        zip: '10001',
      },
    };

    const result = processor.processOrder(orderData);

    expect(result.subtotal).toBe(100.0);
    expect(result.discount).toBe(20.0); // 20% coupon discount
    expect(result.tax).toBe(6.4); // 8% US tax of (100 - 20)
    expect(result.total).toBe(86.4);
  });

  test('should store order and send notifications', () => {
    const orderData = {
      customer_id: 'cust_notify',
      items: [
        {
          product_id: 'prod_6',
          quantity: 1,
          price: 50.0,
        },
      ],
      shipping_address: {
        country: 'DE',
        city: 'Hamburg',
        zip: '20095',
      },
    };

    const result = processor.processOrder(orderData);

    // Check order is stored
    const orders = processor.getOrders();
    expect(orders).toHaveLength(1);
    expect(orders[0]).toEqual(result);

    // Check customer notification
    const notifications = processor.getNotifications();
    expect(notifications).toHaveLength(1);
    expect(notifications[0]?.type).toBe('order_confirmation');
    expect(notifications[0]?.customer_id).toBe('cust_notify');
    expect(notifications[0]?.order_id).toBe(result.id);
  });

  test('should send high value order notification', () => {
    const orderData = {
      customer_id: 'cust_big_spender',
      items: [
        {
          product_id: 'prod_expensive',
          quantity: 1,
          price: 600.0,
        },
      ],
      shipping_address: {
        country: 'DE',
        city: 'Frankfurt',
        zip: '60311',
      },
    };

    processor.processOrder(orderData);

    const notifications = processor.getNotifications();
    expect(notifications).toHaveLength(2); // Customer + Admin notification

    const adminNotification = notifications.find(
      n => n.type === 'high_value_order'
    );
    expect(adminNotification).toBeDefined();
    expect(adminNotification?.total).toBeGreaterThan(500);
  });

  test('should throw error for missing customer ID', () => {
    expect(() => {
      processor.processOrder({
        customer_id: '',
        items: [],
        shipping_address: { country: 'DE', city: 'Berlin', zip: '10115' },
      });
    }).toThrow('Customer ID is required');
  });

  test('should throw error for empty items', () => {
    expect(() => {
      processor.processOrder({
        customer_id: 'cust_123',
        items: [],
        shipping_address: { country: 'DE', city: 'Berlin', zip: '10115' },
      });
    }).toThrow('Order must contain items');
  });

  test('should cap maximum discount at 50%', () => {
    const orderData = {
      customer_id: 'cust_max_discount',
      customer_type: 'premium' as const,
      coupon_code: 'SAVE20',
      items: [
        {
          product_id: 'prod_7',
          quantity: 1,
          price: 200.0,
        },
      ],
      shipping_address: {
        country: 'DE',
        city: 'Berlin',
        zip: '10115',
      },
    };

    const result = processor.processOrder(orderData);

    expect(result.subtotal).toBe(200.0);
    expect(result.discount).toBe(70.0); // 35% of 200 (10% + 5% + 20%)
    expect(result.discount).toBeLessThanOrEqual(100.0); // Max 50% of subtotal
  });
});
