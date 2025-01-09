<template>
  <div class="container">
    <el-container class="main-container">
      <el-header>
        <h1>12306 列车查询系统</h1>
      </el-header>
      
      <el-main>
        <el-form :model="searchForm" label-width="120px" class="search-form">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="出发站">
                <el-autocomplete
                  v-model="searchForm.fromStation"
                  :fetch-suggestions="queryStations"
                  placeholder="请输入出发站"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="到达站">
                <el-autocomplete
                  v-model="searchForm.toStation"
                  :fetch-suggestions="queryStations"
                  placeholder="请输入到达站"
                />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="出发日期">
                <el-date-picker
                  v-model="searchForm.trainDate"
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
                  v-model="searchForm.trainTypes"
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
                  v-model="searchForm.startTime"
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
                  v-model="searchForm.endTime"
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
                  v-model="searchForm.viaStation"
                  :fetch-suggestions="queryStations"
                  placeholder="可选，输入经停站"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item>
            <el-button type="primary" @click="searchTickets" :loading="loading">
              {{ loading ? '查询中...' : '查询车票' }}
            </el-button>
            <el-button @click="resetForm" :disabled="loading">重置</el-button>
          </el-form-item>
        </el-form>

        <!-- 查询结果表格 -->
        <el-table 
          v-if="tickets.length" 
          :data="tickets" 
          style="width: 100%" 
          border
          stripe
          highlight-current-row
          v-loading="loading"
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
                @click="showTrainStops(scope.row.train_code)"
                :loading="stopsLoading"
              >
                经停站
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 无数据时显示提示 -->
        <el-empty
          v-else-if="!loading"
          description="暂无符合条件的车次"
        />
      </el-main>
    </el-container>

    <!-- 经停站弹窗 -->
    <el-dialog
      v-model="stopsDialogVisible"
      title="经停站信息"
      width="50%"
      :close-on-click-modal="false"
    >
      <el-table 
        :data="trainStops" 
        style="width: 100%"
        v-loading="stopsLoading"
      >
        <el-table-column prop="station" label="站名" />
        <el-table-column prop="arriveTime" label="到达时间" />
        <el-table-column prop="departTime" label="出发时间" />
        <el-table-column prop="stopTime" label="停留时间" />
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

// 定义响应式数据
const searchForm = reactive({
  fromStation: '',
  toStation: '',
  trainDate: '',
  trainTypes: [],
  startTime: '',
  endTime: '',
  viaStation: '',
})

const tickets = ref([])
const trainStops = ref([])
const stopsDialogVisible = ref(false)
const loading = ref(false)
const stopsLoading = ref(false)

// API 基础URL
const API_BASE_URL = 'http://localhost:8001/api'

// 站点查询建议
async function queryStations(query, cb) {
  if (query.length < 1) {
    cb([])
    return
  }
  try {
    const response = await axios.get(`${API_BASE_URL}/stations/${query}`)
    const suggestions = response.data.map(station => ({
      value: station.name,
      label: `${station.name} (${station.code})`
    }))
    cb(suggestions)
  } catch (error) {
    console.error('Error fetching stations:', error)
    ElMessage.error('站点查询失败：' + (error.response?.data?.detail || error.message))
    cb([])
  }
}

// 禁用过去的日期
const disablePastDates = (date) => {
  return date < dayjs().startOf('day')
}

// 表单验证
function validateForm() {
  if (!searchForm.fromStation) {
    ElMessage.warning('请输入出发站')
    return false
  }
  if (!searchForm.toStation) {
    ElMessage.warning('请输入到达站')
    return false
  }
  if (!searchForm.trainDate) {
    ElMessage.warning('请选择出发日期')
    return false
  }
  return true
}

// 查询车票
async function searchTickets() {
  if (!validateForm()) return

  loading.value = true
  try {
    const response = await axios.post(`${API_BASE_URL}/tickets/query`, {
      from_station: searchForm.fromStation,
      to_station: searchForm.toStation,
      train_date: dayjs(searchForm.trainDate).format('YYYY-MM-DD'),
      purpose_codes: 'ADULT',
      train_types: searchForm.trainTypes,
      start_time: searchForm.startTime,
      end_time: searchForm.endTime,
      via_station: searchForm.viaStation || undefined
    })
    console.log('Response:', response.data)
    tickets.value = response.data
    if (tickets.value.length === 0) {
      ElMessage.info('未找到符合条件的车次')
    }
  } catch (error) {
    console.error('Error searching tickets:', error)
    ElMessage.error('查询失败：' + (error.response?.data?.detail || error.message))
    tickets.value = []
  } finally {
    loading.value = false
  }
}

// 重置表单
function resetForm() {
  Object.keys(searchForm).forEach(key => {
    searchForm[key] = Array.isArray(searchForm[key]) ? [] : ''
  })
  tickets.value = []
}

// 查看经停站信息
async function showTrainStops(trainCode) {
  stopsLoading.value = true
  try {
    const response = await axios.get(`${API_BASE_URL}/trains/${trainCode}/stops`)
    trainStops.value = response.data.map(stop => ({
      station: stop.station_name,
      arriveTime: stop.arrival_time || '--',
      departTime: stop.departure_time || '--',
      stopTime: stop.stopover_time || '--'
    }))
    stopsDialogVisible.value = true
  } catch (error) {
    console.error('Error fetching train stops:', error)
    ElMessage.error('获取经停站信息失败：' + (error.response?.data?.detail || error.message))
  } finally {
    stopsLoading.value = false
  }
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
