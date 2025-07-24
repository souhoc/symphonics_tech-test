from typing import List, Dict
from datetime import datetime
import logging
import json

from app.schemas.message import Message, DeviceMessage
from app.models.device_update import DeviceUpdate
from app.repositories.bigquery import BigQueryRepository
from app.repositories.pubsub import PubSubRepository

MAX_JSON_SIZE = 1024 * 1024  # Let's make the max size to a json to 1M


class DeviceService:
    """
    Service handle device operations, message processing, and data management
    """

    def __init__(self, project_id: str, table_id: str):
        self.logger = logging.getLogger("DeviceService")
        self.bigquery_repo = BigQueryRepository(project_id)
        self.pubsub_repo = PubSubRepository(project_id)
        self.table_id = table_id

        self.logger.info(
            "Initialized DeviceService with project: %s, table: %s",
            project_id,
            table_id,
        )

    def get_device_message(self, message: Message) -> DeviceMessage:
        if not message.data or not message.data.strip():
            raise ValueError("Missing or empty data in message")

        if len(message.data) > MAX_JSON_SIZE:
            raise ValueError("Message payload too large")

        try:
            message_dict = json.loads(message.data)
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON data: {str(e)}")
            raise ValueError("Invalid JSON data")

        if "data" not in message_dict:
            raise ValueError("Missing 'data' in message")

        data_dict = message_dict["data"]
        return DeviceMessage(**data_dict)

    def process_device_message(self, message: Message) -> List[DeviceUpdate]:
        """
        Process a PubSub message and convert it to DeviceUpdate objects
        Returns a list of DeviceUpdate objects (one per property)
        """
        try:
            device_message = self.get_device_message(message)

            device_updates = []
            for property in device_message.bizData.properties:
                if property.code not in ["instant_power", "temp_interior"]:
                    continue
                device_update = DeviceUpdate(
                    device_id=device_message.bizData.devId,
                    product_id=device_message.bizData.productId,
                    code=property.code,
                    value=property.value,
                    time=datetime.fromtimestamp(property.time / 1000).replace(
                        minute=0, second=0, microsecond=0
                    ),  # Round to the hour
                )
                device_updates.append(device_update)

            devId = "***" + device_message.bizData.devId[-4:]  # sanitize id
            self.logger.info(
                f"Processed message for device {devId}: "
                f"{len(device_updates)} updates"
            )

            return device_updates

        except ValueError as e:
            self.logger.error(f"Failed processing device message: {str(e)}")
            raise e
        except Exception as e:
            self.logger.error(f"Failed processing device message: {str(e)}")
            raise ValueError(f"Failed to process device message: {str(e)}")

    def store_device_updates(self, device_updates: List[DeviceUpdate]):
        """
        Store device updates in BigQuery
        """
        try:
            self.bigquery_repo.batch_insert_device_updates(
                device_updates, self.table_id
            )

            self.logger.info(
                f"Successfully stored {len(device_updates)} device updates"
            )

        except Exception as e:
            self.logger.error(f"Error storing device updates: {str(e)}")
            raise Exception("Error storing device updates")

    def get_device_data(self, start_at: datetime, end_at: datetime) -> List[Dict]:
        """
        Retrieve aggregated device data for a time range
        """
        if start_at >= end_at:
            raise ValueError("start_at must be before end_at")

        try:
            return self.bigquery_repo.fetch_device_updates_per_hour(
                self.table_id, start_at, end_at
            )
        except Exception as e:
            self.logger.error(f"Error fetching device data: {str(e)}")
            raise Exception(f"Failed to fetch device data: {str(e)}")

    def send_switch_message(self, device_id: str, switch: bool):
        """
        Sends a switch command message for a device via Pub/Sub.

        Args:
            device_id (str): The ID of the device to send the command to.
            switch (bool): The switch state to send (True for ON, False for OFF).

        Raises:
            Exception: If there is an error while sending the message.
        """
        try:
            command_message = {"switch": switch, "devId": device_id}

            # Convert the command message to a JSON string
            message_data = json.dumps(command_message)

            # Publish the message to the topic
            message_id = self.pubsub_repo.publish_message(
                topic_name="send_command",  # Topic name for sending commands
                message_data=message_data,
            )

            self.logger.info(
                f"Sent switch command (state: {switch}) to device {device_id}. Message ID: {message_id}"
            )

        except Exception as e:
            self.logger.error(f"Failed to send switch message: {str(e)}")
            raise Exception("Failed to send switch message")
