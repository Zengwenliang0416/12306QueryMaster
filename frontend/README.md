# 12306 列车查询系统 - 前端

基于 Vue 3 + Vite + Element Plus 开发的列车查询系统前端项目。

## 技术栈

- Vue 3.3 - 渐进式 JavaScript 框架
- Vite 5.0 - 下一代前端构建工具
- Element Plus 2.4 - Vue 3 组件库
- Pinia 2.1 - Vue 状态管理
- VueUse 10.7 - Vue 组合式 API 工具集
- Tailwind CSS 3.4 - 原子化 CSS 框架
- Axios - HTTP 客户端
- Day.js - 日期处理库

## 开发环境

- Node.js 16+
- npm 或 yarn

## 快速开始

```bash
# 安装依赖
npm install
# 或
yarn install

# 启动开发服务器
npm run dev
# 或
yarn dev
```

## 环境配置

项目使用以下环境配置文件：

- `.env` - 基础配置
- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置

配置项说明：

```env
# API 基础路径
VITE_API_BASE_URL=/api

# 其他配置项...
```

## 项目结构

```
frontend/
├── src/
│   ├── components/        # Vue 组件
│   │   ├── SearchForm.vue    # 搜索表单组件
│   │   ├── TicketTable.vue   # 车票列表组件
│   │   ├── SeatColumn.vue    # 座位列组件
│   │   ├── StopsDialog.vue   # 经停站弹窗组件
│   │   └── ThemeSettings.vue # 主题设置组件
│   │
│   ├── stores/           # Pinia 状态管理
│   │   ├── ticket.js        # 车票查询状态
│   │   └── theme.js         # 主题状态
│   │
│   ├── styles/          # 全局样式
│   │   └── main.css        # 主样式文件
│   │
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
│
├── public/             # 静态资源
├── index.html          # HTML 模板
├── vite.config.js      # Vite 配置
└── package.json        # 项目配置
```

## 组件文档

### SearchForm.vue

搜索表单组件，用于输入查询条件。

#### Props
无

#### Events
- `search` - 触发查询
- `reset` - 重置表单

#### 使用示例
```vue
<template>
  <SearchForm @search="handleSearch" @reset="handleReset" />
</template>
```

### TicketTable.vue

车票列表组件，展示查询结果。

#### Props
- `tickets` (Array) - 车票列表数据
- `loading` (Boolean) - 加载状态
- `loadingStops` (Object) - 经停站加载状态

#### Events
- `showStops` - 显示经停站信息

#### 使用示例
```vue
<template>
  <TicketTable
    :tickets="tickets"
    :loading="loading"
    :loading-stops="loadingStops"
    @show-stops="handleShowStops"
  />
</template>
```

### SeatColumn.vue

座位列组件，显示各类型座位的余票和价格信息。

#### Props
- `type` (String) - 座位类型
- `ticket` (Object) - 车票信息

#### 使用示例
```vue
<template>
  <SeatColumn type="二等座" :ticket="ticket" />
</template>
```

### StopsDialog.vue

经停站信息弹窗组件。

#### Props
- `modelValue` (Boolean) - 控制弹窗显示
- `stops` (Array) - 经停站列表

#### Events
- `update:modelValue` - 更新弹窗显示状态

#### 使用示例
```vue
<template>
  <StopsDialog v-model="dialogVisible" :stops="trainStops" />
</template>
```

### ThemeSettings.vue

主题设置组件，用于切换深色模式和主题色。

#### Props
无

#### 使用示例
```vue
<template>
  <ThemeSettings />
</template>
```

## 状态管理

### ticket.js

车票查询相关状态管理。

#### State
- `searchForm` - 查询表单数据
- `tickets` - 查询结果
- `loading` - 加载状态
- `trainStops` - 经停站信息

#### Actions
- `searchTickets` - 执行查询
- `resetForm` - 重置表单
- `showTrainStops` - 获取经停站信息

### theme.js

主题相关状态管理。

#### State
- `isDark` - 深色模式状态
- `primaryColor` - 主题色

#### Actions
- `toggleDarkMode` - 切换深色模式
- `setPrimaryColor` - 设置主题色

## 构建部署

```bash
# 构建生产版本
npm run build
# 或
yarn build

# 预览构建结果
npm run preview
# 或
yarn preview
```

## 开发指南

### 代码规范

- 使用 Composition API 和 `<script setup>`
- 组件名使用 PascalCase
- Props 名使用 camelCase
- 事件名使用 kebab-case
- 使用 TypeScript 类型注解

### 样式指南

- 使用 scoped CSS
- 遵循 BEM 命名规范
- 优先使用 Tailwind CSS 类
- 自定义样式使用 CSS 变量

### Git 提交规范

```bash
feat: 添加新功能
fix: 修复问题
docs: 修改文档
style: 修改样式
refactor: 代码重构
test: 添加测试
chore: 修改构建过程或辅助工具
```

## 常见问题

### 1. 开发服务器启动失败
- 检查端口是否被占用
- 确认 Node.js 版本是否符合要求
- 删除 node_modules 重新安装依赖

### 2. 接口请求失败
- 检查后端服务是否正常运行
- 确认环境变量配置是否正确
- 查看网络请求是否有跨域问题

### 3. 组件渲染问题
- 检查 Props 传递是否正确
- 确认响应式数据的定义方式
- 查看控制台是否有错误信息

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

## 许可证

MIT
