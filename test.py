import base64
import json
import binascii 

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_deserialized_data, save_sensor_data, SensorDataInputSchema
from database import Base, get_db, SensorDataModel


client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=StaticPool, connect_args={'check_same_thread':False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Helper function to serialize data to base64
def get_base64_encoded_data(data: dict) -> str:
    json_str = json.dumps(data)
    return base64.b64encode(json_str.encode('utf-8')).decode('utf-8')

def test_get_deserialized_data():
    original_data = {"key": "value"}
    encoded_data = get_base64_encoded_data(original_data)
    deserialized_data = get_deserialized_data(encoded_data)
    assert deserialized_data == original_data

def test_get_deserialized_data_invalid_base64():
    invalid_data = "eyJ2MCI6ICIswMDAxMCIsI"
    try:
        get_deserialized_data(invalid_data)
    except (UnicodeDecodeError, binascii.Error, json.JSONDecodeError):
        assert True

def test_save_sensor_data():
    db = next(override_get_db())
    sensor_data_input = SensorDataInputSchema(v0="12321", v18=42.0, Time="2024-01-01T00:00:00Z")
    save_sensor_data(db, sensor_data_input)
    saved_data = db.query(SensorDataModel).filter(SensorDataModel.sensor_id == sensor_data_input.sensor_id).first()

    assert saved_data is not None
    assert saved_data.sensor_id == sensor_data_input.sensor_id
    assert saved_data.dwell_time == sensor_data_input.dwell_time

def test_receive_valid_data():
    payload = {
        "message": {
            "attributes": {
                "key": "value"
            },
            "data":"eyJ2MCI6ICIwMDAxMCIsICJ2MTgiOiAiMy4xNCIsICJUaW1lIjogIjIwMjItMTEtMDhUMDQ6MDA6MDQuMzE3ODAxIiwgIlR5cGUiOiAieGtndyJ9",
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z"
        },
        "subscription": "projects/myproject/subscriptions/mysubscription"
    }
    response = client.post("/receive/", json=payload)
    assert response.status_code == 202
    assert response.json() is None

def test_receive_invalid_data():
    payload = {
        "message": {
            "data":"eyJ2MCI6ICIwMDAxMCIsICJ2MTgiOiAiMy4xNCIsICJUaW1lIjogIjIwMjItMTEtMDhUMDQ6MDA6MDQuMzE3ODAxIiwgIlR5cGUiOiAieGtndyJ9",
            "messageId": "2070443601311540",
        }
    }
    response = client.post("/receive/", json=payload)
    assert response.status_code == 422

def test_receive_invalid_json():
    invalid_json = base64.b64encode(b"invalid json").decode('utf-8')
    payload = {
        "message": {
            "attributes": {
                "key": "value"
            },
            "data": invalid_json,
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z"
        },
        "subscription": "projects/myproject/subscriptions/mysubscription"
    }
    response = client.post("/receive/", json=payload)
    assert response.status_code == 400

def test_receive_validation_error():
    payload = {
        "message": {
            "attributes": {
                "key": "value"
            },
            "data": get_base64_encoded_data({"key": "value"}),
            "messageId": "2070443601311540",
            "message_id": "2070443601311540",
            "publishTime": "2021-02-26T19:13:55.749Z",
            "publish_time": "2021-02-26T19:13:55.749Z"
        },
        "subscription": "projects/myproject/subscriptions/mysubscription"
    }
    response = client.post("/receive/", json=payload)
    assert response.status_code == 422