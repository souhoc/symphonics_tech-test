from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..models.devices import Message
from ..services.bigquery import BigQueryClientDependency

router = APIRouter()


@router.post("/message")
async def post_message(message: Message, bq_client: BigQueryClientDependency):
    try:
        device_message = message.get_device_message()
        if device_message.bizCode != "devicePropertyMessage":
            return {"status": "no actions"}

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

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/send/{device_id}")
async def post_command(device_id: str, switch: bool):
    try:
        command_message = {"switch": switch, "devId": device_id}
        # TODO: Publish command_message to PubSub
        pass

        return {"status": "command sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
