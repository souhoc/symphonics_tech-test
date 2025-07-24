from pydantic import BaseModel
from typing import List, Optional


class Property(BaseModel):
    code: str
    dpId: int
    time: int
    value: int


class BizData(BaseModel):
    devId: str
    dataId: str
    productId: str
    properties: List[Property]


class DeviceMessage(BaseModel):
    bizCode: str
    bizData: BizData
    ts: int


class Message(BaseModel):
    """ PubSub message """
    data: Optional[str]
    attributes: dict
    messageId: str
    publishTime: str
    orderingKey: str


class MessageResponse(BaseModel):
    status: str
