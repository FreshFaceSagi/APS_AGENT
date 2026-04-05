from dataclasses import dataclass
from pathlib import Path
from typing import List

from src.observability.logging_config import get_logger
from src.agents.ocr_agent import OcrResult
from src.agents.groq_summarizer import SummaryResult

logger = get_logger("packaging")


@dataclass
class PackagingResult:
    artifacts: List[Path]


class PackagingAgent:
    def package(self, pdf_path: Path, ocr_result: OcrResult, summary_result: SummaryResult) -> PackagingResult:
        base = pdf_path.with_suffix("")  # remove .pdf
        ocr_path = base.with_suffix(".ocr.txt")
        summary_path = base.with_suffix(".summary.txt")

        ocr_path.write_text(ocr_result.text, encoding="utf-8")
        summary_path.write_text(summary_result.summary, encoding="utf-8")

        logger.info(
            "packaging_done",
            pdf=str(pdf_path),
            ocr=str(ocr_path),
            summary=str(summary_path),
        )

        return PackagingResult(artifacts=[pdf_path, ocr_path, summary_path])