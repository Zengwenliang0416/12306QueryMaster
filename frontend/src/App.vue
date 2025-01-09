<template>
  <div class="container">
    <el-container class="main-container">
      <el-header>
        <h1>12306 列车查询系统</h1>
        <div class="header-actions">
          <ThemeSettings />
        </div>
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
import { useThemeStore } from './stores/theme'
import SearchForm from './components/SearchForm.vue'
import TicketTable from './components/TicketTable.vue'
import StopsDialog from './components/StopsDialog.vue'
import ThemeSettings from './components/ThemeSettings.vue'

const store = useTicketStore()
const themeStore = useThemeStore()

onMounted(() => {
  // 初始化主题
  themeStore.initDarkMode()
  themeStore.updatePrimaryColor(themeStore.primaryColor)
})
</script>

<style>
.container {
  min-height: 100vh;
  background-color: var(--el-bg-color);
  transition: all 0.3s;
}

.main-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--el-bg-color-overlay);
  margin-bottom: 20px;
  border-radius: 8px;
  box-shadow: var(--el-box-shadow-light);
  transition: all 0.3s;
  padding: 0 20px;
  height: 60px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

h1 {
  color: var(--el-color-primary);
  margin: 0;
  font-size: 24px;
  transition: all 0.3s;
}

/* 暗黑模式适配 */
html.dark {
  color-scheme: dark;
}

html.dark .container {
  background-color: var(--el-bg-color);
}

html.dark .el-header {
  background: var(--el-bg-color);
  box-shadow: var(--el-box-shadow);
}

html.dark h1 {
  color: var(--el-color-primary);
}

/* 过渡动画 */
* {
  transition: background-color 0.3s, border-color 0.3s, color 0.3s;
}
</style>
