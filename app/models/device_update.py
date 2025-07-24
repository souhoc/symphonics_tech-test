from pydantic import BaseModel, validator
from datetime import datetime


class DeviceUpdate(BaseModel):
    device_id: str  # XXX: might want to make it uuid
    product_id: str
    code: str
    value: int
    time: datetime

    @validator("time")
    def check_time(cls, v: datetime):
        if v.minute != 0 or v.second != 0 or v.microsecond != 0:
            raise ValueError("Time must be on the hour.")
        return v
