export class Product {
  constructor(
    private readonly id: string,
    private readonly name: string,
    private readonly price: number,
    private readonly category: string,
    private readonly weight: number,
    private readonly fragile: boolean = false,
    private readonly manufacturer: string = ''
  ) {}

  getId(): string {
    return this.id;
  }

  getName(): string {
    return this.name;
  }

  getPrice(): number {
    return this.price;
  }

  getCategory(): string {
    return this.category;
  }

  getWeight(): number {
    return this.weight;
  }

  isFragile(): boolean {
    return this.fragile;
  }

  getManufacturer(): string {
    return this.manufacturer;
  }
}
