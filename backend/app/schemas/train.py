from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime, time

class TicketQuery(BaseModel):
    from_station: str
    to_station: str
    train_date: str
    purpose_codes: str = "ADULT"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    train_types: Optional[List[str]] = None  # ["G", "D", "Z", "T", "K"]

    class Config:
        schema_extra = {
            "example": {
                "from_station": "BJP",
                "to_station": "SHH",
                "train_date": "2024-01-10",
                "purpose_codes": "ADULT",
                "start_time": "00:00:00",
                "end_time": "23:59:59",
                "train_types": ["G", "D"]
            }
        }

class TrainStop(BaseModel):
    station_name: str
    arrival_time: Optional[str]
    departure_time: Optional[str]
    stopover_time: Optional[str]

class TrainInfo(BaseModel):
    train_no: str
    train_code: str
    train_type: str  # "高铁", "动车", "普通列车"
    from_station: TrainStop
    to_station: TrainStop
    duration: str
    seats: dict
    prices: dict 