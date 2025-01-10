# 开发指南

本文档提供了12306列车查询系统的开发指南，包括项目结构、开发规范和最佳实践。

## 目录

- [项目结构](#项目结构)
- [开发环境](#开发环境)
- [代码规范](#代码规范)
- [开发流程](#开发流程)
- [测试指南](#测试指南)
- [性能优化](#性能优化)
- [安全指南](#安全指南)
- [常见问题](#常见问题)

## 项目结构

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

## 开发环境

### 1. 后端环境

#### Python环境配置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows

# 安装依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt
```

#### 开发工具配置
- VS Code Python插件设置
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "88"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

### 2. 前端环境

#### Node.js环境配置
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

#### VS Code配置
```json
{
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "prettier.semi": false,
    "prettier.singleQuote": true,
    "vetur.format.defaultFormatter.html": "prettier",
    "vetur.format.defaultFormatter.js": "prettier"
}
```

## 代码规范

### 1. Python代码规范

#### 命名规范
- 类名使用驼峰命名法（CamelCase）
- 函数和变量使用小写字母和下划线（snake_case）
- 常量使用大写字母和下划线
- 私有方法和变量以单下划线开头

```python
# 示例
class TrainService:
    DEFAULT_TIMEOUT = 30

    def __init__(self):
        self._cache = {}

    def get_train_info(self, train_code: str) -> dict:
        return self._fetch_train_data(train_code)

    def _fetch_train_data(self, train_code: str) -> dict:
        # 实现细节
        pass
```

#### 类型注解
- 使用类型注解提高代码可读性
- 使用Optional表示可选参数
- 使用Union表示多类型
- 使用TypeVar定义泛型

```python
from typing import Optional, List, Union, TypeVar

T = TypeVar('T')

def find_trains(
    from_station: str,
    to_station: str,
    date: str,
    train_types: Optional[List[str]] = None
) -> List[dict]:
    pass

def get_price(value: Union[int, float]) -> str:
    return f"¥{float(value):.2f}"
```

#### 文档字符串
- 使用Google风格的文档字符串
- 包含参数说明、返回值和异常信息
- 添加示例代码

```python
def query_tickets(
    from_station: str,
    to_station: str,
    date: str
) -> List[dict]:
    """查询车票信息。

    Args:
        from_station: 出发站名称
        to_station: 到达站名称
        date: 出发日期，格式：YYYY-MM-DD

    Returns:
        包含车票信息的列表

    Raises:
        ValueError: 当站名无效时
        HTTPError: 当API请求失败时

    Example:
        >>> query_tickets("北京", "上海", "2024-01-20")
        [{'train_code': 'G1234', ...}]
    """
    pass
```

### 2. Vue代码规范

#### 组件规范
- 使用PascalCase命名组件
- 组件名应该是多个单词
- Props应该使用camelCase
- 事件名使用kebab-case

```vue
<!-- SearchForm.vue -->
<template>
  <div class="search-form">
    <el-form :model="formData" @submit.prevent="handleSubmit">
      <!-- 表单内容 -->
    </el-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useTicketStore } from '@/stores/ticket'

const props = defineProps({
  initialDate: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['search-complete'])

const formData = ref({
  fromStation: '',
  toStation: '',
  date: props.initialDate
})

const handleSubmit = async () => {
  // 处理提交
  emit('search-complete', result)
}
</script>
```

#### 样式规范
- 使用scoped样式
- 使用BEM命名约定
- 避免深层嵌套
- 使用变量管理主题

```vue
<style scoped>
.search-form {
  /* 组件根元素样式 */
}

.search-form__input {
  /* 输入框样式 */
}

.search-form__button {
  /* 按钮样式 */
}

.search-form__button--primary {
  /* 主要按钮样式 */
}
</style>
```

## 开发流程

### 1. 功能开发流程

1. 需求分析
   - 理解需求文档
   - 确定技术方案
   - 评估开发周期

2. 开发阶段
   - 创建功能分支
   - 编写代码
   - 编写测试
   - 本地测试

3. 代码审查
   - 提交Pull Request
   - 代码评审
   - 修改反馈

4. 测试验证
   - 运行测试套件
   - 功能测试
   - 性能测试

5. 发布上线
   - 合并主分支
   - 部署测试环境
   - 部署生产环境

### 2. Git工作流

```bash
# 创建功能分支
git checkout -b feature/ticket-search

# 提交代码
git add .
git commit -m "feat: implement ticket search functionality"

# 推送分支
git push origin feature/ticket-search

# 合并主分支
git checkout main
git merge feature/ticket-search
```

## 测试指南

### 1. 后端测试

#### 单元测试
```python
# test_train_service.py
import pytest
from app.services.train_service import TrainService

def test_get_train_info():
    service = TrainService()
    result = service.get_train_info("G1234")
    
    assert result is not None
    assert result["train_code"] == "G1234"
    assert "seats" in result
```

#### API测试
```python
# test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_tickets():
    response = client.post(
        "/api/tickets/query",
        json={
            "from_station": "北京",
            "to_station": "上海",
            "date": "2024-01-20"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "tickets" in data
```

### 2. 前端测试

#### 组件测试
```javascript
// SearchForm.test.js
import { mount } from '@vue/test-utils'
import SearchForm from './SearchForm.vue'

describe('SearchForm', () => {
  test('emits search-complete event when form is submitted', async () => {
    const wrapper = mount(SearchForm)
    
    await wrapper.find('form').trigger('submit')
    
    expect(wrapper.emitted('search-complete')).toBeTruthy()
  })
})
```

#### E2E测试
```javascript
// search.spec.js
describe('Train Search', () => {
  it('should display search results', () => {
    cy.visit('/')
    
    cy.get('[data-test="from-station"]').type('北京')
    cy.get('[data-test="to-station"]').type('上海')
    cy.get('[data-test="search-button"]').click()
    
    cy.get('[data-test="result-table"]').should('be.visible')
  })
})
```

## 性能优化

### 1. 后端优化

#### 缓存策略
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=1000)
def get_station_info(station_code: str) -> dict:
    # 获取站点信息
    pass

def clear_expired_cache():
    # 清理过期缓存
    pass
```

#### 数据库优化
```python
# 使用异步操作
async def get_train_schedule(train_code: str):
    async with async_session() as session:
        result = await session.execute(
            select(Schedule).where(Schedule.train_code == train_code)
        )
        return result.scalar_one_or_none()
```

### 2. 前端优化

#### 组件优化
```vue
<!-- 使用异步组件 -->
<script setup>
import { defineAsyncComponent } from 'vue'

const TicketTable = defineAsyncComponent(() =>
  import('./components/TicketTable.vue')
)
</script>

<!-- 使用虚拟列表 -->
<template>
  <el-table
    v-virtual-scroll="{ itemSize: 48, buffer: 5 }"
    :data="tickets"
  >
    <!-- 表格内容 -->
  </el-table>
</template>
```

#### 状态管理优化
```javascript
// 使用持久化存储
import { defineStore } from 'pinia'
import { useLocalStorage } from '@vueuse/core'

export const useTicketStore = defineStore('ticket', () => {
  const searchHistory = useLocalStorage('search-history', [])
  
  // store实现
})
```

## 安全指南

### 1. 输入验证
```python
from pydantic import BaseModel, validator
from datetime import date, timedelta

class TicketQuery(BaseModel):
    from_station: str
    to_station: str
    date: date

    @validator('date')
    def validate_date(cls, v):
        today = date.today()
        if v < today:
            raise ValueError('不能查询过去的日期')
        if v > today + timedelta(days=30):
            raise ValueError('只能查询30天内的车票')
        return v
```

### 2. 请求限制
```python
from fastapi import HTTPException
from fastapi.middleware.throttling import ThrottlingMiddleware

app.add_middleware(
    ThrottlingMiddleware,
    rate_limit=100,  # 每分钟请求次数
    rate_window=60   # 时间窗口（秒）
)
```

### 3. 错误处理
```python
from fastapi import HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail,
            "path": request.url.path
        }
    )
```

## 常见问题

### 1. 开发环境问题

#### 问题：环境依赖冲突
解决方案：
- 使用虚拟环境
- 定期更新依赖
- 锁定依赖版本

#### 问题：热重载不生效
解决方案：
- 检查配置文件
- 清除缓存
- 重启开发服务器

### 2. 性能问题

#### 问题：查询响应慢
解决方案：
- 添加缓存
- 优化数据库查询
- 使用异步操作

#### 问题：内存占用高
解决方案：
- 及时释放资源
- 优化数据结构
- 使用连接池

### 3. 部署问题

#### 问题：服务启动失败
解决方案：
- 检查配置文件
- 查看错误日志
- 验证环境变量

#### 问题：静态资源404
解决方案：
- 检查构建配置
- 验证部署路径
- 配置Nginx规则 