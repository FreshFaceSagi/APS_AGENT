from prometheus_client import Counter, Histogram

files_processed_total = Counter(
    "files_processed_total", "Total number of files processed"
)

llm_requests_total = Counter(
    "llm_requests_total", "Total number of LLM requests"
)

llm_requests_failed_total = Counter(
    "llm_requests_failed_total", "Total number of failed LLM requests"
)

ocr_latency_seconds = Histogram(
    "ocr_latency_seconds", "OCR latency in seconds"
)

llm_latency_seconds = Histogram(
    "llm_latency_seconds", "LLM latency in seconds"
)