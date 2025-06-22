<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\LongMethod;

class OrderProcessor
{
    private array $orders = [];
    private array $notifications = [];

    public function processOrder(array $orderData): array
    {
        // Validation block
        if (empty($orderData['customer_id'])) {
            throw new \InvalidArgumentException('Customer ID is required');
        }
        if (empty($orderData['items']) || !is_array($orderData['items'])) {
            throw new \InvalidArgumentException('Order must contain items');
        }
        foreach ($orderData['items'] as $item) {
            if (empty($item['product_id']) || empty($item['quantity']) || $item['quantity'] <= 0) {
                throw new \InvalidArgumentException('Invalid item data');
            }
            if (empty($item['price']) || $item['price'] <= 0) {
                throw new \InvalidArgumentException('Invalid item price');
            }
        }
        if (empty($orderData['shipping_address'])) {
            throw new \InvalidArgumentException('Shipping address is required');
        }

        // Calculate subtotal
        $subtotal = 0.0;
        foreach ($orderData['items'] as $item) {
            $subtotal += $item['price'] * $item['quantity'];
        }

        // Apply discount logic
        $discount = 0.0;
        if ($subtotal > 100.0) {
            $discount = $subtotal * 0.1; // 10% discount for orders over 100
        }
        if (isset($orderData['customer_type']) && $orderData['customer_type'] === 'premium') {
            $discount += $subtotal * 0.05; // Additional 5% for premium customers
        }
        if (isset($orderData['coupon_code']) && $orderData['coupon_code'] === 'SAVE20') {
            $discount += $subtotal * 0.2; // 20% coupon discount
        }
        // Ensure discount doesn't exceed 50% of subtotal
        if ($discount > $subtotal * 0.5) {
            $discount = $subtotal * 0.5;
        }

        // Calculate tax
        $taxRate = 0.19; // 19% VAT
        if (isset($orderData['shipping_address']['country'])) {
            switch ($orderData['shipping_address']['country']) {
                case 'DE':
                    $taxRate = 0.19;
                    break;
                case 'FR':
                    $taxRate = 0.20;
                    break;
                case 'IT':
                    $taxRate = 0.22;
                    break;
                case 'US':
                    $taxRate = 0.08;
                    break;
                default:
                    $taxRate = 0.19;
            }
        }
        $discountedSubtotal = $subtotal - $discount;
        $tax = $discountedSubtotal * $taxRate;
        $total = $discountedSubtotal + $tax;

        // Create order record
        $orderId = uniqid('order_', true);
        $order = [
            'id' => $orderId,
            'customer_id' => $orderData['customer_id'],
            'items' => $orderData['items'],
            'subtotal' => $subtotal,
            'discount' => $discount,
            'tax' => $tax,
            'total' => $total,
            'shipping_address' => $orderData['shipping_address'],
            'status' => 'confirmed',
            'created_at' => date('Y-m-d H:i:s'),
        ];

        // Save order
        $this->orders[$orderId] = $order;

        // Send notifications
        $customerNotification = [
            'type' => 'order_confirmation',
            'customer_id' => $orderData['customer_id'],
            'order_id' => $orderId,
            'message' => "Your order {$orderId} has been confirmed. Total: €" . number_format($total, 2),
            'sent_at' => date('Y-m-d H:i:s'),
        ];
        $this->notifications[] = $customerNotification;

        if ($total > 500.0) {
            $adminNotification = [
                'type' => 'high_value_order',
                'order_id' => $orderId,
                'total' => $total,
                'message' => "High value order received: €" . number_format($total, 2),
                'sent_at' => date('Y-m-d H:i:s'),
            ];
            $this->notifications[] = $adminNotification;
        }

        return $order;
    }

    public function getOrders(): array
    {
        return $this->orders;
    }

    public function getNotifications(): array
    {
        return $this->notifications;
    }
}