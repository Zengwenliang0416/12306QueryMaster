#!/bin/bash

# 检查是否提供了日期参数
if [ $# -eq 0 ]; then
    echo "请提供查询日期，格式为 YYYY-MM-DD"
    echo "例如: ./test_curl.sh 2024-01-25"
    exit 1
fi

# 验证日期格式
if ! date -j -f "%Y-%m-%d" "$1" >/dev/null 2>&1; then
    echo "日期格式无效，请使用 YYYY-MM-DD 格式"
    echo "例如: ./test_curl.sh 2024-01-25"
    exit 1
fi

QUERY_DATE="$1"

# 设置API基础URL
BASE_URL="http://localhost:8001/api"

# Python command for pretty-printing JSON with UTF-8 support
PRETTY_PRINT='python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), ensure_ascii=False, indent=2))"'

echo "查询日期: $QUERY_DATE"
echo "================================"

echo "测试1: 获取北京站代码"
curl -X GET "${BASE_URL}/stations/北京" | eval "$PRETTY_PRINT"

echo -e "\n测试2: 获取上海站代码"
curl -X GET "${BASE_URL}/stations/上海" | eval "$PRETTY_PRINT"

# echo -e "\n测试3: 查询所有车次"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT"
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试4: 只查询高铁车次"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "train_types": ["G"]
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试5: 查询动车和普通列车"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "train_types": ["D", "Z", "T", "K"]
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试6: 查询早上6点到12点的高铁"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "start_time": "07:00:00",
#     "end_time": "08:00:00",
#     "train_types": ["G"]
#   }' | eval "$PRETTY_PRINT"

echo -e "\n测试7: 查询经过南京的所有车次"
curl -X POST "${BASE_URL}/tickets/query" \
-H "Content-Type: application/json" \
-d '{
"from_station": "北京",
"to_station": "上海",
"train_date": "'$QUERY_DATE'",
"purpose_codes": "ADULT",
"start_time": "07:00:00",
"end_time": "08:00:00",
"via_station": "昆山南"
}' | eval "$PRETTY_PRINT"

# echo -e "\n测试7: 查询下午2点到晚上8点的动车"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "start_time": "14:00:00",
#     "end_time": "20:00:00",
#     "train_types": ["D"]
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试8: 查询晚上8点后的所有车次"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "start_time": "20:00:00",
#     "end_time": "23:59:59"
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试9: 查询早上到下午的普通列车"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "start_time": "06:00:00",
#     "end_time": "18:00:00",
#     "train_types": ["Z", "T", "K"]
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试10: 查询晚上的高铁和动车"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "北京",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT",
#     "start_time": "18:00:00",
#     "end_time": "23:59:59",
#     "train_types": ["G", "D"]
#   }' | eval "$PRETTY_PRINT"

# echo -e "\n测试11: 使用无效站名查询"
# curl -X POST "${BASE_URL}/tickets/query" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "from_station": "Invalid Station",
#     "to_station": "上海",
#     "train_date": "'$QUERY_DATE'",
#     "purpose_codes": "ADULT"
#   }' | eval "$PRETTY_PRINT" 