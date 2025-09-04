# Text to PDF API

FastAPI service to convert JSON content with markdown formatting to PDF documents.

## Features
- RESTful API for PDF generation
- Handles JSON content with title and markdown-formatted summary
- Converts markdown to structured PDF (headers, lists, bold text)
- Customizable font size and family
- Automatic file cleanup
- CORS enabled
- OpenAPI documentation

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate environment:
   - Windows: `.venv\Scripts\activate`
   - Unix: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the application: `uvicorn app.main:app --reload`

## API Usage
### Generate PDF
```http
POST /generate-pdf/
Content-Type: application/json

{
  "content": "{\"title\": \"John Doe's - Dialogue Summary\", \"summary\": \"# Patient Background\\n- **Age:** 62\\n- **Occupation:** Self-employed\\n\\n### Symptoms\\n- Difficulty with urination\\n- Recent fracture in the leg\"}",
  "filename": "medical_summary",
  "font_size": 12,
  "font_family": "Arial"
}