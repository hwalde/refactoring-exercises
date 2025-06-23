<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\ShotgunSurgery;

use PHPUnit\Framework\TestCase;

class NotificationServiceTest extends TestCase
{
    private NotificationService $notificationService;

    protected function setUp(): void
    {
        $this->notificationService = new NotificationService();
    }

    protected function tearDown(): void
    {
        $this->notificationService->clearNotifications();
    }

    public function testSendOrderConfirmation(): void
    {
        $customerId = 'customer_123';
        $orderData = [
            'order_id' => 'ORDER_001',
            'total' => '99.99',
            'items' => [
                ['name' => 'Test Product', 'quantity' => 2, 'price' => '49.99']
            ]
        ];

        $this->notificationService->sendOrderConfirmation($customerId, $orderData);

        $notifications = $this->notificationService->getSentNotifications();
        $this->assertNotEmpty($notifications);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Order Confirmation #ORDER_001', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('ORDER_001', $emailNotifications[0]['body']);
        $this->assertStringContainsString('€99.99', $emailNotifications[0]['body']);

        // Should send SMS for customers who prefer SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('ORDER_001', $smsNotifications[0]['message']);
        $this->assertStringContainsString('€99.99', $smsNotifications[0]['message']);

        // Should send push notification for app users
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
        $this->assertEquals('Your order has been confirmed!', $pushNotifications[0]['message']);
        $this->assertEquals('order_confirmation', $pushNotifications[0]['data']['type']);
        $this->assertEquals('ORDER_001', $pushNotifications[0]['data']['order_id']);
    }

    public function testSendOrderConfirmationNoSmsForCustomerNoSms(): void
    {
        $customerId = 'customer_no_sms';
        $orderData = [
            'order_id' => 'ORDER_002',
            'total' => '149.99',
            'items' => []
        ];

        $this->notificationService->sendOrderConfirmation($customerId, $orderData);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);

        // Should NOT send SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(0, $smsNotifications);

        // Should send push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
    }

    public function testSendOrderShipped(): void
    {
        $customerId = 'customer_456';
        $shippingData = [
            'order_id' => 'ORDER_003',
            'tracking_number' => 'TRACK123456',
            'expected_delivery' => '2024-01-15'
        ];

        $this->notificationService->sendOrderShipped($customerId, $shippingData);

        $notifications = $this->notificationService->getSentNotifications();
        $this->assertNotEmpty($notifications);

        // Should send email with tracking info
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Your Order Has Shipped!', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('ORDER_003', $emailNotifications[0]['body']);
        $this->assertStringContainsString('TRACK123456', $emailNotifications[0]['body']);
        $this->assertStringContainsString('2024-01-15', $emailNotifications[0]['body']);

        // Should send SMS with tracking
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('TRACK123456', $smsNotifications[0]['message']);

        // Should send push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
        $this->assertEquals('Package on the way!', $pushNotifications[0]['message']);
        $this->assertEquals('shipping_update', $pushNotifications[0]['data']['type']);
        $this->assertEquals('TRACK123456', $pushNotifications[0]['data']['tracking_number']);
    }

    public function testSendPaymentConfirmation(): void
    {
        $customerId = 'customer_789';
        $paymentData = [
            'order_id' => 'ORDER_004',
            'amount' => 299.99,
            'method' => 'Credit Card',
            'transaction_id' => 'TXN_12345'
        ];

        $this->notificationService->sendPaymentConfirmation($customerId, $paymentData);

        // Should send email with special headers
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Payment Received - Order #ORDER_004', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('€299.99', $emailNotifications[0]['body']);
        $this->assertStringContainsString('Credit Card', $emailNotifications[0]['body']);
        $this->assertStringContainsString('TXN_12345', $emailNotifications[0]['body']);
        $this->assertArrayHasKey('headers', $emailNotifications[0]);
        $this->assertEquals('true', $emailNotifications[0]['headers']['X-Payment-Notification']);
        $this->assertEquals('TXN_12345', $emailNotifications[0]['headers']['X-Transaction-ID']);

        // Should NOT send SMS for low-value payments
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(0, $smsNotifications);
    }

    public function testSendPaymentConfirmationHighValue(): void
    {
        $customerId = 'customer_999';
        $paymentData = [
            'order_id' => 'ORDER_005',
            'amount' => 750.00,
            'method' => 'PayPal',
            'transaction_id' => 'TXN_67890'
        ];

        $this->notificationService->sendPaymentConfirmation($customerId, $paymentData);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);

        // Should send SMS for high-value payments
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('€750', $smsNotifications[0]['message']);
        $this->assertStringContainsString('ORDER_005', $smsNotifications[0]['message']);
    }

    public function testSendPaymentFailed(): void
    {
        $customerId = 'customer_abc';
        $paymentData = [
            'order_id' => 'ORDER_006',
            'failure_reason' => 'Insufficient funds'
        ];

        $this->notificationService->sendPaymentFailed($customerId, $paymentData);

        // Should send urgent email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('URGENT: Payment Failed - Order #ORDER_006', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('Insufficient funds', $emailNotifications[0]['body']);
        $this->assertArrayHasKey('headers', $emailNotifications[0]);
        $this->assertEquals('1', $emailNotifications[0]['headers']['X-Priority']);
        $this->assertEquals('High', $emailNotifications[0]['headers']['X-MSMail-Priority']);

        // Should always send SMS for failed payments
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('ORDER_006', $smsNotifications[0]['message']);

        // Should send high priority push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
        $this->assertEquals('Payment Issue - Action Required', $pushNotifications[0]['message']);
        $this->assertEquals('payment_failed', $pushNotifications[0]['data']['type']);
        $this->assertEquals('high', $pushNotifications[0]['data']['priority']);
    }

    public function testSendAccountUpdateProfileUpdated(): void
    {
        $customerId = 'customer_def';
        $data = ['field' => 'name', 'old_value' => 'John', 'new_value' => 'John Doe'];

        $this->notificationService->sendAccountUpdate($customerId, 'profile_updated', $data);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Profile Updated Successfully', $emailNotifications[0]['subject']);

        // Should send SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertEquals('Profile updated', $smsNotifications[0]['message']);
    }

    public function testSendAccountUpdateEmailVerified(): void
    {
        $customerId = 'customer_ghi';
        $data = ['email' => 'customer@example.com'];

        $this->notificationService->sendAccountUpdate($customerId, 'email_verified', $data);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Email Address Verified', $emailNotifications[0]['subject']);

        // Should NOT send SMS for email verification
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(0, $smsNotifications);
    }

    public function testSendAccountUpdateInvalidType(): void
    {
        $customerId = 'customer_jkl';
        $data = [];

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Unknown update type: invalid_type');

        $this->notificationService->sendAccountUpdate($customerId, 'invalid_type', $data);
    }

    public function testSendWelcomeMessages(): void
    {
        $customerId = 'customer_mno';
        $customerData = [
            'name' => 'Jane Smith',
            'mobile' => '+49123456789',
            'mobile_app' => true
        ];

        $this->notificationService->sendWelcomeMessages($customerId, $customerData);

        // Should send welcome email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('Welcome to Our Store!', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('Jane Smith', $emailNotifications[0]['body']);

        // Should send welcome SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('Jane Smith', $smsNotifications[0]['message']);

        // Should send push notification for app setup
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
        $this->assertEquals('welcome', $pushNotifications[0]['data']['type']);
        $this->assertTrue($pushNotifications[0]['data']['setup_notifications']);
    }

    public function testSendPromotionalOffer(): void
    {
        $customerId = 'customer_pqr';
        $offerData = [
            'title' => '50% Off Sale',
            'description' => 'Get 50% off all items this weekend only!',
            'code' => 'SAVE50',
            'valid_until' => '2024-01-31',
            'campaign_id' => 'CAMP_001'
        ];

        $this->notificationService->sendPromotionalOffer($customerId, $offerData);

        // Should send promotional email with special headers
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);
        $this->assertEquals('🎉 Special Offer: 50% Off Sale', $emailNotifications[0]['subject']);
        $this->assertStringContainsString('SAVE50', $emailNotifications[0]['body']);
        $this->assertStringContainsString('2024-01-31', $emailNotifications[0]['body']);
        $this->assertArrayHasKey('headers', $emailNotifications[0]);
        $this->assertEquals('CAMP_001', $emailNotifications[0]['headers']['X-Campaign-ID']);
        $this->assertEquals('SAVE50', $emailNotifications[0]['headers']['X-Offer-Code']);

        // Should send promotional SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);
        $this->assertStringContainsString('SAVE50', $smsNotifications[0]['message']);

        // Should send promotional push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
        $this->assertEquals('50% Off Sale', $pushNotifications[0]['message']);
        $this->assertEquals('promotion', $pushNotifications[0]['data']['type']);
        $this->assertEquals('SAVE50', $pushNotifications[0]['data']['offer_code']);
    }

    public function testGetNotificationsByCustomer(): void
    {
        $customerId1 = 'customer_111';
        $customerId2 = 'customer_222';

        // Send notifications for first customer
        $this->notificationService->sendOrderConfirmation($customerId1, [
            'order_id' => 'ORDER_111',
            'total' => '50.00',
            'items' => []
        ]);

        // Send notifications for second customer
        $this->notificationService->sendOrderConfirmation($customerId2, [
            'order_id' => 'ORDER_222',
            'total' => '75.00',
            'items' => []
        ]);

        $customer1Notifications = $this->notificationService->getNotificationsByCustomer($customerId1);
        $customer2Notifications = $this->notificationService->getNotificationsByCustomer($customerId2);

        // Each customer should have 3 notifications (email, sms, push)
        $this->assertCount(3, $customer1Notifications);
        $this->assertCount(3, $customer2Notifications);

        // Check that notifications are correctly filtered
        foreach ($customer1Notifications as $notification) {
            $this->assertEquals($customerId1, $notification['customer_id']);
        }

        foreach ($customer2Notifications as $notification) {
            $this->assertEquals($customerId2, $notification['customer_id']);
        }
    }

    public function testGetNotificationsByType(): void
    {
        $customerId = 'customer_333';

        // Send multiple different types of notifications
        $this->notificationService->sendOrderConfirmation($customerId, [
            'order_id' => 'ORDER_333',
            'total' => '100.00',
            'items' => []
        ]);

        $this->notificationService->sendPaymentConfirmation($customerId, [
            'order_id' => 'ORDER_333',
            'amount' => 100.00,
            'method' => 'Credit Card',
            'transaction_id' => 'TXN_333'
        ]);

        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $pushNotifications = $this->notificationService->getNotificationsByType('push');

        // Should have 2 emails (order confirmation + payment confirmation)
        $this->assertCount(2, $emailNotifications);
        // Should have 1 SMS (order confirmation only, payment was under 500)
        $this->assertCount(1, $smsNotifications);
        // Should have 1 push (order confirmation only)
        $this->assertCount(1, $pushNotifications);

        // Verify types are correct
        foreach ($emailNotifications as $notification) {
            $this->assertEquals('email', $notification['type']);
        }
        foreach ($smsNotifications as $notification) {
            $this->assertEquals('sms', $notification['type']);
        }
        foreach ($pushNotifications as $notification) {
            $this->assertEquals('push', $notification['type']);
        }
    }

    public function testClearNotifications(): void
    {
        $customerId = 'customer_444';

        // Send some notifications
        $this->notificationService->sendOrderConfirmation($customerId, [
            'order_id' => 'ORDER_444',
            'total' => '25.00',
            'items' => []
        ]);

        $this->assertNotEmpty($this->notificationService->getSentNotifications());

        // Clear notifications
        $this->notificationService->clearNotifications();

        $this->assertEmpty($this->notificationService->getSentNotifications());
    }

    public function testNoSmsForCustomerWithoutPhone(): void
    {
        $customerId = 'customer_no_phone';

        $this->notificationService->sendOrderConfirmation($customerId, [
            'order_id' => 'ORDER_NO_PHONE',
            'total' => '100.00',
            'items' => []
        ]);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);

        // Should NOT send SMS (no phone number)
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(0, $smsNotifications);

        // Should send push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
    }

    public function testNoPushForCustomerWithoutApp(): void
    {
        $customerId = 'customer_no_app';

        $this->notificationService->sendOrderConfirmation($customerId, [
            'order_id' => 'ORDER_NO_APP',
            'total' => '100.00',
            'items' => []
        ]);

        // Should send email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);

        // Should send SMS
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(1, $smsNotifications);

        // Should NOT send push notification (no app)
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(0, $pushNotifications);
    }

    public function testNoPromoSmsForOptedOutCustomer(): void
    {
        $customerId = 'customer_no_promo';
        $offerData = [
            'title' => 'Test Offer',
            'description' => 'Test description',
            'code' => 'TEST123',
            'valid_until' => '2024-12-31',
            'campaign_id' => 'TEST_CAMP'
        ];

        $this->notificationService->sendPromotionalOffer($customerId, $offerData);

        // Should send promotional email
        $emailNotifications = $this->notificationService->getNotificationsByType('email');
        $this->assertCount(1, $emailNotifications);

        // Should NOT send promotional SMS (opted out)
        $smsNotifications = $this->notificationService->getNotificationsByType('sms');
        $this->assertCount(0, $smsNotifications);

        // Should send push notification
        $pushNotifications = $this->notificationService->getNotificationsByType('push');
        $this->assertCount(1, $pushNotifications);
    }
}