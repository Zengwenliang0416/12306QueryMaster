from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas.train import TicketQuery, TrainInfo
from ..services.train_service import TrainService

router = APIRouter()
train_service = TrainService()

@router.post("/tickets/query", response_model=List[TrainInfo])
async def query_tickets(query: TicketQuery):
    try:
        # Get station codes
        from_code = train_service.get_station_code(query.from_station)
        to_code = train_service.get_station_code(query.to_station)
        
        if not from_code or not to_code:
            raise HTTPException(
                status_code=400,
                detail="Invalid station name. Please check the station names."
            )

        # Convert time objects to strings if they exist
        start_time = query.start_time.strftime("%H:%M") if query.start_time else None
        end_time = query.end_time.strftime("%H:%M") if query.end_time else None

        # Query tickets
        trains = train_service.query_tickets(
            from_code,
            to_code,
            query.train_date,
            start_time=start_time,
            end_time=end_time,
            train_types=query.train_types,
            via_station=query.via_station
        )

        if not trains:
            return []

        return trains

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query tickets: {str(e)}"
        )

@router.get("/stations/{station_name}")
async def get_station_code(station_name: str):
    try:
        code = train_service.get_station_code(station_name)
        if not code:
            raise HTTPException(
                status_code=404,
                detail=f"Station '{station_name}' not found"
            )
        return {"station_name": station_name, "code": code}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get station code: {str(e)}"
        ) 