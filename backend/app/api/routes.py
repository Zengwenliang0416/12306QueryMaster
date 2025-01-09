from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict
from ..schemas.train import TicketQuery, TrainInfo, TrainStop
from ..services.train_service import TrainService
from fastapi.concurrency import run_in_threadpool

router = APIRouter()
train_service = TrainService()

@router.post("/tickets/query", response_model=List[TrainInfo])
async def query_tickets(query: TicketQuery):
    try:
        # Get station codes
        from_code = await run_in_threadpool(train_service.get_station_code, query.from_station)
        to_code = await run_in_threadpool(train_service.get_station_code, query.to_station)
        
        if not from_code or not to_code:
            raise HTTPException(
                status_code=400,
                detail="Invalid station name. Please check the station names."
            )

        # Convert time objects to strings if they exist
        start_time = query.start_time.strftime("%H:%M") if query.start_time else None
        end_time = query.end_time.strftime("%H:%M") if query.end_time else None

        # Query tickets using async method directly
        trains = await train_service._async_query_tickets(
            from_code,
            to_code,
            query.train_date,
            start_time=start_time,
            end_time=end_time,
            train_types=query.train_types,
            via_station=query.via_station,
            include_stops=query.include_stops
        )

        if not trains:
            return []

        return trains

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to query tickets: {str(e)}"
        )

@router.get("/stations/{station_name}", response_model=List[Dict[str, str]])
async def search_stations(station_name: str):
    """搜索站点，支持模糊匹配"""
    try:
        stations = await run_in_threadpool(train_service.search_stations, station_name)
        return stations
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search stations: {str(e)}"
        )

@router.get("/trains/{train_code}/stops", response_model=List[TrainStop])
async def get_train_stops(train_code: str, train_date: str = None):
    """获取列车经停站信息"""
    try:
        # 从文件中读取经停站信息
        stops = await run_in_threadpool(train_service.get_train_stops_from_file, train_code, train_date)
        if not stops:
            raise HTTPException(
                status_code=404,
                detail=f"Train stops not found for train {train_code}"
            )
        return stops
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get train stops: {str(e)}"
        ) 