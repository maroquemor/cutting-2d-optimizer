"""
Script para ejecutar el backend
"""
import uvicorn

if __name__ == "__main__":
    print("🚀 Iniciando servidor de optimización de corte 2D")
    print("🌐 API disponible en: http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/api/docs")
    print("\nPresiona Ctrl+C para detener\n")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )