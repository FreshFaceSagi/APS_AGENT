# 📄 APS OCR + Groq Summarization Pipeline  
A production‑ready, agentic pipeline that processes **scanned APS PDFs**, performs **OCR**, generates **LLM summaries**, and outputs a **processed ZIP** containing:

- Original PDFs  
- OCR text files  
- LLM summaries  
- Full observability logs  

This system is designed for **high‑volume APS processing**, handling **300+ page scanned PDFs**, with **circuit breakers**, **retries**, **structured logging**, and **parallel execution**.

---

## 🚀 Features

### ✔ OCR for scanned PDFs  
- Uses **Tesseract OCR**  
- Handles noisy, skewed, low‑resolution scans  
- Converts each page to text  

### ✔ LLM Summarization (Groq)  
- Summaries generated using Groq LLM API  
- Chunking support for large documents  
- Circuit breaker + retry logic  
- Fallback summaries when LLM unavailable  

### ✔ Agentic Architecture  
- OCR Agent  
- Summarization Agent  
- Packaging Agent  
- Orchestrator with metrics + logs  

### ✔ Observability  
- Structured JSON logs (via structlog)  
- Prometheus metrics  
- Execution tracing per file  

### ✔ Resilience  
- Automatic retries (tenacity)  
- Circuit breaker for LLM failures  
- Graceful degradation  

---

## 📁 Project Structure

aps-ocr-zip-pipeline/ │ ├── requirements.txt ├── README.md └── src/ ├── app.py ├── config.py │ ├── agents/ │   ├── ocr_agent.py │   ├── groq_summarizer.py │   └── packaging_agent.py │ ├── core/ │   ├── circuit_breaker.py │   └── orchestrator.py │ └── observability/ ├── logging_config.py └── metrics.p


---

## 🔧 Installation

### 1. Install system dependencies

#### Tesseract OCR  
Download (Windows):  
https://github.com/UB-Mannheim/tesseract/wiki

Add to PATH:  

C:\Program Files\Tesseract-OCR\

#### Poppler (for pdf2image)  
Download:  
https://github.com/oschwartz10612/poppler-windows/releases/

Add to PATH:  
C:\poppler\Library\bin

---

### 2. Create Python environment

python -m venv .venv .venv\Scripts\activate


### 3. Install dependencies

pip install -r requirements.txt


---

## 🔐 Environment Variables

Create a `.env` file:

GROQ_API_KEY=your_key_here GROQ_MODEL=llama3-70b-8192 MAX_WORKERS=4 OCR_LANG=eng


---

## ▶️ Running the Pipeline

python -m src.app --input-zip aps_scanned_sample.zip --output-zip processed.zip


### Output ZIP contains:

APS_John_Doe_2020.pdf APS_John_Doe_2020.ocr.txt APS_John_Doe_2020.summary.txt ...


---

## 🧪 Generating Synthetic APS Test Data

Use the included generator script to create **300‑page scanned PDFs**:

python generate_scanned_aps_zip.py


This produces:

aps_scanned_sample.zip


---

## 🧠 Architecture Overview


ZIP → Extract PDFs ↓ OCR Agent (Tesseract) ↓ Groq Summarizer (LLM) ↓ Packaging Agent ↓ Processed ZIP


---

## 🛡 Resilience & Safety

### Circuit Breaker  
- Opens after N failures  
- Prevents hammering Groq API  
- Auto‑recovers after timeout  

### Retries  
- Exponential backoff  
- Handles transient network issues  

### Fallback Summaries  
- Ensures output is always generated  

---

## 📊 Observability

### Logging  
- JSON structured logs  
- Per‑file and per‑stage events  

### Metrics  
- OCR latency  
- LLM latency  
- LLM failures  
- Files processed  

---

## 📦 Packaging

Each processed PDF produces:

<name>.pdf <name>.ocr.txt <name>.summary.txt


All artifacts are zipped into the final output.

---

## 📝 License  
Internal use only unless otherwise specified.

---

## 🤝 Contributing  
Pull requests welcome.  
Please open an issue before major changes.

