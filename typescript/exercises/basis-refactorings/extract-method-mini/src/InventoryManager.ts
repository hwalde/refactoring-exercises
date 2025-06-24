export interface InventoryItem {
  readonly active: boolean;
}

export class InventoryManager {
  private readonly items: InventoryItem[];

  constructor(items: InventoryItem[]) {
    this.items = items;
  }

  public generateReport(): string {
    // Calculation block - should be extracted
    let activeItems = 0;
    const total = this.items.length;

    for (const item of this.items) {
      if (item.active) {
        activeItems++;
      }
    }

    const percentage =
      total > 0 ? Math.round((activeItems / total) * 100 * 10) / 10 : 0;

    // Report generation
    return `Inventory Report
Total items: ${total}
Active items: ${activeItems}
Active percentage: ${percentage}%`;
  }
}
