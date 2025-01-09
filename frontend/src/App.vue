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
  border-radius: 12px;
  box-shadow: var(--el-box-shadow-light);
  transition: all 0.3s;
  padding: 0 24px;
  height: 70px;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid var(--el-border-color-light);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

h1 {
  color: var(--el-color-primary);
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 12px;
}

h1::before {
  content: "🚂";
  font-size: 28px;
}

/* 暗黑模式适配 */
html.dark {
  color-scheme: dark;
}

html.dark .container {
  background-color: var(--el-bg-color);
}

html.dark .el-header {
  background: rgba(0, 0, 0, 0.2);
  box-shadow: var(--el-box-shadow);
  border-color: var(--el-border-color-darker);
}

html.dark h1 {
  color: var(--el-color-primary);
}

/* 过渡动画 */
* {
  transition: background-color 0.3s, border-color 0.3s, color 0.3s, box-shadow 0.3s;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .main-container {
    padding: 12px;
  }

  .el-header {
    padding: 0 16px;
    height: 60px;
    margin-bottom: 12px;
  }

  h1 {
    font-size: 20px;
  }

  h1::before {
    font-size: 24px;
  }
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--el-bg-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: var(--el-border-color);
  border-radius: 4px;
  transition: all 0.3s;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--el-text-color-secondary);
}

/* 暗黑模式滚动条 */
html.dark ::-webkit-scrollbar-track {
  background: var(--el-bg-color-darker);
}

html.dark ::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
}

html.dark ::-webkit-scrollbar-thumb:hover {
  background: var(--el-text-color-secondary);
}
</style>
