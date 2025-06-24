<?php

declare(strict_types=1);

namespace RefactoringExercises\BasisRefactorings\ExtractMethodMini;

class InventoryManager
{
    private array $items;

    public function __construct(array $items)
    {
        $this->items = $items;
    }

    public function generateReport(): string
    {
        // Berechnungsblock - soll extrahiert werden
        $activeItems = 0;
        $total = count($this->items);

        foreach ($this->items as $item) {
            if ($item['active']) {
                ++$activeItems;
            }
        }

        $percentage = $total > 0 ? round(($activeItems / $total) * 100, 1) : 0;

        // Berichterstellung
        return "Inventory Report\n"
               ."Total items: {$total}\n"
               ."Active items: {$activeItems}\n"
               ."Active percentage: {$percentage}%";
    }
}
