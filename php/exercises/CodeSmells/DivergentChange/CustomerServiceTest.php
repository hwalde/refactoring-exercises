<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\DivergentChange;

use PHPUnit\Framework\TestCase;

/**
 * @internal
 *
 * @coversNothing
 */
class CustomerServiceTest extends TestCase
{
    private CustomerService $customerService;

    protected function setUp(): void
    {
        $this->customerService = new CustomerService();
    }

    public function testRegisterCustomer(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->assertIsInt($customerId);
        $this->assertGreaterThan(0, $customerId);
    }

    public function testRegisterCustomerWithInvalidEmail(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid email format');

        $this->customerService->registerCustomer(
            'invalid-email',
            'password123',
            'John',
            'Doe'
        );
    }

    public function testRegisterCustomerWithShortPassword(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Password must be at least 8 characters');

        $this->customerService->registerCustomer(
            'john.doe@example.com',
            '123',
            'John',
            'Doe'
        );
    }

    public function testRegisterCustomerWithEmptyNames(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('First name and last name are required');

        $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            '',
            'Doe'
        );
    }

    public function testRegisterCustomerWithDuplicateEmail(): void
    {
        $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Customer with this email already exists');

        $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password456',
            'Jane',
            'Smith'
        );
    }

    public function testAuthenticateCustomerSuccess(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $authenticatedId = $this->customerService->authenticateCustomer(
            'john.doe@example.com',
            'password123'
        );

        $this->assertEquals($customerId, $authenticatedId);
    }

    public function testAuthenticateCustomerWithWrongPassword(): void
    {
        $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $result = $this->customerService->authenticateCustomer(
            'john.doe@example.com',
            'wrongpassword'
        );

        $this->assertNull($result);
    }

    public function testAuthenticateCustomerWithNonExistentEmail(): void
    {
        $result = $this->customerService->authenticateCustomer(
            'nonexistent@example.com',
            'password123'
        );

        $this->assertNull($result);
    }

    public function testAccountLockingAfterFailedAttempts(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        // Make 3 failed attempts
        for ($i = 0; $i < 3; ++$i) {
            $this->customerService->authenticateCustomer('john.doe@example.com', 'wrongpassword');
        }

        $this->expectException(\RuntimeException::class);
        $this->expectExceptionMessage('Account is temporarily locked due to too many failed attempts');

        $this->customerService->authenticateCustomer('john.doe@example.com', 'password123');
    }

    public function testUpdateContactInformation(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->customerService->updateContactInformation(
            $customerId,
            'Johnny',
            'Doe-Smith',
            '+1234567890'
        );

        $profile = $this->customerService->getCustomerProfile($customerId);
        $this->assertEquals('Johnny', $profile['personal']['firstName']);
        $this->assertEquals('Doe-Smith', $profile['personal']['lastName']);
        $this->assertEquals('+1234567890', $profile['personal']['phone']);
    }

    public function testUpdateContactInformationWithInvalidPhone(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid phone number format');

        $this->customerService->updateContactInformation(
            $customerId,
            'Johnny',
            'Doe-Smith',
            'invalid-phone'
        );
    }

    public function testUpdateContactInformationForNonExistentCustomer(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Customer not found');

        $this->customerService->updateContactInformation(
            999,
            'Johnny',
            'Doe-Smith',
            '+1234567890'
        );
    }

    public function testAddCustomerAddress(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $addressId = $this->customerService->addCustomerAddress(
            $customerId,
            '123 Main St',
            'New York',
            '10001',
            'USA',
            true
        );

        $this->assertIsInt($addressId);
        $this->assertGreaterThan(0, $addressId);

        $profile = $this->customerService->getCustomerProfile($customerId);
        $this->assertCount(1, $profile['addresses']);
        $this->assertTrue($profile['addresses'][$addressId]['isDefault']);
    }

    public function testAddMultipleAddresses(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $address1Id = $this->customerService->addCustomerAddress(
            $customerId,
            '123 Main St',
            'New York',
            '10001',
            'USA'
        );

        $address2Id = $this->customerService->addCustomerAddress(
            $customerId,
            '456 Oak Ave',
            'Los Angeles',
            '90210',
            'USA',
            true
        );

        $profile = $this->customerService->getCustomerProfile($customerId);
        $this->assertCount(2, $profile['addresses']);
        $this->assertFalse($profile['addresses'][$address1Id]['isDefault']);
        $this->assertTrue($profile['addresses'][$address2Id]['isDefault']);
    }

    public function testAddAddressWithMissingFields(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('All address fields are required');

        $this->customerService->addCustomerAddress(
            $customerId,
            '',
            'New York',
            '10001',
            'USA'
        );
    }

    public function testUpdateMarketingPreferences(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->customerService->updateMarketingPreferences(
            $customerId,
            false,
            true,
            false,
            ['sms', 'mail']
        );

        $profile = $this->customerService->getCustomerProfile($customerId);
        $marketing = $profile['marketing'];

        $this->assertFalse($marketing['emailMarketing']);
        $this->assertTrue($marketing['smsMarketing']);
        $this->assertFalse($marketing['pushNotifications']);
        $this->assertEquals(['sms', 'mail'], $marketing['preferredChannels']);
    }

    public function testUpdateMarketingPreferencesWithInvalidChannel(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Invalid marketing channel: invalid');

        $this->customerService->updateMarketingPreferences(
            $customerId,
            true,
            false,
            true,
            ['email', 'invalid']
        );
    }

    public function testSendMarketingCampaignSuccess(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $result = $this->customerService->sendMarketingCampaign(
            $customerId,
            'Special Offer',
            'Check out our latest deals!',
            'email'
        );

        $this->assertTrue($result);
    }

    public function testSendMarketingCampaignWithOptOut(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->customerService->updateMarketingPreferences(
            $customerId,
            false,
            false,
            false,
            []
        );

        $result = $this->customerService->sendMarketingCampaign(
            $customerId,
            'Special Offer',
            'Check out our latest deals!',
            'email'
        );

        $this->assertFalse($result);
    }

    public function testSendMarketingCampaignWithUnsupportedChannel(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Unsupported marketing channel: carrier-pigeon');

        $this->customerService->sendMarketingCampaign(
            $customerId,
            'Special Offer',
            'Check out our latest deals!',
            'carrier-pigeon'
        );
    }

    public function testRecordPurchase(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $items = [
            ['name' => 'Product A', 'price' => 29.99, 'quantity' => 2],
            ['name' => 'Product B', 'price' => 15.50, 'quantity' => 1],
        ];

        $orderId = $this->customerService->recordPurchase($customerId, $items, 75.48);

        $this->assertIsInt($orderId);
        $this->assertGreaterThan(0, $orderId);
    }

    public function testRecordPurchaseWithEmptyItems(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Purchase must contain at least one item');

        $this->customerService->recordPurchase($customerId, [], 0.0);
    }

    public function testRecordPurchaseWithInvalidAmount(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $items = [['name' => 'Product A', 'price' => 29.99, 'quantity' => 1]];

        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Total amount must be positive');

        $this->customerService->recordPurchase($customerId, $items, -10.0);
    }

    public function testGetCustomerSpendingHistory(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $items1 = [['name' => 'Product A', 'price' => 29.99, 'quantity' => 1]];
        $items2 = [['name' => 'Product B', 'price' => 15.50, 'quantity' => 2]];

        $this->customerService->recordPurchase($customerId, $items1, 29.99);
        $this->customerService->recordPurchase($customerId, $items2, 31.00);

        $history = $this->customerService->getCustomerSpendingHistory($customerId);

        $this->assertCount(2, $history);
        $this->assertEquals(31.00, $history[0]['amount']); // Most recent first
        $this->assertEquals(29.99, $history[1]['amount']);
    }

    public function testGetCustomerSpendingHistoryForCustomerWithoutOrders(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $history = $this->customerService->getCustomerSpendingHistory($customerId);

        $this->assertEmpty($history);
    }

    public function testCalculateCustomerLifetimeValue(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $items1 = [['name' => 'Product A', 'price' => 29.99, 'quantity' => 1]];
        $items2 = [['name' => 'Product B', 'price' => 15.50, 'quantity' => 2]];

        $this->customerService->recordPurchase($customerId, $items1, 29.99);
        $this->customerService->recordPurchase($customerId, $items2, 31.00);

        $lifetimeValue = $this->customerService->calculateCustomerLifetimeValue($customerId);

        $this->assertEqualsWithDelta(60.99, $lifetimeValue, 0.01);
    }

    public function testCalculateCustomerLifetimeValueForCustomerWithoutOrders(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $lifetimeValue = $this->customerService->calculateCustomerLifetimeValue($customerId);

        $this->assertEquals(0.0, $lifetimeValue);
    }

    public function testGetCustomerProfile(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $this->customerService->updateContactInformation($customerId, 'Johnny', 'Doe', '+1234567890');
        $this->customerService->addCustomerAddress($customerId, '123 Main St', 'New York', '10001', 'USA');
        $this->customerService->recordPurchase($customerId, [['name' => 'Product A', 'price' => 29.99]], 29.99);

        $profile = $this->customerService->getCustomerProfile($customerId);

        $this->assertArrayHasKey('personal', $profile);
        $this->assertArrayHasKey('addresses', $profile);
        $this->assertArrayHasKey('marketing', $profile);
        $this->assertArrayHasKey('orderHistory', $profile);
        $this->assertArrayHasKey('lifetimeValue', $profile);

        $this->assertEquals('Johnny', $profile['personal']['firstName']);
        $this->assertEquals('john.doe@example.com', $profile['personal']['email']);
        $this->assertCount(1, $profile['addresses']);
        $this->assertCount(1, $profile['orderHistory']);
        $this->assertEquals(29.99, $profile['lifetimeValue']);
    }

    public function testGetCustomerProfileForNonExistentCustomer(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Customer not found');

        $this->customerService->getCustomerProfile(999);
    }

    public function testMethodsForNonExistentCustomer(): void
    {
        $nonExistentId = 999;

        $this->expectException(\InvalidArgumentException::class);
        $this->customerService->updateContactInformation($nonExistentId, 'John', 'Doe', '+1234567890');
    }

    public function testDefaultMarketingPreferencesOnRegistration(): void
    {
        $customerId = $this->customerService->registerCustomer(
            'john.doe@example.com',
            'password123',
            'John',
            'Doe'
        );

        $profile = $this->customerService->getCustomerProfile($customerId);
        $marketing = $profile['marketing'];

        $this->assertTrue($marketing['emailMarketing']);
        $this->assertFalse($marketing['smsMarketing']);
        $this->assertTrue($marketing['pushNotifications']);
        $this->assertEquals(['email'], $marketing['preferredChannels']);
    }
}
