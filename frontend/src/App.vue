<template>
  <div class="container">
    <el-container class="main-container">
      <el-header>
        <h1>12306 列车查询系统</h1>
      </el-header>
      
      <el-main>
        <SearchForm />
        
        <TicketTable
          :tickets="store.tickets"
          :loading="store.loading"
          :loading-stops="store.loadingStops"
          @show-stops="store.showTrainStops"
        />

        <StopsDialog
          :model-value="store.stopsDialogVisible"
          @update:model-value="store.stopsDialogVisible = $event"
          :stops="store.trainStops"
        />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useTicketStore } from './stores/ticket'
import SearchForm from './components/SearchForm.vue'
import TicketTable from './components/TicketTable.vue'
import StopsDialog from './components/StopsDialog.vue'

const store = useTicketStore()
</script>

<style>
.container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.el-header {
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h1 {
  color: #409eff;
  margin: 0;
  font-size: 24px;
}
</style>
