from typing import Dict
from datetime import datetime
import logging

from app.repositories.bigquery import BigQueryRepository


class ReportService:
    """Service for generating reports based on device data."""

    def __init__(self, project_id: str, table_id: str):
        self.logger = logging.getLogger("ReportService")
        self.bigquery_repo = BigQueryRepository(project_id)
        self.table_id = table_id

        self.logger.info("Initialized ReportService with project: %s", project_id)


def generate_report(
    self, start_at: datetime, end_at: datetime
) -> Dict[str, Dict[str, int]]:
    """Generates a report of device updates between the specified start and end times.

    Args:
        start_at (datetime): Start time of the report period.
        end_at (datetime): End time of the report period.

    Returns:
        Dict: A dictionary containing the report data structured by date and hour.
    """
    try:
        report_data = self.bigquery_repo.fetch_device_updates_per_hour(
            table_id=self.table_id,
            start_at=start_at,
            end_at=end_at,
        )

        report = {}

        for entry in report_data:
            time_hour = datetime.fromisoformat(entry["time_hour"])
            date_key = time_hour.strftime("%Y-%m-%d")
            hour_key = time_hour.strftime("%H:00")
            value = entry["total_value"]

            if date_key not in report:
                report[date_key] = {}

            report[date_key][hour_key] = value

        self.logger.info(
            "Generated a report"
        )
        return report
    except Exception as e:
        self.logger.error(f"Failed to generate report: {str(e)}")
        raise Exception("Failed to generate report.")
