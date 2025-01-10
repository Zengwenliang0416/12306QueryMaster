# API 文档

本文档详细说明了12306列车查询系统的API接口规范。

## 基础信息

- 基础URL: `/api`
- 所有请求和响应均使用JSON格式
- 所有时间格式遵循ISO 8601标准
- 所有请求需要包含header: `Content-Type: application/json`

## 错误响应格式

当API调用出错时，将返回以下格式的错误信息：

```json
{
  "code": 400,
  "message": "错误描述信息",
  "details": {
    "field": "具体错误字段",
    "reason": "具体错误原因"
  }
}
```

常见错误码：
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 429: 请求过于频繁
- 500: 服务器内部错误

## API 端点

### 1. 车票查询

#### 请求

```http
POST /api/tickets/query
Content-Type: application/json

{
  "from_station": "北京",
  "to_station": "上海",
  "date": "2024-01-20",
  "seat_types": ["商务座", "一等座", "二等座"],
  "train_types": ["G", "D"],
  "departure_time_range": {
    "start": "00:00",
    "end": "23:59"
  }
}
```

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| from_station | string | 是 | 出发站 |
| to_station | string | 是 | 到达站 |
| date | string | 是 | 出发日期(YYYY-MM-DD) |
| seat_types | array | 否 | 座位类型列表 |
| train_types | array | 否 | 车次类型列表 |
| departure_time_range | object | 否 | 发车时间范围 |

#### 响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "tickets": [
      {
        "train_code": "G1234",
        "from_station": "北京南",
        "to_station": "上海虹桥",
        "departure_time": "08:00",
        "arrival_time": "13:30",
        "duration": "5小时30分",
        "seats": {
          "商务座": {
            "count": 10,
            "price": 1800.0
          },
          "一等座": {
            "count": 20,
            "price": 900.0
          },
          "二等座": {
            "count": 100,
            "price": 550.0
          }
        }
      }
    ],
    "total": 1
  }
}
```

### 2. 站点查询

#### 请求

```http
GET /api/stations/query?keyword=北京
```

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| keyword | string | 是 | 站点关键词 |

#### 响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "stations": [
      {
        "code": "BJP",
        "name": "北京",
        "full_name": "北京站",
        "type": "火车站"
      },
      {
        "code": "BJS",
        "name": "北京南",
        "full_name": "北京南站",
        "type": "高铁站"
      }
    ],
    "total": 2
  }
}
```

### 3. 列车经停查询

#### 请求

```http
GET /api/trains/G1234/stops
```

#### 响应

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "train_code": "G1234",
    "stops": [
      {
        "station": "北京南",
        "arrival_time": "始发站",
        "departure_time": "08:00",
        "stopover_time": 0,
        "day_difference": 0
      },
      {
        "station": "济南西",
        "arrival_time": "09:30",
        "departure_time": "09:32",
        "stopover_time": 2,
        "day_difference": 0
      },
      {
        "station": "南京南",
        "arrival_time": "11:45",
        "departure_time": "11:47",
        "stopover_time": 2,
        "day_difference": 0
      },
      {
        "station": "上海虹桥",
        "arrival_time": "13:30",
        "departure_time": "终到站",
        "stopover_time": 0,
        "day_difference": 0
      }
    ]
  }
}
```

## 数据模型

### 1. 车票信息 (Ticket)

```typescript
interface Ticket {
  train_code: string;      // 车次编号
  from_station: string;    // 出发站
  to_station: string;      // 到达站
  departure_time: string;  // 发车时间
  arrival_time: string;    // 到达时间
  duration: string;        // 运行时长
  seats: {                 // 座位信息
    [type: string]: {     // 座位类型
      count: number;      // 剩余票数
      price: number;      // 票价
    }
  }
}
```

### 2. 站点信息 (Station)

```typescript
interface Station {
  code: string;       // 站点代码
  name: string;       // 站点名称
  full_name: string;  // 站点全称
  type: string;       // 站点类型
}
```

### 3. 列车经停信息 (Stop)

```typescript
interface Stop {
  station: string;        // 站点名称
  arrival_time: string;   // 到达时间
  departure_time: string; // 发车时间
  stopover_time: number;  // 停留时间(分钟)
  day_difference: number; // 天数差
}
```

## 使用示例

### Python

```python
import requests

def query_tickets(from_station, to_station, date):
    url = "http://localhost:8001/api/tickets/query"
    payload = {
        "from_station": from_station,
        "to_station": to_station,
        "date": date
    }
    response = requests.post(url, json=payload)
    return response.json()

# 使用示例
tickets = query_tickets("北京", "上海", "2024-01-20")
print(tickets)
```

### JavaScript

```javascript
async function queryTickets(fromStation, toStation, date) {
  const url = '/api/tickets/query';
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from_station: fromStation,
      to_station: toStation,
      date: date,
    }),
  });
  return response.json();
}

// 使用示例
queryTickets('北京', '上海', '2024-01-20')
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### cURL

```bash
# 查询车票
curl -X POST "http://localhost:8001/api/tickets/query" \
  -H "Content-Type: application/json" \
  -d '{
    "from_station": "北京",
    "to_station": "上海",
    "date": "2024-01-20"
  }'

# 查询站点
curl "http://localhost:8001/api/stations/query?keyword=北京"

# 查询经停信息
curl "http://localhost:8001/api/trains/G1234/stops"
```

## 注意事项

1. 请求限制
   - 每个IP每分钟最多100次请求
   - 查询日期范围：当前日期起30天内

2. 数据说明
   - 所有时间均为24小时制
   - 票价单位为人民币元
   - 座位类型包括：商务座、一等座、二等座、软卧、硬卧、软座、硬座、无座

3. 最佳实践
   - 建议实现请求重试机制
   - 对频繁查询的数据进行缓存
   - 添加适当的错误处理
   - 实现请求超时处理

4. 开发建议
   - 使用HTTPS进行安全传输
   - 实现数据压缩以减少传输量
   - 使用合适的缓存策略
   - 实现适当的日志记录

## 更新日志

### v1.0.0 (2024-01-01)
- 初始版本发布
- 支持车票查询
- 支持站点查询
- 支持经停查询

### v1.1.0 (2024-01-15)
- 添加座位价格信息
- 优化查询性能
- 增加错误处理
- 完善文档说明 