<!-- 车票搜索表单组件 -->
<template>
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
</template>

<script setup>
import { useTicketStore } from '../stores/ticket'
import dayjs from 'dayjs'

const store = useTicketStore()

// 禁用过去的日期
const disablePastDates = (date) => {
  return date < dayjs().startOf('day')
}
</script>

<style scoped>
.search-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
</style> 