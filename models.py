from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Report(Base):
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String, nullable=False)
    first_occurrence = Column(DateTime, nullable=False)
    recent_occurrence = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    legal_compliance = Column(Boolean, default=False)
    user_email = Column(String, nullable=True)
    status = Column(String, default="Active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with evidence files
    evidence_files = relationship("EvidenceFile", back_populates="report")

class EvidenceFile(Base):
    __tablename__ = "evidence_files"
    
    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    original_filename = Column(String, nullable=False)
    stored_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)  # e.g., 'image/jpeg', 'video/mp4'
    file_size = Column(Integer, nullable=False)  # Size in bytes
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with report
    report = relationship("Report", back_populates="evidence_files")