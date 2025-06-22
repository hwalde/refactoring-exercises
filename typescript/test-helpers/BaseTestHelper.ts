/**
 * Base test helper utilities for refactoring exercises.
 */

/**
 * Assert that a method exists on an object.
 */
export function assertMethodExists(obj: object, methodName: string): void {
  const hasMethod = typeof (obj as any)[methodName] === 'function';
  if (!hasMethod) {
    throw new Error(`Method '${methodName}' should exist on ${obj.constructor.name}`);
  }
}

/**
 * Assert that a method is private (starts with _ or is not enumerable).
 */
export function assertMethodIsPrivate(obj: object, methodName: string): void {
  const descriptor = Object.getOwnPropertyDescriptor(obj, methodName) ||
                    Object.getOwnPropertyDescriptor(Object.getPrototypeOf(obj), methodName);
  
  if (!descriptor) {
    throw new Error(`Method '${methodName}' does not exist`);
  }

  // In TypeScript, private methods often start with _ by convention
  const isPrivateByNaming = methodName.startsWith('_');
  const isNotEnumerable = !descriptor.enumerable;
  
  if (!isPrivateByNaming && descriptor.enumerable) {
    throw new Error(`Method '${methodName}' should be private (start with _ or be non-enumerable)`);
  }
}

/**
 * Assert that an object has all expected properties.
 */
export function assertHasProperties<T extends object>(
  obj: T,
  expectedProperties: (keyof T)[],
  message?: string
): void {
  for (const prop of expectedProperties) {
    if (!(prop in obj)) {
      throw new Error(message || `Object should have property '${String(prop)}'`);
    }
  }
}

/**
 * Assert that a number is within a certain range.
 */
export function assertWithinRange(
  expected: number,
  actual: number,
  delta: number = 0.01,
  message?: string
): void {
  const diff = Math.abs(expected - actual);
  if (diff > delta) {
    throw new Error(
      message || 
      `Expected ${actual} to be within ${delta} of ${expected}, but difference was ${diff}`
    );
  }
}

/**
 * Mock function factory for testing.
 */
export function createMockFunction<T extends (...args: any[]) => any>(): T & {
  calls: Parameters<T>[];
  returns: ReturnType<T>[];
  mockReturnValue: (value: ReturnType<T>) => void;
} {
  const calls: Parameters<T>[] = [];
  const returns: ReturnType<T>[] = [];
  let returnValue: ReturnType<T>;

  const mockFn = ((...args: Parameters<T>) => {
    calls.push(args);
    const result = returnValue;
    returns.push(result);
    return result;
  }) as T & {
    calls: Parameters<T>[];
    returns: ReturnType<T>[];
    mockReturnValue: (value: ReturnType<T>) => void;
  };

  mockFn.calls = calls;
  mockFn.returns = returns;
  mockFn.mockReturnValue = (value: ReturnType<T>) => {
    returnValue = value;
  };

  return mockFn;
}

/**
 * Deep clone utility for test data.
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item)) as unknown as T;
  }

  const cloned = {} as T;
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      cloned[key] = deepClone(obj[key]);
    }
  }

  return cloned;
}