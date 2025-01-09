# 12306 列车查询系统前端

这是12306列车查询系统的Vue 3前端项目，使用Element Plus组件库构建。

## 功能特点

- ✨ 车票查询界面
- 🚉 站点自动补全
- 🕒 时间段筛选
- 🚄 车型筛选
- 📍 经停站查询
- 📱 响应式设计

## 技术栈

- Vue 3
- Vite
- Element Plus
- Axios
- Day.js

## 开发环境要求

- Node.js 16.0 或更高版本
- npm 7.0 或更高版本

## 快速开始

1. 安装依赖：

```bash
npm install
```

2. 启动开发服务器：

```bash
npm run dev
```

3. 构建生产版本：

```bash
npm run build
```

## 项目结构

```
frontend/
├── src/
│   ├── assets/        # 静态资源
│   ├── components/    # Vue组件
│   ├── App.vue        # 根组件
│   ├── main.js        # 入口文件
│   └── style.css      # 全局样式
├── public/            # 公共资源
├── index.html         # HTML模板
├── package.json       # 项目配置
└── vite.config.js     # Vite配置
```

## 开发指南

1. 本地开发时，确保后端服务器运行在 `http://localhost:8001`
2. API请求都在 `src/App.vue` 中处理
3. 使用Element Plus组件进行界面开发
4. 使用 `npm run dev` 启动开发服务器

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
