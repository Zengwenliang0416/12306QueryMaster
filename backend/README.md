# 12306 Backend API

This is the backend API for the 12306 train ticket query system. It provides endpoints for querying train tickets and station information.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Query Train Tickets
```http
POST /api/tickets/query
```

Request body:
```json
{
  "from_station": "北京",
  "to_station": "上海",
  "train_date": "2024-02-20",
  "purpose_codes": "ADULT",
  "start_time": "00:00",
  "end_time": "23:59"
}
```

### Get All Station Codes
```http
GET /api/stations
```

### Get Station Code by Name
```http
GET /api/stations/{station_name}
```

## API Documentation

After starting the server, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

The project structure:
```
backend/
├── app/
│   ├── api/
│   │   └── routes.py
│   ├── core/
│   ├── models/
│   ├── schemas/
│   │   └── train.py
│   ├── services/
│   │   └── train_service.py
│   └── main.py
├── requirements.txt
└── README.md
``` 