export type CustomerStatus = 'active' | 'inactive' | 'suspended';
export type MarketingChannel = 'email' | 'sms' | 'push' | 'mail';
export type OrderStatus = 'pending' | 'completed' | 'cancelled';

export interface Customer {
  readonly id: number;
  readonly email: string;
  readonly password: string;
  readonly firstName: string;
  readonly lastName: string;
  readonly status: CustomerStatus;
  readonly createdAt: Date;
  readonly lastLogin: Date | null;
  readonly phone?: string;
}

export interface Address {
  readonly id: number;
  readonly street: string;
  readonly city: string;
  readonly zipCode: string;
  readonly country: string;
  readonly isDefault: boolean;
}

export interface MarketingPreferences {
  readonly emailMarketing: boolean;
  readonly smsMarketing: boolean;
  readonly pushNotifications: boolean;
  readonly preferredChannels: readonly MarketingChannel[];
}

export interface OrderItem {
  readonly name: string;
  readonly price: number;
  readonly quantity: number;
}

export interface Order {
  readonly id: number;
  readonly items: readonly OrderItem[];
  readonly totalAmount: number;
  readonly orderDate: Date;
  readonly status: OrderStatus;
}

export interface SpendingHistoryEntry {
  readonly orderId: number;
  readonly amount: number;
  readonly date: Date;
  readonly itemCount: number;
}

export interface CustomerProfile {
  readonly personal: {
    readonly id: number;
    readonly firstName: string;
    readonly lastName: string;
    readonly email: string;
    readonly phone: string | null;
    readonly status: CustomerStatus;
  };
  readonly addresses: readonly Address[];
  readonly marketing: MarketingPreferences | null;
  readonly orderHistory: readonly SpendingHistoryEntry[];
  readonly lifetimeValue: number;
}

export class CustomerService {
  private customers: Map<number, Customer> = new Map();
  private loginAttempts: Map<string, Date[]> = new Map();
  private marketingPreferences: Map<number, MarketingPreferences> = new Map();
  private orderHistory: Map<number, Order[]> = new Map();
  private addresses: Map<number, Address[]> = new Map();
  private nextCustomerId: number = 1;

  public registerCustomer(
    email: string,
    password: string,
    firstName: string,
    lastName: string
  ): number {
    if (!this.isValidEmail(email)) {
      throw new Error('Invalid email format');
    }

    if (password.length < 8) {
      throw new Error('Password must be at least 8 characters');
    }

    if (!firstName.trim() || !lastName.trim()) {
      throw new Error('First name and last name are required');
    }

    if (this.findCustomerByEmail(email)) {
      throw new Error('Customer with this email already exists');
    }

    const customerId = this.nextCustomerId++;
    const customer: Customer = {
      id: customerId,
      email,
      password: this.hashPassword(password),
      firstName,
      lastName,
      status: 'active',
      createdAt: new Date(),
      lastLogin: null,
    };

    this.customers.set(customerId, customer);

    const defaultPreferences: MarketingPreferences = {
      emailMarketing: true,
      smsMarketing: false,
      pushNotifications: true,
      preferredChannels: ['email'],
    };
    this.marketingPreferences.set(customerId, defaultPreferences);

    return customerId;
  }

  public authenticateCustomer(email: string, password: string): number | null {
    const customer = this.findCustomerByEmail(email);

    if (!customer) {
      this.recordFailedLoginAttempt(email);
      return null;
    }

    if (this.isAccountLocked(customer.id)) {
      throw new Error(
        'Account is temporarily locked due to too many failed attempts'
      );
    }

    if (!this.verifyPassword(password, customer.password)) {
      this.recordFailedLoginAttempt(email);
      return null;
    }

    this.clearFailedLoginAttempts(customer.id);
    this.updateLastLogin(customer.id);

    return customer.id;
  }

  public updateContactInformation(
    customerId: number,
    firstName: string,
    lastName: string,
    phone: string
  ): void {
    const customer = this.customers.get(customerId);
    if (!customer) {
      throw new Error('Customer not found');
    }

    if (!firstName.trim() || !lastName.trim()) {
      throw new Error('First name and last name are required');
    }

    if (phone && !this.isValidPhone(phone)) {
      throw new Error('Invalid phone number format');
    }

    const updatedCustomer: Customer = {
      ...customer,
      firstName,
      lastName,
      phone,
    };

    this.customers.set(customerId, updatedCustomer);
  }

  public addCustomerAddress(
    customerId: number,
    street: string,
    city: string,
    zipCode: string,
    country: string,
    isDefault: boolean = false
  ): number {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    if (!street.trim() || !city.trim() || !zipCode.trim() || !country.trim()) {
      throw new Error('All address fields are required');
    }

    const customerAddresses = this.addresses.get(customerId) || [];
    const addressId = customerAddresses.length + 1;

    if (isDefault) {
      // Remove default flag from existing addresses
      customerAddresses.forEach((addr, index) => {
        customerAddresses[index] = { ...addr, isDefault: false };
      });
    }

    const newAddress: Address = {
      id: addressId,
      street,
      city,
      zipCode,
      country,
      isDefault: isDefault || customerAddresses.length === 0,
    };

    const updatedAddresses = [...customerAddresses, newAddress];
    this.addresses.set(customerId, updatedAddresses);

    return addressId;
  }

  public updateMarketingPreferences(
    customerId: number,
    emailMarketing: boolean,
    smsMarketing: boolean,
    pushNotifications: boolean,
    preferredChannels: MarketingChannel[]
  ): void {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    const validChannels: MarketingChannel[] = ['email', 'sms', 'push', 'mail'];
    for (const channel of preferredChannels) {
      if (!validChannels.includes(channel)) {
        throw new Error(`Invalid marketing channel: ${channel}`);
      }
    }

    const preferences: MarketingPreferences = {
      emailMarketing,
      smsMarketing,
      pushNotifications,
      preferredChannels,
    };

    this.marketingPreferences.set(customerId, preferences);
  }

  public sendMarketingCampaign(
    customerId: number,
    _subject: string,
    _content: string,
    channel: MarketingChannel
  ): boolean {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    const preferences = this.marketingPreferences.get(customerId);
    if (!preferences) {
      return false;
    }

    switch (channel) {
      case 'email':
        return (
          preferences.emailMarketing &&
          preferences.preferredChannels.includes('email')
        );
      case 'sms':
        return (
          preferences.smsMarketing &&
          preferences.preferredChannels.includes('sms')
        );
      case 'push':
        return (
          preferences.pushNotifications &&
          preferences.preferredChannels.includes('push')
        );
      case 'mail':
        return preferences.preferredChannels.includes('mail');
      default:
        throw new Error(`Unsupported marketing channel: ${channel}`);
    }
  }

  public recordPurchase(
    customerId: number,
    items: OrderItem[],
    totalAmount: number
  ): number {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    if (items.length === 0) {
      throw new Error('Purchase must contain at least one item');
    }

    if (totalAmount <= 0) {
      throw new Error('Total amount must be positive');
    }

    const customerOrders = this.orderHistory.get(customerId) || [];
    const orderId = customerOrders.length + 1;

    const order: Order = {
      id: orderId,
      items,
      totalAmount,
      orderDate: new Date(),
      status: 'completed',
    };

    const updatedOrders = [...customerOrders, order];
    this.orderHistory.set(customerId, updatedOrders);

    return orderId;
  }

  public getCustomerSpendingHistory(
    customerId: number
  ): SpendingHistoryEntry[] {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    const orders = this.orderHistory.get(customerId) || [];
    const history: SpendingHistoryEntry[] = orders.map(order => ({
      orderId: order.id,
      amount: order.totalAmount,
      date: order.orderDate,
      itemCount: order.items.length,
    }));

    return history.sort((a, b) => b.date.getTime() - a.date.getTime());
  }

  public calculateCustomerLifetimeValue(customerId: number): number {
    if (!this.customers.has(customerId)) {
      throw new Error('Customer not found');
    }

    const orders = this.orderHistory.get(customerId) || [];
    return orders.reduce((total, order) => total + order.totalAmount, 0);
  }

  public getCustomerProfile(customerId: number): CustomerProfile {
    const customer = this.customers.get(customerId);
    if (!customer) {
      throw new Error('Customer not found');
    }

    return {
      personal: {
        id: customer.id,
        firstName: customer.firstName,
        lastName: customer.lastName,
        email: customer.email,
        phone: customer.phone || null,
        status: customer.status,
      },
      addresses: this.addresses.get(customerId) || [],
      marketing: this.marketingPreferences.get(customerId) || null,
      orderHistory: this.getCustomerSpendingHistory(customerId),
      lifetimeValue: this.calculateCustomerLifetimeValue(customerId),
    };
  }

  private findCustomerByEmail(email: string): Customer | null {
    for (const customer of this.customers.values()) {
      if (customer.email === email) {
        return customer;
      }
    }
    return null;
  }

  private recordFailedLoginAttempt(email: string): void {
    const attempts = this.loginAttempts.get(email) || [];
    attempts.push(new Date());
    this.loginAttempts.set(email, attempts);
  }

  private isAccountLocked(customerId: number): boolean {
    const customer = this.customers.get(customerId);
    if (!customer) {
      return false;
    }

    const attempts = this.loginAttempts.get(customer.email) || [];
    const fifteenMinutesAgo = new Date(Date.now() - 15 * 60 * 1000);
    const recentAttempts = attempts.filter(
      attempt => attempt > fifteenMinutesAgo
    );

    return recentAttempts.length >= 3;
  }

  private clearFailedLoginAttempts(customerId: number): void {
    const customer = this.customers.get(customerId);
    if (customer) {
      this.loginAttempts.delete(customer.email);
    }
  }

  private updateLastLogin(customerId: number): void {
    const customer = this.customers.get(customerId);
    if (customer) {
      const updatedCustomer: Customer = {
        ...customer,
        lastLogin: new Date(),
      };
      this.customers.set(customerId, updatedCustomer);
    }
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }

  private isValidPhone(phone: string): boolean {
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    return phoneRegex.test(phone);
  }

  private hashPassword(password: string): string {
    // Simple hash simulation for this exercise
    return `hashed_${password}`;
  }

  private verifyPassword(plaintext: string, hashed: string): boolean {
    return hashed === `hashed_${plaintext}`;
  }
}
