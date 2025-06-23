export class Customer {
  constructor(
    private readonly id: string,
    private readonly name: string,
    private readonly email: string,
    private readonly type: string,
    private readonly loyaltyYears: number,
    private readonly address: string = '',
    private readonly phoneNumber: string = ''
  ) {}

  getId(): string {
    return this.id;
  }

  getName(): string {
    return this.name;
  }

  getEmail(): string {
    return this.email;
  }

  getType(): string {
    return this.type;
  }

  getLoyaltyYears(): number {
    return this.loyaltyYears;
  }

  getAddress(): string {
    return this.address;
  }

  getPhoneNumber(): string {
    return this.phoneNumber;
  }
}
