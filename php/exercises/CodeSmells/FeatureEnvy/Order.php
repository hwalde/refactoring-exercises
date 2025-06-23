<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\FeatureEnvy;

class Order
{
    private string $id;
    private Customer $customer;
    private array $items; // array of ['product' => Product, 'quantity' => int]
    private string $status;
    private string $shippingAddress;
    private string $orderDate;
    private bool $isExpress;

    public function __construct(
        string $id,
        Customer $customer,
        array $items,
        string $shippingAddress,
        bool $isExpress = false
    ) {
        $this->id = $id;
        $this->customer = $customer;
        $this->items = $items;
        $this->status = 'pending';
        $this->shippingAddress = $shippingAddress;
        $this->orderDate = date('Y-m-d H:i:s');
        $this->isExpress = $isExpress;
    }

    public function getId(): string
    {
        return $this->id;
    }

    public function getCustomer(): Customer
    {
        return $this->customer;
    }

    public function getItems(): array
    {
        return $this->items;
    }

    public function getStatus(): string
    {
        return $this->status;
    }

    public function getShippingAddress(): string
    {
        return $this->shippingAddress;
    }

    public function getOrderDate(): string
    {
        return $this->orderDate;
    }

    public function isExpress(): bool
    {
        return $this->isExpress;
    }

    public function setStatus(string $status): void
    {
        $this->status = $status;
    }

    public function addItem(Product $product, int $quantity): void
    {
        $this->items[] = ['product' => $product, 'quantity' => $quantity];
    }
}