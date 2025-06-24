import { User } from '../src/User';

describe('User', () => {
  test('can create user with valid email', () => {
    const user = new User('John Doe', 'john@example.com');

    expect(user.name).toBe('John Doe');
    expect(user.getEmail()).toBe('john@example.com');
  });

  test('can get display name', () => {
    const user = new User('Jane Smith', 'jane@company.com');

    expect(user.getDisplayName()).toBe('Jane Smith (jane@company.com)');
  });

  test('can detect business email', () => {
    const businessUser = new User('Bob Manager', 'bob@company.com');
    const externalUser = new User('Alice Client', 'alice@external.com');

    expect(businessUser.hasBusinessEmail()).toBe(true);
    expect(externalUser.hasBusinessEmail()).toBe(false);
  });

  test('can get email domain', () => {
    const user = new User('Tom Developer', 'tom@example.org');

    expect(user.getEmailDomain()).toBe('example.org');
  });

  test('can set email after creation', () => {
    const user = new User('Sarah Tester', 'sarah@old.com');

    user.setEmail('sarah@new.com');

    expect(user.getEmail()).toBe('sarah@new.com');
  });

  test('currently allows empty email', () => {
    // This test demonstrates the current problematic behavior
    // After refactoring, this should throw an exception
    const user = new User('Invalid User', '');

    expect(user.getEmail()).toBe('');
  });

  test('currently allows email without at symbol', () => {
    // This test demonstrates the current problematic behavior
    // After refactoring, this should throw an exception
    const user = new User('Invalid User', 'notanemail');

    expect(user.getEmail()).toBe('notanemail');
  });

  test('currently allows setting empty email', () => {
    // This test demonstrates the current problematic behavior
    // After refactoring, this should throw an exception
    const user = new User('Valid User', 'valid@email.com');

    user.setEmail('');

    expect(user.getEmail()).toBe('');
  });

  test('currently allows setting email without at symbol', () => {
    // This test demonstrates the current problematic behavior
    // After refactoring, this should throw an exception
    const user = new User('Valid User', 'valid@email.com');

    user.setEmail('invalid-email');

    expect(user.getEmail()).toBe('invalid-email');
  });

  test('can set valid email after creation', () => {
    const user = new User('Change User', 'old@domain.com');

    user.setEmail('new@domain.com');

    expect(user.getEmail()).toBe('new@domain.com');
    expect(user.getDisplayName()).toBe('Change User (new@domain.com)');
  });

  test('email domain works after email change', () => {
    const user = new User('Domain User', 'user@first.com');

    user.setEmail('user@second.org');

    expect(user.getEmailDomain()).toBe('second.org');
  });

  test('business email detection works after email change', () => {
    const user = new User('Business User', 'user@external.com');
    expect(user.hasBusinessEmail()).toBe(false);

    user.setEmail('user@company.com');
    expect(user.hasBusinessEmail()).toBe(true);
  });
});
