import { Order } from './Order';
import { Product } from './Product';

interface TotalCalculation {
  subtotal: number;
  discount_rate: number;
  discount_amount: number;
  subtotal_after_discount: number;
  tax_rate: number;
  tax_amount: number;
  shipping_cost: number;
  total: number;
  weight: number;
}

/**
 * OrderCalculator demonstrates Feature Envy code smell
 *
 * This class shows "Feature Envy" by having methods that use data and methods
 * from other objects (Order, Customer, Product) more than their own data.
 * The business logic should be moved closer to the data it operates on.
 */
export class OrderCalculator {
  // This class has minimal state of its own
  private readonly taxRates: Record<string, number> = {
    standard: 0.2,
    premium: 0.15,
    vip: 0.1,
  };

  private readonly shippingRates: Record<string, number> = {
    standard: 5.99,
    express: 12.99,
  };

  /**
   * Feature Envy: This method uses mostly Customer data
   * Should be moved to Customer class
   */
  calculateCustomerDiscount(order: Order): number {
    const customer = order.getCustomer();
    const customerType = customer.getType();
    const loyaltyYears = customer.getLoyaltyYears();

    // Complex customer-specific discount logic
    if (customerType === 'vip') {
      return 0.15 + Math.min(loyaltyYears * 0.01, 0.1); // Up to 25% for VIP
    }

    if (customerType === 'premium') {
      return 0.1 + Math.min(loyaltyYears * 0.005, 0.05); // Up to 15% for Premium
    }

    if (customerType === 'standard') {
      if (loyaltyYears >= 5) {
        return 0.05; // 5% for loyal standard customers
      }
      if (loyaltyYears >= 2) {
        return 0.02; // 2% for somewhat loyal customers
      }
    }

    return 0.0; // No discount for new standard customers
  }

  /**
   * Feature Envy: This method uses mostly Product data
   * Should be moved to Product class
   */
  calculateProductShippingCost(product: Product, quantity: number): number {
    const weight = product.getWeight();
    const isFragile = product.isFragile();
    const category = product.getCategory();

    let baseCost = weight * quantity * 0.5;

    // Category-specific shipping costs
    if (category === 'electronics') {
      baseCost *= 1.2; // Electronics have higher shipping costs
    } else if (category === 'books') {
      baseCost *= 0.8; // Books have lower shipping costs
    } else if (category === 'furniture') {
      baseCost *= 2.0; // Furniture is expensive to ship
    }

    // Fragile items cost more to ship
    if (isFragile) {
      baseCost *= 1.5;
    }

    return Math.round(baseCost * 100) / 100;
  }

  /**
   * Feature Envy: This method uses mostly Order data
   * Should be moved to Order class
   */
  calculateOrderSubtotal(order: Order): number {
    let subtotal = 0.0;
    const items = order.getItems();

    for (const item of items) {
      const product = item.product;
      const quantity = item.quantity;
      const productPrice = product.getPrice();

      subtotal += productPrice * quantity;
    }

    return Math.round(subtotal * 100) / 100;
  }

  /**
   * Feature Envy: This method uses mostly Order and Customer data
   * Could be moved to Order class
   */
  calculateOrderWeight(order: Order): number {
    let totalWeight = 0.0;
    const items = order.getItems();

    for (const item of items) {
      const product = item.product;
      const quantity = item.quantity;
      const productWeight = product.getWeight();

      totalWeight += productWeight * quantity;
    }

    return Math.round(totalWeight * 100) / 100;
  }

  /**
   * Feature Envy: This method mostly uses data from Customer (via Order)
   * Should be moved to Customer class
   */
  calculateTaxRate(order: Order): number {
    const customerType = order.getCustomer().getType();

    return (this.taxRates[customerType] || this.taxRates['standard']) as number;
  }

  /**
   * Feature Envy: Uses Order data and shipping logic
   * Could be moved to Order class
   */
  calculateShippingCost(order: Order): number {
    let totalShippingCost = 0.0;
    const isExpress = order.isExpress();
    const items = order.getItems();

    // Base shipping cost
    const baseRate = isExpress
      ? this.shippingRates['express']
      : this.shippingRates['standard'];
    totalShippingCost += baseRate || 0;

    // Add per-product shipping costs
    for (const item of items) {
      const product = item.product;
      const quantity = item.quantity;

      const productShippingCost = this.calculateProductShippingCost(
        product,
        quantity
      );
      totalShippingCost += productShippingCost;
    }

    return Math.round(totalShippingCost * 100) / 100;
  }

  /**
   * Main calculation method - coordinates other calculations
   * This method should remain in OrderCalculator as it coordinates everything
   */
  calculateTotal(order: Order): TotalCalculation {
    const subtotal = this.calculateOrderSubtotal(order);
    const discount = this.calculateCustomerDiscount(order);
    const discountAmount = subtotal * discount;
    const subtotalAfterDiscount = subtotal - discountAmount;

    const taxRate = this.calculateTaxRate(order);
    const taxAmount = subtotalAfterDiscount * taxRate;

    const shippingCost = this.calculateShippingCost(order);

    const total = subtotalAfterDiscount + taxAmount + shippingCost;

    return {
      subtotal,
      discount_rate: discount,
      discount_amount: Math.round(discountAmount * 100) / 100,
      subtotal_after_discount: Math.round(subtotalAfterDiscount * 100) / 100,
      tax_rate: taxRate,
      tax_amount: Math.round(taxAmount * 100) / 100,
      shipping_cost: shippingCost,
      total: Math.round(total * 100) / 100,
      weight: this.calculateOrderWeight(order),
    };
  }

  /**
   * Feature Envy: Uses mostly Customer data
   * Should be moved to Customer class
   */
  isEligibleForFreeShipping(order: Order): boolean {
    const customer = order.getCustomer();
    const customerType = customer.getType();
    const subtotal = this.calculateOrderSubtotal(order);

    // VIP customers get free shipping on orders over 50
    if (customerType === 'vip' && subtotal >= 50.0) {
      return true;
    }

    // Premium customers get free shipping on orders over 75
    if (customerType === 'premium' && subtotal >= 75.0) {
      return true;
    }

    // Standard customers get free shipping on orders over 100
    if (customerType === 'standard' && subtotal >= 100.0) {
      return true;
    }

    return false;
  }

  /**
   * Feature Envy: Uses mostly Product data
   * Should be moved to Product class
   */
  requiresSpecialHandling(product: Product): boolean {
    return (
      product.isFragile() ||
      product.getWeight() > 20.0 ||
      product.getCategory() === 'electronics'
    );
  }

  /**
   * Feature Envy: Uses mostly Order and Product data
   * Could be moved to Order class
   */
  hasSpecialHandlingItems(order: Order): boolean {
    const items = order.getItems();

    for (const item of items) {
      const product = item.product;
      if (this.requiresSpecialHandling(product)) {
        return true;
      }
    }

    return false;
  }

  /**
   * Feature Envy: Uses mostly Customer data (via Order)
   * Should be moved to Customer class
   */
  getCustomerPriorityLevel(order: Order): string {
    const customer = order.getCustomer();
    const customerType = customer.getType();
    const loyaltyYears = customer.getLoyaltyYears();

    if (customerType === 'vip') {
      return 'high';
    }

    if (customerType === 'premium') {
      return 'medium';
    }

    if (customerType === 'standard' && loyaltyYears >= 5) {
      return 'medium';
    }

    return 'low';
  }
}
