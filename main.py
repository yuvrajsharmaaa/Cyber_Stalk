from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
from database import SessionLocal, engine
from models import Base, Report, EvidenceFile
from typing import Optional, List
import aiofiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api import report
from datetime import datetime

def safe_parse_date(date_str):
    try:
        # Accepts 'YYYY-MM-DD' or 'YYYY-MM-DDTHH:MM:SS' (ISO format)
        return datetime.fromisoformat(date_str)
    except Exception:
        return None

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cyberstalking Report System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/public", StaticFiles(directory="public"), name="public")

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(report.router, prefix="/api")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/report/homepage")
async def submit_report(
    incident_type: str = Form(...),
    first_occurrence: str = Form(...),
    recent_occurrence: str = Form(...),
    description: str = Form(...),
    legal_compliance: bool = Form(False),
    user_email: Optional[str] = Form(None),
    evidence: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Safely parse dates
        first_occurrence_dt = safe_parse_date(first_occurrence)
        recent_occurrence_dt = safe_parse_date(recent_occurrence)

        if not first_occurrence_dt or not recent_occurrence_dt:
            raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY-MM-DD.")

        # Create report
        report = Report(
            incident_type=incident_type,
            first_occurrence=first_occurrence_dt,
            recent_occurrence=recent_occurrence_dt,
            description=description,
            legal_compliance=legal_compliance,
            user_email=user_email
        )
        db.add(report)
        db.flush()  # Get the report ID without committing

        # Handle file uploads
        for file in evidence:
            # Validate file size (max 25MB)
            file_size = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            while chunk := await file.read(chunk_size):
                file_size += len(chunk)
                if file_size > 25 * 1024 * 1024:  # 25MB limit
                    raise HTTPException(status_code=400, detail=f"File {file.filename} too large. Maximum size is 25MB")
            
            # Reset file pointer
            await file.seek(0)
            
            # Create safe filename
            safe_filename = f"{report.id}_{file.filename.replace(' ', '_')}"
            file_location = os.path.join(UPLOAD_DIR, safe_filename)
            
            # Save file
            async with aiofiles.open(file_location, 'wb') as buffer:
                while chunk := await file.read(chunk_size):
                    await buffer.write(chunk)
            
            # Save file metadata to DB
            evidence_file = EvidenceFile(
                report_id=report.id,
                original_filename=file.filename,
                stored_filename=safe_filename,
                file_path=file_location,
                file_type=file.content_type,
                file_size=file_size
            )
            db.add(evidence_file)
        
        db.commit()
        return {
            "message": "Report submitted successfully",
            "report_id": report.id
        }
        
    except Exception as e:
        db.rollback()
        # Clean up any uploaded files if there was an error
        if 'report' in locals() and report.id:
            for evidence_file in report.evidence_files:
                if os.path.exists(evidence_file.file_path):
                    os.remove(evidence_file.file_path)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
def get_reports(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    reports = db.query(Report).offset(skip).limit(limit).all()
    return reports

@app.get("/")
async def root():
    return {"message": "Welcome to the File Upload API"} 