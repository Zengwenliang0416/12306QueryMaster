<template>
  <div class="container">
    <el-container class="main-container">
      <el-header>
        <h1>12306 列车查询系统</h1>
      </el-header>
      
      <el-main>
        <el-form :model="store.searchForm" label-width="120px" class="search-form">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="出发站">
                <el-autocomplete
                  v-model="store.searchForm.fromStation"
                  :fetch-suggestions="store.queryStations"
                  placeholder="请输入出发站"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="到达站">
                <el-autocomplete
                  v-model="store.searchForm.toStation"
                  :fetch-suggestions="store.queryStations"
                  placeholder="请输入到达站"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="出发日期">
                <el-date-picker
                  v-model="store.searchForm.trainDate"
                  type="date"
                  placeholder="选择日期"
                  :disabled-date="disablePastDates"
                  format="YYYY-MM-DD"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="车型">
                <el-select
                  v-model="store.searchForm.trainTypes"
                  multiple
                  placeholder="选择车型"
                >
                  <el-option label="高铁" value="G" />
                  <el-option label="动车" value="D" />
                  <el-option label="普通车" value="K" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="出发时间">
                <el-time-select
                  v-model="store.searchForm.startTime"
                  placeholder="起始时间"
                  start="00:00"
                  step="00:30"
                  end="23:30"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="到达时间">
                <el-time-select
                  v-model="store.searchForm.endTime"
                  placeholder="结束时间"
                  start="00:00"
                  step="00:30"
                  end="23:30"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row>
            <el-col :span="24">
              <el-form-item label="经停站">
                <el-autocomplete
                  v-model="store.searchForm.viaStation"
                  :fetch-suggestions="store.queryStations"
                  placeholder="可选，输入经停站"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <el-button type="primary" @click="store.searchTickets" :loading="store.loading">
              {{ store.loading ? '查询中...' : '查询车票' }}
            </el-button>
            <el-button @click="store.resetForm" :disabled="store.loading">重置</el-button>
          </el-form-item>
        </el-form>

        <!-- 查询结果表格 -->
        <el-table 
          v-if="store.tickets.length" 
          :data="store.tickets" 
          style="width: 100%" 
          border
          stripe
          highlight-current-row
          v-loading="store.loading"
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
          <el-table-column label="商务座" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.商务座 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.商务座">¥{{ scope.row.prices.商务座 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="一等座" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.一等座 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.一等座">¥{{ scope.row.prices.一等座 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="二等座" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.二等座 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.二等座">¥{{ scope.row.prices.二等座 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="软卧" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.软卧 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.软卧">¥{{ scope.row.prices.软卧 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="硬卧" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.硬卧 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.硬卧">¥{{ scope.row.prices.硬卧 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="硬座" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.硬座 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.硬座">¥{{ scope.row.prices.硬座 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="无座" min-width="90" align="center">
            <template #default="scope">
              <div>
                <div>{{ scope.row.seats?.无座 || '--' }}</div>
                <div class="price-tag" v-if="scope.row.prices?.无座">¥{{ scope.row.prices.无座 }}</div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="90" align="center" fixed="right">
            <template #default="scope">
              <el-button
                type="primary"
                size="small"
                @click="store.showTrainStops(scope.row.train_code)"
                :loading="store.loadingStops[scope.row.train_code]"
              >
                经停站
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 无数据时显示提示 -->
        <el-empty
          v-else-if="!store.loading"
          description="暂无符合条件的车次"
        />
      </el-main>
    </el-container>

    <!-- 经停站弹窗 -->
    <el-dialog
      v-model="store.stopsDialogVisible"
      title="经停站信息"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-table 
        :data="store.trainStops" 
        style="width: 100%"
      >
        <el-table-column prop="station_name" label="站名" align="center" />
        <el-table-column label="到达时间" align="center">
          <template #default="scope">
            {{ scope.row.arrival_time || '--' }}
          </template>
        </el-table-column>
        <el-table-column label="出发时间" align="center">
          <template #default="scope">
            {{ scope.row.departure_time || '--' }}
          </template>
        </el-table-column>
        <el-table-column label="停留时间" align="center">
          <template #default="scope">
            {{ scope.row.stopover_time || '--' }}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import dayjs from 'dayjs'
import { useTicketStore } from './stores/ticket'

const store = useTicketStore()

// 在组件挂载时从 localStorage 恢复状态
onMounted(() => {
  store.initializeFromStorage()
})

// 禁用过去的日期
const disablePastDates = (date) => {
  return date < dayjs().startOf('day')
}
</script>

<style scoped>
.container {
  width: 100%;
  min-height: 100vh;
  padding: 0;
  margin: 0;
}

.main-container {
  height: 100vh;
}

.el-header {
  text-align: center;
  line-height: 60px;
  background-color: #f5f7fa;
  padding: 0;
  height: 60px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12);
}

.el-main {
  padding: 20px;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.search-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.text-gray {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.price-tag {
  color: #F56C6C;
  font-size: 12px;
  margin-top: 4px;
}

:deep(.el-table) {
  margin-top: 20px;
  border-radius: 8px;
  overflow: hidden;
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
