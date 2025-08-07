



"""
Circuit breaker implementation for resilient service calls
"""
import time
import logging
from typing import Callable, Optional, Any
from functools import wraps
from custom_exceptions import CircuitBreakerError, RetryableError

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """
    Circuit breaker pattern implementation
    """

    def __init__(
        self,
        name: str,
        max_failures: int = 3,
        reset_timeout: int = 60,
        on_state_change: Optional[Callable] = None
    ):
        """
        Initialize circuit breaker

        Args:
            name: Name of the circuit breaker
            max_failures: Maximum failures before opening circuit
            reset_timeout: Time in seconds before attempting reset
            on_state_change: Callback for state changes
        """
        self.name = name
        self.max_failures = max_failures
        self.reset_timeout = reset_timeout
        self.on_state_change = on_state_change

        # State variables
        self._state = "closed"
        self._failure_count = 0
        self._last_failure_time = 0
        self._next_reset_time = 0

    @property
    def state(self) -> str:
        """Get current state"""
        return self._state

    def _set_state(self, new_state: str):
        """Set new state and call callback if provided"""
        if new_state != self._state:
            old_state = self._state
            self._state = new_state
            logger.info(f"Circuit breaker '{self.name}': {old_state} -> {new_state}")

            if self.on_state_change:
                try:
                    self.on_state_change(self.name, old_state, new_state)
                except Exception as e:
                    logger.error(f"Error in state change callback: {e}")

    def _can_attempt_reset(self) -> bool:
        """Check if reset can be attempted"""
        if self._state != "open":
            return True

        current_time = time.time()
        if current_time >= self._next_reset_time:
            return True

        return False

    def _attempt_reset(self):
        """Attempt to reset the circuit"""
        self._set_state("half-open")
        logger.info(f"Circuit breaker '{self.name}' attempting reset")

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection

        Args:
            func: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Result of function call

        Raises:
            CircuitBreakerError: If circuit is open
            Exception: Any exception from the function call
        """
        if self._state == "open":
            if not self._can_attempt_reset():
                raise CircuitBreakerError(
                    f"Circuit breaker '{self.name}' is open. "
                    f"Will attempt reset at {time.ctime(self._next_reset_time)}"
                )

            # Attempt reset
            self._attempt_reset()

        try:
            result = func(*args, **kwargs)

            # Success - reset failure count and ensure circuit is closed
            if self._state in ["half-open", "closed"]:
                self._failure_count = 0
                self._set_state("closed")

            return result

        except Exception as e:
            # Handle failure
            self._failure_count += 1
            self._last_failure_time = time.time()

            if self._state == "half-open":
                # Reset failed, go back to open
                self._next_reset_time = time.time() + self.reset_timeout
                self._set_state("open")
            elif self._state == "closed" and self._failure_count >= self.max_failures:
                # Exceeded max failures, open circuit
                self._next_reset_time = time.time() + self.reset_timeout
                self._set_state("open")

            # Re-raise the original exception
            raise

    def decorator(self, func: Callable) -> Callable:
        """
        Decorator version of circuit breaker

        Args:
            func: Function to decorate

        Returns:
            Wrapped function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def reset(self):
        """Manually reset the circuit breaker"""
        self._failure_count = 0
        self._set_state("closed")
        logger.info(f"Circuit breaker '{self.name}' manually reset")

    def get_status(self) -> dict:
        """Get current status"""
        return {
            "name": self.name,
            "state": self._state,
            "failure_count": self._failure_count,
            "last_failure_time": self._last_failure_time,
            "next_reset_time": self._next_reset_time,
            "max_failures": self.max_failures,
            "reset_timeout": self.reset_timeout
        }

# Global circuit breakers registry
_circuit_breakers = {}

def get_circuit_breaker(name: str, **kwargs) -> CircuitBreaker:
    """
    Get or create a circuit breaker

    Args:
        name: Name of the circuit breaker
        **kwargs: Additional arguments for CircuitBreaker constructor

    Returns:
        CircuitBreaker instance
    """
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(name, **kwargs)

    return _circuit_breakers[name]

def circuit_breaker(name: str, **kwargs):
    """
    Decorator factory for circuit breaker

    Args:
        name: Name of the circuit breaker
        **kwargs: Additional arguments for CircuitBreaker constructor

    Returns:
        Decorator function
    """
    def decorator(func):
        cb = get_circuit_breaker(name, **kwargs)
        return cb.decorator(func)
    return decorator


