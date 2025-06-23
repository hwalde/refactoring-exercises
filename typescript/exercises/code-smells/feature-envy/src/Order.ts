import { Customer } from './Customer';
import { Product } from './Product';

export interface OrderItem {
  product: Product;
  quantity: number;
}

export class Order {
  private status: string = 'pending';
  private readonly orderDate: string;

  constructor(
    private readonly id: string,
    private readonly customer: Customer,
    private readonly items: OrderItem[],
    private readonly shippingAddress: string,
    private readonly express: boolean = false
  ) {
    this.orderDate = new Date().toISOString();
  }

  getId(): string {
    return this.id;
  }

  getCustomer(): Customer {
    return this.customer;
  }

  getItems(): OrderItem[] {
    return this.items;
  }

  getStatus(): string {
    return this.status;
  }

  getShippingAddress(): string {
    return this.shippingAddress;
  }

  getOrderDate(): string {
    return this.orderDate;
  }

  isExpress(): boolean {
    return this.express;
  }

  setStatus(status: string): void {
    this.status = status;
  }

  addItem(product: Product, quantity: number): void {
    this.items.push({ product, quantity });
  }
}
