# 12306 列车查询前端

这是一个基于 Vue 3 + Vite 实现的12306列车查询前端界面。

## 环境要求

- Node.js 16.x 或更高版本
- npm 或 yarn 包管理器

## 快速开始

### 1. 安装依赖

```bash
npm install
# 或
yarn install
```

### 2. 环境配置

项目使用以下环境配置文件：

- `.env`: 默认环境配置
- `.env.development`: 开发环境配置
- `.env.production`: 生产环境配置

可用的环境变量：

- `VITE_API_BASE_URL`: API 请求的基础路径
- `VITE_BACKEND_HOST`: 后端服务器主机名
- `VITE_BACKEND_PORT`: 后端服务器端口
- `VITE_BACKEND_URL`: 后端服务器完整地址

开发环境下，API 请求会通过 Vite 的代理功能转发到后端服务器。生产环境通常使用相对路径，由反向代理服务器（如 Nginx）处理请求转发。

### 3. 开发服务器

```bash
npm run dev
# 或
yarn dev
```

### 4. 构建生产版本

```bash
npm run build
# 或
yarn build
```

## 项目结构

```
frontend/
├── src/
│   ├── components/     # 组件目录
│   ├── stores/        # Pinia 状态管理
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── .env               # 默认环境配置
├── .env.development   # 开发环境配置
├── .env.production    # 生产环境配置
└── vite.config.js     # Vite 配置文件
```

## 功能特点

- 支持车次查询
- 支持车型筛选
- 支持时间段筛选
- 支持经停站查询
- 自动保存查询条件
- 响应式设计

## 开发说明

- 使用 Vue 3 Composition API
- 使用 Element Plus UI 组件库
- 使用 Pinia 进行状态管理
- 使用 Vite 作为构建工具

## 生产部署

1. 运行 `npm run build` 生成生产版本
2. 将 `dist` 目录下的文件部署到Web服务器

## 注意事项

1. 确保后端API服务可用
2. 检查API基础URL配置
3. 所有日期格式使用 `YYYY-MM-DD`
4. 时间格式使用 `HH:mm:ss`

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

MIT License - 详见 LICENSE 文件
