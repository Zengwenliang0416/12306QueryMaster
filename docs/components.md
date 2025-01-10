# 组件使用指南

## 组件总览

本项目包含以下主要组件：
- SearchForm - 车票搜索表单
- TicketTable - 车票列表展示
- SeatColumn - 座位信息列
- StopsDialog - 经停站信息弹窗
- ThemeSettings - 主题设置

## SearchForm

### 功能描述
提供车票查询的表单界面，包括出发地、目的地、出发日期、车型等筛选条件。

### Props
无

### Events
| 事件名 | 说明 | 参数 |
|--------|------|------|
| search | 触发查询 | - |
| reset | 重置表单 | - |

### 插槽
无

### 使用示例

```vue
<template>
  <div class="search-container">
    <SearchForm
      @search="handleSearch"
      @reset="handleReset"
    />
  </div>
</template>

<script setup>
import { SearchForm } from '@/components'

const handleSearch = () => {
  // 处理搜索事件
}

const handleReset = () => {
  // 处理重置事件
}
</script>
```

### 表单验证规则
- 出发站：必填
- 到达站：必填
- 出发日期：必填，不能选择过去的日期
- 时间范围：结束时间必须大于开始时间

## TicketTable

### 功能描述
展示车票查询结果，包括车次信息、时间信息、票价信息等。

### Props
| 属性名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| tickets | 车票列表数据 | Array | [] | 是 |
| loading | 加载状态 | Boolean | false | 否 |
| loadingStops | 经停站加载状态 | Object | {} | 否 |

### Events
| 事件名 | 说明 | 参数 |
|--------|------|------|
| showStops | 显示经停站信息 | trainCode: string |

### 使用示例

```vue
<template>
  <TicketTable
    :tickets="tickets"
    :loading="loading"
    :loading-stops="loadingStops"
    @show-stops="handleShowStops"
  />
</template>

<script setup>
import { ref } from 'vue'
import { TicketTable } from '@/components'

const tickets = ref([])
const loading = ref(false)
const loadingStops = ref({})

const handleShowStops = (trainCode) => {
  // 处理显示经停站信息
}
</script>
```

## SeatColumn

### 功能描述
显示特定类型座位的余票和价格信息。

### Props
| 属性名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| type | 座位类型 | String | - | 是 |
| ticket | 车票信息 | Object | - | 是 |

### 使用示例

```vue
<template>
  <el-table>
    <SeatColumn
      v-for="type in seatTypes"
      :key="type"
      :type="type"
      :ticket="ticket"
    />
  </el-table>
</template>

<script setup>
import { SeatColumn } from '@/components'

const seatTypes = [
  '商务座',
  '一等座',
  '二等座',
  '软卧',
  '硬卧',
  '硬座',
  '无座'
]
</script>
```

## StopsDialog

### 功能描述
显示列车经停站信息的弹窗组件。

### Props
| 属性名 | 说明 | 类型 | 默认值 | 必填 |
|--------|------|------|--------|------|
| modelValue | 控制弹窗显示 | Boolean | false | 是 |
| stops | 经停站列表 | Array | [] | 是 |

### Events
| 事件名 | 说明 | 参数 |
|--------|------|------|
| update:modelValue | 更新弹窗显示状态 | visible: boolean |

### 使用示例

```vue
<template>
  <StopsDialog
    v-model="dialogVisible"
    :stops="trainStops"
  />
</template>

<script setup>
import { ref } from 'vue'
import { StopsDialog } from '@/components'

const dialogVisible = ref(false)
const trainStops = ref([])

// 显示弹窗
const showDialog = () => {
  dialogVisible.value = true
}
</script>
```

## ThemeSettings

### 功能描述
提供主题设置功能，包括深色模式切换和主题色选择。

### Props
无

### 使用示例

```vue
<template>
  <div class="theme-settings">
    <ThemeSettings />
  </div>
</template>

<script setup>
import { ThemeSettings } from '@/components'
</script>

<style>
.theme-settings {
  position: fixed;
  right: 20px;
  top: 20px;
}
</style>
```

## 组件样式定制

### 全局样式变量

```css
:root {
  /* 主题色 */
  --el-color-primary: #409eff;
  
  /* 文字颜色 */
  --el-text-color-primary: #303133;
  --el-text-color-regular: #606266;
  --el-text-color-secondary: #909399;
  
  /* 边框颜色 */
  --el-border-color-base: #dcdfe6;
  --el-border-color-light: #e4e7ed;
  
  /* 背景颜色 */
  --el-bg-color: #ffffff;
  --el-bg-color-overlay: #ffffff;
}

/* 深色模式 */
html.dark {
  --el-bg-color: #141414;
  --el-bg-color-overlay: #1d1e1f;
  --el-text-color-primary: #ffffff;
  --el-border-color-base: #434343;
}
```

### 组件样式覆盖

```vue
<style scoped>
/* 自定义组件样式 */
.search-form {
  background: var(--el-bg-color-overlay);
  border-radius: 8px;
  padding: 20px;
  box-shadow: var(--el-box-shadow-light);
}

/* 深色模式适配 */
:global(.dark) .search-form {
  background: var(--el-bg-color-overlay);
  box-shadow: var(--el-box-shadow-dark);
}
</style>
```

## 最佳实践

### 1. 组件通信
- 使用 Props 和 Events 进行父子组件通信
- 使用 Pinia store 进行跨组件状态管理
- 避免使用全局事件总线

### 2. 性能优化
- 合理使用 `v-show` 和 `v-if`
- 使用 `computed` 缓存计算结果
- 大列表使用虚拟滚动

### 3. 错误处理
- 为所有必填 Props 添加验证
- 添加适当的错误边界
- 使用 try-catch 处理异步操作

### 4. 可访问性
- 添加适当的 ARIA 属性
- 确保键盘可访问性
- 提供足够的颜色对比度

### 5. 响应式设计
- 使用相对单位（rem, em）
- 添加媒体查询断点
- 测试不同屏幕尺寸 