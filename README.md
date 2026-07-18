# ResumeShortlistingAI

ResumeShortlistingAI is an AI-powered resume screening system developed for the InternLoom Hackathon 2026. It allows recruiters to upload multiple resume PDFs, extract candidate information, evaluate resumes against a selected job description, rank applicants, and export shortlisted results.

## Features

- Upload multiple PDF resumes
- Automatic PDF parsing
- Candidate information extraction
- Skill extraction
- CGPA extraction
- Project counting
- Required vs Preferred skill matching
- ATS Score (0–100)
- Parse Quality
- Confidence Level
- Candidate Ranking
- Shortlisted / Reserve Status
- CSV export
- Interactive recruiter dashboard

## Technology Stack

- Python
- Streamlit
- PyMuPDF
- Pandas
- Regex

## Folder Structure

- app.py
- parser.py
- matcher.py
- scorer.py
- requirements.txt
- README.md
- Design_Decisions.md
- AI_Usage_Log.md
- Parse_Report.csv

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Authors

InternLoom Hackathon Team
