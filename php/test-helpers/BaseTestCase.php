<?php

declare(strict_types=1);

namespace RefactoringExercises\TestHelpers;

use PHPUnit\Framework\TestCase;

/**
 * Base test case with common utilities for refactoring exercises.
 */
abstract class BaseTestCase extends TestCase
{
    /**
     * Assert that a method exists and is callable.
     */
    protected function assertMethodExists(object $object, string $methodName): void
    {
        $this->assertTrue(
            method_exists($object, $methodName),
            "Method '{$methodName}' should exist on " . get_class($object)
        );
        
        $this->assertTrue(
            is_callable([$object, $methodName]),
            "Method '{$methodName}' should be callable on " . get_class($object)
        );
    }

    /**
     * Assert that a method is private or protected (not public).
     */
    protected function assertMethodIsPrivate(object $object, string $methodName): void
    {
        $reflection = new \ReflectionClass($object);
        $this->assertTrue(
            $reflection->hasMethod($methodName),
            "Method '{$methodName}' should exist"
        );
        
        $method = $reflection->getMethod($methodName);
        $this->assertTrue(
            $method->isPrivate() || $method->isProtected(),
            "Method '{$methodName}' should be private or protected"
        );
    }

    /**
     * Get private/protected method for testing via reflection.
     */
    protected function getPrivateMethod(object $object, string $methodName): \ReflectionMethod
    {
        $reflection = new \ReflectionClass($object);
        $method = $reflection->getMethod($methodName);
        $method->setAccessible(true);
        
        return $method;
    }

    /**
     * Assert array contains all expected keys.
     */
    protected function assertArrayHasKeys(array $expectedKeys, array $array, string $message = ''): void
    {
        foreach ($expectedKeys as $key) {
            $this->assertArrayHasKey($key, $array, $message ?: "Array should contain key '{$key}'");
        }
    }

    /**
     * Assert that a value is within a certain range.
     */
    protected function assertWithinRange(float $expected, float $actual, float $delta = 0.01, string $message = ''): void
    {
        $this->assertEqualsWithDelta($expected, $actual, $delta, $message);
    }
}