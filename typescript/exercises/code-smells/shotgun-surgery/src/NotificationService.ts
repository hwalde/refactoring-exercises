/**
 * NotificationService demonstrates the Shotgun Surgery code smell.
 *
 * This class contains notification logic that's scattered across different domains.
 * When we need to add a new notification channel or change notification behavior,
 * we have to modify code in multiple places, making maintenance difficult.
 *
 * The notification logic here should be centralized and organized better.
 */

interface OrderData {
  readonly order_id: string;
  readonly total: string;
  readonly items: readonly OrderItem[];
}

interface OrderItem {
  readonly name: string;
  readonly quantity: number;
  readonly price: string;
}

interface ShippingData {
  readonly order_id: string;
  readonly tracking_number: string;
  readonly expected_delivery: string;
}

interface PaymentData {
  readonly order_id: string;
  readonly amount: number;
  readonly method: string;
  readonly transaction_id: string;
  readonly failure_reason?: string;
}

interface CustomerData {
  readonly name: string;
  readonly mobile?: string;
  readonly mobile_app?: boolean;
}

interface OfferData {
  readonly title: string;
  readonly description: string;
  readonly code: string;
  readonly valid_until: string;
  readonly campaign_id: string;
}

// Configuration interfaces for demo purposes
// interface EmailConfig {
//   readonly smtp_host: string;
//   readonly smtp_port: number;
//   readonly username: string;
// }
//
// interface SmsConfig {
//   readonly provider: string;
//   readonly api_key: string;
// }
//
// interface PushConfig {
//   readonly firebase_key: string;
// }

interface NotificationRecord {
  readonly id: string;
  readonly type: 'email' | 'sms' | 'push';
  readonly customer_id: string;
  readonly recipient?: string;
  readonly device_token?: string;
  readonly subject?: string;
  readonly body?: string;
  readonly message?: string;
  readonly headers?: Record<string, string>;
  readonly data?: Record<string, unknown>;
  readonly sent_at: string;
  readonly status: 'sent';
}

type UpdateType = 'profile_updated' | 'password_changed' | 'email_verified';

interface UpdateTemplate {
  readonly email_subject: string;
  readonly email_body: string;
  readonly sms_message: string | null;
}

export class NotificationService {
  private sentNotifications: NotificationRecord[] = [];
  constructor() {
    // Configuration would be injected in a real implementation
  }

  // ORDER-RELATED NOTIFICATIONS (scattered in different methods)

  sendOrderConfirmation(customerId: string, orderData: OrderData): void {
    // Email notification
    const emailSubject = `Order Confirmation #${orderData.order_id}`;
    const emailBody = this.buildOrderConfirmationEmailBody(orderData);
    this.sendEmail(customerId, emailSubject, emailBody);

    // SMS notification if customer prefers SMS
    if (this.customerPrefersSms(customerId)) {
      const smsMessage = `Order #${orderData.order_id} confirmed. Total: €${orderData.total}`;
      this.sendSms(customerId, smsMessage);
    }

    // Push notification for mobile app users
    if (this.customerHasMobileApp(customerId)) {
      const pushMessage = 'Your order has been confirmed!';
      this.sendPushNotification(customerId, pushMessage, {
        type: 'order_confirmation',
        order_id: orderData.order_id,
      });
    }
  }

  sendOrderShipped(customerId: string, shippingData: ShippingData): void {
    // Email with tracking info
    const emailSubject = 'Your Order Has Shipped!';
    let emailBody = `Your order #${shippingData.order_id} has been shipped.\n`;
    emailBody += `Tracking Number: ${shippingData.tracking_number}\n`;
    emailBody += `Expected Delivery: ${shippingData.expected_delivery}\n`;
    this.sendEmail(customerId, emailSubject, emailBody);

    // SMS with short tracking info
    if (this.customerPrefersSms(customerId)) {
      const smsMessage = `Order shipped! Track: ${shippingData.tracking_number}`;
      this.sendSms(customerId, smsMessage);
    }

    // Push notification
    if (this.customerHasMobileApp(customerId)) {
      this.sendPushNotification(customerId, 'Package on the way!', {
        type: 'shipping_update',
        tracking_number: shippingData.tracking_number,
      });
    }
  }

  // PAYMENT-RELATED NOTIFICATIONS (scattered logic)

  sendPaymentConfirmation(customerId: string, paymentData: PaymentData): void {
    // Different email format for payments
    const emailSubject = `Payment Received - Order #${paymentData.order_id}`;
    let emailBody = 'Thank you for your payment!\n\n';
    emailBody += `Amount: €${paymentData.amount}\n`;
    emailBody += `Payment Method: ${paymentData.method}\n`;
    emailBody += `Transaction ID: ${paymentData.transaction_id}\n`;

    // Add payment-specific email config
    const emailHeaders = {
      'X-Payment-Notification': 'true',
      'X-Transaction-ID': paymentData.transaction_id,
    };
    this.sendEmailWithHeaders(
      customerId,
      emailSubject,
      emailBody,
      emailHeaders
    );

    // SMS for high-value payments
    if (paymentData.amount > 500.0) {
      const smsMessage = `Payment of €${paymentData.amount} confirmed for order #${paymentData.order_id}`;
      this.sendSms(customerId, smsMessage);
    }
  }

  sendPaymentFailed(customerId: string, paymentData: PaymentData): void {
    // Urgent email notification
    const emailSubject = `URGENT: Payment Failed - Order #${paymentData.order_id}`;
    let emailBody = 'Your payment could not be processed.\n\n';
    emailBody += `Reason: ${paymentData.failure_reason}\n`;
    emailBody += 'Please update your payment method to complete your order.\n';

    const urgentHeaders = {
      'X-Priority': '1',
      'X-MSMail-Priority': 'High',
    };
    this.sendEmailWithHeaders(
      customerId,
      emailSubject,
      emailBody,
      urgentHeaders
    );

    // Always send SMS for failed payments
    const smsMessage = `Payment failed for order #${paymentData.order_id}. Please check your payment method.`;
    this.sendSms(customerId, smsMessage);

    // Push notification with high priority
    if (this.customerHasMobileApp(customerId)) {
      this.sendPushNotification(customerId, 'Payment Issue - Action Required', {
        type: 'payment_failed',
        order_id: paymentData.order_id,
        priority: 'high',
      });
    }
  }

  // CUSTOMER SERVICE NOTIFICATIONS (different patterns again)

  sendAccountUpdate(
    customerId: string,
    updateType: UpdateType,
    data: Record<string, unknown>
  ): void {
    void data; // Acknowledge but don't use in demo
    const templates: Record<UpdateType, UpdateTemplate> = {
      profile_updated: {
        email_subject: 'Profile Updated Successfully',
        email_body: 'Your profile has been updated.',
        sms_message: 'Profile updated',
      },
      password_changed: {
        email_subject: 'Password Changed',
        email_body: 'Your password has been changed successfully.',
        sms_message: 'Password changed',
      },
      email_verified: {
        email_subject: 'Email Address Verified',
        email_body: 'Your email address has been verified.',
        sms_message: null, // No SMS for email verification
      },
    };

    if (!(updateType in templates)) {
      throw new Error(`Unknown update type: ${updateType}`);
    }

    const template = templates[updateType];

    // Send email
    this.sendEmail(customerId, template.email_subject, template.email_body);

    // Send SMS if template has SMS message
    if (template.sms_message && this.customerPrefersSms(customerId)) {
      this.sendSms(customerId, template.sms_message);
    }
  }

  sendWelcomeMessages(customerId: string, customerData: CustomerData): void {
    // Welcome email series
    const welcomeEmailSubject = 'Welcome to Our Store!';
    let welcomeEmailBody = `Dear ${customerData.name},\n\n`;
    welcomeEmailBody +=
      "Welcome to our online store! We're excited to have you.\n";
    this.sendEmail(customerId, welcomeEmailSubject, welcomeEmailBody);

    // SMS welcome if customer provided mobile
    if (customerData.mobile && customerData.mobile.length > 0) {
      const welcomeSms = `Welcome ${customerData.name}! Thanks for joining us.`;
      this.sendSms(customerId, welcomeSms);
    }

    // Setup push notifications
    if (customerData.mobile_app) {
      this.sendPushNotification(
        customerId,
        'Welcome! Get notified about deals and orders.',
        {
          type: 'welcome',
          setup_notifications: true,
        }
      );
    }
  }

  // PROMOTIONAL NOTIFICATIONS (yet another different approach)

  sendPromotionalOffer(customerId: string, offerData: OfferData): void {
    // Promotional emails have different styling and tracking
    const promoSubject = `🎉 Special Offer: ${offerData.title}`;
    const promoBody = this.buildPromoEmailBody(offerData);

    const promoHeaders = {
      'X-Campaign-ID': offerData.campaign_id,
      'X-Offer-Code': offerData.code,
      'List-Unsubscribe': '<mailto:unsubscribe@example.com>',
    };
    this.sendEmailWithHeaders(
      customerId,
      promoSubject,
      promoBody,
      promoHeaders
    );

    // SMS promos are shorter and different
    if (this.customerAcceptsPromoSms(customerId)) {
      const promoSms = `🎁 ${offerData.title} - Use code ${offerData.code}. Reply STOP to opt out.`;
      this.sendSms(customerId, promoSms);
    }

    // Push notifications for app users
    if (this.customerHasMobileApp(customerId)) {
      this.sendPushNotification(customerId, offerData.title, {
        type: 'promotion',
        offer_code: offerData.code,
        campaign_id: offerData.campaign_id,
      });
    }
  }

  // LOW-LEVEL NOTIFICATION METHODS (implementation details mixed with business logic)

  private sendEmail(customerId: string, subject: string, body: string): void {
    const customerEmail = this.getCustomerEmail(customerId);

    // Simulate email sending
    const notification: NotificationRecord = {
      id: this.generateId('email_'),
      type: 'email',
      customer_id: customerId,
      recipient: customerEmail,
      subject: subject,
      body: body,
      sent_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
      status: 'sent',
    };

    this.sentNotifications.push(notification);
  }

  private sendEmailWithHeaders(
    customerId: string,
    subject: string,
    body: string,
    headers: Record<string, string>
  ): void {
    const customerEmail = this.getCustomerEmail(customerId);

    const notification: NotificationRecord = {
      id: this.generateId('email_'),
      type: 'email',
      customer_id: customerId,
      recipient: customerEmail,
      subject: subject,
      body: body,
      headers: headers,
      sent_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
      status: 'sent',
    };

    this.sentNotifications.push(notification);
  }

  private sendSms(customerId: string, message: string): void {
    const customerPhone = this.getCustomerPhone(customerId);

    if (!customerPhone) {
      return; // Skip if no phone number
    }

    const notification: NotificationRecord = {
      id: this.generateId('sms_'),
      type: 'sms',
      customer_id: customerId,
      recipient: customerPhone,
      message: message,
      sent_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
      status: 'sent',
    };

    this.sentNotifications.push(notification);
  }

  private sendPushNotification(
    customerId: string,
    message: string,
    data: Record<string, unknown> = {}
  ): void {
    const deviceToken = this.getCustomerDeviceToken(customerId);

    if (!deviceToken) {
      return; // Skip if no device token
    }

    const notification: NotificationRecord = {
      id: this.generateId('push_'),
      type: 'push',
      customer_id: customerId,
      device_token: deviceToken,
      message: message,
      data: data,
      sent_at: new Date().toISOString().slice(0, 19).replace('T', ' '),
      status: 'sent',
    };

    this.sentNotifications.push(notification);
  }

  // HELPER METHODS (scattered customer preference logic)

  private customerPrefersSms(customerId: string): boolean {
    // Simulate customer preference lookup
    return customerId !== 'customer_no_sms';
  }

  private customerHasMobileApp(customerId: string): boolean {
    return customerId !== 'customer_no_app';
  }

  private customerAcceptsPromoSms(customerId: string): boolean {
    return (
      customerId !== 'customer_no_promo' && this.customerPrefersSms(customerId)
    );
  }

  private getCustomerEmail(customerId: string): string {
    // Simulate customer email lookup
    return `customer.${customerId}@example.com`;
  }

  private getCustomerPhone(customerId: string): string | null {
    if (customerId === 'customer_no_phone') {
      return null;
    }
    return '+49123456789';
  }

  private getCustomerDeviceToken(customerId: string): string | null {
    if (customerId === 'customer_no_app') {
      return null;
    }
    return `device_token_for_${customerId}`;
  }

  // EMAIL TEMPLATE BUILDERS (mixed with business logic)

  private buildOrderConfirmationEmailBody(orderData: OrderData): string {
    let body = 'Dear Customer,\n\n';
    body += 'Thank you for your order!\n\n';
    body += 'Order Details:\n';
    body += `Order ID: ${orderData.order_id}\n`;
    body += `Total: €${orderData.total}\n`;
    body += 'Items:\n';

    for (const item of orderData.items) {
      body += `- ${item.name} (Qty: ${item.quantity}) - €${item.price}\n`;
    }

    body += '\nYour order will be processed within 1-2 business days.\n';
    body += '\nBest regards,\nYour Online Store';

    return body;
  }

  private buildPromoEmailBody(offerData: OfferData): string {
    let body = '🎉 Special Offer Just for You! 🎉\n\n';
    body += `${offerData.title}\n\n`;
    body += `${offerData.description}\n\n`;
    body += `Use code: ${offerData.code}\n`;
    body += `Valid until: ${offerData.valid_until}\n\n`;
    body += 'Shop now and save!\n';
    body += '\nTo unsubscribe from promotional emails, click here.';

    return body;
  }

  // UTILITY METHODS

  private generateId(prefix: string): string {
    return prefix + Math.random().toString(36).substr(2, 9);
  }

  // PUBLIC API METHODS

  getSentNotifications(): readonly NotificationRecord[] {
    return [...this.sentNotifications];
  }

  getNotificationsByType(
    type: 'email' | 'sms' | 'push'
  ): readonly NotificationRecord[] {
    return this.sentNotifications.filter(
      notification => notification.type === type
    );
  }

  getNotificationsByCustomer(
    customerId: string
  ): readonly NotificationRecord[] {
    return this.sentNotifications.filter(
      notification => notification.customer_id === customerId
    );
  }

  clearNotifications(): void {
    this.sentNotifications = [];
  }
}
