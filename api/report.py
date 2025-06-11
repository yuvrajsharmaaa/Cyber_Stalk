from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import json
import os
from datetime import datetime
import uuid
import boto3
from botocore.exceptions import ClientError

from database import get_db
from models import CyberReport

router = APIRouter()

# AWS S3 Configuration
S3_BUCKET = os.getenv('AWS_S3_BUCKET')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

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
        
        # Handle file uploads to S3
        evidence_files = []
        if evidence:
            for file in evidence:
                file_key = f"evidence/{reference_id}/{file.filename}"
                try:
                    # Upload file to S3
                    s3_client.upload_fileobj(
                        file.file,
                        S3_BUCKET,
                        file_key,
                        ExtraArgs={'ACL': 'public-read'}
                    )
                    
                    # Generate the URL for the uploaded file
                    file_url = f"https://{S3_BUCKET}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
                    evidence_files.append(file_url)
                except ClientError as e:
                    raise HTTPException(status_code=500, detail=f"Failed to upload file to S3: {str(e)}")
        
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