import io
import time
from dataclasses import dataclass
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path

from src.observability.logging_config import get_logger
from src.observability.metrics import ocr_latency_seconds
from src.config import OCR_LANG

logger = get_logger("ocr")


@dataclass
class OcrResult:
    text: str
    pages: int


class OcrAgent:
    def __init__(self, lang: str = OCR_LANG):
        self.lang = lang

    def run(self, pdf_path: Path) -> OcrResult:
        start = time.time()
        logger.info("ocr_start", file=str(pdf_path))

        #images = convert_from_path(str(pdf_path))
        images = convert_from_path(
           str(pdf_path),
          poppler_path=r"C:\Project\poppler-25.12.0\Library\bin"
      )

        texts = []

        for idx, img in enumerate(images):
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            page_text = pytesseract.image_to_string(img, lang=self.lang)
            texts.append(page_text)
            logger.info("ocr_page_done", file=str(pdf_path), page=idx + 1)

        full_text = "\n\n".join(texts)
        duration = time.time() - start
        ocr_latency_seconds.observe(duration)
        logger.info("ocr_done", file=str(pdf_path), duration=duration)

        return OcrResult(text=full_text, pages=len(images))