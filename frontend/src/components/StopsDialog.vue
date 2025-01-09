<!-- 经停站弹窗组件 -->
<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="经停站信息"
    width="50%"
    :close-on-click-modal="false"
    class="stops-dialog"
  >
    <el-table 
      :data="stops" 
      style="width: 100%"
      :max-height="500"
    >
      <el-table-column prop="station_name" label="站名" align="center" min-width="120" />
      <el-table-column label="到达时间" align="center" min-width="120">
        <template #default="scope">
          <span :class="{ 'highlight-time': scope.row.arrival_time }">
            {{ scope.row.arrival_time || '--' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="出发时间" align="center" min-width="120">
        <template #default="scope">
          <span :class="{ 'highlight-time': scope.row.departure_time }">
            {{ scope.row.departure_time || '--' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column label="停留时间" align="center" min-width="120">
        <template #default="scope">
          <span :class="{ 'stopover-time': scope.row.stopover_time }">
            {{ scope.row.stopover_time || '--' }}
          </span>
        </template>
      </el-table-column>
    </el-table>
  </el-dialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  stops: {
    type: Array,
    required: true
  }
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
:deep(.stops-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-dialog) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-dialog__header) {
  margin: 0;
  padding: 20px 24px;
  border-bottom: 1px solid var(--el-border-color-light);
}

:deep(.el-dialog__title) {
  font-weight: 600;
  font-size: 18px;
}

:deep(.el-dialog__body) {
  padding: 0;
}

:deep(.el-table) {
  border-radius: 0;
}

:deep(.el-table th) {
  background-color: var(--el-bg-color-overlay) !important;
  height: 50px;
  font-weight: 600;
  font-size: 14px;
  color: var(--el-text-color-primary) !important;
  border-bottom: 1px solid var(--el-border-color-light);
}

:deep(.el-table td) {
  padding: 12px 0;
}

.highlight-time {
  color: var(--el-color-primary);
  font-weight: 500;
  transition: all 0.3s;
}

.highlight-time:hover {
  color: var(--el-color-primary-dark-2);
  transform: scale(1.05);
}

.stopover-time {
  color: var(--el-color-warning);
  font-weight: 500;
  transition: all 0.3s;
}

.stopover-time:hover {
  color: var(--el-color-warning-dark-2);
  transform: scale(1.05);
}

/* 暗黑模式适配 */
:global(.dark) :deep(.el-dialog) {
  background-color: var(--el-bg-color);
  border: 1px solid var(--el-border-color-darker);
  box-shadow: var(--el-box-shadow);
}

:global(.dark) :deep(.el-dialog__header) {
  border-bottom-color: var(--el-border-color-darker);
}

:global(.dark) :deep(.el-table) {
  background-color: var(--el-bg-color);
}

:global(.dark) :deep(.el-table th) {
  background-color: rgba(0, 0, 0, 0.2) !important;
  border-bottom-color: var(--el-border-color-darker);
}

:global(.dark) :deep(.el-table td) {
  border-bottom-color: var(--el-border-color-darker);
}

:global(.dark) .highlight-time {
  color: var(--el-color-primary-light-3);
}

:global(.dark) .highlight-time:hover {
  color: var(--el-color-primary-light-5);
}

:global(.dark) .stopover-time {
  color: var(--el-color-warning-light-3);
}

:global(.dark) .stopover-time:hover {
  color: var(--el-color-warning-light-5);
}

/* 响应式布局 */
@media (max-width: 768px) {
  :deep(.el-dialog) {
    width: 90% !important;
    margin: 0 auto;
  }

  :deep(.el-dialog__header) {
    padding: 16px 20px;
  }

  :deep(.el-dialog__title) {
    font-size: 16px;
  }

  :deep(.el-table th) {
    padding: 8px;
    font-size: 13px;
  }

  :deep(.el-table td) {
    padding: 8px;
    font-size: 13px;
  }
}
</style> 