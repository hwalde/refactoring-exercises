<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\LongMethod;

use PHPUnit\Framework\TestCase;

class OrderProcessorTest extends TestCase
{
    private OrderProcessor $processor;

    protected function setUp(): void
    {
        $this->processor = new OrderProcessor();
    }

    public function testProcessSimpleOrder(): void
    {
        $orderData = [
            'customer_id' => 'cust_123',
            'items' => [
                [
                    'product_id' => 'prod_1',
                    'quantity' => 2,
                    'price' => 25.0,
                ],
                [
                    'product_id' => 'prod_2',
                    'quantity' => 1,
                    'price' => 50.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'DE',
                'city' => 'Berlin',
                'zip' => '10115',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        $this->assertIsArray($result);
        $this->assertArrayHasKey('id', $result);
        $this->assertEquals('cust_123', $result['customer_id']);
        $this->assertEquals(100.0, $result['subtotal']);
        $this->assertEquals(0.0, $result['discount']); // No discount for 100.0
        $this->assertEquals(19.0, $result['tax']); // 19% of 100.0
        $this->assertEquals(119.0, $result['total']);
        $this->assertEquals('confirmed', $result['status']);
    }

    public function testProcessOrderWithDiscount(): void
    {
        $orderData = [
            'customer_id' => 'cust_456',
            'items' => [
                [
                    'product_id' => 'prod_3',
                    'quantity' => 1,
                    'price' => 150.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'DE',
                'city' => 'Munich',
                'zip' => '80331',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        $this->assertEquals(150.0, $result['subtotal']);
        $this->assertEquals(15.0, $result['discount']); // 10% discount for orders > 100
        $this->assertEquals(25.65, $result['tax']); // 19% of (150 - 15)
        $this->assertEquals(160.65, $result['total']);
    }

    public function testProcessPremiumCustomerOrder(): void
    {
        $orderData = [
            'customer_id' => 'cust_premium',
            'customer_type' => 'premium',
            'items' => [
                [
                    'product_id' => 'prod_4',
                    'quantity' => 1,
                    'price' => 200.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'FR',
                'city' => 'Paris',
                'zip' => '75001',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        $this->assertEquals(200.0, $result['subtotal']);
        $this->assertEquals(30.0, $result['discount']); // 10% + 5% premium discount
        $this->assertEquals(34.0, $result['tax']); // 20% FR tax of (200 - 30)
        $this->assertEquals(204.0, $result['total']);
    }

    public function testProcessOrderWithCoupon(): void
    {
        $orderData = [
            'customer_id' => 'cust_789',
            'coupon_code' => 'SAVE20',
            'items' => [
                [
                    'product_id' => 'prod_5',
                    'quantity' => 1,
                    'price' => 100.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'US',
                'city' => 'New York',
                'zip' => '10001',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        $this->assertEquals(100.0, $result['subtotal']);
        $this->assertEquals(20.0, $result['discount']); // 20% coupon discount
        $this->assertEquals(6.4, $result['tax']); // 8% US tax of (100 - 20)
        $this->assertEquals(86.4, $result['total']);
    }

    public function testOrderStorageAndNotifications(): void
    {
        $orderData = [
            'customer_id' => 'cust_notify',
            'items' => [
                [
                    'product_id' => 'prod_6',
                    'quantity' => 1,
                    'price' => 50.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'DE',
                'city' => 'Hamburg',
                'zip' => '20095',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        // Check order is stored
        $orders = $this->processor->getOrders();
        $this->assertArrayHasKey($result['id'], $orders);
        $this->assertEquals($result, $orders[$result['id']]);

        // Check customer notification
        $notifications = $this->processor->getNotifications();
        $this->assertCount(1, $notifications);
        $this->assertEquals('order_confirmation', $notifications[0]['type']);
        $this->assertEquals('cust_notify', $notifications[0]['customer_id']);
        $this->assertEquals($result['id'], $notifications[0]['order_id']);
    }

    public function testHighValueOrderNotification(): void
    {
        $orderData = [
            'customer_id' => 'cust_big_spender',
            'items' => [
                [
                    'product_id' => 'prod_expensive',
                    'quantity' => 1,
                    'price' => 600.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'DE',
                'city' => 'Frankfurt',
                'zip' => '60311',
            ],
        ];

        $this->processor->processOrder($orderData);

        $notifications = $this->processor->getNotifications();
        $this->assertCount(2, $notifications); // Customer + Admin notification
        
        $adminNotification = array_filter($notifications, fn($n) => $n['type'] === 'high_value_order');
        $this->assertCount(1, $adminNotification);
    }

    public function testValidationErrors(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Customer ID is required');

        $this->processor->processOrder([]);
    }

    public function testItemValidation(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->expectExceptionMessage('Order must contain items');

        $this->processor->processOrder([
            'customer_id' => 'cust_123',
            'items' => [],
            'shipping_address' => ['country' => 'DE'],
        ]);
    }

    public function testMaximumDiscountCap(): void
    {
        $orderData = [
            'customer_id' => 'cust_max_discount',
            'customer_type' => 'premium',
            'coupon_code' => 'SAVE20',
            'items' => [
                [
                    'product_id' => 'prod_7',
                    'quantity' => 1,
                    'price' => 200.0,
                ],
            ],
            'shipping_address' => [
                'country' => 'DE',
                'city' => 'Berlin',
                'zip' => '10115',
            ],
        ];

        $result = $this->processor->processOrder($orderData);

        // Total discount would be 10% + 5% + 20% = 35%, but let's check it's capped
        $this->assertEquals(200.0, $result['subtotal']);
        $this->assertEquals(70.0, $result['discount']); // 35% of 200 (10% + 5% + 20%)
        $this->assertLessThanOrEqual(100.0, $result['discount']); // Max 50% of subtotal
    }
}