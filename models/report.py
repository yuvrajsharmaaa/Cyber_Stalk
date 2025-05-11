from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from config.database import Base

class CyberReport(Base):
    __tablename__ = "cyber_reports"

    id = Column(Integer, primary_key=True, index=True)
    incident_type = Column(String(100))
    first_occurrence = Column(DateTime)
    recent_occurrence = Column(DateTime)
    description = Column(Text)
    evidence_files = Column(Text)  # Store file paths as JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="pending")
    reference_id = Column(String(50), unique=True) 