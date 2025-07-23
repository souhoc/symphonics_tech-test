from fastapi import APIRouter,HTTPException

from ..models.devices import Message 

router = APIRouter()

@router.post("/message")
async def receive_message(message: Message):
    try:
        device_message  = message.get_device_message()

        print("div_msg: ", device_message)
        if device_message.bizCode != "devicePropertyMessage":
            return {"status": "no actions"}

        data = device_message.bizData

        # Get the wanted data
        for property in device_message.bizData.properties:
            if property.code in ["instant_power", "temp_interior"]:
                print(property)
                entry = {
                    "dev_id": data.devId,
                    "product_id": data.productId,
                    "code": property.code,
                    "value": property.value,
                    "time": property.time, # XXX: save time in %Y-%m-%d %H:00
                }
                # TODO: save entry to BigQuery
                pass

        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/send/{device_id}")
async def send_command(device_id: str, switch: bool):
    try:
        command_message = {
            "switch": switch,
            "devId": device_id
        }
        # TODO: Publish command_message to PubSub
        pass

        return {"status": "command sent"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
