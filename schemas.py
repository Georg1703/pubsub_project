from pydantic import BaseModel, Field
from datetime import datetime


class SensorDataInputSchema(BaseModel):
    sensor_id: str = Field(alias='v0')
    dwell_time: float = Field(alias='v18')
    timestamp: datetime = Field(alias='Time')

class SensorDataOutputSchema(BaseModel):
    sensor_id: str
    dwell_time: float
    timestamp: datetime

class MessageAttributesSchema(BaseModel):
    key: str

class MessageSchema(BaseModel):
    attributes: MessageAttributesSchema
    data: str
    messageId: str
    message_id: str
    publishTime: str
    publish_time: str

class SubscriptionPayloadSchema(BaseModel):
    message: MessageSchema
    subscription: str