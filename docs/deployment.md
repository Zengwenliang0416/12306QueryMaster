# 部署指南

本文档提供了在不同环境下部署 12306 列车查询系统的详细说明。

## 目录
- [系统要求](#系统要求)
- [开发环境部署](#开发环境部署)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [Nginx 配置](#nginx-配置)
- [监控和日志](#监控和日志)
- [常见问题](#常见问题)

## 系统要求

### 最低配置
- CPU: 2 核
- 内存: 4GB
- 磁盘: 20GB
- 操作系统: Ubuntu 20.04+ / CentOS 8+ / macOS 12+

### 软件要求
- Python 3.8+
- Node.js 16+
- Nginx 1.18+
- Redis 6+ (可选，用于缓存)
- PostgreSQL 12+ (可选，用于数据持久化)

## 开发环境部署

### 1. 后端服务

```bash
# 创建并激活虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 2. 前端服务

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

## 生产环境部署

### 1. 后端部署

#### 使用 Gunicorn

```bash
# 安装 Gunicorn
pip install gunicorn

# 创建 gunicorn.conf.py
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
bind = '0.0.0.0:8001'
keepalive = 120
errorlog = '/var/log/gunicorn/error.log'
accesslog = '/var/log/gunicorn/access.log'
capture_output = True

# 启动服务
gunicorn app.main:app -c gunicorn.conf.py
```

#### 使用 Supervisor

```ini
[program:12306-backend]
command=/path/to/venv/bin/gunicorn app.main:app -c /path/to/gunicorn.conf.py
directory=/path/to/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/supervisor/12306-backend.err.log
stdout_logfile=/var/log/supervisor/12306-backend.out.log
```

### 2. 前端部署

```bash
# 构建生产版本
npm run build

# 输出目录: dist/
```

## Docker 部署

### 1. 后端 Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8001

# 启动命令
CMD ["gunicorn", "app.main:app", "-c", "gunicorn.conf.py"]
```

### 2. 前端 Dockerfile

```dockerfile
# 构建阶段
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 3. Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8001:8001"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./backend:/app
      - ./logs:/var/log
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

## Nginx 配置

### 1. 前端配置

```nginx
server {
    listen 80;
    server_name example.com;
    root /usr/share/nginx/html;
    index index.html;

    # 启用 gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # 缓存配置
    location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
        expires max;
        add_header Cache-Control "public, no-transform";
    }

    # API 代理
    location /api {
        proxy_pass http://backend:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # 前端路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 2. SSL 配置

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # 现代配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;
}
```

## 监控和日志

### 1. Prometheus 配置

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: '12306-backend'
    static_configs:
      - targets: ['localhost:8001']
```

### 2. Grafana 仪表板

```json
{
  "dashboard": {
    "id": null,
    "title": "12306 监控面板",
    "panels": [
      {
        "title": "请求响应时间",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "http_request_duration_seconds"
          }
        ]
      },
      {
        "title": "错误率",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])"
          }
        ]
      }
    ]
  }
}
```

### 3. 日志配置

```python
# logging.conf
[loggers]
keys=root,gunicorn.error,gunicorn.access

[handlers]
keys=console,error_file,access_file

[formatters]
keys=generic,access

[logger_root]
level=INFO
handlers=console

[logger_gunicorn.error]
level=INFO
handlers=error_file
propagate=0
qualname=gunicorn.error

[logger_gunicorn.access]
level=INFO
handlers=access_file
propagate=0
qualname=gunicorn.access

[handler_console]
class=StreamHandler
formatter=generic
args=(sys.stdout, )

[handler_error_file]
class=logging.handlers.RotatingFileHandler
formatter=generic
args=('/var/log/gunicorn/error.log', 'a', 10485760, 10)

[handler_access_file]
class=logging.handlers.RotatingFileHandler
formatter=access
args=('/var/log/gunicorn/access.log', 'a', 10485760, 10)

[formatter_generic]
format=%(asctime)s [%(process)d] [%(levelname)s] %(message)s
datefmt=%Y-%m-%d %H:%M:%S
class=logging.Formatter

[formatter_access]
format=%(message)s
class=logging.Formatter
```

## 常见问题

### 1. 502 Bad Gateway
- 检查后端服务是否正常运行
- 检查 Nginx 配置中的代理地址
- 查看错误日志

### 2. 内存使用过高
- 调整 Gunicorn worker 数量
- 检查内存泄漏
- 增加 swap 空间

### 3. 静态资源加载失败
- 检查 Nginx 配置
- 确认文件权限
- 验证缓存配置

### 4. 性能优化
- 启用 HTTP/2
- 配置适当的缓存策略
- 使用 CDN 加速静态资源

### 5. 安全加固
- 启用 HTTPS
- 配置安全头部
- 限制请求频率

## 维护指南

### 1. 日常维护
- 监控系统资源使用
- 检查日志文件
- 定期备份数据

### 2. 更新部署
- 使用蓝绿部署
- 保持依赖包更新
- 定期安全补丁

### 3. 故障恢复
- 保持系统快照
- 制定回滚计划
- 维护文档更新 