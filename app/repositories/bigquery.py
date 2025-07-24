from google.cloud import bigquery
from datetime import datetime
from typing import List, Dict
import logging

from app.models.device_update import DeviceUpdate


class BigQueryRepository:
    """Repository for batch inserting device updates or fetching them per hour.

    This class provides functionality to interact with Google BigQuery, specifically
    for handling batch insertions of device updates and fetching aggregated device
    data on an hourly basis.
    """

    def __init__(self, project_id: str):
        """Initializes the BigQueryRepository with the given project ID.

        Args:
            project_id (str): The Google Cloud project ID where the BigQuery dataset resides.

        Attributes:
            logger: Logger for logging information and errors.
            client: BigQuery client used for interacting with BigQuery.
        """
        self.logger = logging.getLogger("BigQueryRepository")
        self.client = bigquery.Client(project=project_id)

        self.logger.info("Initialized BigQueryRepository with project: %s", project_id)

    def batch_insert_device_updates(
        self, device_updates: List[DeviceUpdate], table_id: str
    ):
        """Inserts a batch of device updates into a specified BigQuery table.

        Args:
            device_updates (List[DeviceUpdate]): A list of DeviceUpdate objects to be inserted.
            table_id (str): The BigQuery table ID to insert the updates into.

        Raises:
            Exception: If there is an error during the batch insert operation.
        """
        rows_to_insert = [
            {
                "device_id": update.device_id,
                "product_id": update.product_id,
                "code": update.code,
                "value": update.value,
                "time": update.time.isoformat(),
            }
            for update in device_updates
        ]

        try:
            errors = self.client.insert_rows_json(table_id, rows_to_insert)
            if errors:
                self.logger.error("Errors while inserting rows: %s", errors)
            else:
                self.logger.info(
                    "Successfully inserted batch of %d rows.", len(rows_to_insert)
                )
        except Exception as e:
            self.logger.error("Exception during batch insert: %s", str(e))
            raise Exception("Couldn't store the updates")

    def fetch_device_updates_per_hour(
        self, table_id: str, start_at: datetime, end_at: datetime
    ) -> List[Dict]:
        """Fetches device updates aggregated per hour from a specified BigQuery table.

        This method queries the specified table and returns the total value of device
        updates for each hour within the given time range.

        Args:
            table_id (str): The BigQuery table ID to query.
            start_at (datetime): Start time of the interval.
            end_at (datetime): End time of the interval.

        Returns:
            List[Dict]: A list of dictionaries containing the hour timestamp and the total value of device updates.

        Raises:
            Exception: If there is an error during the query operation.
        """
        query = """
            SELECT
                TIMESTAMP_TRUNC(time, HOUR) as time_hour,
                SUM(value) as total_value
            FROM `@table_id`
            WHERE time BETWEEN @start_at AND @end_at
            GROUP BY time_hour
            ORDER BY time_hour
        """
        try:
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("table_id", "STRING", table_id),
                    bigquery.ScalarQueryParameter("start_at", "TIMESTAMP", start_at),
                    bigquery.ScalarQueryParameter("end_at", "TIMESTAMP", end_at),
                ]
            )
            query_job = self.client.query(query, job_config=job_config)
            results = query_job.result()

            output = []
            for row in results:
                output.append(
                    {
                        "time_hour": row.time_hour.isoformat(),
                        "total_value": row.total_value,
                    }
                )

            return output
        except Exception as e:
            self.logger.error("Exception during updates query: %s", str(e))
            raise Exception("Failed to fetch updates")


# Example usage:
# repository = BigQueryRepository('your_project_id')
# update = DeviceUpdate(device_id='device1', product_id='product1', code='update_code', value=123, time=datetime.now())
# repository.insert_device_update(update, 'your_project.your_dataset.your_table')
