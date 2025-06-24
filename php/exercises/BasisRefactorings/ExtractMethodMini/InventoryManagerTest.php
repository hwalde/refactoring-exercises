<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\ExtractMethodMini;

use PHPUnit\Framework\TestCase;

/**
 * @internal
 *
 * @coversNothing
 */
final class InventoryManagerTest extends TestCase
{
    public function testGenerateReportWithAllActiveItems(): void
    {
        $items = [
            ['name' => 'Item1', 'active' => true],
            ['name' => 'Item2', 'active' => true],
        ];

        $manager = new InventoryManager($items);
        $report = $manager->generateReport();

        $this->assertStringContainsString('Total items: 2', $report);
        $this->assertStringContainsString('Active items: 2', $report);
        $this->assertStringContainsString('Active percentage: 100%', $report);
    }

    public function testGenerateReportWithNoActiveItems(): void
    {
        $items = [
            ['name' => 'Item1', 'active' => false],
            ['name' => 'Item2', 'active' => false],
        ];

        $manager = new InventoryManager($items);
        $report = $manager->generateReport();

        $this->assertStringContainsString('Total items: 2', $report);
        $this->assertStringContainsString('Active items: 0', $report);
        $this->assertStringContainsString('Active percentage: 0%', $report);
    }

    public function testGenerateReportWithMixedItems(): void
    {
        $items = [
            ['name' => 'Item1', 'active' => true],
            ['name' => 'Item2', 'active' => false],
            ['name' => 'Item3', 'active' => true],
        ];

        $manager = new InventoryManager($items);
        $report = $manager->generateReport();

        $this->assertStringContainsString('Total items: 3', $report);
        $this->assertStringContainsString('Active items: 2', $report);
        $this->assertStringContainsString('Active percentage: 66.7%', $report);
    }

    public function testGenerateReportWithEmptyItems(): void
    {
        $items = [];

        $manager = new InventoryManager($items);
        $report = $manager->generateReport();

        $this->assertStringContainsString('Total items: 0', $report);
        $this->assertStringContainsString('Active items: 0', $report);
        $this->assertStringContainsString('Active percentage: 0%', $report);
    }
}
