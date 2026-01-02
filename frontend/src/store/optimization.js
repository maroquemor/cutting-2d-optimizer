import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useOptimizationStore = defineStore('optimization', () => {
  // Estado
  const optimizations = ref([])
  const currentOptimization = ref(null)
  const isLoading = ref(false)
  const stats = ref({
    total: 0,
    averageTime: 0,
    averageWaste: 0
  })

  // Getters
  const totalOptimizations = computed(() => optimizations.value.length)
  const averageTime = computed(() => stats.value.averageTime)
  const averageWaste = computed(() => stats.value.averageWaste)

  // Acciones
  const loadStats = async () => {
    try {
      const response = await api.get('/api/estadisticas')
      stats.value = {
        total: response.data.optimizaciones_realizadas || 0,
        averageTime: response.data.tiempo_promedio || 0,
        averageWaste: response.data.promedio_desperdicio || 0
      }
    } catch (error) {
      console.error('Error cargando estadísticas:', error)
    }
  }

  const loadExample = async (exampleName) => {
    try {
      const response = await api.get('/api/ejemplos')
      return response.data[exampleName]
    } catch (error) {
      console.error('Error cargando ejemplo:', error)
      return null
    }
  }

  const predictWaste = async (optimizationData) => {
    try {
      const response = await api.post('/api/predecir', optimizationData)
      return response.data
    } catch (error) {
      console.error('Error en predicción ML:', error)
      throw error
    }
  }

  const optimize = async (optimizationData) => {
    isLoading.value = true
    try {
      const response = await api.post('/api/optimizar', optimizationData)
      const result = response.data
      
      // Guardar en historial
      optimizations.value.unshift({
        ...result,
        id: Date.now(),
        timestamp: new Date().toISOString(),
        config: optimizationData.config
      })
      
      currentOptimization.value = result
      return result
    } catch (error) {
      console.error('Error en optimización:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const saveToHistory = (optimization) => {
    optimizations.value.unshift({
      ...optimization,
      id: Date.now(),
      saved: true,
      savedAt: new Date().toISOString()
    })
  }

  const deleteFromHistory = (id) => {
    const index = optimizations.value.findIndex(opt => opt.id === id)
    if (index !== -1) {
      optimizations.value.splice(index, 1)
    }
  }

  const clearHistory = () => {
    optimizations.value = []
  }

  return {
    // Estado
    optimizations,
    currentOptimization,
    isLoading,
    stats,
    
    // Getters
    totalOptimizations,
    averageTime,
    averageWaste,
    
    // Acciones
    loadStats,
    loadExample,
    predictWaste,
    optimize,
    saveToHistory,
    deleteFromHistory,
    clearHistory
  }
})