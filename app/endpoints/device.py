from fastapi import APIRouter, HTTPException, Path, Query, Body

from app.schemas.message import Message, MessageResponse
from app.schemas.command import CommandResponse
from app.services import device

device_service = device.DeviceService("", "")

router = APIRouter(prefix="/devices")


@router.post("/message", response_model=MessageResponse)
def post_message(message: Message = Body(..., description="Message from pubsub")):
    try:
        updates = device_service.process_device_message(message)
        # NOTE: uncomment when connected to bigquery
        # device_service.store_device_updates(updates)
        return MessageResponse(status="success")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=502)  # no detail for unexpected error


@router.post("/{device_id}/send", response_model=CommandResponse)
def post_device_send(
    device_id: str = Path(
        ..., description="Device's id to which the commend must be sent"
    ),
    switch: bool = Query(False, description="The value to send"),
):
    try:
        # NOTE: uncomment when connected to pubsub
        # device_service.send_switch_message(device_id, switch)
        return CommandResponse(status="success")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
