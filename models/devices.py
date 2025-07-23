from pydantic import BaseModel
import json

class Property(BaseModel):
    code: str
    dpId: int
    time: int
    value: float

class BizData(BaseModel):
    devId: str
    dataId: str
    productId: str
    properties: list[Property]

class DeviceMessage(BaseModel):
    bizCode: str
    bizData: BizData
    ts: int

# PubSub message
class Message(BaseModel):
    data: str
    attributes: dict
    messageId: str
    publishTime: str
    orderingKey: str
    def get_device_message(self) -> DeviceMessage:
            message_dict = json.loads(self.data)

            # DeviceMessage is in data.data
            data_dict = message_dict['data']

            return DeviceMessage(**data_dict)
