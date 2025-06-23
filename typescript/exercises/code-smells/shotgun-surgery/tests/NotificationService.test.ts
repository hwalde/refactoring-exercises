import { NotificationService } from '../src/NotificationService';

describe('NotificationService', () => {
  let notificationService: NotificationService;

  beforeEach(() => {
    notificationService = new NotificationService();
  });

  afterEach(() => {
    notificationService.clearNotifications();
  });

  test('sendOrderConfirmation', () => {
    const customerId = 'customer_123';
    const orderData = {
      order_id: 'ORDER_001',
      total: '99.99',
      items: [{ name: 'Test Product', quantity: 2, price: '49.99' }],
    };

    notificationService.sendOrderConfirmation(customerId, orderData);

    const notifications = notificationService.getSentNotifications();
    expect(notifications).not.toHaveLength(0);

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe(
      'Order Confirmation #ORDER_001'
    );
    expect(emailNotifications[0]!.body).toContain('ORDER_001');
    expect(emailNotifications[0]!.body).toContain('€99.99');

    // Should send SMS for customers who prefer SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('ORDER_001');
    expect(smsNotifications[0]!.message).toContain('€99.99');

    // Should send push notification for app users
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
    expect(pushNotifications[0]!.message).toBe(
      'Your order has been confirmed!'
    );
    expect(pushNotifications[0]!.data?.['type']).toBe('order_confirmation');
    expect(pushNotifications[0]!.data?.['order_id']).toBe('ORDER_001');
  });

  test("sendOrderConfirmation - no SMS for customer who doesn't want SMS", () => {
    const customerId = 'customer_no_sms';
    const orderData = {
      order_id: 'ORDER_002',
      total: '149.99',
      items: [],
    };

    notificationService.sendOrderConfirmation(customerId, orderData);

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);

    // Should NOT send SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(0);

    // Should send push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
  });

  test('sendOrderShipped', () => {
    const customerId = 'customer_456';
    const shippingData = {
      order_id: 'ORDER_003',
      tracking_number: 'TRACK123456',
      expected_delivery: '2024-01-15',
    };

    notificationService.sendOrderShipped(customerId, shippingData);

    const notifications = notificationService.getSentNotifications();
    expect(notifications).not.toHaveLength(0);

    // Should send email with tracking info
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe('Your Order Has Shipped!');
    expect(emailNotifications[0]!.body).toContain('ORDER_003');
    expect(emailNotifications[0]!.body).toContain('TRACK123456');
    expect(emailNotifications[0]!.body).toContain('2024-01-15');

    // Should send SMS with tracking
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('TRACK123456');

    // Should send push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
    expect(pushNotifications[0]!.message).toBe('Package on the way!');
    expect(pushNotifications[0]!.data?.['type']).toBe('shipping_update');
    expect(pushNotifications[0]!.data?.['tracking_number']).toBe('TRACK123456');
  });

  test('sendPaymentConfirmation', () => {
    const customerId = 'customer_789';
    const paymentData = {
      order_id: 'ORDER_004',
      amount: 299.99,
      method: 'Credit Card',
      transaction_id: 'TXN_12345',
    };

    notificationService.sendPaymentConfirmation(customerId, paymentData);

    // Should send email with special headers
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe(
      'Payment Received - Order #ORDER_004'
    );
    expect(emailNotifications[0]!.body).toContain('€299.99');
    expect(emailNotifications[0]!.body).toContain('Credit Card');
    expect(emailNotifications[0]!.body).toContain('TXN_12345');
    expect(emailNotifications[0]!.headers).toBeDefined();
    expect(emailNotifications[0]!.headers!['X-Payment-Notification']).toBe(
      'true'
    );
    expect(emailNotifications[0]!.headers!['X-Transaction-ID']).toBe(
      'TXN_12345'
    );

    // Should NOT send SMS for low-value payments
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(0);
  });

  test('sendPaymentConfirmation - high value payment', () => {
    const customerId = 'customer_999';
    const paymentData = {
      order_id: 'ORDER_005',
      amount: 750.0,
      method: 'PayPal',
      transaction_id: 'TXN_67890',
    };

    notificationService.sendPaymentConfirmation(customerId, paymentData);

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);

    // Should send SMS for high-value payments
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('€750');
    expect(smsNotifications[0]!.message).toContain('ORDER_005');
  });

  test('sendPaymentFailed', () => {
    const customerId = 'customer_abc';
    const paymentData = {
      order_id: 'ORDER_006',
      amount: 100,
      method: 'Credit Card',
      transaction_id: 'TXN_FAILED',
      failure_reason: 'Insufficient funds',
    };

    notificationService.sendPaymentFailed(customerId, paymentData);

    // Should send urgent email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe(
      'URGENT: Payment Failed - Order #ORDER_006'
    );
    expect(emailNotifications[0]!.body).toContain('Insufficient funds');
    expect(emailNotifications[0]!.headers).toBeDefined();
    expect(emailNotifications[0]!.headers!['X-Priority']).toBe('1');
    expect(emailNotifications[0]!.headers!['X-MSMail-Priority']).toBe('High');

    // Should always send SMS for failed payments
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('ORDER_006');

    // Should send high priority push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
    expect(pushNotifications[0]!.message).toBe(
      'Payment Issue - Action Required'
    );
    expect(pushNotifications[0]!.data?.['type']).toBe('payment_failed');
    expect(pushNotifications[0]!.data?.['priority']).toBe('high');
  });

  test('sendAccountUpdate - profile updated', () => {
    const customerId = 'customer_def';
    const data = { field: 'name', old_value: 'John', new_value: 'John Doe' };

    notificationService.sendAccountUpdate(customerId, 'profile_updated', data);

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe('Profile Updated Successfully');

    // Should send SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toBe('Profile updated');
  });

  test('sendAccountUpdate - email verified', () => {
    const customerId = 'customer_ghi';
    const data = { email: 'customer@example.com' };

    notificationService.sendAccountUpdate(customerId, 'email_verified', data);

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe('Email Address Verified');

    // Should NOT send SMS for email verification
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(0);
  });

  test('sendAccountUpdate - invalid type', () => {
    const customerId = 'customer_jkl';
    const data = {};

    expect(() => {
      notificationService.sendAccountUpdate(
        customerId,
        'invalid_type' as
          | 'profile_updated'
          | 'password_changed'
          | 'email_verified',
        data
      );
    }).toThrow('Unknown update type: invalid_type');
  });

  test('sendWelcomeMessages', () => {
    const customerId = 'customer_mno';
    const customerData = {
      name: 'Jane Smith',
      mobile: '+49123456789',
      mobile_app: true,
    };

    notificationService.sendWelcomeMessages(customerId, customerData);

    // Should send welcome email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe('Welcome to Our Store!');
    expect(emailNotifications[0]!.body).toContain('Jane Smith');

    // Should send welcome SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('Jane Smith');

    // Should send push notification for app setup
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
    expect(pushNotifications[0]!.data?.['type']).toBe('welcome');
    expect(pushNotifications[0]!.data?.['setup_notifications']).toBe(true);
  });

  test('sendPromotionalOffer', () => {
    const customerId = 'customer_pqr';
    const offerData = {
      title: '50% Off Sale',
      description: 'Get 50% off all items this weekend only!',
      code: 'SAVE50',
      valid_until: '2024-01-31',
      campaign_id: 'CAMP_001',
    };

    notificationService.sendPromotionalOffer(customerId, offerData);

    // Should send promotional email with special headers
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);
    expect(emailNotifications[0]!.subject).toBe(
      '🎉 Special Offer: 50% Off Sale'
    );
    expect(emailNotifications[0]!.body).toContain('SAVE50');
    expect(emailNotifications[0]!.body).toContain('2024-01-31');
    expect(emailNotifications[0]!.headers).toBeDefined();
    expect(emailNotifications[0]!.headers!['X-Campaign-ID']).toBe('CAMP_001');
    expect(emailNotifications[0]!.headers!['X-Offer-Code']).toBe('SAVE50');

    // Should send promotional SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);
    expect(smsNotifications[0]!.message).toContain('SAVE50');

    // Should send promotional push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
    expect(pushNotifications[0]!.message).toBe('50% Off Sale');
    expect(pushNotifications[0]!.data?.['type']).toBe('promotion');
    expect(pushNotifications[0]!.data?.['offer_code']).toBe('SAVE50');
  });

  test('getNotificationsByCustomer', () => {
    const customerId1 = 'customer_111';
    const customerId2 = 'customer_222';

    // Send notifications for first customer
    notificationService.sendOrderConfirmation(customerId1, {
      order_id: 'ORDER_111',
      total: '50.00',
      items: [],
    });

    // Send notifications for second customer
    notificationService.sendOrderConfirmation(customerId2, {
      order_id: 'ORDER_222',
      total: '75.00',
      items: [],
    });

    const customer1Notifications =
      notificationService.getNotificationsByCustomer(customerId1);
    const customer2Notifications =
      notificationService.getNotificationsByCustomer(customerId2);

    // Each customer should have 3 notifications (email, sms, push)
    expect(customer1Notifications).toHaveLength(3);
    expect(customer2Notifications).toHaveLength(3);

    // Check that notifications are correctly filtered
    for (const notification of customer1Notifications) {
      expect(notification.customer_id).toBe(customerId1);
    }

    for (const notification of customer2Notifications) {
      expect(notification.customer_id).toBe(customerId2);
    }
  });

  test('getNotificationsByType', () => {
    const customerId = 'customer_333';

    // Send multiple different types of notifications
    notificationService.sendOrderConfirmation(customerId, {
      order_id: 'ORDER_333',
      total: '100.00',
      items: [],
    });

    notificationService.sendPaymentConfirmation(customerId, {
      order_id: 'ORDER_333',
      amount: 100.0,
      method: 'Credit Card',
      transaction_id: 'TXN_333',
    });

    const emailNotifications =
      notificationService.getNotificationsByType('email');
    const smsNotifications = notificationService.getNotificationsByType('sms');
    const pushNotifications =
      notificationService.getNotificationsByType('push');

    // Should have 2 emails (order confirmation + payment confirmation)
    expect(emailNotifications).toHaveLength(2);
    // Should have 1 SMS (order confirmation only, payment was under 500)
    expect(smsNotifications).toHaveLength(1);
    // Should have 1 push (order confirmation only)
    expect(pushNotifications).toHaveLength(1);

    // Verify types are correct
    for (const notification of emailNotifications) {
      expect(notification.type).toBe('email');
    }
    for (const notification of smsNotifications) {
      expect(notification.type).toBe('sms');
    }
    for (const notification of pushNotifications) {
      expect(notification.type).toBe('push');
    }
  });

  test('clearNotifications', () => {
    const customerId = 'customer_444';

    // Send some notifications
    notificationService.sendOrderConfirmation(customerId, {
      order_id: 'ORDER_444',
      total: '25.00',
      items: [],
    });

    expect(notificationService.getSentNotifications()).not.toHaveLength(0);

    // Clear notifications
    notificationService.clearNotifications();

    expect(notificationService.getSentNotifications()).toHaveLength(0);
  });

  test('no SMS for customer without phone', () => {
    const customerId = 'customer_no_phone';

    notificationService.sendOrderConfirmation(customerId, {
      order_id: 'ORDER_NO_PHONE',
      total: '100.00',
      items: [],
    });

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);

    // Should NOT send SMS (no phone number)
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(0);

    // Should send push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
  });

  test('no push for customer without app', () => {
    const customerId = 'customer_no_app';

    notificationService.sendOrderConfirmation(customerId, {
      order_id: 'ORDER_NO_APP',
      total: '100.00',
      items: [],
    });

    // Should send email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);

    // Should send SMS
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(1);

    // Should NOT send push notification (no app)
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(0);
  });

  test('no promo SMS for opted out customer', () => {
    const customerId = 'customer_no_promo';
    const offerData = {
      title: 'Test Offer',
      description: 'Test description',
      code: 'TEST123',
      valid_until: '2024-12-31',
      campaign_id: 'TEST_CAMP',
    };

    notificationService.sendPromotionalOffer(customerId, offerData);

    // Should send promotional email
    const emailNotifications =
      notificationService.getNotificationsByType('email');
    expect(emailNotifications).toHaveLength(1);

    // Should NOT send promotional SMS (opted out)
    const smsNotifications = notificationService.getNotificationsByType('sms');
    expect(smsNotifications).toHaveLength(0);

    // Should send push notification
    const pushNotifications =
      notificationService.getNotificationsByType('push');
    expect(pushNotifications).toHaveLength(1);
  });
});
