from fastapi import APIRouter, HTTPException 

from ..models.report import Report
from ..services.bigquery import BigQueryClientDependency

router = APIRouter()

@router.get("/report")
async def get_report(start_at: str, end_at: str, bq_client: BigQueryClientDependency) -> Report:
    try:
        table_id = "project_id.dataset.devices_properties" # XXX: get it from env

        query = f"""
            SELECT
                TIMESTAMP_TRUNC(time, HOUR) as time_hour,
                SUM(value) as total_value
            FROM `{table_id}`
            WHERE time BETWEEN TIMESTAMP('{start_at}') AND TIMESTAMP('{end_at}')
            GROUP BY time_hour
            ORDER BY time_hour
        """

        query_job = bq_client.query(query)
        results = query_job.result()

        report: Report = {}
        for row in results:
            date_str = row.time_hour.strftime('%Y-%m-%d')
            hour_str = row.time_hour.strftime('%H:00')
            total_value = row.total_value

            if date_str not in report:
                report[date_str] = {}
            report[date_str][hour_str] = total_value

        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
