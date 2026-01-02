import axios from 'axios'

// Configurar axios
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 30000 // 30 segundos timeout
})

// Interceptor para manejar errores
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    
    let message = 'Error en la comunicación con el servidor'
    
    if (error.response) {
      // El servidor respondió con un código de error
      switch (error.response.status) {
        case 400:
          message = 'Datos inválidos enviados al servidor'
          break
        case 404:
          message = 'Recurso no encontrado'
          break
        case 500:
          message = 'Error interno del servidor'
          break
        case 504:
          message = 'Tiempo de espera agotado. El servidor está tardando demasiado'
          break
      }
    } else if (error.request) {
      // La petición fue hecha pero no hubo respuesta
      message = 'No se pudo conectar con el servidor. Verifica tu conexión a internet'
    }
    
    error.message = message
    return Promise.reject(error)
  }
)

// Métodos de la API
const apiService = {
  // Optimización
  optimize(data) {
    return api.post('/api/optimizar', data)
  },
  
  predict(data) {
    return api.post('/api/predecir', data)
  },
  
  getExamples() {
    return api.get('/api/ejemplos')
  },
  
  getStats() {
    return api.get('/api/estadisticas')
  },
  
  healthCheck() {
    return api.get('/health')
  },
  
  // Para subir archivos
  uploadFile(file, onProgress) {
    const formData = new FormData()
    formData.append('file', file)
    
    return api.post('/api/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: onProgress
    })
  }
}

export default apiService