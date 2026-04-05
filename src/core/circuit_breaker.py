import time
from enum import Enum
from threading import Lock


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    def __init__(self, failure_threshold: int, reset_timeout: int):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._lock = Lock()

    @property
    def state(self) -> CircuitState:
        return self._state

    def before_call(self):
        with self._lock:
            if self._state == CircuitState.OPEN:
                if time.time() - self._last_failure_time > self.reset_timeout:
                    self._state = CircuitState.HALF_OPEN
                else:
                    raise RuntimeError("CircuitBreaker is OPEN; short-circuiting call")

    def on_success(self):
        with self._lock:
            self._failure_count = 0
            self._state = CircuitState.CLOSED

    def on_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN