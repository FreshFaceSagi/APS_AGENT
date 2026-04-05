@echo off
echo ============================================
echo   APS OCR + Groq Summarization Pipeline
echo   Starting environment setup...
echo ============================================

REM ---- Set Poppler path ----
set "PATH=C:\Project\poppler-25.12.0\Library\bin;%PATH%"
echo Poppler path added.

REM ---- Set Tesseract path ----
set "PATH=C:\Users\Bala\AppData\Local\Programs\Tesseract-OCR;%PATH%"
echo Tesseract path added.

REM ---- Set environment variables ----
set GROQ_API_KEY=your_groq_api_key_here
set GROQ_MODEL=llama3-70b-8192
set MAX_WORKERS=4
set OCR_LANG=eng

echo Environment variables configured.

REM ---- Activate virtual environment ----
echo Activating Python virtual environment...
call .venv\Scripts\activate

if %errorlevel% neq 0 (
    echo ERROR: Could not activate virtual environment.
    echo Make sure .venv exists and Python is installed.
    pause
    exit /b 1
)

echo Virtual environment activated.

REM ---- Run the application ----
echo Running APS OCR Pipeline...
python -m src.app --input-zip aps_scanned_sample.zip --output-zip processed_output.zip

echo ============================================
echo   Pipeline execution completed.
echo   Output ZIP: processed_output.zip
echo ============================================

pause