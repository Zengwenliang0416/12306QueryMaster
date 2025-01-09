<!-- 车票查询结果表格组件 -->
<template>
  <div>
    <el-table 
      v-if="tickets && tickets.length > 0" 
      :data="tickets" 
      style="width: 100%" 
      border
      stripe
      highlight-current-row
      :loading="loading"
      max-height="calc(100vh - 400px)"
    >
      <el-table-column prop="train_code" label="车次" min-width="80" align="center" />
      <el-table-column label="出发站" min-width="100" align="center">
        <template #default="scope">
          {{ scope.row.from_station.station_name }}
        </template>
      </el-table-column>
      <el-table-column label="到达站" min-width="100" align="center">
        <template #default="scope">
          {{ scope.row.to_station.station_name }}
        </template>
      </el-table-column>
      <el-table-column label="出发时间" min-width="150" align="center">
        <template #default="scope">
          <div>{{ scope.row.from_station.departure_time }}</div>
          <div class="text-gray">{{ scope.row.from_station.station_name }}</div>
        </template>
      </el-table-column>
      <el-table-column label="到达时间" min-width="150" align="center">
        <template #default="scope">
          <div>{{ scope.row.to_station.arrival_time }}</div>
          <div class="text-gray">{{ scope.row.to_station.station_name }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="duration" label="历时" min-width="80" align="center" />
      
      <SeatColumn v-for="type in seatTypes" :key="type" :type="type" />

      <el-table-column label="操作" min-width="90" align="center" fixed="right">
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="onShowStops(scope.row.train_code)"
            :loading="loadingStops[scope.row.train_code]"
          >
            经停站
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-empty
      v-else-if="!loading && (!tickets || tickets.length === 0)"
      description="暂无符合条件的车次"
    />
  </div>
</template>

<script setup>
import { watchEffect } from 'vue'
import SeatColumn from './SeatColumn.vue'

const props = defineProps({
  tickets: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingStops: {
    type: Object,
    default: () => ({})
  }
})

// Add watcher for debugging
watchEffect(() => {
  console.log('TicketTable tickets prop:', props.tickets)
  console.log('TicketTable tickets length:', props.tickets.length)
})

const emit = defineEmits(['showStops'])

const seatTypes = [
  '商务座',
  '一等座',
  '二等座',
  '软卧',
  '硬卧',
  '硬座',
  '无座'
]

const onShowStops = (trainCode) => {
  emit('showStops', trainCode)
}
</script>

<style scoped>
.text-gray {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
  transition: all 0.3s;
  border: 1px solid var(--el-border-color-light);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

:deep(.el-table:hover) {
  box-shadow: var(--el-box-shadow);
  transform: translateY(-2px);
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
  transition: all 0.3s;
}

:deep(.el-table tr:hover td) {
  background-color: var(--el-bg-color-overlay) !important;
}

:deep(.el-table .cell) {
  white-space: nowrap;
  line-height: 1.5;
}

:deep(.el-button--small) {
  padding: 8px 16px;
  font-weight: 500;
  transition: all 0.3s;
  border-radius: 6px;
}

:deep(.el-button--small:not(.is-disabled):hover) {
  transform: translateY(-2px);
}

:deep(.el-empty) {
  padding: 40px 0;
}

:deep(.el-empty__description) {
  margin-top: 16px;
  color: var(--el-text-color-secondary);
}

:deep(.el-empty__image) {
  opacity: 0.8;
}

/* 暗黑模式适配 */
:global(.dark) :deep(.el-table) {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color-darker);
}

:global(.dark) :deep(.el-table th) {
  background-color: rgba(0, 0, 0, 0.2) !important;
  border-bottom-color: var(--el-border-color-darker);
}

:global(.dark) :deep(.el-table td) {
  border-bottom-color: var(--el-border-color-darker);
}

:global(.dark) :deep(.el-table tr:hover td) {
  background-color: rgba(0, 0, 0, 0.2) !important;
}

:global(.dark) :deep(.el-table--enable-row-hover .el-table__body tr:hover > td.el-table__cell) {
  background-color: rgba(0, 0, 0, 0.3) !important;
}

/* 响应式布局 */
@media (max-width: 768px) {
  :deep(.el-table th) {
    padding: 8px;
    font-size: 13px;
  }

  :deep(.el-table td) {
    padding: 8px;
  }

  :deep(.el-button--small) {
    padding: 6px 12px;
    font-size: 12px;
  }

  .text-gray {
    font-size: 11px;
  }
}
</style> 