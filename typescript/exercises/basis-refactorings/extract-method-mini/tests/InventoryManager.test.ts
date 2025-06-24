import { InventoryManager, InventoryItem } from '../src/InventoryManager';

describe('InventoryManager', () => {
  test('generates report with all active items', () => {
    const items: InventoryItem[] = [
      { active: true },
      { active: true },
      { active: true },
    ];

    const manager = new InventoryManager(items);
    const report = manager.generateReport();

    expect(report).toContain('Total items: 3');
    expect(report).toContain('Active items: 3');
    expect(report).toContain('Active percentage: 100%');
  });

  test('generates report with no active items', () => {
    const items: InventoryItem[] = [
      { active: false },
      { active: false },
      { active: false },
    ];

    const manager = new InventoryManager(items);
    const report = manager.generateReport();

    expect(report).toContain('Total items: 3');
    expect(report).toContain('Active items: 0');
    expect(report).toContain('Active percentage: 0%');
  });

  test('generates report with mixed items', () => {
    const items: InventoryItem[] = [
      { active: true },
      { active: false },
      { active: true },
    ];

    const manager = new InventoryManager(items);
    const report = manager.generateReport();

    expect(report).toContain('Total items: 3');
    expect(report).toContain('Active items: 2');
    expect(report).toContain('Active percentage: 66.7%');
  });

  test('generates report with empty items', () => {
    const items: InventoryItem[] = [];

    const manager = new InventoryManager(items);
    const report = manager.generateReport();

    expect(report).toContain('Total items: 0');
    expect(report).toContain('Active items: 0');
    expect(report).toContain('Active percentage: 0%');
  });
});
