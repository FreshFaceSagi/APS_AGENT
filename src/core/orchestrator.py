import time
from dataclasses import dataclass
from pathlib import Path

from src.agents.ocr_agent import OcrAgent, OcrResult
from src.agents.groq_summarizer import GroqSummarizer, SummaryResult
from src.agents.packaging_agent import PackagingAgent, PackagingResult
from src.observability.logging_config import get_logger
from src.observability.metrics import files_processed_total

logger = get_logger("orchestrator")


@dataclass
class FileProcessResult:
    pdf_path: Path
    artifacts: list[Path]
    success: bool
    error: str | None = None


class JobOrchestrator:
    def __init__(self, ocr_agent: OcrAgent, summarizer: GroqSummarizer, packer: PackagingAgent):
        self.ocr_agent = ocr_agent
        self.summarizer = summarizer
        self.packer = packer

    def process_file(self, pdf_path: Path) -> FileProcessResult:
        start = time.time()
        logger.info("file_process_start", file=str(pdf_path))

        try:
            ocr_result: OcrResult = self.ocr_agent.run(pdf_path)
            summary_result: SummaryResult = self.summarizer.summarize(ocr_result.text)
            packaging_result: PackagingResult = self.packer.package(pdf_path, ocr_result, summary_result)

            duration = time.time() - start
            files_processed_total.inc()
            logger.info("file_process_done", file=str(pdf_path), duration=duration)

            return FileProcessResult(
                pdf_path=pdf_path,
                artifacts=packaging_result.artifacts,
                success=True,
            )
        except Exception as e:
            duration = time.time() - start
            logger.error("file_process_error", file=str(pdf_path), error=str(e), duration=duration)
            return FileProcessResult(
                pdf_path=pdf_path,
                artifacts=[],
                success=False,
                error=str(e),
            )