from typing import List
import json
import base64
import binascii

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError

from schemas import SubscriptionPayloadSchema, SensorDataInputSchema, SensorDataOutputSchema
from database import get_db, SensorDataModel


app = FastAPI()

def get_deserialized_data(data: str) -> dict:
    decoded_bytes = base64.b64decode(data)
    decoded_str = decoded_bytes.decode('utf-8')
    return json.loads(decoded_str)

def save_sensor_data(db, data: SensorDataInputSchema):
    sensor_data_model = SensorDataModel(**data.model_dump())
    db.add(sensor_data_model)
    db.commit()


@app.post("/receive/", status_code=status.HTTP_202_ACCEPTED)
def receive(payload: SubscriptionPayloadSchema, db: Session = Depends(get_db)):
    """
        Receives data from Pub/Sub push subscription and save it in the db
    """

    try:
        data = get_deserialized_data(payload.message.data)
    except (UnicodeDecodeError, json.JSONDecodeError, binascii.Error) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:
        sensor_data = SensorDataInputSchema(**data)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))

    save_sensor_data(db, sensor_data)


@app.get("/provide/", response_model=List[SensorDataOutputSchema])
async def provide(db: Session = Depends(get_db)):
    """
        Returns all existing fata from SensorDataModel
    """
    sensor_data = db.query(SensorDataModel).all()
    return sensor_data