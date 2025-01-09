import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useDark } from '@vueuse/core'

export const useThemeStore = defineStore('theme', () => {
  // 使用 VueUse 的暗黑模式工具
  const isDark = useDark({
    selector: 'html',
    attribute: 'class',
    valueDark: 'dark',
    valueLight: '',
    storageKey: 'theme-dark-mode',
    storage: localStorage,
    onChanged: (dark) => {
      document.documentElement.className = dark ? 'dark' : ''
    }
  })

  // 是否手动控制
  const isManualControl = ref(localStorage.getItem('theme-manual-control') === 'true')

  // 检查是否在自动暗黑模式时间范围内
  const isInDarkModeTimeRange = () => {
    const now = new Date()
    const hour = now.getHours()
    return hour >= 18 || hour < 8
  }

  // 自动切换暗黑模式
  const autoSwitchDarkMode = () => {
    if (!isManualControl.value) {
      const shouldBeDark = isInDarkModeTimeRange()
      isDark.value = shouldBeDark
    }
  }

  let autoSwitchTimer = null

  // 切换暗黑模式
  function toggleDarkMode(value) {
    isDark.value = value
    
    // 标记为手动控制
    isManualControl.value = true
    localStorage.setItem('theme-manual-control', 'true')
    
    // 在午夜重置手动控制状态
    const now = new Date()
    const midnight = new Date(now)
    midnight.setHours(24, 0, 0, 0)
    const timeUntilMidnight = midnight - now
    
    // 清除之前的定时器
    if (window._resetManualControlTimer) {
      clearTimeout(window._resetManualControlTimer)
    }
    
    // 设置新的定时器
    window._resetManualControlTimer = setTimeout(() => {
      isManualControl.value = false
      localStorage.removeItem('theme-manual-control')
      autoSwitchDarkMode() // 立即执行一次自动切换检查
    }, timeUntilMidnight)
  }

  // 主题色
  const primaryColor = ref(localStorage.getItem('theme-primary-color') || '#409eff')

  // 初始化暗黑模式
  const initDarkMode = () => {
    // 清除之前的定时器
    if (autoSwitchTimer) {
      clearInterval(autoSwitchTimer)
    }
    
    // 检查是否有保存的手动控制状态
    const savedManualControl = localStorage.getItem('theme-manual-control') === 'true'
    isManualControl.value = savedManualControl
    
    if (!savedManualControl) {
      // 如果不是手动控制，执行自动切换
      autoSwitchDarkMode()
    }

    // 设置定时器，每分钟检查一次
    autoSwitchTimer = setInterval(autoSwitchDarkMode, 60000)
  }

  // 更新主题色
  function updatePrimaryColor(color) {
    if (!color) return
    
    primaryColor.value = color
    localStorage.setItem('theme-primary-color', color)
    
    // 更新 CSS 变量
    const el = document.documentElement
    el.style.setProperty('--el-color-primary', color)
    
    // 生成不同深度的主题色
    const mix = (color1, color2, weight) => {
      color1 = color1.replace('#', '')
      color2 = color2.replace('#', '')
      
      const d2h = (d) => d.toString(16).padStart(2, '0')
      const h2d = (h) => parseInt(h, 16)
      
      let color = '#'
      for(let i = 0; i < 3; i++) {
        const c1 = h2d(color1.substr(i * 2, 2))
        const c2 = h2d(color2.substr(i * 2, 2))
        const c = d2h(Math.round(c1 * weight + c2 * (1 - weight)))
        color += c
      }
      return color
    }
    
    // 生成不同深度的主题色变量
    for(let i = 1; i <= 9; i++) {
      const lightColor = mix(color, '#ffffff', i * 0.1)
      el.style.setProperty(`--el-color-primary-light-${i}`, lightColor)
    }
    
    // 生成深色变量
    const darkColor = mix(color, '#000000', 0.2)
    el.style.setProperty('--el-color-primary-dark-2', darkColor)
  }

  return {
    isDark,
    toggleDarkMode,
    primaryColor,
    updatePrimaryColor,
    initDarkMode,
    isManualControl
  }
}) 