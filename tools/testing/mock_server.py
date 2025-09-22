#!/usr/bin/env python3
"""
Mock API server for Tavo SDK testing
"""

from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Tavo Mock API", version="1.0.0")

# Constants
TIMESTAMP_1 = "2023-01-01T00:00:00Z"
TIMESTAMP_2 = "2023-01-01T00:00:01Z"


# Data models
class ScanRequest(BaseModel):
    repository_url: str
    scan_type: Optional[str] = "security"
    branch: Optional[str] = "main"
    commit: Optional[str] = None


class ScanResponse(BaseModel):
    id: str
    status: str
    repository_url: str
    scan_type: str
    created_at: str
    updated_at: str
    results: Optional[Dict] = None


class ReportResponse(BaseModel):
    id: str
    scan_id: str
    status: str
    created_at: str
    findings: List[Dict]


# In-memory storage
scans_db: Dict[str, ScanResponse] = {}
reports_db: Dict[str, ReportResponse] = {}
scan_counter = 0
report_counter = 0


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": TIMESTAMP_1,
        "version": "1.0.0"
    }


@app.post("/api/v1/scans")
async def create_scan(request: ScanRequest):
    """Create a new scan"""
    global scan_counter
    scan_counter += 1
    scan_id = f"scan-{scan_counter}"

    scan = ScanResponse(
        id=scan_id,
        status="pending",
        repository_url=request.repository_url,
        scan_type=request.scan_type or "security",
        created_at=TIMESTAMP_1,
        updated_at=TIMESTAMP_1
    )

    scans_db[scan_id] = scan

    # Simulate async processing - mark as completed after creation
    scan.status = "completed"
    scan.updated_at = TIMESTAMP_2
    scan.results = {
        "vulnerabilities": [
            {
                "id": "vuln-1",
                "severity": "high",
                "title": "Test vulnerability",
                "description": "This is a test vulnerability for testing"
            }
        ],
        "summary": {
            "total_vulnerabilities": 1,
            "critical_count": 0,
            "high_count": 1,
            "medium_count": 0,
            "low_count": 0
        }
    }

    return scan


@app.get("/api/v1/scans/{scan_id}")
async def get_scan(scan_id: str):
    """Get scan details"""
    if scan_id not in scans_db:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scans_db[scan_id]


@app.get("/api/v1/scans")
async def list_scans(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = None
):
    """List scans"""
    scans = list(scans_db.values())

    if status:
        scans = [s for s in scans if s.status == status]

    total = len(scans)
    scans = scans[offset:offset + limit]

    return {
        "scans": scans,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@app.get("/api/v1/reports/{report_id}")
async def get_report(report_id: str):
    """Get report details"""
    if report_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found")
    return reports_db[report_id]


@app.get("/api/v1/reports")
async def list_reports(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    scan_id: Optional[str] = None
):
    """List reports"""
    reports = list(reports_db.values())

    if scan_id:
        reports = [r for r in reports if r.scan_id == scan_id]

    total = len(reports)
    reports = reports[offset:offset + limit]

    return {
        "reports": reports,
        "total": total,
        "limit": limit,
        "offset": offset
    }


@app.on_event("startup")
async def startup_event():
    """Initialize some test data"""
    # Create a sample scan and report
    scan = ScanResponse(
        id="sample-scan-1",
        status="completed",
        repository_url="https://github.com/test/repo",
        scan_type="security",
        created_at=TIMESTAMP_1,
        updated_at=TIMESTAMP_2,
        results={
            "vulnerabilities": [],
            "summary": {
                "total_vulnerabilities": 0,
                "critical_count": 0,
                "high_count": 0,
                "medium_count": 0,
                "low_count": 0
            }
        }
    )
    scans_db[scan.id] = scan

    report = ReportResponse(
        id="sample-report-1",
        scan_id=scan.id,
        status="completed",
        created_at=TIMESTAMP_2,
        findings=[]
    )
    reports_db[report.id] = report


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
