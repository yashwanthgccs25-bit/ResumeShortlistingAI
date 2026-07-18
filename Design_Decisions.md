# Design Decisions

## 1. PDF Parsing

The system uses **PyMuPDF (fitz)** to extract text from PDF resumes.

This approach was selected because it is lightweight, fast, and supports most digital PDF resumes. Text is extracted page by page and combined into a single document before further processing.

Known Limitation:
- Scanned image PDFs without embedded text are not fully supported. These are classified with lower parse quality.

---

## 2. Skill Extraction

Skills are extracted using a predefined technical skills database.

The complete resume text is scanned for occurrences of known technologies such as:

- Python
- Java
- SQL
- React
- Docker
- Git
- MongoDB
- AWS
- REST API

Skills are divided into:

- Required Skills
- Preferred Skills

based on the selected Job Description.

---

## 3. Resume Scoring

Candidates are evaluated using a weighted ATS score.

Weight Distribution:

- Required Skills → 60 Marks
- Preferred Skills → 20 Marks
- CGPA → 10 Marks
- Projects → 10 Marks

Maximum Score = 100

Candidates are ranked according to the final ATS score.

---

## 4. Parse Quality

Each resume receives a parse quality based on extracted text length.

- 🟢 Clean
- 🟡 Partial
- 🔴 Failed

Confidence is calculated using both parse quality and ATS score.

---

## Future Improvements

- OCR support for scanned resumes.
- Semantic skill matching using NLP.
- Better multi-column PDF parsing.
- Automatic Job Description parsing using LLMs.