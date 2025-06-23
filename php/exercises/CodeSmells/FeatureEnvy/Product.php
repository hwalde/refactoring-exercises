<?php

declare(strict_types=1);

namespace RefactoringExercises\CodeSmells\FeatureEnvy;

class Product
{
    private string $id;
    private string $name;
    private float $price;
    private string $category;
    private float $weight;
    private bool $isFragile;
    private string $manufacturer;

    public function __construct(
        string $id,
        string $name,
        float $price,
        string $category,
        float $weight,
        bool $isFragile = false,
        string $manufacturer = ''
    ) {
        $this->id = $id;
        $this->name = $name;
        $this->price = $price;
        $this->category = $category;
        $this->weight = $weight;
        $this->isFragile = $isFragile;
        $this->manufacturer = $manufacturer;
    }

    public function getId(): string
    {
        return $this->id;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function getPrice(): float
    {
        return $this->price;
    }

    public function getCategory(): string
    {
        return $this->category;
    }

    public function getWeight(): float
    {
        return $this->weight;
    }

    public function isFragile(): bool
    {
        return $this->isFragile;
    }

    public function getManufacturer(): string
    {
        return $this->manufacturer;
    }
}