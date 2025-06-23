<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\FeatureEnvy;

/**
 * OrderCalculator demonstrates Feature Envy code smell
 * 
 * This class shows "Feature Envy" by having methods that use data and methods 
 * from other objects (Order, Customer, Product) more than their own data.
 * The business logic should be moved closer to the data it operates on.
 */
class OrderCalculator
{
    // This class has minimal state of its own
    private array $taxRates = [
        'standard' => 0.20,
        'premium' => 0.15,
        'vip' => 0.10
    ];

    private array $shippingRates = [
        'standard' => 5.99,
        'express' => 12.99
    ];

    /**
     * Feature Envy: This method uses mostly Customer data
     * Should be moved to Customer class
     */
    public function calculateCustomerDiscount(Order $order): float
    {
        $customer = $order->getCustomer();
        $customerType = $customer->getType();
        $loyaltyYears = $customer->getLoyaltyYears();

        // Complex customer-specific discount logic
        if ($customerType === 'vip') {
            return 0.15 + min($loyaltyYears * 0.01, 0.10); // Up to 25% for VIP
        }

        if ($customerType === 'premium') {
            return 0.10 + min($loyaltyYears * 0.005, 0.05); // Up to 15% for Premium
        }

        if ($customerType === 'standard') {
            if ($loyaltyYears >= 5) {
                return 0.05; // 5% for loyal standard customers
            }
            if ($loyaltyYears >= 2) {
                return 0.02; // 2% for somewhat loyal customers
            }
        }

        return 0.0; // No discount for new standard customers
    }

    /**
     * Feature Envy: This method uses mostly Product data
     * Should be moved to Product class
     */
    public function calculateProductShippingCost(Product $product, int $quantity): float
    {
        $weight = $product->getWeight();
        $isFragile = $product->isFragile();
        $category = $product->getCategory();

        $baseCost = $weight * $quantity * 0.5;

        // Category-specific shipping costs
        if ($category === 'electronics') {
            $baseCost *= 1.2; // Electronics have higher shipping costs
        } elseif ($category === 'books') {
            $baseCost *= 0.8; // Books have lower shipping costs
        } elseif ($category === 'furniture') {
            $baseCost *= 2.0; // Furniture is expensive to ship
        }

        // Fragile items cost more to ship
        if ($isFragile) {
            $baseCost *= 1.5;
        }

        return round($baseCost, 2);
    }

    /**
     * Feature Envy: This method uses mostly Order data
     * Should be moved to Order class
     */
    public function calculateOrderSubtotal(Order $order): float
    {
        $subtotal = 0.0;
        $items = $order->getItems();

        foreach ($items as $item) {
            $product = $item['product'];
            $quantity = $item['quantity'];
            $productPrice = $product->getPrice();
            
            $subtotal += $productPrice * $quantity;
        }

        return round($subtotal, 2);
    }

    /**
     * Feature Envy: This method uses mostly Order and Customer data
     * Could be moved to Order class
     */
    public function calculateOrderWeight(Order $order): float
    {
        $totalWeight = 0.0;
        $items = $order->getItems();

        foreach ($items as $item) {
            $product = $item['product'];
            $quantity = $item['quantity'];
            $productWeight = $product->getWeight();
            
            $totalWeight += $productWeight * $quantity;
        }

        return round($totalWeight, 2);
    }

    /**
     * Feature Envy: This method mostly uses data from Customer (via Order)
     * Should be moved to Customer class
     */
    public function calculateTaxRate(Order $order): float
    {
        $customerType = $order->getCustomer()->getType();
        
        return $this->taxRates[$customerType] ?? $this->taxRates['standard'];
    }

    /**
     * Feature Envy: Uses Order data and shipping logic
     * Could be moved to Order class
     */
    public function calculateShippingCost(Order $order): float
    {
        $totalShippingCost = 0.0;
        $isExpress = $order->isExpress();
        $items = $order->getItems();

        // Base shipping cost
        $baseRate = $isExpress ? $this->shippingRates['express'] : $this->shippingRates['standard'];
        $totalShippingCost += $baseRate;

        // Add per-product shipping costs
        foreach ($items as $item) {
            $product = $item['product'];
            $quantity = $item['quantity'];
            
            $productShippingCost = $this->calculateProductShippingCost($product, $quantity);
            $totalShippingCost += $productShippingCost;
        }

        return round($totalShippingCost, 2);
    }

    /**
     * Main calculation method - coordinates other calculations
     * This method should remain in OrderCalculator as it coordinates everything
     */
    public function calculateTotal(Order $order): array
    {
        $subtotal = $this->calculateOrderSubtotal($order);
        $discount = $this->calculateCustomerDiscount($order);
        $discountAmount = $subtotal * $discount;
        $subtotalAfterDiscount = $subtotal - $discountAmount;
        
        $taxRate = $this->calculateTaxRate($order);
        $taxAmount = $subtotalAfterDiscount * $taxRate;
        
        $shippingCost = $this->calculateShippingCost($order);
        
        $total = $subtotalAfterDiscount + $taxAmount + $shippingCost;

        return [
            'subtotal' => $subtotal,
            'discount_rate' => $discount,
            'discount_amount' => round($discountAmount, 2),
            'subtotal_after_discount' => round($subtotalAfterDiscount, 2),
            'tax_rate' => $taxRate,
            'tax_amount' => round($taxAmount, 2),
            'shipping_cost' => $shippingCost,
            'total' => round($total, 2),
            'weight' => $this->calculateOrderWeight($order)
        ];
    }

    /**
     * Feature Envy: Uses mostly Customer data
     * Should be moved to Customer class
     */
    public function isEligibleForFreeShipping(Order $order): bool
    {
        $customer = $order->getCustomer();
        $customerType = $customer->getType();
        $subtotal = $this->calculateOrderSubtotal($order);

        // VIP customers get free shipping on orders over 50
        if ($customerType === 'vip' && $subtotal >= 50.0) {
            return true;
        }

        // Premium customers get free shipping on orders over 75
        if ($customerType === 'premium' && $subtotal >= 75.0) {
            return true;
        }

        // Standard customers get free shipping on orders over 100
        if ($customerType === 'standard' && $subtotal >= 100.0) {
            return true;
        }

        return false;
    }

    /**
     * Feature Envy: Uses mostly Product data
     * Should be moved to Product class
     */
    public function requiresSpecialHandling(Product $product): bool
    {
        return $product->isFragile() || 
               $product->getWeight() > 20.0 || 
               $product->getCategory() === 'electronics';
    }

    /**
     * Feature Envy: Uses mostly Order and Product data
     * Could be moved to Order class
     */
    public function hasSpecialHandlingItems(Order $order): bool
    {
        $items = $order->getItems();

        foreach ($items as $item) {
            $product = $item['product'];
            if ($this->requiresSpecialHandling($product)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Feature Envy: Uses mostly Customer data (via Order)
     * Should be moved to Customer class
     */
    public function getCustomerPriorityLevel(Order $order): string
    {
        $customer = $order->getCustomer();
        $customerType = $customer->getType();
        $loyaltyYears = $customer->getLoyaltyYears();

        if ($customerType === 'vip') {
            return 'high';
        }

        if ($customerType === 'premium') {
            return 'medium';
        }

        if ($customerType === 'standard' && $loyaltyYears >= 5) {
            return 'medium';
        }

        return 'low';
    }
}