from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from .models import PDFRequest, PDFResponse
from .pdf_generator import PDFGenerator
from .utils import validate_file_path, cleanup_old_files
import os
import json

app = FastAPI(
    title="Text to PDF API",
    description="Convert JSON content with markdown to PDF documents",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-pdf/", response_model=PDFResponse)
async def generate_pdf(request: PDFRequest, background_tasks: BackgroundTasks):
    try:
        try:
            json.loads(request.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON content")
        
        file_path = PDFGenerator.create_pdf(
            content=request.content,
            filename=request.filename or "document"
        )
        
        background_tasks.add_task(cleanup_old_files, "output")
        
        return PDFResponse(
            message="PDF generated successfully",
            download_url=f"/download-pdf/{os.path.basename(file_path)}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/download-pdf/{filename}")
async def download_pdf(filename: str):
    file_path = os.path.join("output", filename)
    validate_file_path(file_path)
    
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=filename
    )

@app.get("/")
async def root():
    return {"message": "Text to PDF API is running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)