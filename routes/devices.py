from fastapi import APIRouter, HTTPException
from datetime import datetime
import json

from ..models.devices import Message, Status
from ..services.bigquery import BigQueryClientDependency
from ..services.pubsub import PubSubPublisherClientDependency

router = APIRouter()


@router.post("/message")
def post_message(message: Message, bq_client: BigQueryClientDependency)->Status:
    try:
        device_message = message.get_device_message()
        if device_message.bizCode != "devicePropertyMessage":
            return Status("no actions")

        data = device_message.bizData

        rows_to_insert = []

        for property in data.properties:
            if property.code in ["instant_power", "temp_interior"]:
                entry = {
                    "dev_id": data.devId,
                    "product_id": data.productId,
                    "code": property.code,
                    "value": property.value,
                    "time": datetime.fromtimestamp(property.time / 1000).strftime(
                        "%Y-%m-%d %H:00"
                    ), # Time need to be precise up to the hour
                }
                rows_to_insert.append(entry)

        # Write to BigQuery
        if rows_to_insert:
            table_id = "project_id.dataset.devices_properties"  # XXX: get it from env

            errors = bq_client.insert_rows_json(table_id, rows_to_insert)
            if errors:
                raise HTTPException(
                    status_code=502, detail="Failed to insert"
                )  # Better not precise the stack

        return Status("success")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send/{device_id}")
def post_command(device_id: str, switch: bool, publisher_client: PubSubPublisherClientDependency) -> Status:
    try:
        command_message = {"switch": switch, "devId": device_id}

        project_id = "project-id" # XXX: get it from env
        topic_id = "send_command" # XXX: can be moved in env or config file 

        topic_path = publisher_client.topic_path(project_id, topic_id)

        message_json = json.dumps(command_message)
        message_bytes = message_json.encode('utf-8')

        future = publisher_client.publish(topic_path, message_bytes)
        message_id = future.result()
        print(f"Message {message_id} send to {device_id}")

        return Status("command sent")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
