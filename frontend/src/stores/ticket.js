import { defineStore } from 'pinia'
import { ref, reactive, watch } from 'vue'
import axios from 'axios'
import dayjs from 'dayjs'
import { ElMessage } from 'element-plus'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL

export const useTicketStore = defineStore('ticket', () => {
  // 状态
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
  const loadingStops = ref({})

  // 从 localStorage 恢复状态
  function initializeFromStorage() {
    const savedForm = localStorage.getItem('ticketSearchForm')
    if (savedForm) {
      const parsed = JSON.parse(savedForm)
      Object.keys(searchForm).forEach(key => {
        if (key === 'trainDate' && parsed[key]) {
          searchForm[key] = dayjs(parsed[key]).toDate()
        } else {
          searchForm[key] = parsed[key]
        }
      })
    }

    // 恢复其他状态
    const savedTickets = localStorage.getItem('tickets')
    if (savedTickets) {
      tickets.value = JSON.parse(savedTickets)
    }
  }

  // 监听状态变化并保存
  watch(
    () => ({
      ...searchForm,
      trainDate: searchForm.trainDate ? dayjs(searchForm.trainDate).format('YYYY-MM-DD') : ''
    }),
    (newValue) => {
      localStorage.setItem('ticketSearchForm', JSON.stringify(newValue))
    },
    { deep: true }
  )

  watch(
    tickets,
    (newValue) => {
      localStorage.setItem('tickets', JSON.stringify(newValue))
    },
    { deep: true }
  )

  // 站点查询建议
  async function queryStations(query) {
    if (query.length < 1) {
      return []
    }
    try {
      const response = await axios.get(`${API_BASE_URL}/stations/${query}`)
      return response.data.map(station => ({
        value: station.name,
        label: `${station.name} (${station.code})`
      }))
    } catch (error) {
      console.error('Error fetching stations:', error)
      ElMessage.error('站点查询失败：' + (error.response?.data?.detail || error.message))
      return []
    }
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
        via_station: searchForm.viaStation || undefined,
        include_stops: true
      })

      if (Array.isArray(response.data)) {
        tickets.value = response.data.map(ticket => ({
          ...ticket,
          seats: Object.fromEntries(
            Object.entries(ticket.seats).map(([key, value]) => [
              key,
              value === '有' ? '有票' : value === '无' ? '无票' : value
            ])
          )
        }))
      } else {
        tickets.value = []
      }
      
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
    loadingStops.value = {}
    // 清除存储的状态
    localStorage.removeItem('ticketSearchForm')
    localStorage.removeItem('tickets')
  }

  // 查看经停站信息
  async function showTrainStops(trainCode) {
    const train = tickets.value.find(t => t.train_code === trainCode)
    if (train && train.stops) {
      trainStops.value = train.stops
      stopsDialogVisible.value = true
      return
    }

    loadingStops.value[trainCode] = true
    try {
      const currentDate = dayjs(searchForm.trainDate).format('YYYY-MM-DD')
      const response = await axios.get(`${API_BASE_URL}/trains/${trainCode}/stops?train_date=${currentDate}`)
      trainStops.value = response.data
      if (trainStops.value.length === 0) {
        ElMessage.warning('暂无经停站信息')
        return
      }
      stopsDialogVisible.value = true
    } catch (error) {
      console.error('Error fetching train stops:', error)
      ElMessage.error('获取经停站信息失败：' + (error.response?.data?.detail || error.message))
    } finally {
      loadingStops.value[trainCode] = false
    }
  }

  // 初始化状态
  initializeFromStorage()

  return {
    searchForm,
    tickets,
    trainStops,
    stopsDialogVisible,
    loading,
    loadingStops,
    queryStations,
    searchTickets,
    resetForm,
    showTrainStops
  }
}) 