<!-- 座位列组件 -->
<template>
  <el-table-column :label="type" min-width="90" align="center">
    <template #default="scope">
      <div>
        <div :class="getSeatClass(scope.row.seats?.[type])">
          {{ formatSeatInfo(scope.row.seats?.[type]) }}
        </div>
        <div class="price-tag" v-if="scope.row.prices?.[type]">¥{{ scope.row.prices[type] }}</div>
      </div>
    </template>
  </el-table-column>
</template>

<script setup>
defineProps({
  type: {
    type: String,
    required: true
  }
})

const formatSeatInfo = (value) => {
  if (!value || value === '--') return '--'
  if (value === '有票' || value === '有') return '有票'
  if (value === '无票' || value === '无') return '无票'
  return value
}

const getSeatClass = (value) => {
  if (!value || value === '--') return 'text-gray'
  if (value === '有票' || value === '有') return 'text-success'
  if (value === '无票' || value === '无') return 'text-danger'
  return 'text-warning'
}
</script>

<style scoped>
.price-tag {
  color: var(--el-color-danger);
  font-size: 12px;
  margin-top: 4px;
  font-weight: 500;
  transition: all 0.3s;
}

.text-success {
  color: var(--el-color-success);
  font-weight: 500;
  transition: all 0.3s;
}

.text-success:hover {
  color: var(--el-color-success-dark-2);
  transform: scale(1.05);
}

.text-warning {
  color: var(--el-color-warning);
  font-weight: 500;
  transition: all 0.3s;
}

.text-warning:hover {
  color: var(--el-color-warning-dark-2);
  transform: scale(1.05);
}

.text-danger {
  color: var(--el-color-danger);
  font-weight: 500;
  transition: all 0.3s;
}

.text-danger:hover {
  color: var(--el-color-danger-dark-2);
  transform: scale(1.05);
}

.text-gray {
  color: var(--el-text-color-secondary);
  font-weight: 500;
  transition: all 0.3s;
}

.text-gray:hover {
  color: var(--el-text-color-primary);
  transform: scale(1.05);
}

/* 暗黑模式适配 */
:global(.dark) .price-tag {
  color: var(--el-color-danger-light-3);
}

:global(.dark) .text-success {
  color: var(--el-color-success-light-3);
}

:global(.dark) .text-success:hover {
  color: var(--el-color-success-light-5);
}

:global(.dark) .text-warning {
  color: var(--el-color-warning-light-3);
}

:global(.dark) .text-warning:hover {
  color: var(--el-color-warning-light-5);
}

:global(.dark) .text-danger {
  color: var(--el-color-danger-light-3);
}

:global(.dark) .text-danger:hover {
  color: var(--el-color-danger-light-5);
}

:global(.dark) .text-gray {
  color: var(--el-text-color-secondary);
}

:global(.dark) .text-gray:hover {
  color: var(--el-text-color-primary);
}

/* 响应式布局 */
@media (max-width: 768px) {
  .price-tag {
    font-size: 11px;
    margin-top: 2px;
  }
}
</style> 