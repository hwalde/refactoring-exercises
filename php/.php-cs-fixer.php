<?php

declare(strict_types=1);

$finder = PhpCsFixer\Finder::create()
    ->in(__DIR__ . '/exercises')
    ->name('*.php')
    ->exclude('vendor')
    ->exclude('coverage')
    ->exclude('.phpunit.cache');

return (new PhpCsFixer\Config())
    ->setRules([
        '@PSR12' => true,
        '@PhpCsFixer' => true,
        'strict_param' => true,
        'declare_strict_types' => true,
        'array_syntax' => ['syntax' => 'short'],
        'ordered_imports' => ['sort_algorithm' => 'alpha'],
        'no_unused_imports' => true,
        'phpdoc_order' => true,
        'phpdoc_align' => ['align' => 'left'],
        'class_attributes_separation' => [
            'elements' => [
                'const' => 'one',
                'method' => 'one',
                'property' => 'one',
            ],
        ],
    ])
    ->setFinder($finder)
    ->setRiskyAllowed(true);