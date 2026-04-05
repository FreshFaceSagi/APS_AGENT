import time
from dataclasses import dataclass

import requests
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import GROQ_API_KEY, GROQ_API_URL, GROQ_MODEL, CIRCUIT_FAILURE_THRESHOLD, CIRCUIT_RESET_TIMEOUT_SECONDS
from src.core.circuit_breaker import CircuitBreaker
from src.observability.logging_config import get_logger
from src.observability.metrics import llm_requests_total, llm_requests_failed_total, llm_latency_seconds

logger = get_logger("summarizer")


@dataclass
class SummaryResult:
    summary: str
    fallback_used: bool = False


class GroqSummarizer:
    def __init__(self):
        self.circuit = CircuitBreaker(
            failure_threshold=CIRCUIT_FAILURE_THRESHOLD,
            reset_timeout=CIRCUIT_RESET_TIMEOUT_SECONDS,
        )

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _call_groq(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a concise document summarizer. Provide a clear, structured summary.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
        }

        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    def summarize(self, text: str) -> SummaryResult:
        llm_requests_total.inc()
        start = time.time()
        logger.info("llm_summarize_start", text_length=len(text), circuit_state=self.circuit.state)

        try:
            self.circuit.before_call()
        except RuntimeError:
            llm_requests_failed_total.inc()
            logger.warning("llm_circuit_open", msg="Circuit open, returning fallback summary")
            return SummaryResult(
                summary="Summary temporarily unavailable due to upstream LLM issues.",
                fallback_used=True,
            )

        try:
            # You may want to truncate or chunk text before this call
            prompt = f"Summarize the following document:\n\n{text[:12000]}"
            summary = self._call_groq(prompt)
            self.circuit.on_success()
            duration = time.time() - start
            llm_latency_seconds.observe(duration)
            logger.info("llm_summarize_done", duration=duration)
            return SummaryResult(summary=summary, fallback_used=False)
        except Exception as e:
            self.circuit.on_failure()
            llm_requests_failed_total.inc()
            duration = time.time() - start
            llm_latency_seconds.observe(duration)
            logger.error("llm_summarize_error", error=str(e), duration=duration)
            return SummaryResult(
                summary="Summary unavailable due to an error in the LLM pipeline.",
                fallback_used=True,
            )