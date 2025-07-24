from fastapi import APIRouter, HTTPException

from app.schemas.message import Message, MessageResponse
from app.services import device

device_service = device.DeviceService("", "")

router = APIRouter()


@router.post("/message", response_model=MessageResponse)
def post_message(message: Message):
    try:
        updates = device_service.process_device_message(message)
        # NOTE: uncomment when connected to bigquery
        # device_service.store_device_updates(updates)
        return MessageResponse(status="success")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        return HTTPException(status_code=502, detail=str(e))


# TODO: @router.post("/send", response_model=)
