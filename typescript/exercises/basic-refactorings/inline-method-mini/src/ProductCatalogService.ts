interface Product {
  readonly name: string;
  readonly stock: number;
  readonly price: number;
}

interface ProductRecommendation {
  readonly id: string;
  readonly name: string;
  readonly price: number;
}

export class ProductCatalogService {
  private readonly products: Record<string, Product> = {};

  constructor() {
    this.products = {
      'laptop-001': { name: 'Business Laptop', stock: 15, price: 899.99 },
      'phone-002': { name: 'Smartphone Pro', stock: 0, price: 699.99 },
      'tablet-003': { name: 'Tablet Air', stock: 8, price: 399.99 },
      'monitor-004': { name: '27" Monitor', stock: 3, price: 299.99 },
      'keyboard-005': { name: 'Mechanical Keyboard', stock: 25, price: 129.99 },
    };
  }

  public getAvailableProducts(): Record<string, Product> {
    const availableProducts: Record<string, Product> = {};

    for (const [productId, product] of Object.entries(this.products)) {
      if (this.isProductAvailable(productId)) {
        availableProducts[productId] = product;
      }
    }

    return availableProducts;
  }

  public getProductRecommendations(category: string): ProductRecommendation[] {
    const recommendations: ProductRecommendation[] = [];

    for (const [productId, product] of Object.entries(this.products)) {
      if (productId.includes(category) && this.isProductAvailable(productId)) {
        recommendations.push({
          id: productId,
          name: product.name,
          price: product.price,
        });
      }
    }

    return recommendations;
  }

  public canAddToCart(productId: string, quantity: number): boolean {
    if (!this.isProductAvailable(productId)) {
      return false;
    }

    return this.products[productId]!.stock >= quantity;
  }

  // This is the unnecessary wrapper method that should be inlined
  private isProductAvailable(productId: string): boolean {
    return this.checkProductStock(productId);
  }

  private checkProductStock(productId: string): boolean {
    const product = this.products[productId];
    if (!product) {
      return false;
    }

    return product.stock > 0;
  }

  public getProductDetails(productId: string): Product | null {
    const product = this.products[productId];
    if (!product) {
      return null;
    }

    return product;
  }
}
