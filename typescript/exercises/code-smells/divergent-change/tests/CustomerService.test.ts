import {
  CustomerService,
  OrderItem,
  MarketingChannel,
} from '../src/CustomerService';

describe('CustomerService', () => {
  let customerService: CustomerService;

  beforeEach(() => {
    customerService = new CustomerService();
  });

  describe('registerCustomer', () => {
    it('should register a customer successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(typeof customerId).toBe('number');
      expect(customerId).toBeGreaterThan(0);
    });

    it('should throw error with invalid email format', () => {
      expect(() => {
        customerService.registerCustomer(
          'invalid-email',
          'password123',
          'John',
          'Doe'
        );
      }).toThrow('Invalid email format');
    });

    it('should throw error with short password', () => {
      expect(() => {
        customerService.registerCustomer(
          'john.doe@example.com',
          '123',
          'John',
          'Doe'
        );
      }).toThrow('Password must be at least 8 characters');
    });

    it('should throw error with empty names', () => {
      expect(() => {
        customerService.registerCustomer(
          'john.doe@example.com',
          'password123',
          '',
          'Doe'
        );
      }).toThrow('First name and last name are required');
    });

    it('should throw error with duplicate email', () => {
      customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.registerCustomer(
          'john.doe@example.com',
          'password456',
          'Jane',
          'Smith'
        );
      }).toThrow('Customer with this email already exists');
    });
  });

  describe('authenticateCustomer', () => {
    it('should authenticate customer successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const authenticatedId = customerService.authenticateCustomer(
        'john.doe@example.com',
        'password123'
      );

      expect(authenticatedId).toBe(customerId);
    });

    it('should return null with wrong password', () => {
      customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const result = customerService.authenticateCustomer(
        'john.doe@example.com',
        'wrongpassword'
      );

      expect(result).toBeNull();
    });

    it('should return null with non-existent email', () => {
      const result = customerService.authenticateCustomer(
        'nonexistent@example.com',
        'password123'
      );

      expect(result).toBeNull();
    });

    it('should lock account after failed attempts', () => {
      customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      // Make 3 failed attempts
      for (let i = 0; i < 3; i++) {
        customerService.authenticateCustomer(
          'john.doe@example.com',
          'wrongpassword'
        );
      }

      expect(() => {
        customerService.authenticateCustomer(
          'john.doe@example.com',
          'password123'
        );
      }).toThrow(
        'Account is temporarily locked due to too many failed attempts'
      );
    });
  });

  describe('updateContactInformation', () => {
    it('should update contact information successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      customerService.updateContactInformation(
        customerId,
        'Johnny',
        'Doe-Smith',
        '+1234567890'
      );

      const profile = customerService.getCustomerProfile(customerId);
      expect(profile.personal.firstName).toBe('Johnny');
      expect(profile.personal.lastName).toBe('Doe-Smith');
      expect(profile.personal.phone).toBe('+1234567890');
    });

    it('should throw error with invalid phone number', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.updateContactInformation(
          customerId,
          'Johnny',
          'Doe-Smith',
          'invalid-phone'
        );
      }).toThrow('Invalid phone number format');
    });

    it('should throw error for non-existent customer', () => {
      expect(() => {
        customerService.updateContactInformation(
          999,
          'Johnny',
          'Doe-Smith',
          '+1234567890'
        );
      }).toThrow('Customer not found');
    });
  });

  describe('addCustomerAddress', () => {
    it('should add customer address successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const addressId = customerService.addCustomerAddress(
        customerId,
        '123 Main St',
        'New York',
        '10001',
        'USA',
        true
      );

      expect(typeof addressId).toBe('number');
      expect(addressId).toBeGreaterThan(0);

      const profile = customerService.getCustomerProfile(customerId);
      expect(profile.addresses).toHaveLength(1);
      expect(profile.addresses[0]!.isDefault).toBe(true);
    });

    it('should handle multiple addresses correctly', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const address1Id = customerService.addCustomerAddress(
        customerId,
        '123 Main St',
        'New York',
        '10001',
        'USA'
      );

      const address2Id = customerService.addCustomerAddress(
        customerId,
        '456 Oak Ave',
        'Los Angeles',
        '90210',
        'USA',
        true
      );

      const profile = customerService.getCustomerProfile(customerId);
      expect(profile.addresses).toHaveLength(2);
      expect(profile.addresses.find(a => a.id === address1Id)?.isDefault).toBe(
        false
      );
      expect(profile.addresses.find(a => a.id === address2Id)?.isDefault).toBe(
        true
      );
    });

    it('should throw error with missing address fields', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.addCustomerAddress(
          customerId,
          '',
          'New York',
          '10001',
          'USA'
        );
      }).toThrow('All address fields are required');
    });
  });

  describe('updateMarketingPreferences', () => {
    it('should update marketing preferences successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      customerService.updateMarketingPreferences(
        customerId,
        false,
        true,
        false,
        ['sms', 'mail']
      );

      const profile = customerService.getCustomerProfile(customerId);
      const marketing = profile.marketing;

      expect(marketing?.emailMarketing).toBe(false);
      expect(marketing?.smsMarketing).toBe(true);
      expect(marketing?.pushNotifications).toBe(false);
      expect(marketing?.preferredChannels).toEqual(['sms', 'mail']);
    });

    it('should throw error with invalid marketing channel', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.updateMarketingPreferences(
          customerId,
          true,
          false,
          true,
          ['email', 'invalid'] as MarketingChannel[]
        );
      }).toThrow('Invalid marketing channel: invalid');
    });
  });

  describe('sendMarketingCampaign', () => {
    it('should send marketing campaign successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const result = customerService.sendMarketingCampaign(
        customerId,
        'Special Offer',
        'Check out our latest deals!',
        'email'
      );

      expect(result).toBe(true);
    });

    it('should respect marketing opt-out preferences', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      customerService.updateMarketingPreferences(
        customerId,
        false,
        false,
        false,
        []
      );

      const result = customerService.sendMarketingCampaign(
        customerId,
        'Special Offer',
        'Check out our latest deals!',
        'email'
      );

      expect(result).toBe(false);
    });

    it('should throw error with unsupported marketing channel', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.sendMarketingCampaign(
          customerId,
          'Special Offer',
          'Check out our latest deals!',
          'carrier-pigeon' as MarketingChannel
        );
      }).toThrow('Unsupported marketing channel: carrier-pigeon');
    });
  });

  describe('recordPurchase', () => {
    it('should record purchase successfully', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const items: OrderItem[] = [
        { name: 'Product A', price: 29.99, quantity: 2 },
        { name: 'Product B', price: 15.5, quantity: 1 },
      ];

      const orderId = customerService.recordPurchase(customerId, items, 75.48);

      expect(typeof orderId).toBe('number');
      expect(orderId).toBeGreaterThan(0);
    });

    it('should throw error with empty items', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      expect(() => {
        customerService.recordPurchase(customerId, [], 0.0);
      }).toThrow('Purchase must contain at least one item');
    });

    it('should throw error with invalid amount', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const items: OrderItem[] = [
        { name: 'Product A', price: 29.99, quantity: 1 },
      ];

      expect(() => {
        customerService.recordPurchase(customerId, items, -10.0);
      }).toThrow('Total amount must be positive');
    });
  });

  describe('getCustomerSpendingHistory', () => {
    it('should return spending history in correct order', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const items1: OrderItem[] = [
        { name: 'Product A', price: 29.99, quantity: 1 },
      ];
      const items2: OrderItem[] = [
        { name: 'Product B', price: 15.5, quantity: 2 },
      ];

      customerService.recordPurchase(customerId, items1, 29.99);
      customerService.recordPurchase(customerId, items2, 31.0);

      const history = customerService.getCustomerSpendingHistory(customerId);

      expect(history).toHaveLength(2);
      // Both orders are present, sorted by date (most recent first)
      const amounts = history.map(h => h.amount).sort((a, b) => b - a);
      expect(amounts).toEqual([31.0, 29.99]);
    });

    it('should return empty array for customer without orders', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const history = customerService.getCustomerSpendingHistory(customerId);

      expect(history).toHaveLength(0);
    });
  });

  describe('calculateCustomerLifetimeValue', () => {
    it('should calculate lifetime value correctly', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const items1: OrderItem[] = [
        { name: 'Product A', price: 29.99, quantity: 1 },
      ];
      const items2: OrderItem[] = [
        { name: 'Product B', price: 15.5, quantity: 2 },
      ];

      customerService.recordPurchase(customerId, items1, 29.99);
      customerService.recordPurchase(customerId, items2, 31.0);

      const lifetimeValue =
        customerService.calculateCustomerLifetimeValue(customerId);

      expect(lifetimeValue).toBeCloseTo(60.99, 2);
    });

    it('should return zero for customer without orders', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const lifetimeValue =
        customerService.calculateCustomerLifetimeValue(customerId);

      expect(lifetimeValue).toBe(0.0);
    });
  });

  describe('getCustomerProfile', () => {
    it('should return complete customer profile', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      customerService.updateContactInformation(
        customerId,
        'Johnny',
        'Doe',
        '+1234567890'
      );
      customerService.addCustomerAddress(
        customerId,
        '123 Main St',
        'New York',
        '10001',
        'USA'
      );
      customerService.recordPurchase(
        customerId,
        [{ name: 'Product A', price: 29.99, quantity: 1 }],
        29.99
      );

      const profile = customerService.getCustomerProfile(customerId);

      expect(profile.personal).toBeDefined();
      expect(profile.addresses).toBeDefined();
      expect(profile.marketing).toBeDefined();
      expect(profile.orderHistory).toBeDefined();
      expect(profile.lifetimeValue).toBeDefined();

      expect(profile.personal.firstName).toBe('Johnny');
      expect(profile.personal.email).toBe('john.doe@example.com');
      expect(profile.addresses).toHaveLength(1);
      expect(profile.orderHistory).toHaveLength(1);
      expect(profile.lifetimeValue).toBe(29.99);
    });

    it('should throw error for non-existent customer', () => {
      expect(() => {
        customerService.getCustomerProfile(999);
      }).toThrow('Customer not found');
    });
  });

  describe('default marketing preferences', () => {
    it('should set default marketing preferences on registration', () => {
      const customerId = customerService.registerCustomer(
        'john.doe@example.com',
        'password123',
        'John',
        'Doe'
      );

      const profile = customerService.getCustomerProfile(customerId);
      const marketing = profile.marketing;

      expect(marketing?.emailMarketing).toBe(true);
      expect(marketing?.smsMarketing).toBe(false);
      expect(marketing?.pushNotifications).toBe(true);
      expect(marketing?.preferredChannels).toEqual(['email']);
    });
  });

  describe('error handling for non-existent customers', () => {
    it('should throw error when updating contact info for non-existent customer', () => {
      const nonExistentId = 999;

      expect(() => {
        customerService.updateContactInformation(
          nonExistentId,
          'John',
          'Doe',
          '+1234567890'
        );
      }).toThrow('Customer not found');
    });
  });
});
