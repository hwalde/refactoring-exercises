<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\FeatureEnvy;

use PHPUnit\Framework\TestCase;

class OrderCalculatorTest extends TestCase
{
    private OrderCalculator $calculator;
    private Customer $standardCustomer;
    private Customer $premiumCustomer;
    private Customer $vipCustomer;
    private Product $book;
    private Product $electronics;
    private Product $furniture;

    protected function setUp(): void
    {
        $this->calculator = new OrderCalculator();
        
        $this->standardCustomer = new Customer('1', 'John Doe', 'john@example.com', 'standard', 1);
        $this->premiumCustomer = new Customer('2', 'Jane Smith', 'jane@example.com', 'premium', 3);
        $this->vipCustomer = new Customer('3', 'Bob Wilson', 'bob@example.com', 'vip', 5);
        
        $this->book = new Product('book1', 'Programming Book', 29.99, 'books', 0.5, false);
        $this->electronics = new Product('phone1', 'Smartphone', 699.99, 'electronics', 0.2, true);
        $this->furniture = new Product('chair1', 'Office Chair', 199.99, 'furniture', 15.0, false);
    }

    public function testCalculateCustomerDiscountForStandardCustomer(): void
    {
        $order = new Order('1', $this->standardCustomer, [], 'Address');
        
        $discount = $this->calculator->calculateCustomerDiscount($order);
        
        $this->assertEquals(0.0, $discount);
    }

    public function testCalculateCustomerDiscountForStandardLoyalCustomer(): void
    {
        $loyalCustomer = new Customer('4', 'Loyal Customer', 'loyal@example.com', 'standard', 5);
        $order = new Order('1', $loyalCustomer, [], 'Address');
        
        $discount = $this->calculator->calculateCustomerDiscount($order);
        
        $this->assertEquals(0.05, $discount);
    }

    public function testCalculateCustomerDiscountForPremiumCustomer(): void
    {
        $order = new Order('1', $this->premiumCustomer, [], 'Address');
        
        $discount = $this->calculator->calculateCustomerDiscount($order);
        
        $this->assertEquals(0.115, $discount); // 0.10 + (3 * 0.005)
    }

    public function testCalculateCustomerDiscountForVipCustomer(): void
    {
        $order = new Order('1', $this->vipCustomer, [], 'Address');
        
        $discount = $this->calculator->calculateCustomerDiscount($order);
        
        $this->assertEquals(0.20, $discount); // 0.15 + (5 * 0.01)
    }

    public function testCalculateProductShippingCostForBook(): void
    {
        $cost = $this->calculator->calculateProductShippingCost($this->book, 2);
        
        // weight(0.5) * quantity(2) * base(0.5) * book_modifier(0.8) = 0.4
        $this->assertEquals(0.40, $cost);
    }

    public function testCalculateProductShippingCostForElectronics(): void
    {
        $cost = $this->calculator->calculateProductShippingCost($this->electronics, 1);
        
        // weight(0.2) * quantity(1) * base(0.5) * electronics_modifier(1.2) * fragile_modifier(1.5) = 0.18
        $this->assertEquals(0.18, $cost);
    }

    public function testCalculateProductShippingCostForFurniture(): void
    {
        $cost = $this->calculator->calculateProductShippingCost($this->furniture, 1);
        
        // weight(15.0) * quantity(1) * base(0.5) * furniture_modifier(2.0) = 15.0
        $this->assertEquals(15.0, $cost);
    }

    public function testCalculateOrderSubtotal(): void
    {
        $items = [
            ['product' => $this->book, 'quantity' => 2],
            ['product' => $this->electronics, 'quantity' => 1]
        ];
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $subtotal = $this->calculator->calculateOrderSubtotal($order);
        
        // (29.99 * 2) + (699.99 * 1) = 59.98 + 699.99 = 759.97
        $this->assertEquals(759.97, $subtotal);
    }

    public function testCalculateOrderWeight(): void
    {
        $items = [
            ['product' => $this->book, 'quantity' => 2],
            ['product' => $this->furniture, 'quantity' => 1]
        ];
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $weight = $this->calculator->calculateOrderWeight($order);
        
        // (0.5 * 2) + (15.0 * 1) = 1.0 + 15.0 = 16.0
        $this->assertEquals(16.0, $weight);
    }

    public function testCalculateTaxRateForStandardCustomer(): void
    {
        $order = new Order('1', $this->standardCustomer, [], 'Address');
        
        $taxRate = $this->calculator->calculateTaxRate($order);
        
        $this->assertEquals(0.20, $taxRate);
    }

    public function testCalculateTaxRateForPremiumCustomer(): void
    {
        $order = new Order('1', $this->premiumCustomer, [], 'Address');
        
        $taxRate = $this->calculator->calculateTaxRate($order);
        
        $this->assertEquals(0.15, $taxRate);
    }

    public function testCalculateTaxRateForVipCustomer(): void
    {
        $order = new Order('1', $this->vipCustomer, [], 'Address');
        
        $taxRate = $this->calculator->calculateTaxRate($order);
        
        $this->assertEquals(0.10, $taxRate);
    }

    public function testCalculateShippingCostStandard(): void
    {
        $items = [['product' => $this->book, 'quantity' => 1]];
        $order = new Order('1', $this->standardCustomer, $items, 'Address', false);
        
        $shippingCost = $this->calculator->calculateShippingCost($order);
        
        // Base rate(5.99) + book shipping(0.5 * 1 * 0.5 * 0.8) = 5.99 + 0.2 = 6.19
        $this->assertEquals(6.19, $shippingCost);
    }

    public function testCalculateShippingCostExpress(): void
    {
        $items = [['product' => $this->book, 'quantity' => 1]];
        $order = new Order('1', $this->standardCustomer, $items, 'Address', true);
        
        $shippingCost = $this->calculator->calculateShippingCost($order);
        
        // Base rate(12.99) + book shipping(0.2) = 13.19
        $this->assertEquals(13.19, $shippingCost);
    }

    public function testCalculateTotal(): void
    {
        $items = [['product' => $this->book, 'quantity' => 2]];
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $result = $this->calculator->calculateTotal($order);
        
        $this->assertEquals(59.98, $result['subtotal']);
        $this->assertEquals(0.0, $result['discount_rate']);
        $this->assertEquals(0.0, $result['discount_amount']);
        $this->assertEquals(59.98, $result['subtotal_after_discount']);
        $this->assertEquals(0.20, $result['tax_rate']);
        $this->assertEquals(12.0, $result['tax_amount']); // 59.98 * 0.20 rounded
        $this->assertEquals(6.39, $result['shipping_cost']); // 5.99 + 0.4
        $this->assertEquals(78.37, $result['total']); // 59.98 + 11.996 + 6.39
        $this->assertEquals(1.0, $result['weight']);
    }

    public function testCalculateTotalWithDiscount(): void
    {
        $items = [['product' => $this->book, 'quantity' => 2]];
        $order = new Order('1', $this->premiumCustomer, $items, 'Address');
        
        $result = $this->calculator->calculateTotal($order);
        
        $this->assertEquals(59.98, $result['subtotal']);
        $this->assertEquals(0.115, $result['discount_rate']);
        $this->assertEquals(6.90, $result['discount_amount']);
        $this->assertEquals(53.08, $result['subtotal_after_discount']);
        $this->assertEquals(0.15, $result['tax_rate']);
        $this->assertEquals(7.96, $result['tax_amount']);
        $this->assertEquals(67.43, $result['total']);
    }

    public function testIsEligibleForFreeShippingStandardCustomer(): void
    {
        $items = [['product' => $this->electronics, 'quantity' => 1]]; // 699.99 > 100
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $isEligible = $this->calculator->isEligibleForFreeShipping($order);
        
        $this->assertTrue($isEligible);
    }

    public function testIsEligibleForFreeShippingStandardCustomerNotEligible(): void
    {
        $items = [['product' => $this->book, 'quantity' => 2]]; // 59.98 < 100
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $isEligible = $this->calculator->isEligibleForFreeShipping($order);
        
        $this->assertFalse($isEligible);
    }

    public function testIsEligibleForFreeShippingPremiumCustomer(): void
    {
        $items = [['product' => $this->furniture, 'quantity' => 1]]; // 199.99 > 75
        $order = new Order('1', $this->premiumCustomer, $items, 'Address');
        
        $isEligible = $this->calculator->isEligibleForFreeShipping($order);
        
        $this->assertTrue($isEligible);
    }

    public function testIsEligibleForFreeShippingVipCustomer(): void
    {
        $items = [['product' => $this->book, 'quantity' => 2]]; // 59.98 > 50
        $order = new Order('1', $this->vipCustomer, $items, 'Address');
        
        $isEligible = $this->calculator->isEligibleForFreeShipping($order);
        
        $this->assertTrue($isEligible);
    }

    public function testRequiresSpecialHandlingForFragileProduct(): void
    {
        $requiresSpecialHandling = $this->calculator->requiresSpecialHandling($this->electronics);
        
        $this->assertTrue($requiresSpecialHandling); // fragile and electronics
    }

    public function testRequiresSpecialHandlingForHeavyProduct(): void
    {
        $heavyProduct = new Product('heavy1', 'Heavy Item', 99.99, 'other', 25.0, false);
        $requiresSpecialHandling = $this->calculator->requiresSpecialHandling($heavyProduct);
        
        $this->assertTrue($requiresSpecialHandling); // weight > 20
    }

    public function testRequiresSpecialHandlingForNormalProduct(): void
    {
        $requiresSpecialHandling = $this->calculator->requiresSpecialHandling($this->book);
        
        $this->assertFalse($requiresSpecialHandling);
    }

    public function testHasSpecialHandlingItems(): void
    {
        $items = [
            ['product' => $this->book, 'quantity' => 1],
            ['product' => $this->electronics, 'quantity' => 1] // fragile
        ];
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $hasSpecialHandling = $this->calculator->hasSpecialHandlingItems($order);
        
        $this->assertTrue($hasSpecialHandling);
    }

    public function testHasNoSpecialHandlingItems(): void
    {
        $items = [['product' => $this->book, 'quantity' => 2]];
        $order = new Order('1', $this->standardCustomer, $items, 'Address');
        
        $hasSpecialHandling = $this->calculator->hasSpecialHandlingItems($order);
        
        $this->assertFalse($hasSpecialHandling);
    }

    public function testGetCustomerPriorityLevelForVip(): void
    {
        $order = new Order('1', $this->vipCustomer, [], 'Address');
        
        $priority = $this->calculator->getCustomerPriorityLevel($order);
        
        $this->assertEquals('high', $priority);
    }

    public function testGetCustomerPriorityLevelForPremium(): void
    {
        $order = new Order('1', $this->premiumCustomer, [], 'Address');
        
        $priority = $this->calculator->getCustomerPriorityLevel($order);
        
        $this->assertEquals('medium', $priority);
    }

    public function testGetCustomerPriorityLevelForLoyalStandard(): void
    {
        $loyalCustomer = new Customer('5', 'Loyal Standard', 'loyal@example.com', 'standard', 5);
        $order = new Order('1', $loyalCustomer, [], 'Address');
        
        $priority = $this->calculator->getCustomerPriorityLevel($order);
        
        $this->assertEquals('medium', $priority);
    }

    public function testGetCustomerPriorityLevelForNewStandard(): void
    {
        $order = new Order('1', $this->standardCustomer, [], 'Address');
        
        $priority = $this->calculator->getCustomerPriorityLevel($order);
        
        $this->assertEquals('low', $priority);
    }

    public function testCompleteOrderWorkflow(): void
    {
        $items = [
            ['product' => $this->book, 'quantity' => 2],
            ['product' => $this->electronics, 'quantity' => 1]
        ];
        $order = new Order('1', $this->vipCustomer, $items, 'Address', true);
        
        // Test various calculations work together
        $total = $this->calculator->calculateTotal($order);
        $this->assertGreaterThan(0, $total['total']);
        
        $isEligible = $this->calculator->isEligibleForFreeShipping($order);
        $this->assertTrue($isEligible); // VIP with high-value order
        
        $hasSpecialHandling = $this->calculator->hasSpecialHandlingItems($order);
        $this->assertTrue($hasSpecialHandling); // Electronics is fragile
        
        $priority = $this->calculator->getCustomerPriorityLevel($order);
        $this->assertEquals('high', $priority); // VIP customer
    }
}