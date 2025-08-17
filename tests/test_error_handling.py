

"""
Test Error Handling Framework
"""

import pytest
from utils.error_handling import (
    AIBacklogError, DependencyError, ProcessingError,
    ValidationError, handle_exception, log_error,
    ErrorSeverity, safe_execute
)

def test_error_hierarchy():
    """Test that all custom errors inherit from AIBacklogError"""
    base_error = AIBacklogError("Base error")
    assert isinstance(base_error, AIBacklogError)

    dep_error = DependencyError("Dependency error", "test_service")
    assert isinstance(dep_error, AIBacklogError)
    assert isinstance(dep_error, DependencyError)

    proc_error = ProcessingError("Processing error")
    assert isinstance(proc_error, AIBacklogError)
    assert isinstance(proc_error, ProcessingError)

    val_error = ValidationError("Validation error", "test_field")
    assert isinstance(val_error, AIBacklogError)
    assert isinstance(val_error, ValidationError)

def test_error_properties():
    """Test error properties are correctly set"""
    error = AIBacklogError(
        "Test error",
        severity=ErrorSeverity.WARNING,
        error_code="TEST123",
        context={"key": "value"}
    )

    assert error.severity == ErrorSeverity.WARNING
    assert error.error_code == "TEST123"
    assert error.context == {"key": "value"}
    assert hasattr(error, "timestamp")

def test_handle_exception():
    """Test exception handling"""
    try:
        raise ValueError("Test value error")
    except ValueError as e:
        handled_error = handle_exception(
            e,
            severity=ErrorSeverity.ERROR,
            error_code="TEST_HANDLE",
            context={"test": True}
        )

        assert isinstance(handled_error, AIBacklogError)
        assert handled_error.original_exception == e
        assert handled_error.error_code == "TEST_HANDLE"
        assert handled_error.context["test"] is True

def test_safe_execute():
    """Test safe execution"""
    def failing_function():
        raise RuntimeError("Test runtime error")

    result, error = safe_execute(failing_function)
    assert result is None
    assert isinstance(error, AIBacklogError)
    assert error.original_exception is not None

    def successful_function():
        return "success"

    result, error = safe_execute(successful_function)
    assert result == "success"
    assert error is None

def test_error_logging(caplog):
    """Test error logging (requires pytest-capturelog)"""
    error = AIBacklogError("Log test error", severity=ErrorSeverity.INFO)
    assert "Log test error" in caplog.text
    assert "AIBA_INFO" in caplog.text

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

