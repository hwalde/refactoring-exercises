<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\InlineMethodMini;

class ProductCatalogService
{
    private array $products = [];
    
    public function __construct()
    {
        $this->products = [
            'laptop-001' => ['name' => 'Business Laptop', 'stock' => 15, 'price' => 899.99],
            'phone-002' => ['name' => 'Smartphone Pro', 'stock' => 0, 'price' => 699.99],
            'tablet-003' => ['name' => 'Tablet Air', 'stock' => 8, 'price' => 399.99],
            'monitor-004' => ['name' => '27" Monitor', 'stock' => 3, 'price' => 299.99],
            'keyboard-005' => ['name' => 'Mechanical Keyboard', 'stock' => 25, 'price' => 129.99],
        ];
    }
    
    public function getAvailableProducts(): array
    {
        $availableProducts = [];
        
        foreach ($this->products as $productId => $product) {
            if ($this->isProductAvailable($productId)) {
                $availableProducts[$productId] = $product;
            }
        }
        
        return $availableProducts;
    }
    
    public function getProductRecommendations(string $category): array
    {
        $recommendations = [];
        
        foreach ($this->products as $productId => $product) {
            if (str_contains($productId, $category) && $this->isProductAvailable($productId)) {
                $recommendations[] = [
                    'id' => $productId,
                    'name' => $product['name'],
                    'price' => $product['price']
                ];
            }
        }
        
        return $recommendations;
    }
    
    public function canAddToCart(string $productId, int $quantity): bool
    {
        if (!$this->isProductAvailable($productId)) {
            return false;
        }
        
        return $this->products[$productId]['stock'] >= $quantity;
    }
    
    // This is the unnecessary wrapper method that should be inlined
    private function isProductAvailable(string $productId): bool
    {
        return $this->checkProductStock($productId);
    }
    
    private function checkProductStock(string $productId): bool
    {
        if (!isset($this->products[$productId])) {
            return false;
        }
        
        return $this->products[$productId]['stock'] > 0;
    }
    
    public function getProductDetails(string $productId): ?array
    {
        if (!isset($this->products[$productId])) {
            return null;
        }
        
        return $this->products[$productId];
    }
}