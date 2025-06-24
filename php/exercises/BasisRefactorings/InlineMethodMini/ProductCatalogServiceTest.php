<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\InlineMethodMini;

use PHPUnit\Framework\TestCase;

final class ProductCatalogServiceTest extends TestCase
{
    private ProductCatalogService $service;
    
    protected function setUp(): void
    {
        $this->service = new ProductCatalogService();
    }
    
    public function testGetAvailableProductsReturnsOnlyProductsWithStock(): void
    {
        $availableProducts = $this->service->getAvailableProducts();
        
        $this->assertCount(4, $availableProducts);
        $this->assertArrayHasKey('laptop-001', $availableProducts);
        $this->assertArrayHasKey('tablet-003', $availableProducts);
        $this->assertArrayHasKey('monitor-004', $availableProducts);
        $this->assertArrayHasKey('keyboard-005', $availableProducts);
        $this->assertArrayNotHasKey('phone-002', $availableProducts);
    }
    
    public function testGetAvailableProductsReturnsCorrectProductData(): void
    {
        $availableProducts = $this->service->getAvailableProducts();
        
        $this->assertEquals('Business Laptop', $availableProducts['laptop-001']['name']);
        $this->assertEquals(15, $availableProducts['laptop-001']['stock']);
        $this->assertEquals(899.99, $availableProducts['laptop-001']['price']);
    }
    
    public function testGetProductRecommendationsFiltersAvailableProductsByCategory(): void
    {
        $laptopRecommendations = $this->service->getProductRecommendations('laptop');
        
        $this->assertCount(1, $laptopRecommendations);
        $this->assertEquals('laptop-001', $laptopRecommendations[0]['id']);
        $this->assertEquals('Business Laptop', $laptopRecommendations[0]['name']);
        $this->assertEquals(899.99, $laptopRecommendations[0]['price']);
    }
    
    public function testGetProductRecommendationsExcludesOutOfStockProducts(): void
    {
        $phoneRecommendations = $this->service->getProductRecommendations('phone');
        
        $this->assertCount(0, $phoneRecommendations);
    }
    
    public function testGetProductRecommendationsReturnsMultipleMatchingProducts(): void
    {
        $keyboardRecommendations = $this->service->getProductRecommendations('keyboard');
        
        $this->assertCount(1, $keyboardRecommendations);
        $this->assertEquals('keyboard-005', $keyboardRecommendations[0]['id']);
    }
    
    public function testGetProductRecommendationsReturnsEmptyArrayForUnknownCategory(): void
    {
        $unknownRecommendations = $this->service->getProductRecommendations('unknown');
        
        $this->assertCount(0, $unknownRecommendations);
    }
    
    public function testCanAddToCartReturnsTrueForAvailableProductWithSufficientStock(): void
    {
        $canAdd = $this->service->canAddToCart('laptop-001', 5);
        
        $this->assertTrue($canAdd);
    }
    
    public function testCanAddToCartReturnsFalseForUnavailableProduct(): void
    {
        $canAdd = $this->service->canAddToCart('phone-002', 1);
        
        $this->assertFalse($canAdd);
    }
    
    public function testCanAddToCartReturnsFalseForInsufficientStock(): void
    {
        $canAdd = $this->service->canAddToCart('monitor-004', 5);
        
        $this->assertFalse($canAdd);
    }
    
    public function testCanAddToCartReturnsFalseForNonexistentProduct(): void
    {
        $canAdd = $this->service->canAddToCart('nonexistent-999', 1);
        
        $this->assertFalse($canAdd);
    }
    
    public function testCanAddToCartReturnsTrueForExactStockAmount(): void
    {
        $canAdd = $this->service->canAddToCart('monitor-004', 3);
        
        $this->assertTrue($canAdd);
    }
    
    public function testGetProductDetailsReturnsCorrectDataForExistingProduct(): void
    {
        $productDetails = $this->service->getProductDetails('tablet-003');
        
        $this->assertIsArray($productDetails);
        $this->assertEquals('Tablet Air', $productDetails['name']);
        $this->assertEquals(8, $productDetails['stock']);
        $this->assertEquals(399.99, $productDetails['price']);
    }
    
    public function testGetProductDetailsReturnsNullForNonexistentProduct(): void
    {
        $productDetails = $this->service->getProductDetails('nonexistent-999');
        
        $this->assertNull($productDetails);
    }
    
    public function testGetProductDetailsWorksForOutOfStockProduct(): void
    {
        $productDetails = $this->service->getProductDetails('phone-002');
        
        $this->assertIsArray($productDetails);
        $this->assertEquals('Smartphone Pro', $productDetails['name']);
        $this->assertEquals(0, $productDetails['stock']);
        $this->assertEquals(699.99, $productDetails['price']);
    }
}