import fitz
import os

def extract_text(pdf_path):
    """
    Extract text from a PDF using PyMuPDF.
    """

    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

    except Exception as e:
        print(e)

    return text


def get_all_resume_texts(folder_path):

    resumes = []

    if not os.path.exists(folder_path):
        return resumes

    for file in os.listdir(folder_path):

        if file.lower().endswith(".pdf"):

            path = os.path.join(folder_path, file)

            text = extract_text(path)

            resumes.append({
                "filename": file,
                "text": text
            })

    return resumes