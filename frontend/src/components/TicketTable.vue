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
  color: #909399;
  font-size: 12px;
}

:deep(.el-table) {
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
}

:deep(.el-table th) {
  background-color: #f5f7fa !important;
  height: 50px;
}

:deep(.el-table td) {
  padding: 8px 0;
}

:deep(.el-button--small) {
  padding: 6px 12px;
}

:deep(.el-table .cell) {
  white-space: nowrap;
}
</style> 