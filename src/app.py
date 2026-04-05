import argparse
import tempfile
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from src.agents.ocr_agent import OcrAgent
from src.agents.groq_summarizer import GroqSummarizer
from src.agents.packaging_agent import PackagingAgent
from src.core.orchestrator import JobOrchestrator
from src.observability.logging_config import configure_logging, get_logger
from src.config import MAX_WORKERS

logger = get_logger("app")


def process_zip(input_zip: Path, output_zip: Path):
    configure_logging()
    logger.info("job_start", input_zip=str(input_zip), output_zip=str(output_zip))

    ocr_agent = OcrAgent()
    summarizer = GroqSummarizer()
    packer = PackagingAgent()
    orchestrator = JobOrchestrator(ocr_agent, summarizer, packer)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        # Extract
        with zipfile.ZipFile(input_zip, "r") as zf:
            zf.extractall(tmpdir)

        pdf_files = list(tmpdir.glob("**/*.pdf"))
        logger.info("pdf_files_found", count=len(pdf_files))

        results = []

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            future_to_pdf = {
                pool.submit(orchestrator.process_file, pdf): pdf for pdf in pdf_files
            }

            for future in as_completed(future_to_pdf):
                res = future.result()
                results.append(res)

        # Re-zip outputs
        with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as out_zip:
            for res in results:
                if not res.success:
                    logger.warning("file_failed", file=str(res.pdf_path), error=res.error)
                    continue
                for artifact in res.artifacts:
                    # store relative to tmpdir root
                    arcname = artifact.relative_to(tmpdir)
                    out_zip.write(artifact, arcname=str(arcname))

    logger.info("job_done", input_zip=str(input_zip), output_zip=str(output_zip))


def main():
    parser = argparse.ArgumentParser(description="OCR + Groq summarization ZIP pipeline")
    parser.add_argument("--input-zip", required=True, help="Path to input ZIP containing PDFs")
    parser.add_argument("--output-zip", required=True, help="Path to output processed ZIP")
    args = parser.parse_args()

    process_zip(Path(args.input_zip), Path(args.output_zip))


if __name__ == "__main__":
    main()