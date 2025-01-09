# 12306 列车查询后端服务

这是一个基于 FastAPI 实现的12306列车查询服务，支持查询车次信息、经停站点等功能。

## 功能特点

- ✨ 支持查询指定日期的列车车次信息
- 🚄 支持按车型筛选（高铁/动车/普通列车）
- 🕒 支持按时间段筛选
- 📍 支持查询经停站点信息
- 🔍 支持按经停站点筛选车次

## 环境要求

- Python 3.8 或更高版本
- pip（Python包管理器）

## 快速开始

### 1. 安装 Python

如果您还没有安装 Python，请先从 [Python官网](https://www.python.org/downloads/) 下载并安装 Python 3.8 或更高版本。

### 2. 创建虚拟环境

在终端（Windows用户使用命令提示符或PowerShell）中执行以下命令：

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 确保pip是最新版本
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 4. 启动服务

```bash
# 启动FastAPI服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

看到类似以下输出则表示服务启动成功：
```
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### 5. 测试服务

我们提供了一个测试脚本来验证服务是否正常运行。在新的终端窗口中执行：

```bash
# 确保在backend目录下
cd backend

# 添加执行权限（仅Unix系统需要）
chmod +x test_curl.sh

# 运行测试脚本（使用明天的日期）
./test_curl.sh 2024-01-21
```

测试脚本会执行一系列查询，包括：
- 获取站点代码
- 查询所有车次
- 按车型筛选
- 按时间段筛选
- 查询经停站点

## API 文档

启动服务后，可以通过以下地址访问API文档：
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 主要API接口

### 1. 查询车票信息

```bash
POST /api/tickets/query

请求体示例：
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
```

### 2. 获取站点代码

```bash
GET /api/stations/{station_name}

示例：
GET /api/stations/北京
```

## 常见问题

1. **端口被占用**
   ```bash
   # 查找占用端口的进程
   lsof -i :8001
   
   # 终止进程
   kill -9 <进程ID>
   ```

2. **ModuleNotFoundError**
   - 确保您在正确的目录下
   - 确保已激活虚拟环境
   - 重新安装依赖：`pip install -r requirements.txt`

3. **Permission denied**
   ```bash
   # 添加执行权限
   chmod +x test_curl.sh
   ```

## 数据说明

- 查询结果会保存在 `backend/data` 目录下
- 经停站信息保存在 `train_stops.txt` 文件中

## 开发说明

- 项目使用 FastAPI 框架开发
- 使用 Pydantic 进行数据验证
- 遵循 RESTful API 设计规范
- 采用异步编程模式

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件 