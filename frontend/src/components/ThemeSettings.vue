<!-- 主题设置组件 -->
<template>
  <el-popover
    placement="bottom-end"
    :width="300"
    trigger="click"
  >
    <template #reference>
      <el-button circle>
        <el-icon><Brush /></el-icon>
      </el-button>
    </template>

    <div class="theme-settings">
      <h3>主题设置</h3>
      
      <!-- 暗黑模式切换 -->
      <div class="setting-item">
        <span>暗黑模式</span>
        <div class="mode-control">
          <el-switch
            :model-value="store.isDark"
            @update:model-value="store.toggleDarkMode"
            :active-text="store.isManualControl ? '开启' : '自动'"
            inactive-text="关闭"
          />
          <div class="auto-mode-hint" v-if="!store.isManualControl">
            {{ store.isDark ? '当前为夜间模式' : '当前为日间模式' }}
            <el-tooltip
              content="每天18:00-次日8:00自动开启暗黑模式，其他时间自动关闭。手动切换后将保持到午夜重置。"
              placement="top"
            >
              <el-icon class="info-icon"><InfoFilled /></el-icon>
            </el-tooltip>
          </div>
        </div>
      </div>

      <!-- 主题色选择 -->
      <div class="setting-item">
        <span>主题色</span>
        <el-color-picker
          v-model="store.primaryColor"
          :predefine="predefineColors"
          @change="store.updatePrimaryColor"
        />
      </div>

      <!-- 预设主题色 -->
      <div class="preset-colors">
        <div
          v-for="color in predefineColors"
          :key="color"
          class="color-item"
          :style="{ backgroundColor: color }"
          @click="store.updatePrimaryColor(color)"
        />
      </div>
    </div>
  </el-popover>
</template>

<script setup>
import { Brush, InfoFilled } from '@element-plus/icons-vue'
import { useThemeStore } from '../stores/theme'

const store = useThemeStore()

// 预定义的主题色
const predefineColors = [
  '#409eff', // 默认蓝色
  '#67c23a', // 绿色
  '#e6a23c', // 黄色
  '#f56c6c', // 红色
  '#909399', // 灰色
  '#8e44ad', // 紫色
  '#2c3e50', // 深蓝色
  '#16a085', // 青色
  '#d35400', // 橙色
  '#c0392b'  // 深红色
]
</script>

<style scoped>
.theme-settings {
  padding: 12px;
}

.theme-settings h3 {
  margin: 0 0 16px;
  font-size: 16px;
  font-weight: 500;
}

.setting-item {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 16px;
}

.mode-control {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.auto-mode-hint {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-icon {
  cursor: help;
  font-size: 14px;
  color: var(--el-color-info);
}

.preset-colors {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-top: 16px;
}

.color-item {
  width: 100%;
  padding-bottom: 100%;
  border-radius: 4px;
  cursor: pointer;
  transition: transform 0.2s;
  border: 1px solid var(--el-border-color);
}

.color-item:hover {
  transform: scale(1.1);
}

:deep(.el-color-picker__trigger) {
  border: none;
  padding: 0;
}
</style> 