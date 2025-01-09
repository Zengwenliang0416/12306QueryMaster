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
            class="search-input"
            :popper-class="isDark ? 'dark-suggestions' : ''"
          />
        </el-form-item>
      </el-col>
      <el-col :span="8">
        <el-form-item label="到达站">
          <el-autocomplete
            v-model="store.searchForm.toStation"
            :fetch-suggestions="store.queryStations"
            placeholder="请输入到达站"
            class="search-input"
            :popper-class="isDark ? 'dark-suggestions' : ''"
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
            class="search-input"
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
            class="search-input"
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
            class="search-input"
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
            class="search-input"
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
            class="search-input"
            :popper-class="isDark ? 'dark-suggestions' : ''"
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
import { useThemeStore } from '../stores/theme'
import { computed } from 'vue'
import dayjs from 'dayjs'

const store = useTicketStore()
const themeStore = useThemeStore()

const isDark = computed(() => themeStore.isDark)

// 禁用过去的日期
const disablePastDates = (date) => {
  return date < dayjs().startOf('day')
}
</script>

<style scoped>
.search-form {
  background: var(--el-bg-color-overlay);
  padding: 20px;
  border-radius: 8px;
  box-shadow: var(--el-box-shadow-light);
  margin-bottom: 20px;
  transition: all 0.3s;
}

.search-input {
  width: 100%;
}

:deep(.el-input__wrapper) {
  background-color: var(--el-bg-color-overlay);
  border-color: var(--el-border-color);
  box-shadow: 0 0 0 1px var(--el-border-color) inset;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset !important;
}

:deep(.el-input__inner) {
  color: var(--el-text-color-primary);
}

:deep(.el-input__inner::placeholder) {
  color: var(--el-text-color-placeholder);
}

/* 暗黑模式适配 */
:global(.dark) .search-form {
  background: var(--el-bg-color);
  box-shadow: var(--el-box-shadow);
}

:global(.dark) :deep(.el-form-item__label) {
  color: var(--el-text-color-primary);
}

:global(.dark) :deep(.el-input__wrapper) {
  background-color: var(--el-bg-color);
}

:global(.dark) :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-border-color-hover) inset;
}

:global(.dark) :deep(.el-select__tags) {
  background-color: transparent;
}

/* 下拉建议框暗黑模式 */
:global(.dark-suggestions) {
  background-color: var(--el-bg-color) !important;
  border-color: var(--el-border-color) !important;
}

:global(.dark-suggestions .el-autocomplete-suggestion__wrap) {
  background-color: var(--el-bg-color) !important;
}

:global(.dark-suggestions .el-autocomplete-suggestion__list li) {
  color: var(--el-text-color-primary) !important;
}

:global(.dark-suggestions .el-autocomplete-suggestion__list li:hover) {
  background-color: var(--el-fill-color-light) !important;
}

/* 日期选择器暗黑模式 */
:deep(.el-picker__popper) {
  background-color: var(--el-bg-color) !important;
  border-color: var(--el-border-color) !important;
}

:deep(.el-picker-panel) {
  background-color: var(--el-bg-color) !important;
  border-color: var(--el-border-color) !important;
}

:deep(.el-picker-panel__icon-btn) {
  color: var(--el-text-color-primary) !important;
}

:deep(.el-date-picker__header-label) {
  color: var(--el-text-color-primary) !important;
}

:deep(.el-date-table th) {
  color: var(--el-text-color-regular) !important;
}

:deep(.el-date-table td.next-month .el-date-table-cell__text,
      .el-date-table td.prev-month .el-date-table-cell__text) {
  color: var(--el-text-color-placeholder) !important;
}
</style> 