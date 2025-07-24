from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
import logging
import re

from app.schemas.message import Message, MessageResponse
from app.schemas.command import CommandResponse
from app.services.device import DeviceService, get_device_service


logger = logging.getLogger("deviceEndpoint")

router = APIRouter(prefix="/devices")


@router.post("/message", response_model=MessageResponse)
def post_message(
    message: Message = Body(..., description="Message from pubsub"),
    device_service: DeviceService = Depends(get_device_service)
):
    try:
        updates = device_service.process_device_message(message)
        # NOTE: uncomment when connected to bigquery
        # device_service.store_device_updates(updates)
        return MessageResponse(status="success")
    except ValueError as e:
        logger.error(f"Failed handle a message on value error: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid input provided")
    except Exception as e:
        logger.error(f"Failed handle a message: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/{device_id}/send", response_model=CommandResponse)
def post_device_send(
    device_id: str = Path(
        ..., description="Device's id to which the commend must be sent"
    ),
    switch: bool = Query(False, description="The value to send"),
    device_service: DeviceService = Depends(get_device_service)
):
    if not re.match(r"^[a-zA-Z0-9_-]+$", device_id):
        raise HTTPException(status_code=400, detail="Invalid device ID format")

    try:
        # NOTE: uncomment when connected to pubsub
        # device_service.send_switch_message(device_id, switch)
        return CommandResponse(status="success")
    except Exception as e:
        logger.error(f"Failed handle a message: {str(e)}")
        raise HTTPException(status_code=400, detail="Unexpected error occured")
