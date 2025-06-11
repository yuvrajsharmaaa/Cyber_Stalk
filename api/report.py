from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
import os
from datetime import datetime
import uuid

from database import get_db
from models import CyberReport

router = APIRouter()

UPLOAD_DIR = "uploads"

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/report/homepage")
async def create_report(
    incident_type: str,
    first_occurrence: datetime,
    recent_occurrence: datetime,
    description: str,
    evidence: List[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        # Generate unique reference ID
        reference_id = f"CSB-{uuid.uuid4().hex[:8].upper()}"
        
        # Handle file uploads
        evidence_files = []
        if evidence:
            for file in evidence:
                file_path = os.path.join(UPLOAD_DIR, f"{reference_id}_{file.filename}")
                with open(file_path, "wb") as f:
                    f.write(await file.read())
                evidence_files.append(file_path)
        
        # Create report in database
        report = CyberReport(
            incident_type=incident_type,
            first_occurrence=first_occurrence,
            recent_occurrence=recent_occurrence,
            description=description,
            evidence_files=json.dumps(evidence_files),
            reference_id=reference_id
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return {
            "status": "success",
            "message": "Report submitted successfully",
            "reference_id": reference_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/{reference_id}")
def get_report(reference_id: str, db: Session = Depends(get_db)):
    report = db.query(CyberReport).filter(CyberReport.reference_id == reference_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report 