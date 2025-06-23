<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\ShotgunSurgery;

/**
 * NotificationService demonstrates the Shotgun Surgery code smell.
 * 
 * This class contains notification logic that's scattered across different domains.
 * When we need to add a new notification channel or change notification behavior,
 * we have to modify code in multiple places, making maintenance difficult.
 * 
 * The notification logic here should be centralized and organized better.
 */
class NotificationService
{
    private array $sentNotifications = [];

    public function __construct()
    {
        // Configuration could be injected here in a real implementation
    }

    // ORDER-RELATED NOTIFICATIONS (scattered in different methods)
    
    public function sendOrderConfirmation(string $customerId, array $orderData): void
    {
        // Email notification
        $emailSubject = 'Order Confirmation #' . $orderData['order_id'];
        $emailBody = $this->buildOrderConfirmationEmailBody($orderData);
        $this->sendEmail($customerId, $emailSubject, $emailBody);
        
        // SMS notification if customer prefers SMS
        if ($this->customerPrefersSms($customerId)) {
            $smsMessage = "Order #{$orderData['order_id']} confirmed. Total: €{$orderData['total']}";
            $this->sendSms($customerId, $smsMessage);
        }
        
        // Push notification for mobile app users
        if ($this->customerHasMobileApp($customerId)) {
            $pushMessage = "Your order has been confirmed!";
            $this->sendPushNotification($customerId, $pushMessage, [
                'type' => 'order_confirmation',
                'order_id' => $orderData['order_id']
            ]);
        }
    }

    public function sendOrderShipped(string $customerId, array $shippingData): void
    {
        // Email with tracking info
        $emailSubject = 'Your Order Has Shipped!';
        $emailBody = "Your order #{$shippingData['order_id']} has been shipped.\n";
        $emailBody .= "Tracking Number: {$shippingData['tracking_number']}\n";
        $emailBody .= "Expected Delivery: {$shippingData['expected_delivery']}\n";
        $this->sendEmail($customerId, $emailSubject, $emailBody);
        
        // SMS with short tracking info
        if ($this->customerPrefersSms($customerId)) {
            $smsMessage = "Order shipped! Track: {$shippingData['tracking_number']}";
            $this->sendSms($customerId, $smsMessage);
        }
        
        // Push notification
        if ($this->customerHasMobileApp($customerId)) {
            $this->sendPushNotification($customerId, "Package on the way!", [
                'type' => 'shipping_update',
                'tracking_number' => $shippingData['tracking_number']
            ]);
        }
    }

    // PAYMENT-RELATED NOTIFICATIONS (scattered logic)
    
    public function sendPaymentConfirmation(string $customerId, array $paymentData): void
    {
        // Different email format for payments
        $emailSubject = 'Payment Received - Order #' . $paymentData['order_id'];
        $emailBody = "Thank you for your payment!\n\n";
        $emailBody .= "Amount: €{$paymentData['amount']}\n";
        $emailBody .= "Payment Method: {$paymentData['method']}\n";
        $emailBody .= "Transaction ID: {$paymentData['transaction_id']}\n";
        
        // Add payment-specific email config
        $emailHeaders = [
            'X-Payment-Notification' => 'true',
            'X-Transaction-ID' => $paymentData['transaction_id']
        ];
        $this->sendEmailWithHeaders($customerId, $emailSubject, $emailBody, $emailHeaders);
        
        // SMS for high-value payments
        if ($paymentData['amount'] > 500.0) {
            $smsMessage = "Payment of €{$paymentData['amount']} confirmed for order #{$paymentData['order_id']}";
            $this->sendSms($customerId, $smsMessage);
        }
    }

    public function sendPaymentFailed(string $customerId, array $paymentData): void
    {
        // Urgent email notification
        $emailSubject = 'URGENT: Payment Failed - Order #' . $paymentData['order_id'];
        $emailBody = "Your payment could not be processed.\n\n";
        $emailBody .= "Reason: {$paymentData['failure_reason']}\n";
        $emailBody .= "Please update your payment method to complete your order.\n";
        
        $urgentHeaders = [
            'X-Priority' => '1',
            'X-MSMail-Priority' => 'High'
        ];
        $this->sendEmailWithHeaders($customerId, $emailSubject, $emailBody, $urgentHeaders);
        
        // Always send SMS for failed payments
        $smsMessage = "Payment failed for order #{$paymentData['order_id']}. Please check your payment method.";
        $this->sendSms($customerId, $smsMessage);
        
        // Push notification with high priority
        if ($this->customerHasMobileApp($customerId)) {
            $this->sendPushNotification($customerId, "Payment Issue - Action Required", [
                'type' => 'payment_failed',
                'order_id' => $paymentData['order_id'],
                'priority' => 'high'
            ]);
        }
    }

    // CUSTOMER SERVICE NOTIFICATIONS (different patterns again)
    
    public function sendAccountUpdate(string $customerId, string $updateType, array $data): void
    {
        $templates = [
            'profile_updated' => [
                'email_subject' => 'Profile Updated Successfully',
                'email_body' => 'Your profile has been updated.',
                'sms_message' => 'Profile updated'
            ],
            'password_changed' => [
                'email_subject' => 'Password Changed',
                'email_body' => 'Your password has been changed successfully.',
                'sms_message' => 'Password changed'
            ],
            'email_verified' => [
                'email_subject' => 'Email Address Verified',
                'email_body' => 'Your email address has been verified.',
                'sms_message' => null // No SMS for email verification
            ]
        ];
        
        if (!isset($templates[$updateType])) {
            throw new \InvalidArgumentException("Unknown update type: {$updateType}");
        }
        
        $template = $templates[$updateType];
        
        // Send email
        $this->sendEmail($customerId, $template['email_subject'], $template['email_body']);
        
        // Send SMS if template has SMS message
        if ($template['sms_message'] && $this->customerPrefersSms($customerId)) {
            $this->sendSms($customerId, $template['sms_message']);
        }
    }

    public function sendWelcomeMessages(string $customerId, array $customerData): void
    {
        // Welcome email series
        $welcomeEmailSubject = 'Welcome to Our Store!';
        $welcomeEmailBody = "Dear {$customerData['name']},\n\n";
        $welcomeEmailBody .= "Welcome to our online store! We're excited to have you.\n";
        $this->sendEmail($customerId, $welcomeEmailSubject, $welcomeEmailBody);
        
        // SMS welcome if customer provided mobile
        if (isset($customerData['mobile']) && !empty($customerData['mobile'])) {
            $welcomeSms = "Welcome {$customerData['name']}! Thanks for joining us.";
            $this->sendSms($customerId, $welcomeSms);
        }
        
        // Setup push notifications
        if (isset($customerData['mobile_app']) && $customerData['mobile_app']) {
            $this->sendPushNotification($customerId, "Welcome! Get notified about deals and orders.", [
                'type' => 'welcome',
                'setup_notifications' => true
            ]);
        }
    }

    // PROMOTIONAL NOTIFICATIONS (yet another different approach)
    
    public function sendPromotionalOffer(string $customerId, array $offerData): void
    {
        // Promotional emails have different styling and tracking
        $promoSubject = "🎉 Special Offer: {$offerData['title']}";
        $promoBody = $this->buildPromoEmailBody($offerData);
        
        $promoHeaders = [
            'X-Campaign-ID' => $offerData['campaign_id'],
            'X-Offer-Code' => $offerData['code'],
            'List-Unsubscribe' => '<mailto:unsubscribe@example.com>'
        ];
        $this->sendEmailWithHeaders($customerId, $promoSubject, $promoBody, $promoHeaders);
        
        // SMS promos are shorter and different
        if ($this->customerAcceptsPromoSms($customerId)) {
            $promoSms = "🎁 {$offerData['title']} - Use code {$offerData['code']}. Reply STOP to opt out.";
            $this->sendSms($customerId, $promoSms);
        }
        
        // Push notifications for app users
        if ($this->customerHasMobileApp($customerId)) {
            $this->sendPushNotification($customerId, $offerData['title'], [
                'type' => 'promotion',
                'offer_code' => $offerData['code'],
                'campaign_id' => $offerData['campaign_id']
            ]);
        }
    }

    // LOW-LEVEL NOTIFICATION METHODS (implementation details mixed with business logic)
    
    private function sendEmail(string $customerId, string $subject, string $body): void
    {
        $customerEmail = $this->getCustomerEmail($customerId);
        
        // Simulate email sending
        $notification = [
            'id' => uniqid('email_'),
            'type' => 'email',
            'customer_id' => $customerId,
            'recipient' => $customerEmail,
            'subject' => $subject,
            'body' => $body,
            'sent_at' => date('Y-m-d H:i:s'),
            'status' => 'sent'
        ];
        
        $this->sentNotifications[] = $notification;
    }
    
    private function sendEmailWithHeaders(string $customerId, string $subject, string $body, array $headers): void
    {
        $customerEmail = $this->getCustomerEmail($customerId);
        
        $notification = [
            'id' => uniqid('email_'),
            'type' => 'email',
            'customer_id' => $customerId,
            'recipient' => $customerEmail,
            'subject' => $subject,
            'body' => $body,
            'headers' => $headers,
            'sent_at' => date('Y-m-d H:i:s'),
            'status' => 'sent'
        ];
        
        $this->sentNotifications[] = $notification;
    }
    
    private function sendSms(string $customerId, string $message): void
    {
        $customerPhone = $this->getCustomerPhone($customerId);
        
        if (!$customerPhone) {
            return; // Skip if no phone number
        }
        
        $notification = [
            'id' => uniqid('sms_'),
            'type' => 'sms',
            'customer_id' => $customerId,
            'recipient' => $customerPhone,
            'message' => $message,
            'sent_at' => date('Y-m-d H:i:s'),
            'status' => 'sent'
        ];
        
        $this->sentNotifications[] = $notification;
    }
    
    private function sendPushNotification(string $customerId, string $message, array $data = []): void
    {
        $deviceToken = $this->getCustomerDeviceToken($customerId);
        
        if (!$deviceToken) {
            return; // Skip if no device token
        }
        
        $notification = [
            'id' => uniqid('push_'),
            'type' => 'push',
            'customer_id' => $customerId,
            'device_token' => $deviceToken,
            'message' => $message,
            'data' => $data,
            'sent_at' => date('Y-m-d H:i:s'),
            'status' => 'sent'
        ];
        
        $this->sentNotifications[] = $notification;
    }

    // HELPER METHODS (scattered customer preference logic)
    
    private function customerPrefersSms(string $customerId): bool
    {
        // Simulate customer preference lookup
        return $customerId !== 'customer_no_sms';
    }
    
    private function customerHasMobileApp(string $customerId): bool
    {
        return $customerId !== 'customer_no_app';
    }
    
    private function customerAcceptsPromoSms(string $customerId): bool
    {
        return $customerId !== 'customer_no_promo' && $this->customerPrefersSms($customerId);
    }
    
    private function getCustomerEmail(string $customerId): string
    {
        // Simulate customer email lookup
        return "customer.{$customerId}@example.com";
    }
    
    private function getCustomerPhone(string $customerId): ?string
    {
        if ($customerId === 'customer_no_phone') {
            return null;
        }
        return "+49123456789";
    }
    
    private function getCustomerDeviceToken(string $customerId): ?string
    {
        if ($customerId === 'customer_no_app') {
            return null;
        }
        return "device_token_for_{$customerId}";
    }

    // EMAIL TEMPLATE BUILDERS (mixed with business logic)
    
    private function buildOrderConfirmationEmailBody(array $orderData): string
    {
        $body = "Dear Customer,\n\n";
        $body .= "Thank you for your order!\n\n";
        $body .= "Order Details:\n";
        $body .= "Order ID: {$orderData['order_id']}\n";
        $body .= "Total: €{$orderData['total']}\n";
        $body .= "Items:\n";
        
        foreach ($orderData['items'] as $item) {
            $body .= "- {$item['name']} (Qty: {$item['quantity']}) - €{$item['price']}\n";
        }
        
        $body .= "\nYour order will be processed within 1-2 business days.\n";
        $body .= "\nBest regards,\nYour Online Store";
        
        return $body;
    }
    
    private function buildPromoEmailBody(array $offerData): string
    {
        $body = "🎉 Special Offer Just for You! 🎉\n\n";
        $body .= "{$offerData['title']}\n\n";
        $body .= "{$offerData['description']}\n\n";
        $body .= "Use code: {$offerData['code']}\n";
        $body .= "Valid until: {$offerData['valid_until']}\n\n";
        $body .= "Shop now and save!\n";
        $body .= "\nTo unsubscribe from promotional emails, click here.";
        
        return $body;
    }

    // PUBLIC API METHODS
    
    public function getSentNotifications(): array
    {
        return $this->sentNotifications;
    }
    
    public function getNotificationsByType(string $type): array
    {
        return array_values(array_filter($this->sentNotifications, function($notification) use ($type) {
            return $notification['type'] === $type;
        }));
    }
    
    public function getNotificationsByCustomer(string $customerId): array
    {
        return array_values(array_filter($this->sentNotifications, function($notification) use ($customerId) {
            return $notification['customer_id'] === $customerId;
        }));
    }
    
    public function clearNotifications(): void
    {
        $this->sentNotifications = [];
    }
}