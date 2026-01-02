<template>
  <div class="app-container">
    <!-- Header -->
    <header class="app-header">
      <div class="header-content">
        <div class="logo">
          <h1><i class="el-icon-s-operation"></i> Optimizador de Corte 2D</h1>
          <p class="subtitle">Sistema inteligente basado en investigación operativa</p>
        </div>
        <nav class="nav-menu">
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            @select="handleMenuSelect"
            class="nav-menu"
          >
            <el-menu-item index="optimizer">
              <i class="el-icon-s-operation"></i> Optimizador
            </el-menu-item>
            <el-menu-item index="history">
              <i class="el-icon-time"></i> Historial
            </el-menu-item>
            <el-menu-item index="examples">
              <i class="el-icon-collection"></i> Ejemplos
            </el-menu-item>
            <el-menu-item index="about">
              <i class="el-icon-info"></i> Acerca de
            </el-menu-item>
          </el-menu>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="app-main">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="app-footer">
      <div class="footer-content">
        <div class="footer-info">
          <p>© 2024 Sistema de Optimización de Corte 2D</p>
          <p>Basado en investigación de Medina, De León y Leiva (2020)</p>
        </div>
        <div class="footer-stats">
          <el-tag type="info" size="small">
            <i class="el-icon-cpu"></i> Optimizaciones: {{ stats.total }}
          </el-tag>
          <el-tag type="success" size="small">
            <i class="el-icon-timer"></i> Tiempo promedio: {{ stats.avgTime }}s
          </el-tag>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useOptimizationStore } from '@/store/optimization'

const router = useRouter()
const route = useRoute()
const optimizationStore = useOptimizationStore()

const activeMenu = computed(() => {
  return route.name || 'optimizer'
})

const stats = computed(() => {
  return {
    total: optimizationStore.totalOptimizations || 0,
    avgTime: optimizationStore.averageTime?.toFixed(2) || '0.00'
  }
})

const handleMenuSelect = (index) => {
  router.push({ name: index })
}

onMounted(async () => {
  await optimizationStore.loadStats()
})
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.logo h1 {
  margin: 0;
  font-size: 1.8em;
  font-weight: 700;
}

.subtitle {
  margin: 5px 0 0;
  font-size: 0.9em;
  opacity: 0.9;
}

.nav-menu {
  background: transparent !important;
  border: none !important;
}

.nav-menu .el-menu-item {
  color: white !important;
  font-size: 1em;
}

.nav-menu .el-menu-item:hover {
  background: rgba(255,255,255,0.1) !important;
}

.nav-menu .el-menu-item.is-active {
  background: rgba(255,255,255,0.2) !important;
  border-bottom: 3px solid white !important;
}

.app-main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.app-footer {
  background: #f5f7fa;
  border-top: 1px solid #e4e7ed;
  padding: 20px;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-info p {
  margin: 5px 0;
  color: #666;
  font-size: 0.9em;
}

.footer-stats {
  display: flex;
  gap: 10px;
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>