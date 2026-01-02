<template>
  <div class="optimizer-view">
    <!-- Título -->
    <div class="page-header">
      <h2><i class="el-icon-s-operation"></i> Optimizador de Corte</h2>
      <p class="page-description">
        Configura tu problema de corte y obtén la solución óptima
      </p>
    </div>

    <!-- Contenido principal -->
    <div class="optimizer-content">
      <!-- Panel izquierdo: Configuración -->
      <div class="config-panel">
        <el-card class="config-card">
          <template #header>
            <div class="card-header">
              <h3><i class="el-icon-s-data"></i> Configuración del Problema</h3>
              <el-button 
                type="primary" 
                size="small"
                @click="loadExample"
              >
                <i class="el-icon-download"></i> Cargar Ejemplo
              </el-button>
            </div>
          </template>

          <!-- Paso 1: Materiales -->
          <div class="config-section">
            <h4><i class="el-icon-box"></i> Materia Prima</h4>
            <el-button 
              type="success" 
              size="small" 
              @click="addMaterial"
              class="add-btn"
            >
              <i class="el-icon-plus"></i> Añadir Material
            </el-button>

            <div class="items-list">
              <div 
                v-for="(material, index) in materials" 
                :key="index"
                class="item-card"
              >
                <div class="item-header">
                  <span class="item-title">Material {{ index + 1 }}</span>
                  <el-button 
                    type="danger" 
                    size="small" 
                    circle
                    @click="removeMaterial(index)"
                    :disabled="materials.length <= 1"
                  >
                    <i class="el-icon-delete"></i>
                  </el-button>
                </div>
                
                <div class="item-fields">
                  <el-input 
                    v-model="material.nombre"
                    placeholder="Nombre (opcional)"
                    size="small"
                  />
                  
                  <div class="field-row">
                    <el-input-number 
                      v-model="material.ancho"
                      :min="1"
                      :step="1"
                      size="small"
                      placeholder="Ancho (cm)"
                    />
                    <span class="field-label">×</span>
                    <el-input-number 
                      v-model="material.alto"
                      :min="1"
                      :step="1"
                      size="small"
                      placeholder="Alto (cm)"
                    />
                  </div>
                  
                  <el-input-number 
                    v-model="material.cantidad"
                    :min="1"
                    :step="1"
                    size="small"
                    placeholder="Cantidad"
                    class="quantity-input"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 2: Piezas -->
          <div class="config-section">
            <h4><i class="el-icon-copy-document"></i> Piezas a Cortar</h4>
            <el-button 
              type="success" 
              size="small" 
              @click="addPiece"
              class="add-btn"
            >
              <i class="el-icon-plus"></i> Añadir Pieza
            </el-button>

            <div class="items-list">
              <div 
                v-for="(piece, index) in pieces" 
                :key="index"
                class="item-card"
              >
                <div class="item-header">
                  <span class="item-title">Pieza {{ index + 1 }}</span>
                  <el-button 
                    type="danger" 
                    size="small" 
                    circle
                    @click="removePiece(index)"
                    :disabled="pieces.length <= 1"
                  >
                    <i class="el-icon-delete"></i>
                  </el-button>
                </div>
                
                <div class="item-fields">
                  <el-input 
                    v-model="piece.nombre"
                    placeholder="Nombre (opcional)"
                    size="small"
                  />
                  
                  <div class="field-row">
                    <el-input-number 
                      v-model="piece.ancho"
                      :min="1"
                      :step="1"
                      size="small"
                      placeholder="Ancho (cm)"
                    />
                    <span class="field-label">×</span>
                    <el-input-number 
                      v-model="piece.alto"
                      :min="1"
                      :step="1"
                      size="small"
                      placeholder="Alto (cm)"
                    />
                  </div>
                  
                  <el-input-number 
                    v-model="piece.demanda"
                    :min="1"
                    :step="1"
                    size="small"
                    placeholder="Demanda"
                    class="quantity-input"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Paso 3: Configuración avanzada -->
          <div class="config-section">
            <h4><i class="el-icon-setting"></i> Configuración Avanzada</h4>
            <div class="advanced-settings">
              <el-switch
                v-model="useSubstitution"
                active-text="Usar variantes de sustitución"
              />
              
              <div class="setting-row">
                <span class="setting-label">Límite de tiempo (segundos):</span>
                <el-input-number 
                  v-model="timeLimit"
                  :min="30"
                  :max="600"
                  :step="30"
                  size="small"
                />
              </div>
              
              <div class="setting-row">
                <span class="setting-label">Máximo de patrones:</span>
                <el-input-number 
                  v-model="maxPatterns"
                  :min="100"
                  :max="5000"
                  :step="100"
                  size="small"
                />
              </div>
            </div>
          </div>

          <!-- Botón de optimización -->
          <div class="action-buttons">
            <el-button 
              type="primary" 
              size="large"
              @click="predictWithML"
              :loading="predicting"
              class="predict-btn"
            >
              <i class="el-icon-magic-stick"></i> Predecir con ML
            </el-button>
            
            <el-button 
              type="success" 
              size="large"
              @click="runOptimization"
              :loading="optimizing"
              class="optimize-btn"
            >
              <i class="el-icon-video-play"></i> Ejecutar Optimización
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- Panel derecho: Resultados y ML -->
      <div class="results-panel">
        <!-- Predicción ML -->
        <el-card v-if="mlPrediction" class="ml-card">
          <template #header>
            <h3><i class="el-icon-magic-stick"></i> Predicción ML</h3>
          </template>
          
          <div class="ml-results">
            <div class="ml-metric">
              <span class="metric-label">Desperdicio estimado:</span>
              <span class="metric-value">
                {{ mlPrediction.desperdicio_estimado?.toFixed(2) || 'N/A' }} cm²
              </span>
            </div>
            
            <div class="ml-metric">
              <span class="metric-label">Confianza:</span>
              <el-progress 
                :percentage="mlPrediction.confianza * 100" 
                :status="getConfidenceStatus(mlPrediction.confianza)"
                :stroke-width="10"
              />
            </div>
            
            <div v-if="mlPrediction.recomendaciones" class="ml-recommendations">
              <h5>Recomendaciones:</h5>
              <ul>
                <li v-for="(rec, idx) in mlPrediction.recomendaciones" :key="idx">
                  {{ rec }}
                </li>
              </ul>
            </div>
          </div>
        </el-card>

        <!-- Resultados de optimización -->
        <el-card v-if="optimizationResult" class="results-card">
          <template #header>
            <h3><i class="el-icon-success"></i> Resultados de Optimización</h3>
          </template>
          
          <div class="optimization-results">
            <!-- Métricas principales -->
            <div class="main-metrics">
              <div class="metric-card success">
                <div class="metric-icon">
                  <i class="el-icon-coin"></i>
                </div>
                <div class="metric-content">
                  <div class="metric-value">
                    {{ optimizationResult.desperdicio?.toFixed(2) || 'N/A' }} cm²
                  </div>
                  <div class="metric-label">Desperdicio total</div>
                </div>
              </div>
              
              <div class="metric-card info">
                <div class="metric-icon">
                  <i class="el-icon-timer"></i>
                </div>
                <div class="metric-content">
                  <div class="metric-value">
                    {{ optimizationResult.tiempo_ejecucion?.toFixed(2) || 'N/A' }} s
                  </div>
                  <div class="metric-label">Tiempo de ejecución</div>
                </div>
              </div>
              
              <div class="metric-card warning">
                <div class="metric-icon">
                  <i class="el-icon-copy-document"></i>
                </div>
                <div class="metric-content">
                  <div class="metric-value">
                    {{ optimizationResult.patrones_utilizados || 0 }}
                  </div>
                  <div class="metric-label">Patrones utilizados</div>
                </div>
              </div>
            </div>

            <!-- Visualización -->
            <div v-if="optimizationResult.visualizacion_url" class="visualization">
              <h4>Visualización del Corte</h4>
              <img 
                :src="optimizationResult.visualizacion_url" 
                alt="Visualización del patrón de corte"
                class="visualization-img"
              />
            </div>

            <!-- Instrucciones -->
            <div v-if="optimizationResult.instrucciones" class="instructions">
              <h4>Instrucciones de Corte</h4>
              <el-collapse>
                <el-collapse-item 
                  v-for="(instruction, idx) in optimizationResult.instrucciones" 
                  :key="idx"
                  :title="`Paso ${idx + 1}`"
                >
                  {{ instruction }}
                </el-collapse-item>
              </el-collapse>
            </div>

            <!-- Acciones -->
            <div class="result-actions">
              <el-button type="primary" @click="downloadPDF">
                <i class="el-icon-download"></i> Descargar PDF
              </el-button>
              <el-button type="success" @click="saveOptimization">
                <i class="el-icon-folder-add"></i> Guardar en Historial
              </el-button>
              <el-button type="info" @click="shareResults">
                <i class="el-icon-share"></i> Compartir
              </el-button>
            </div>
          </div>
        </el-card>

        <!-- Estadísticas -->
        <el-card class="stats-card">
          <template #header>
            <h3><i class="el-icon-data-analysis"></i> Estadísticas</h3>
          </template>
          
          <div class="stats-content">
            <div class="stat-item">
              <span class="stat-label">Material total:</span>
              <span class="stat-value">
                {{ totalMaterialArea.toFixed(2) }} cm²
              </span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Piezas totales:</span>
              <span class="stat-value">
                {{ totalPiecesArea.toFixed(2) }} cm²
              </span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Utilización estimada:</span>
              <span class="stat-value">
                {{ estimatedUtilization.toFixed(1) }}%
              </span>
            </div>
            
            <div class="stat-item">
              <span class="stat-label">Dificultad:</span>
              <el-tag :type="getDifficultyType(estimatedDifficulty)" size="small">
                {{ estimatedDifficulty }}
              </el-tag>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useOptimizationStore } from '@/store/optimization'

const optimizationStore = useOptimizationStore()

// Datos del formulario
const materials = ref([
  { ancho: 100, alto: 70, cantidad: 5, nombre: 'Vidrio 100x70' }
])

const pieces = ref([
  { ancho: 30, alto: 20, demanda: 10, nombre: 'Ventana pequeña' },
  { ancho: 40, alto: 30, demanda: 5, nombre: 'Ventana grande' }
])

// Configuración
const useSubstitution = ref(true)
const timeLimit = ref(300)
const maxPatterns = ref(1000)

// Estado
const predicting = ref(false)
const optimizing = ref(false)
const mlPrediction = ref(null)
const optimizationResult = ref(null)

// Computed
const totalMaterialArea = computed(() => {
  return materials.value.reduce((sum, m) => sum + (m.ancho * m.alto * m.cantidad), 0)
})

const totalPiecesArea = computed(() => {
  return pieces.value.reduce((sum, p) => sum + (p.ancho * p.alto * p.demanda), 0)
})

const estimatedUtilization = computed(() => {
  if (totalMaterialArea.value === 0) return 0
  return Math.min((totalPiecesArea.value / totalMaterialArea.value) * 100, 100)
})

const estimatedDifficulty = computed(() => {
  const complexity = pieces.value.length * materials.value.length
  if (complexity < 10) return 'Fácil'
  if (complexity < 20) return 'Media'
  return 'Difícil'
})

// Métodos
const addMaterial = () => {
  materials.value.push({
    ancho: 100,
    alto: 70,
    cantidad: 1,
    nombre: `Material ${materials.value.length + 1}`
  })
}

const removeMaterial = (index) => {
  if (materials.value.length > 1) {
    materials.value.splice(index, 1)
  }
}

const addPiece = () => {
  pieces.value.push({
    ancho: 30,
    alto: 20,
    demanda: 5,
    nombre: `Pieza ${pieces.value.length + 1}`
  })
}

const removePiece = (index) => {
  if (pieces.value.length > 1) {
    pieces.value.splice(index, 1)
  }
}

const loadExample = async () => {
  try {
    const example = await optimizationStore.loadExample('paper')
    if (example) {
      materials.value = example.materiales || materials.value
      pieces.value = example.piezas || pieces.value
      ElMessage.success('Ejemplo cargado correctamente')
    }
  } catch (error) {
    ElMessage.error('Error al cargar el ejemplo')
  }
}

const predictWithML = async () => {
  predicting.value = true
  try {
    const requestData = {
      materiales: materials.value,
      piezas: pieces.value,
      config: {
        usar_sustitucion: useSubstitution.value,
        tiempo_limite: timeLimit.value,
        max_patrones: maxPatterns.value
      }
    }
    
    mlPrediction.value = await optimizationStore.predictWaste(requestData)
    ElMessage.success('Predicción ML completada')
  } catch (error) {
    ElMessage.error('Error en predicción ML')
  } finally {
    predicting.value = false
  }
}

const runOptimization = async () => {
  optimizing.value = true
  try {
    const requestData = {
      materiales: materials.value,
      piezas: pieces.value,
      config: {
        usar_sustitucion: useSubstitution.value,
        tiempo_limite: timeLimit.value,
        max_patrones: maxPatterns.value
      }
    }
    
    optimizationResult.value = await optimizationStore.optimize(requestData)
    ElMessage.success('Optimización completada exitosamente')
  } catch (error) {
    ElMessage.error('Error en optimización: ' + error.message)
  } finally {
    optimizing.value = false
  }
}

const getConfidenceStatus = (confidence) => {
  if (confidence > 0.8) return 'success'
  if (confidence > 0.6) return 'warning'
  return 'exception'
}

const getDifficultyType = (difficulty) => {
  switch (difficulty) {
    case 'Fácil': return 'success'
    case 'Media': return 'warning'
    case 'Difícil': return 'danger'
    default: return 'info'
  }
}

const downloadPDF = () => {
  // Implementar generación de PDF
  ElMessage.info('Función de PDF en desarrollo')
}

const saveOptimization = () => {
  if (optimizationResult.value) {
    optimizationStore.saveToHistory(optimizationResult.value)
    ElMessage.success('Guardado en historial')
  }
}

const shareResults = () => {
  ElMessage.info('Función de compartir en desarrollo')
}

onMounted(() => {
  // Cargar datos iniciales
})
</script>

<style scoped>
.optimizer-view {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  color: #333;
  font-size: 2em;
  margin-bottom: 10px;
}

.page-description {
  color: #666;
  font-size: 1.1em;
}

.optimizer-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 1024px) {
  .optimizer-content {
    grid-template-columns: 1fr;
  }
}

.config-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-section {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.config-section:last-child {
  border-bottom: none;
}

.config-section h4 {
  color: #409eff;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.add-btn {
  margin-bottom: 15px;
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.item-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 15px;
  background: #fafafa;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.item-title {
  font-weight: bold;
  color: #333;
}

.item-fields {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.field-row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.field-label {
  font-size: 1.2em;
  color: #666;
}

.quantity-input {
  width: 120px;
}

.advanced-settings {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.setting-label {
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 25px;
}

.predict-btn, .optimize-btn {
  flex: 1;
  height: 50px;
  font-size: 1.1em;
}

.results-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ml-card, .results-card, .stats-card {
  width: 100%;
}

.ml-results {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.ml-metric {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.metric-label {
  color: #666;
}

.metric-value {
  font-weight: bold;
  color: #333;
}

.ml-recommendations {
  margin-top: 15px;
  padding: 15px;
  background: #f0f9ff;
  border-radius: 6px;
}

.ml-recommendations h5 {
  margin-bottom: 10px;
  color: #409eff;
}

.ml-recommendations ul {
  margin: 0;
  padding-left: 20px;
}

.ml-recommendations li {
  margin-bottom: 5px;
  color: #666;
}

.main-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.metric-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
}

.metric-card.success {
  border-left: 4px solid #67c23a;
}

.metric-card.info {
  border-left: 4px solid #409eff;
}

.metric-card.warning {
  border-left: 4px solid #e6a23c;
}

.metric-icon {
  font-size: 2em;
  color: #666;
}

.metric-content {
  flex: 1;
}

.metric-value {
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
}

.metric-label {
  font-size: 0.9em;
  color: #666;
}

.visualization {
  margin: 20px 0;
}

.visualization h4 {
  margin-bottom: 10px;
  color: #333;
}

.visualization-img {
  width: 100%;
  max-height: 400px;
  object-fit: contain;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 10px;
  background: white;
}

.instructions {
  margin: 20px 0;
}

.instructions h4 {
  margin-bottom: 15px;
  color: #333;
}

.result-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.stats-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: bold;
  color: #333;
}
</style>