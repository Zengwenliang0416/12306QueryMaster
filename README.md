# 12306 列车查询系统

<div align="center">

![logo](./images/logo.png)

[![GitHub license](https://img.shields.io/github/license/Zengwenliang0416/12306QueryMaster)](https://github.com/Zengwenliang0416/12306QueryMaster/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Zengwenliang0416/12306QueryMaster)](https://github.com/Zengwenliang0416/12306QueryMaster/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Zengwenliang0416/12306QueryMaster)](https://github.com/Zengwenliang0416/12306QueryMaster/network)
[![GitHub issues](https://img.shields.io/github/issues/Zengwenliang0416/12306QueryMaster)](https://github.com/Zengwenliang0416/12306QueryMaster/issues)

<p align="center">
  <a href="#功能特点">功能特点</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#技术栈">技术栈</a> •
  <a href="#项目结构">项目结构</a> •
  <a href="#环境配置">环境配置</a> •
  <a href="#API文档">API文档</a> •
  <a href="#贡献指南">贡献指南</a>
</p>

</div>

## 📖 项目介绍

12306列车查询系统是一个现代化的铁路票务查询平台，基于FastAPI和Vue 3构建。本系统提供直观的用户界面和高效的查询服务，帮助用户快速获取列车票务信息。

### ✨ 主要特性

- 🎯 **精准查询**: 支持车次、站点、经停等多维度查询
- 🚀 **高性能**: 采用异步处理和智能缓存
- 🎨 **现代UI**: 支持深色模式和主题定制
- 📱 **响应式**: 完美适配各种设备尺寸
- ⚡️ **实时更新**: 准确显示余票和价格信息
- 🔍 **智能过滤**: 灵活的车次筛选功能
- 🌐 **跨平台**: 支持各种主流浏览器

## 🎯 功能特点

### 🚄 实时列车查询
- **车次查询**: 支持车次号、始发站、终点站等多条件查询
- **站点查询**: 查看所有经过指定站点的列车
- **经停查询**: 显示完整的车次经停信息
- **票价显示**: 实时显示各种座位类型的票价

### 🎨 现代化界面
- **响应式设计**: 完美适配桌面端和移动端
- **深色模式**: 自动/手动切换深色模式
- **主题定制**: 支持个性化主题颜色
- **优雅动画**: 流畅的过渡和交互效果

### ⚡️ 高性能
- **异步处理**: 采用异步请求提升响应速度
- **智能缓存**: 缓存常用数据减少请求
- **延迟加载**: 按需加载提升页面性能
- **虚拟滚动**: 高效处理大量数据展示

### 🛡️ 安全可靠
- **输入验证**: 严格的数据验证机制
- **请求限制**: 防止恶意请求
- **错误处理**: 友好的错误提示
- **安全头部**: 标准的安全响应头

## 🚀 快速开始

### 1️⃣ 克隆项目

```bash
git clone https://github.com/Zengwenliang0416/12306QueryMaster.git
cd 12306QueryMaster
```

### 2️⃣ 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

### 3️⃣ 前端设置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 🛠️ 技术栈

### 后端技术
- **FastAPI**: 现代化的Python Web框架
- **Pydantic**: 数据验证和序列化
- **aiohttp**: 异步HTTP客户端
- **uvicorn**: 高性能ASGI服务器

### 前端技术
- **Vue 3**: 渐进式JavaScript框架
- **Vite**: 下一代前端构建工具
- **Element Plus**: 优雅的UI组件库
- **Pinia**: 直观的状态管理
- **VueUse**: 实用的组合式API集合
- **Tailwind CSS**: 高效的原子化CSS框架

## 📁 项目结构

```
.
├── backend/                # 后端项目目录
│   ├── app/               # 应用代码
│   │   ├── api/          # API路由
│   │   ├── core/         # 核心功能
│   │   ├── models/       # 数据模型
│   │   ├── schemas/      # Pydantic模型
│   │   ├── services/     # 业务逻辑
│   │   └── utils/        # 工具函数
│   ├── tests/            # 测试代码
│   └── requirements.txt   # 依赖管理
│
├── frontend/              # 前端项目目录
│   ├── src/              # 源代码
│   │   ├── components/   # Vue组件
│   │   ├── stores/       # 状态管理
│   │   ├── styles/       # 样式文件
│   │   └── utils/        # 工具函数
│   ├── public/           # 静态资源
│   └── package.json      # 依赖管理
│
├── docs/                 # 项目文档
└── README.md            # 项目说明
```

## ⚙️ 环境配置

### 后端环境变量
```env
# 服务配置
HOST=0.0.0.0
PORT=8001
DEBUG=True
```

### 前端环境变量
```env
VITE_API_BASE_URL=/api
VITE_APP_TITLE=12306列车查询
```

## 📸 功能展示

### 车票查询
![车票查询](docs/images/ticket-search.png)

### 站点查询
![站点查询](docs/images/station-search.png)

### 经停查询
![经停查询](docs/images/train-stops.png)

## 📚 文档

- [API文档](docs/api.md)
- [开发指南](docs/development.md)
- [部署指南](docs/deployment.md)
- [Git操作指南](docs/git_operations.md)

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

## 📝 更新日志

### v1.1.0 (2024-01-09)
- ✨ 前后端联调完成
- 🚀 新增功能
  - 显示座位和余票情况
  - 站点查询功能
  - 经停站过滤功能
- 🔧 性能优化
  - 优化查询性能
  - 统一环境配置
- 🎨 界面优化
  - 添加前端样式
  - 优化前端界面
  - 完善状态管理

### v1.0.0 (2024-01-08)
- 🎉 项目初始化
- ✨ 实现第一代车票查询脚本
- 🔨 完成后端基础接口开发
  - 车次查询功能
  - 经停站信息查询
  - 经停站筛选功能
- 📚 完善后端文档

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。

## 👥 联系方式

- 项目维护者：曾文亮
- 邮箱：wenliang_zeng416@163.com
- 项目链接：[GitHub](https://github.com/Zengwenliang0416/12306QueryMaster)

## 🙏 致谢

- [12306](https://www.12306.cn/index/) - 数据来源
- [FastAPI](https://fastapi.tiangolo.com/) - 后端框架
- [Vue.js](https://vuejs.org/) - 前端框架
- [Element Plus](https://element-plus.org/) - UI组件库
- [Tailwind CSS](https://tailwindcss.com/) - CSS框架 
