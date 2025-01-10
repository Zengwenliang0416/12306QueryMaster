# 12306 列车查询系统 - 后端

基于 FastAPI 开发的列车查询系统后端服务，提供高性能的列车信息查询 API。

## 功能特点

- ✨ 实时查询列车车次信息
- 💰 提供各席别票价信息
- 🚄 支持按车型筛选（高铁/动车/普通列车）
- 🕒 支持按时间段筛选
- 📍 支持查询经停站点信息
- 🔍 支持按经停站点筛选车次
- 🚀 异步处理提升性能
- 🔄 自动重试机制
- 📝 详细的日志记录

## 技术栈

- FastAPI 0.105 - 高性能的 Python Web 框架
- Pydantic 2.5 - 数据验证和序列化
- aiohttp 3.9 - 异步 HTTP 客户端
- uvicorn 0.25 - ASGI 服务器
- Python-Jose - JWT 认证
- SQLAlchemy 2.0 - ORM（可选）

## 系统要求

- Python 3.8+
- pip 包管理器
- 虚拟环境（推荐）

## 快速开始

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   └── routes.py     # API 端点定义
│   │
│   ├── schemas/          # 数据模型
│   │   ├── train.py      # 列车相关模型
│   │   └── base.py       # 基础模型
│   │
│   ├── services/         # 业务逻辑
│   │   └── train_service.py  # 列车查询服务
│   │
│   ├── core/            # 核心配置
│   │   ├── config.py    # 应用配置
│   │   └── logging.py   # 日志配置
│   │
│   └── main.py         # 应用入口
│
├── data/               # 数据文件
├── tests/             # 测试文件
├── requirements.txt    # 项目依赖
└── README.md          # 项目文档
```

## API 文档

### 1. 查询车票信息

```http
POST /api/tickets/query

请求体：
{
    "from_station": "北京",
    "to_station": "上海",
    "train_date": "2024-01-21",
    "purpose_codes": "ADULT",
    "train_types": ["G"],          # 可选，车型过滤
    "start_time": "08:00:00",      # 可选，发车时间起
    "end_time": "18:00:00",        # 可选，发车时间止
    "via_station": "南京南"        # 可选，经停站点
}

响应：
[
    {
        "train_no": "5l0000G101",
        "train_code": "G1",
        "train_type": "高铁",
        "from_station": {
            "station_name": "北京南",
            "departure_time": "09:00"
        },
        "to_station": {
            "station_name": "上海虹桥",
            "arrival_time": "13:48"
        },
        "duration": "4:48",
        "seats": {
            "商务座": "有",
            "一等座": "有",
            "二等座": "有"
        },
        "prices": {
            "商务座": "1748.0",
            "一等座": "933.0",
            "二等座": "553.0"
        }
    }
]
```

### 2. 获取站点代码

```http
GET /api/stations/{station_name}

响应：
[
    {
        "name": "北京南",
        "code": "VNP"
    }
]
```

### 3. 获取经停站信息

```http
GET /api/trains/{train_code}/stops

响应：
[
    {
        "station_name": "北京南",
        "arrival_time": "--",
        "departure_time": "09:00",
        "stopover_time": "--"
    },
    {
        "station_name": "南京南",
        "arrival_time": "11:24",
        "departure_time": "11:26",
        "stopover_time": "2分钟"
    }
]
```

## 开发指南

### 1. 代码规范

- 使用 Python 类型注解
- 遵循 PEP 8 编码规范
- 使用异步函数处理 I/O 操作
- 使用 Pydantic 模型验证数据

### 2. 错误处理

```python
from fastapi import HTTPException

async def get_station_code(station_name: str):
    try:
        code = await train_service.get_station_code(station_name)
        if not code:
            raise HTTPException(
                status_code=404,
                detail="Station not found"
            )
        return code
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
```

### 3. 日志记录

```python
import logging

logger = logging.getLogger(__name__)

async def query_tickets(query: TicketQuery):
    logger.info(f"Querying tickets: {query}")
    try:
        result = await train_service.search_tickets(query)
        logger.info(f"Found {len(result)} trains")
        return result
    except Exception as e:
        logger.error(f"Failed to query tickets: {e}")
        raise
```

### 4. 性能优化

- 使用连接池管理 HTTP 连接
- 实现缓存机制减少请求次数
- 使用异步并发处理多个请求
- 优化数据结构减少内存使用

## 部署指南

### 1. 使用 Docker

```dockerfile
FROM python:3.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 2. 使用 Supervisor

```ini
[program:12306-backend]
command=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/12306-backend.err.log
stdout_logfile=/var/log/12306-backend.out.log
```

## 常见问题

### 1. 接口访问失败
- 检查网络连接
- 确认 12306 接口可用性
- 查看错误日志

### 2. 性能问题
- 调整连接池大小
- 优化并发请求数量
- 添加缓存机制

### 3. 内存占用过高
- 减少数据缓存时间
- 优化数据结构
- 及时释放资源

## 测试

```bash
# 运行单元测试
pytest tests/

# 运行特定测试
pytest tests/test_train_service.py -v

# 生成测试覆盖率报告
pytest --cov=app tests/
```

## 监控

- 使用 Prometheus 收集指标
- 使用 Grafana 展示监控面板
- 关键指标：
  - 请求响应时间
  - 错误率
  - 并发请求数
  - 内存使用率

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 许可证

MIT 