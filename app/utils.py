import os
from fastapi import HTTPException

def validate_file_path(file_path: str) -> None:
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF file not found")
    
    if not file_path.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format")

def cleanup_old_files(directory: str, max_age_hours: int = 24) -> None:
    """Clean up files older than specified hours"""
    import time
    current_time = time.time()
    
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_hours * 3600:
                os.remove(file_path)