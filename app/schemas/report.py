from pydantic import BaseModel
from typing import Dict


class ReportResponse(BaseModel):
    """
    Represents a complete report with dates as keys and hourly data as nested dictionaries.
    """

    data: Dict[str, Dict[str, int]]

    class Config:
        schema_extra = {
            "example": {
                "data": {
                    "2025-01-01": {"00:00": 24577, "01:00": 42304, "23:00": 99228},
                    "2025-01-02": {"00:00": 15477, "01:00": 31200, "23:00": 80210},
                }
            }
        }
