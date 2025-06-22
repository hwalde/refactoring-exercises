"""Base test helper utilities for refactoring exercises."""

import inspect
from typing import Any, Dict, List, TypeVar, Union
import copy

T = TypeVar("T")


def assert_method_exists(obj: Any, method_name: str) -> None:
    """Assert that a method exists and is callable on an object."""
    if not hasattr(obj, method_name):
        raise AssertionError(
            f"Method '{method_name}' should exist on {obj.__class__.__name__}"
        )

    method = getattr(obj, method_name)
    if not callable(method):
        raise AssertionError(
            f"Method '{method_name}' should be callable on {obj.__class__.__name__}"
        )


def assert_method_is_private(obj: Any, method_name: str) -> None:
    """Assert that a method is private (starts with _ by Python convention)."""
    if not hasattr(obj, method_name):
        raise AssertionError(f"Method '{method_name}' does not exist")

    if not method_name.startswith("_"):
        raise AssertionError(f"Method '{method_name}' should be private (start with _)")


def assert_has_attributes(
    obj: Any, expected_attributes: List[str], message: str = ""
) -> None:
    """Assert that an object has all expected attributes."""
    for attr in expected_attributes:
        if not hasattr(obj, attr):
            error_msg = message or f"Object should have attribute '{attr}'"
            raise AssertionError(error_msg)


def assert_within_range(
    expected: float, actual: float, delta: float = 0.01, message: str = ""
) -> None:
    """Assert that a number is within a certain range."""
    diff = abs(expected - actual)
    if diff > delta:
        error_msg = (
            message
            or f"Expected {actual} to be within {delta} of {expected}, but difference was {diff}"
        )
        raise AssertionError(error_msg)


def assert_dict_contains_keys(
    expected_keys: List[str], actual_dict: Dict[str, Any], message: str = ""
) -> None:
    """Assert that a dictionary contains all expected keys."""
    for key in expected_keys:
        if key not in actual_dict:
            error_msg = message or f"Dictionary should contain key '{key}'"
            raise AssertionError(error_msg)


class MockFunction:
    """Simple mock function for testing."""

    def __init__(self, return_value: Any = None) -> None:
        self.calls: List[tuple] = []
        self.returns: List[Any] = []
        self._return_value = return_value

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        self.calls.append((args, kwargs))
        self.returns.append(self._return_value)
        return self._return_value

    def mock_return_value(self, value: Any) -> None:
        """Set the return value for future calls."""
        self._return_value = value

    @property
    def call_count(self) -> int:
        """Number of times the function was called."""
        return len(self.calls)

    def assert_called_with(self, *expected_args: Any, **expected_kwargs: Any) -> None:
        """Assert the function was called with specific arguments."""
        expected_call = (expected_args, expected_kwargs)
        if expected_call not in self.calls:
            raise AssertionError(
                f"Expected call {expected_call} not found in {self.calls}"
            )


def deep_copy(obj: T) -> T:
    """Deep copy utility for test data."""
    return copy.deepcopy(obj)


def get_method_line_count(obj: Any, method_name: str) -> int:
    """Get the number of lines in a method (useful for testing refactoring)."""
    if not hasattr(obj, method_name):
        raise ValueError(
            f"Method '{method_name}' does not exist on {obj.__class__.__name__}"
        )

    method = getattr(obj, method_name)
    try:
        source_lines = inspect.getsourcelines(method)[0]
        # Filter out empty lines and comments
        code_lines = [
            line
            for line in source_lines
            if line.strip() and not line.strip().startswith("#")
        ]
        return len(code_lines)
    except OSError:
        # Method might be built-in or defined dynamically
        return 0


def assert_method_line_count_below(obj: Any, method_name: str, max_lines: int) -> None:
    """Assert that a method has fewer than a certain number of lines."""
    line_count = get_method_line_count(obj, method_name)
    if line_count > max_lines:
        raise AssertionError(
            f"Method '{method_name}' has {line_count} lines, should be <= {max_lines}"
        )
