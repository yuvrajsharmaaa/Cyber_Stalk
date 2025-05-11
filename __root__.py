# ROOT PIPELINE: @noql -> 3691
# Reference: http://aquilify.vvfin.in/pipeline/root

# Warning: Avoid altering this __root__.py file; it serves as the main tunnel for your application.
# To prevent pipeline errors, refrain from interfering with or renaming this file.

from aquilify.core import Aquilify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
import os, shutil
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Report

# Importing the core project of Aquilify.

__instance__ = Aquilify()

# Warning: If using uvicorn or other ASGI Servers, refrain from using __file__ or __instance__ to run the server.
# Warning: Changing the default __instance__ name might lead to pipeline errors. Maintain the default naming convention to prevent issues.

# Visit http://aquilify.vvfin.in/pipeline/study for comprehensive information on customizing or modifying the pipeline.

# For further assistance, contact us at control@vvfin.in or confict.con@gmail.com.

# This __root__ file is a component of the Aquilify project governed by the BSD-4 Clause LICENSE.

DATABASE_URL = "postgresql://username:password@localhost:5432/yourdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/report/homepage")
async def submit_report(
    description: str = Form(...),
    user_email: str = Form(None),
    evidence: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save file
    file_location = os.path.join(UPLOAD_DIR, evidence.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(evidence.file, buffer)
    # Save to DB
    report = Report(
        user_email=user_email,
        description=description,
        file_path=file_location
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return {"message": "Report submitted successfully", "report_id": report.id}
