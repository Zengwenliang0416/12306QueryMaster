<!-- 经停站弹窗组件 -->
<template>
  <el-dialog
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    title="经停站信息"
    width="50%"
    :close-on-click-modal="false"
  >
    <el-table 
      :data="stops" 
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
.el-dialog {
  border-radius: 8px;
  overflow: hidden;
}

.el-table {
  margin: -20px;
}
</style> 