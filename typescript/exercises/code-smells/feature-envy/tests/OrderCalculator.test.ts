import { OrderCalculator } from '../src/OrderCalculator';
import { Customer } from '../src/Customer';
import { Product } from '../src/Product';
import { Order } from '../src/Order';

describe('OrderCalculator', () => {
  let calculator: OrderCalculator;
  let standardCustomer: Customer;
  let premiumCustomer: Customer;
  let vipCustomer: Customer;
  let book: Product;
  let electronics: Product;
  let furniture: Product;

  beforeEach(() => {
    calculator = new OrderCalculator();

    standardCustomer = new Customer(
      '1',
      'John Doe',
      'john@example.com',
      'standard',
      1
    );
    premiumCustomer = new Customer(
      '2',
      'Jane Smith',
      'jane@example.com',
      'premium',
      3
    );
    vipCustomer = new Customer('3', 'Bob Wilson', 'bob@example.com', 'vip', 5);

    book = new Product('book1', 'Programming Book', 29.99, 'books', 0.5, false);
    electronics = new Product(
      'phone1',
      'Smartphone',
      699.99,
      'electronics',
      0.2,
      true
    );
    furniture = new Product(
      'chair1',
      'Office Chair',
      199.99,
      'furniture',
      15.0,
      false
    );
  });

  describe('Customer Discount Calculations', () => {
    test('should calculate no discount for standard customer', () => {
      const order = new Order('1', standardCustomer, [], 'Address');

      const discount = calculator.calculateCustomerDiscount(order);

      expect(discount).toBe(0.0);
    });

    test('should calculate discount for loyal standard customer', () => {
      const loyalCustomer = new Customer(
        '4',
        'Loyal Customer',
        'loyal@example.com',
        'standard',
        5
      );
      const order = new Order('1', loyalCustomer, [], 'Address');

      const discount = calculator.calculateCustomerDiscount(order);

      expect(discount).toBe(0.05);
    });

    test('should calculate discount for premium customer', () => {
      const order = new Order('1', premiumCustomer, [], 'Address');

      const discount = calculator.calculateCustomerDiscount(order);

      expect(discount).toBe(0.115); // 0.10 + (3 * 0.005)
    });

    test('should calculate discount for VIP customer', () => {
      const order = new Order('1', vipCustomer, [], 'Address');

      const discount = calculator.calculateCustomerDiscount(order);

      expect(discount).toBe(0.2); // 0.15 + (5 * 0.01)
    });
  });

  describe('Product Shipping Cost Calculations', () => {
    test('should calculate shipping cost for book', () => {
      const cost = calculator.calculateProductShippingCost(book, 2);

      // weight(0.5) * quantity(2) * base(0.5) * book_modifier(0.8) = 0.4
      expect(cost).toBe(0.4);
    });

    test('should calculate shipping cost for electronics', () => {
      const cost = calculator.calculateProductShippingCost(electronics, 1);

      // weight(0.2) * quantity(1) * base(0.5) * electronics_modifier(1.2) * fragile_modifier(1.5) = 0.18
      expect(cost).toBe(0.18);
    });

    test('should calculate shipping cost for furniture', () => {
      const cost = calculator.calculateProductShippingCost(furniture, 1);

      // weight(15.0) * quantity(1) * base(0.5) * furniture_modifier(2.0) = 15.0
      expect(cost).toBe(15.0);
    });
  });

  describe('Order Calculations', () => {
    test('should calculate order subtotal', () => {
      const items = [
        { product: book, quantity: 2 },
        { product: electronics, quantity: 1 },
      ];
      const order = new Order('1', standardCustomer, items, 'Address');

      const subtotal = calculator.calculateOrderSubtotal(order);

      // (29.99 * 2) + (699.99 * 1) = 59.98 + 699.99 = 759.97
      expect(subtotal).toBe(759.97);
    });

    test('should calculate order weight', () => {
      const items = [
        { product: book, quantity: 2 },
        { product: furniture, quantity: 1 },
      ];
      const order = new Order('1', standardCustomer, items, 'Address');

      const weight = calculator.calculateOrderWeight(order);

      // (0.5 * 2) + (15.0 * 1) = 1.0 + 15.0 = 16.0
      expect(weight).toBe(16.0);
    });
  });

  describe('Tax Rate Calculations', () => {
    test('should calculate tax rate for standard customer', () => {
      const order = new Order('1', standardCustomer, [], 'Address');

      const taxRate = calculator.calculateTaxRate(order);

      expect(taxRate).toBe(0.2);
    });

    test('should calculate tax rate for premium customer', () => {
      const order = new Order('1', premiumCustomer, [], 'Address');

      const taxRate = calculator.calculateTaxRate(order);

      expect(taxRate).toBe(0.15);
    });

    test('should calculate tax rate for VIP customer', () => {
      const order = new Order('1', vipCustomer, [], 'Address');

      const taxRate = calculator.calculateTaxRate(order);

      expect(taxRate).toBe(0.1);
    });
  });

  describe('Shipping Cost Calculations', () => {
    test('should calculate standard shipping cost', () => {
      const items = [{ product: book, quantity: 1 }];
      const order = new Order('1', standardCustomer, items, 'Address', false);

      const shippingCost = calculator.calculateShippingCost(order);

      // Base rate(5.99) + book shipping(0.5 * 1 * 0.5 * 0.8) = 5.99 + 0.2 = 6.19
      expect(shippingCost).toBe(6.19);
    });

    test('should calculate express shipping cost', () => {
      const items = [{ product: book, quantity: 1 }];
      const order = new Order('1', standardCustomer, items, 'Address', true);

      const shippingCost = calculator.calculateShippingCost(order);

      // Base rate(12.99) + book shipping(0.2) = 13.19
      expect(shippingCost).toBe(13.19);
    });
  });

  describe('Total Calculations', () => {
    test('should calculate total without discount', () => {
      const items = [{ product: book, quantity: 2 }];
      const order = new Order('1', standardCustomer, items, 'Address');

      const result = calculator.calculateTotal(order);

      expect(result.subtotal).toBe(59.98);
      expect(result.discount_rate).toBe(0.0);
      expect(result.discount_amount).toBe(0.0);
      expect(result.subtotal_after_discount).toBe(59.98);
      expect(result.tax_rate).toBe(0.2);
      expect(result.tax_amount).toBe(12.0); // 59.98 * 0.20 rounded
      expect(result.shipping_cost).toBe(6.39); // 5.99 + 0.4
      expect(result.total).toBe(78.37); // 59.98 + 12.0 + 6.39
      expect(result.weight).toBe(1.0);
    });

    test('should calculate total with discount', () => {
      const items = [{ product: book, quantity: 2 }];
      const order = new Order('1', premiumCustomer, items, 'Address');

      const result = calculator.calculateTotal(order);

      expect(result.subtotal).toBe(59.98);
      expect(result.discount_rate).toBe(0.115);
      expect(result.discount_amount).toBe(6.9);
      expect(result.subtotal_after_discount).toBe(53.08);
      expect(result.tax_rate).toBe(0.15);
      expect(result.tax_amount).toBe(7.96);
      expect(result.total).toBe(67.43);
    });
  });

  describe('Free Shipping Eligibility', () => {
    test('should determine standard customer eligible for free shipping', () => {
      const items = [{ product: electronics, quantity: 1 }]; // 699.99 > 100
      const order = new Order('1', standardCustomer, items, 'Address');

      const isEligible = calculator.isEligibleForFreeShipping(order);

      expect(isEligible).toBe(true);
    });

    test('should determine standard customer not eligible for free shipping', () => {
      const items = [{ product: book, quantity: 2 }]; // 59.98 < 100
      const order = new Order('1', standardCustomer, items, 'Address');

      const isEligible = calculator.isEligibleForFreeShipping(order);

      expect(isEligible).toBe(false);
    });

    test('should determine premium customer eligible for free shipping', () => {
      const items = [{ product: furniture, quantity: 1 }]; // 199.99 > 75
      const order = new Order('1', premiumCustomer, items, 'Address');

      const isEligible = calculator.isEligibleForFreeShipping(order);

      expect(isEligible).toBe(true);
    });

    test('should determine VIP customer eligible for free shipping', () => {
      const items = [{ product: book, quantity: 2 }]; // 59.98 > 50
      const order = new Order('1', vipCustomer, items, 'Address');

      const isEligible = calculator.isEligibleForFreeShipping(order);

      expect(isEligible).toBe(true);
    });
  });

  describe('Special Handling', () => {
    test('should require special handling for fragile product', () => {
      const requiresSpecialHandling =
        calculator.requiresSpecialHandling(electronics);

      expect(requiresSpecialHandling).toBe(true); // fragile and electronics
    });

    test('should require special handling for heavy product', () => {
      const heavyProduct = new Product(
        'heavy1',
        'Heavy Item',
        99.99,
        'other',
        25.0,
        false
      );
      const requiresSpecialHandling =
        calculator.requiresSpecialHandling(heavyProduct);

      expect(requiresSpecialHandling).toBe(true); // weight > 20
    });

    test('should not require special handling for normal product', () => {
      const requiresSpecialHandling = calculator.requiresSpecialHandling(book);

      expect(requiresSpecialHandling).toBe(false);
    });

    test('should detect order has special handling items', () => {
      const items = [
        { product: book, quantity: 1 },
        { product: electronics, quantity: 1 }, // fragile
      ];
      const order = new Order('1', standardCustomer, items, 'Address');

      const hasSpecialHandling = calculator.hasSpecialHandlingItems(order);

      expect(hasSpecialHandling).toBe(true);
    });

    test('should detect order has no special handling items', () => {
      const items = [{ product: book, quantity: 2 }];
      const order = new Order('1', standardCustomer, items, 'Address');

      const hasSpecialHandling = calculator.hasSpecialHandlingItems(order);

      expect(hasSpecialHandling).toBe(false);
    });
  });

  describe('Customer Priority Levels', () => {
    test('should get high priority for VIP customer', () => {
      const order = new Order('1', vipCustomer, [], 'Address');

      const priority = calculator.getCustomerPriorityLevel(order);

      expect(priority).toBe('high');
    });

    test('should get medium priority for premium customer', () => {
      const order = new Order('1', premiumCustomer, [], 'Address');

      const priority = calculator.getCustomerPriorityLevel(order);

      expect(priority).toBe('medium');
    });

    test('should get medium priority for loyal standard customer', () => {
      const loyalCustomer = new Customer(
        '5',
        'Loyal Standard',
        'loyal@example.com',
        'standard',
        5
      );
      const order = new Order('1', loyalCustomer, [], 'Address');

      const priority = calculator.getCustomerPriorityLevel(order);

      expect(priority).toBe('medium');
    });

    test('should get low priority for new standard customer', () => {
      const order = new Order('1', standardCustomer, [], 'Address');

      const priority = calculator.getCustomerPriorityLevel(order);

      expect(priority).toBe('low');
    });
  });

  describe('Complete Order Workflow', () => {
    test('should handle complete order workflow', () => {
      const items = [
        { product: book, quantity: 2 },
        { product: electronics, quantity: 1 },
      ];
      const order = new Order('1', vipCustomer, items, 'Address', true);

      // Test various calculations work together
      const total = calculator.calculateTotal(order);
      expect(total.total).toBeGreaterThan(0);

      const isEligible = calculator.isEligibleForFreeShipping(order);
      expect(isEligible).toBe(true); // VIP with high-value order

      const hasSpecialHandling = calculator.hasSpecialHandlingItems(order);
      expect(hasSpecialHandling).toBe(true); // Electronics is fragile

      const priority = calculator.getCustomerPriorityLevel(order);
      expect(priority).toBe('high'); // VIP customer
    });
  });
});
