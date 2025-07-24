from fastapi import APIRouter, HTTPException, Path,Depends
from datetime import datetime
import logging
import os

from app.services.report import ReportService, get_report_service
from app.schemas.report import ReportResponse

logger = logging.getLogger("reportEndpoint")


router = APIRouter()


@router.get("/report", response_model=ReportResponse)
def get_report(
    start_at: datetime = Path(..., description="Start time of the report period"),
    end_at: datetime = Path(..., description="End time of the report period"),
    report_service: ReportService = Depends(get_report_service)
):
    try:
        if start_at >= end_at:
            raise ValueError("start_at must be before end_at")

        formatted_report = report_service.generate_report(start_at, end_at)
        return formatted_report
    except ValueError as e:
        logger.error(f"Failed to get the report on value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get the report: {str(e)}")
        raise HTTPException(status_code=502)
