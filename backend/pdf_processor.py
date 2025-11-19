import os
import boto3
import fitz  # PyMuPDF
import pickle

# ------------ S3 SETTINGS ------------
S3_BUCKET = os.getenv("AWS_BUCKET_NAME")
PDF_KEYS = [
    "Chemistry_updated.pdf",
    "Physics_updated.pdf"
]

LOCAL_PDF_FOLDER = "pdfs/"
CACHED_TEXT_FILE = "cached_pdf_text.pkl"

# S3 CLIENT
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)


# ------------ DOWNLOAD PDFs FROM S3 ------------
def download_pdfs_from_s3():
    if not os.path.exists(LOCAL_PDF_FOLDER):
        os.makedirs(LOCAL_PDF_FOLDER)

    for key in PDF_KEYS:
        local_path = os.path.join(LOCAL_PDF_FOLDER, key)

        if not os.path.exists(local_path):
            print(f"📥 Downloading {key} from S3...")
            s3.download_file(S3_BUCKET, key, local_path)

        else:
            print(f"✔ {key} already exists locally — skipping.")


# ------------ EXTRACT TEXT USING FITZ ------------
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


# ------------ PROCESS ALL PDFs (ONLY ONCE) ------------
def process_pdfs_from_s3():
    # load cached text if available
    if os.path.exists(CACHED_TEXT_FILE):
        print("✔ Loading cached PDF text…")
        return pickle.load(open(CACHED_TEXT_FILE, "rb"))

    print("📥 Downloading PDFs from S3…")
    download_pdfs_from_s3()

    print("📘 Extracting text from PDFs…")
    all_text = ""

    for key in PDF_KEYS:
        pdf_path = os.path.join(LOCAL_PDF_FOLDER, key)
        text = extract_text_from_pdf(pdf_path)
        all_text += text + "\n\n"

    print("💾 Caching extracted text…")
    pickle.dump(all_text, open(CACHED_TEXT_FILE, "wb"))

    return all_text
