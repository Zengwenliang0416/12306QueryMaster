from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import time

class TrainStop(BaseModel):
    station_name: str
    arrival_time: Optional[str] = None
    departure_time: Optional[str] = None
    stopover_time: Optional[str] = None

class TrainInfo(BaseModel):
    train_no: str
    train_code: str
    train_type: str
    from_station: TrainStop
    to_station: TrainStop
    duration: str
    seats: Dict[str, str]
    prices: Dict[str, float]
    stops: Optional[List[TrainStop]] = None

class TicketQuery(BaseModel):
    from_station: str
    to_station: str
    train_date: str
    purpose_codes: str = "ADULT"
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    train_types: Optional[List[str]] = None
    via_station: Optional[str] = None
    include_stops: Optional[bool] = False 