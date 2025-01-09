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
import { defineProps } from 'vue'

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
  color: #f56c6c;
  font-size: 12px;
  margin-top: 2px;
}

.text-success {
  color: #67c23a;
}

.text-warning {
  color: #e6a23c;
}

.text-danger {
  color: #f56c6c;
}

.text-gray {
  color: #909399;
}
</style> 