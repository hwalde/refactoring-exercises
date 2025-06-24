import { ProductCatalogService } from '../src/ProductCatalogService';

describe('ProductCatalogService', () => {
  let service: ProductCatalogService;

  beforeEach(() => {
    service = new ProductCatalogService();
  });

  describe('getAvailableProducts', () => {
    test('returns only products with stock', () => {
      const availableProducts = service.getAvailableProducts();

      expect(Object.keys(availableProducts)).toHaveLength(4);
      expect(availableProducts).toHaveProperty('laptop-001');
      expect(availableProducts).toHaveProperty('tablet-003');
      expect(availableProducts).toHaveProperty('monitor-004');
      expect(availableProducts).toHaveProperty('keyboard-005');
      expect(availableProducts).not.toHaveProperty('phone-002');
    });

    test('returns correct product data', () => {
      const availableProducts = service.getAvailableProducts();

      expect(availableProducts['laptop-001']!.name).toBe('Business Laptop');
      expect(availableProducts['laptop-001']!.stock).toBe(15);
      expect(availableProducts['laptop-001']!.price).toBe(899.99);
    });
  });

  describe('getProductRecommendations', () => {
    test('filters available products by category', () => {
      const laptopRecommendations = service.getProductRecommendations('laptop');

      expect(laptopRecommendations).toHaveLength(1);
      expect(laptopRecommendations[0]!.id).toBe('laptop-001');
      expect(laptopRecommendations[0]!.name).toBe('Business Laptop');
      expect(laptopRecommendations[0]!.price).toBe(899.99);
    });

    test('excludes out of stock products', () => {
      const phoneRecommendations = service.getProductRecommendations('phone');

      expect(phoneRecommendations).toHaveLength(0);
    });

    test('returns multiple matching products', () => {
      const keyboardRecommendations =
        service.getProductRecommendations('keyboard');

      expect(keyboardRecommendations).toHaveLength(1);
      expect(keyboardRecommendations[0]!.id).toBe('keyboard-005');
    });

    test('returns empty array for unknown category', () => {
      const unknownRecommendations =
        service.getProductRecommendations('unknown');

      expect(unknownRecommendations).toHaveLength(0);
    });
  });

  describe('canAddToCart', () => {
    test('returns true for available product with sufficient stock', () => {
      const canAdd = service.canAddToCart('laptop-001', 5);

      expect(canAdd).toBe(true);
    });

    test('returns false for unavailable product', () => {
      const canAdd = service.canAddToCart('phone-002', 1);

      expect(canAdd).toBe(false);
    });

    test('returns false for insufficient stock', () => {
      const canAdd = service.canAddToCart('monitor-004', 5);

      expect(canAdd).toBe(false);
    });

    test('returns false for nonexistent product', () => {
      const canAdd = service.canAddToCart('nonexistent-999', 1);

      expect(canAdd).toBe(false);
    });

    test('returns true for exact stock amount', () => {
      const canAdd = service.canAddToCart('monitor-004', 3);

      expect(canAdd).toBe(true);
    });
  });

  describe('getProductDetails', () => {
    test('returns correct data for existing product', () => {
      const productDetails = service.getProductDetails('tablet-003');

      expect(productDetails).not.toBeNull();
      expect(productDetails!.name).toBe('Tablet Air');
      expect(productDetails!.stock).toBe(8);
      expect(productDetails!.price).toBe(399.99);
    });

    test('returns null for nonexistent product', () => {
      const productDetails = service.getProductDetails('nonexistent-999');

      expect(productDetails).toBeNull();
    });

    test('works for out of stock product', () => {
      const productDetails = service.getProductDetails('phone-002');

      expect(productDetails).not.toBeNull();
      expect(productDetails!.name).toBe('Smartphone Pro');
      expect(productDetails!.stock).toBe(0);
      expect(productDetails!.price).toBe(699.99);
    });
  });
});
