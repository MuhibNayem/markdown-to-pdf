from pydantic import BaseModel, Field
from typing import Optional

class PDFRequest(BaseModel):
    content: str = Field(..., description="JSON string containing title and summary")
    filename: Optional[str] = Field("document", description="Output filename (without extension)")

class PDFResponse(BaseModel):
    message: str
    download_url: str