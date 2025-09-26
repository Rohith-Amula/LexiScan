# LexiScan
# LexiScan

LexiScan is an OCR (Optical Character Recognition) and text-correction project that:

- Extracts text from scanned or uploaded images (handwritten or printed) using Tesseract OCR.
- Applies grammar correction using a T5 transformer model (Hugging Face).
- Provides a Streamlit web interface for uploading images, viewing corrected text, and exporting the results in multiple formats.


## 🚀 Features
- OCR for both printed and handwritten text
- Grammar and sentence-structure correction
- Export results as PDF, DOCX, TXT, etc.
- Simple and interactive Streamlit UI


## 🛠️ Tech Stack
- Python 3
- Tesseract OCR
- Hugging Face Transformers (T5 model)
- Streamlit
- OpenCV / Pillow (for image handling)


## ⚡ Quick Start

### 1. Clone the repository

git clone https://github.com/<your-username>/LexiScan.git
cd LexiScan

2. Install dependencies

pip install -r requirements.txt
3. Run the Streamlit app

streamlit run app.py
Open the given URL (usually http://localhost:8501) in your browser
