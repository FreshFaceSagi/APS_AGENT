import cv2
import numpy as np
from fpdf import FPDF
from pathlib import Path
import zipfile
import random
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageFilter, ImageOps


from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import cv2

def generate_scanned_page(text: str):
    """Generate a synthetic scanned-looking page as an image."""

    # Create blank white page
    img = Image.new("RGB", (1700, 2200), "white")
    draw = ImageDraw.Draw(img)

    # Use a basic font (PIL default)
    font = ImageFont.load_default()

    # Draw text
    y = 50
    for line in text.split("\n"):
        draw.text((50, y), line, fill="black", font=font)
        y += 20

    # Convert to numpy for noise
    arr = np.array(img)

    # Add Gaussian noise
    noise = np.random.normal(0, 18, arr.shape).astype(np.int16)
    noisy = np.clip(arr + noise, 0, 255).astype(np.uint8)

    # Convert back to PIL
    noisy_img = Image.fromarray(noisy)

    # Add blur
    noisy_img = noisy_img.filter(ImageFilter.GaussianBlur(radius=1.2))

    # Add slight rotation (scanner skew)
    angle = random.uniform(-1.5, 1.5)
    noisy_img = noisy_img.rotate(angle, expand=False, fillcolor="white")

    # Add JPEG compression artifacts
    noisy_img.save("compressed.jpg", "JPEG", quality=35)
    final_img = Image.open("compressed.jpg")

    return final_img


def generate_aps_pdf(output_path: Path, patient_name: str, pages=300):
    pdf = FPDF(unit="pt", format=[1700, 2200])

    for i in range(pages):
        text = f"""
Attending Physician Statement (APS)
Patient Name: {patient_name}
DOB: 1975-04-12
Physician: Dr. Emily Carter, MD
Visit Date: 2020-06-15

Page {i+1} of {pages}

Chief Complaint:
Patient reports intermittent chest discomfort and fatigue.

Medical History:
- Hypertension (diagnosed 2015)
- Hyperlipidemia (diagnosed 2018)

Medications:
- Lisinopril 10mg daily
- Atorvastatin 20mg nightly

Recent Labs:
- LDL: 142 mg/dL
- HDL: 48 mg/dL
- A1C: 5.8%
- BP: 138/86

Physician Notes:
Patient advised to continue medication regimen. Recommended lifestyle modifications.
"""

        img = generate_scanned_page(text)
        img_path = "page_temp.jpg"
        img.save(img_path)

        pdf.add_page()
        pdf.image(img_path, 0, 0, 1700, 2200)

    pdf.output(str(output_path))


def generate_zip():
    out_dir = Path("synthetic_aps")
    out_dir.mkdir(exist_ok=True)

    files = [
        ("APS_John_Doe_2020.pdf", "John Doe"),
        ("APS_Jane_Smith_2019.pdf", "Jane Smith"),
        ("APS_Robert_Brown_2021.pdf", "Robert Brown"),
    ]

    pdf_paths = []

    for fname, name in files:
        pdf_path = out_dir / fname
        print(f"Generating {fname} (300 pages)...")
        generate_aps_pdf(pdf_path, name, pages=300)
        pdf_paths.append(pdf_path)

    zip_path = Path("aps_scanned_sample.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for pdf in pdf_paths:
            zf.write(pdf, arcname=pdf.name)

    print(f"\nCreated ZIP: {zip_path.resolve()}")


if __name__ == "__main__":
    generate_zip()