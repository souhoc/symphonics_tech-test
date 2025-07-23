from fastapi import APIRouter,HTTPException

from ..models.report import Report

router = APIRouter()

# TODO: see dependency injection for reading to BigQuery
@router.get("/report")
async def get_report(start_at: str, end_at: str) -> Report:
    try:
        # Get data from start to end
        # format
        report: Report = { }
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
