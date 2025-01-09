#!/bin/bash

# 设置API基础URL
BASE_URL="http://localhost:8001/api"

# Python command for pretty-printing JSON with UTF-8 support
PRETTY_PRINT='python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), ensure_ascii=False, indent=2))"'

echo "测试1: 获取北京站代码"
curl -X GET "${BASE_URL}/stations/北京" | eval "$PRETTY_PRINT"

echo -e "\n测试2: 获取上海站代码"
curl -X GET "${BASE_URL}/stations/上海" | eval "$PRETTY_PRINT"

echo -e "\n测试3: 查询今天的所有车次"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT"
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试4: 只查询高铁车次"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "train_types": ["G"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试5: 查询动车和普通列车"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "train_types": ["D", "Z", "T", "K"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试6: 查询早上6点到12点的高铁"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "start_time": "06:00:00",
    "end_time": "12:00:00",
    "train_types": ["G"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试7: 查询下午2点到晚上8点的动车"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "start_time": "14:00:00",
    "end_time": "20:00:00",
    "train_types": ["D"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试8: 查询晚上8点后的所有车次"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "start_time": "20:00:00",
    "end_time": "23:59:59"
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试9: 查询早上到下午的普通列车"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "start_time": "06:00:00",
    "end_time": "18:00:00",
    "train_types": ["Z", "T", "K"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试10: 查询晚上的高铁和动车"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT",
    "start_time": "18:00:00",
    "end_time": "23:59:59",
    "train_types": ["G", "D"]
  }' | eval "$PRETTY_PRINT"

echo -e "\n测试11: 使用无效站名查询"
curl -X POST "${BASE_URL}/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "Invalid Station",
    "to_station": "上海",
    "train_date": "'$(date +%Y-%m-%d)'",
    "purpose_codes": "ADULT"
  }' | eval "$PRETTY_PRINT" 