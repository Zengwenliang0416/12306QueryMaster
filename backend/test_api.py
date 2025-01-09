import asyncio
import aiohttp
import json
from datetime import datetime, timedelta

async def test_api():
    base_url = "http://localhost:8001/api"
    
    async with aiohttp.ClientSession() as session:
        # Test 1: Get station code for Beijing
        print("\nTest 1: Get station code for Beijing")
        async with session.get(f"{base_url}/stations/北京") as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            else:
                print(f"Error: {await response.text()}")

        # Test 2: Get station code for Shanghai
        print("\nTest 2: Get station code for Shanghai")
        async with session.get(f"{base_url}/stations/上海") as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                print(f"Response: {json.dumps(data, ensure_ascii=False, indent=2)}")
            else:
                print(f"Error: {await response.text()}")

        # Test 3: Query tickets for today
        print("\nTest 3: Query tickets for today")
        query_data = {
            "from_station": "北京",
            "to_station": "上海",
            "train_date": datetime.now().strftime("%Y-%m-%d"),
            "purpose_codes": "ADULT"
        }
        
        async with session.post(f"{base_url}/tickets/query", json=query_data) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                # Only print first 2 trains for brevity
                print(f"Response (first 2 trains): {json.dumps(data[:2], ensure_ascii=False, indent=2)}")
                print(f"Total trains found: {len(data)}")
            else:
                print(f"Error: {await response.text()}")

        # Test 4: Query tickets for tomorrow
        print("\nTest 4: Query tickets for tomorrow")
        tomorrow = datetime.now() + timedelta(days=1)
        query_data = {
            "from_station": "北京",
            "to_station": "上海",
            "train_date": tomorrow.strftime("%Y-%m-%d"),
            "purpose_codes": "ADULT"
        }
        
        async with session.post(f"{base_url}/tickets/query", json=query_data) as response:
            print(f"Status: {response.status}")
            if response.status == 200:
                data = await response.json()
                # Only print first 2 trains for brevity
                print(f"Response (first 2 trains): {json.dumps(data[:2], ensure_ascii=False, indent=2)}")
                print(f"Total trains found: {len(data)}")
            else:
                print(f"Error: {await response.text()}")

        # Test 5: Query with invalid station name
        print("\nTest 5: Query with invalid station name")
        query_data = {
            "from_station": "Invalid Station",
            "to_station": "上海",
            "train_date": datetime.now().strftime("%Y-%m-%d"),
            "purpose_codes": "ADULT"
        }
        
        async with session.post(f"{base_url}/tickets/query", json=query_data) as response:
            print(f"Status: {response.status}")
            print(f"Response: {await response.text()}")

if __name__ == "__main__":
    asyncio.run(test_api()) 