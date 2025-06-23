<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\PrimitiveObsession;

class InvoiceGenerator
{
    private array $invoices = [];
    private int $nextInvoiceNumber = 1;

    public function createInvoice(
        string $customerId,
        string $customerEmail,
        array $items,
        string $currency = 'EUR'
    ): array {
        if (empty($customerId)) {
            throw new \InvalidArgumentException('Customer ID cannot be empty');
        }

        if (!filter_var($customerEmail, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Invalid email format');
        }

        if (empty($items)) {
            throw new \InvalidArgumentException('Invoice must have at least one item');
        }

        $invoiceId = 'INV-' . str_pad((string)$this->nextInvoiceNumber, 6, '0', STR_PAD_LEFT);
        $this->nextInvoiceNumber++;

        $totalAmount = 0.0;
        $processedItems = [];

        foreach ($items as $item) {
            if (!isset($item['name']) || !isset($item['price']) || !isset($item['quantity'])) {
                throw new \InvalidArgumentException('Each item must have name, price, and quantity');
            }

            if ($item['price'] < 0) {
                throw new \InvalidArgumentException('Item price cannot be negative');
            }

            if ($item['quantity'] <= 0) {
                throw new \InvalidArgumentException('Item quantity must be positive');
            }

            $itemTotal = $item['price'] * $item['quantity'];
            $totalAmount += $itemTotal;

            $processedItems[] = [
                'name' => $item['name'],
                'price' => round($item['price'], 2),
                'quantity' => $item['quantity'],
                'total' => round($itemTotal, 2)
            ];
        }

        $invoice = [
            'id' => $invoiceId,
            'customerId' => $customerId,
            'customerEmail' => $customerEmail,
            'items' => $processedItems,
            'totalAmount' => round($totalAmount, 2),
            'currency' => $currency,
            'status' => 'draft',
            'createdAt' => date('Y-m-d H:i:s'),
            'dueDate' => date('Y-m-d', strtotime('+30 days'))
        ];

        $this->invoices[$invoiceId] = $invoice;

        return $invoice;
    }

    public function updateInvoiceStatus(string $invoiceId, string $newStatus): void
    {
        if (!isset($this->invoices[$invoiceId])) {
            throw new \InvalidArgumentException('Invoice not found');
        }

        $allowedStatuses = ['draft', 'sent', 'paid', 'overdue', 'cancelled'];
        if (!in_array($newStatus, $allowedStatuses)) {
            throw new \InvalidArgumentException('Invalid status');
        }

        $currentStatus = $this->invoices[$invoiceId]['status'];

        $validTransitions = [
            'draft' => ['sent', 'cancelled'],
            'sent' => ['paid', 'overdue', 'cancelled'],
            'paid' => [],
            'overdue' => ['paid', 'cancelled'],
            'cancelled' => []
        ];

        if (!in_array($newStatus, $validTransitions[$currentStatus])) {
            throw new \InvalidArgumentException("Cannot transition from {$currentStatus} to {$newStatus}");
        }

        $this->invoices[$invoiceId]['status'] = $newStatus;
    }

    public function getInvoice(string $invoiceId): ?array
    {
        return $this->invoices[$invoiceId] ?? null;
    }

    public function getInvoicesByCustomer(string $customerId): array
    {
        $customerInvoices = [];
        foreach ($this->invoices as $invoice) {
            if ($invoice['customerId'] === $customerId) {
                $customerInvoices[] = $invoice;
            }
        }
        return $customerInvoices;
    }

    public function calculateTotalRevenue(string $currency = 'EUR'): float
    {
        $total = 0.0;
        foreach ($this->invoices as $invoice) {
            if ($invoice['currency'] === $currency && $invoice['status'] === 'paid') {
                $total += $invoice['totalAmount'];
            }
        }
        return round($total, 2);
    }

    public function addDiscountToInvoice(string $invoiceId, float $discountPercentage): void
    {
        if (!isset($this->invoices[$invoiceId])) {
            throw new \InvalidArgumentException('Invoice not found');
        }

        if ($discountPercentage < 0 || $discountPercentage > 100) {
            throw new \InvalidArgumentException('Discount percentage must be between 0 and 100');
        }

        if ($this->invoices[$invoiceId]['status'] !== 'draft') {
            throw new \InvalidArgumentException('Can only apply discount to draft invoices');
        }

        $discountMultiplier = 1 - ($discountPercentage / 100);
        $originalAmount = $this->invoices[$invoiceId]['totalAmount'];
        $discountedAmount = $originalAmount * $discountMultiplier;

        $this->invoices[$invoiceId]['totalAmount'] = round($discountedAmount, 2);
        $this->invoices[$invoiceId]['discountPercentage'] = $discountPercentage;
    }

    public function sendInvoiceByEmail(string $invoiceId, string $fromEmail): bool
    {
        if (!isset($this->invoices[$invoiceId])) {
            throw new \InvalidArgumentException('Invoice not found');
        }

        if (!filter_var($fromEmail, FILTER_VALIDATE_EMAIL)) {
            throw new \InvalidArgumentException('Invalid sender email format');
        }

        $invoice = $this->invoices[$invoiceId];
        if ($invoice['status'] !== 'draft') {
            throw new \InvalidArgumentException('Can only send draft invoices');
        }

        $this->invoices[$invoiceId]['status'] = 'sent';
        $this->invoices[$invoiceId]['sentAt'] = date('Y-m-d H:i:s');
        $this->invoices[$invoiceId]['sentFrom'] = $fromEmail;

        return true;
    }
}