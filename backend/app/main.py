"""
Backend principal - API REST para optimización de corte 2D
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import uvicorn
import json
from datetime import datetime

# Importar nuestros módulos
from .optimizer import CuttingOptimizer2D
from .ml_predictor import WastePredictor
from .models import (
    OptimizationRequest, 
    OptimizationResponse,
    MaterialInput,
    PieceInput
)

# Crear aplicación FastAPI
app = FastAPI(
    title="API de Optimización de Corte 2D",
    description="API REST para optimizar problemas de corte 2D usando PLE",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configurar CORS (para que el frontend pueda acceder)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar componentes
optimizer = CuttingOptimizer2D()
ml_predictor = WastePredictor()

@app.get("/")
async def root():
    """Página principal de la API"""
    return {
        "message": "Bienvenido a la API de Optimización de Corte 2D",
        "version": "1.0.0",
        "endpoints": {
            "documentación": "/api/docs",
            "optimizar": "/api/optimizar",
            "predecir": "/api/predecir",
            "estadísticas": "/api/estadisticas"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar que la API está funcionando"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/optimizar", response_model=OptimizationResponse)
async def optimizar_corte(request: OptimizationRequest):
    """
    Endpoint principal para optimizar problemas de corte 2D
    
    Recibe:
    - Lista de materiales (materia prima)
    - Lista de piezas a cortar
    - Parámetros de configuración
    
    Devuelve:
    - Solución óptima
    - Patrones de corte
    - Instrucciones detalladas
    """
    try:
        print(f"Recibida solicitud de optimización: {len(request.materiales)} materiales, {len(request.piezas)} piezas")
        
        # Configurar el optimizador
        optimizer.clear()
        
        # Añadir materiales
        for material in request.materiales:
            optimizer.add_material(
                width=material.ancho,
                height=material.alto,
                quantity=material.cantidad,
                name=material.nombre
            )
        
        # Añadir piezas
        for i, pieza in enumerate(request.piezas):
            optimizer.add_piece(
                id=i+1,
                width=pieza.ancho,
                height=pieza.alto,
                demand=pieza.demanda,
                name=pieza.nombre
            )
        
        # Configurar parámetros
        if request.config:
            optimizer.set_config(
                use_substitution=request.config.usar_sustitucion,
                max_patterns=request.config.max_patrones,
                time_limit=request.config.tiempo_limite
            )
        
        # Ejecutar optimización
        resultado = optimizer.solve()
        
        # Generar respuesta
        respuesta = OptimizationResponse(
            success=True,
            desperdicio=resultado["waste"],
            tiempo_ejecucion=resultado["time"],
            patrones_utilizados=resultado["patterns_used"],
            instrucciones=resultado["instructions"],
            visualizacion_url=f"/api/visualizar/{resultado['id']}",
            resumen=resultado["summary"]
        )
        
        return respuesta
        
    except Exception as e:
        print(f"Error en optimización: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error en optimización: {str(e)}")

@app.post("/api/predecir")
async def predecir_desperdicio(request: OptimizationRequest):
    """
    Usar ML para predecir el desperdicio antes de optimizar
    """
    try:
        # Extraer características para ML
        caracteristicas = {
            "num_materiales": len(request.materiales),
            "num_piezas": len(request.piezas),
            "area_total_materiales": sum(m.ancho * m.alto * m.cantidad for m in request.materiales),
            "area_total_piezas": sum(p.ancho * p.alto * p.demanda for p in request.piezas),
            "utilizacion_estimada": 0.85  # Valor inicial
        }
        
        # Calcular utilización estimada
        if caracteristicas["area_total_materiales"] > 0:
            caracteristicas["utilizacion_estimada"] = min(
                caracteristicas["area_total_piezas"] / caracteristicas["area_total_materiales"],
                0.95
            )
        
        # Predecir con ML
        prediccion = ml_predictor.predict(caracteristicas)
        
        return {
            "prediccion_ml": True,
            "desperdicio_estimado": prediccion["waste"],
            "confianza": prediccion["confidence"],
            "recomendaciones": prediccion["recommendations"],
            "caracteristicas_usadas": caracteristicas
        }
        
    except Exception as e:
        return {
            "prediccion_ml": False,
            "error": str(e),
            "desperdicio_estimado": None
        }

@app.get("/api/ejemplos")
async def obtener_ejemplos():
    """Devuelve ejemplos predefinidos para probar"""
    ejemplos = {
        "ejemplo_papel": {
            "nombre": "Ejemplo del artículo de investigación",
            "descripcion": "Caso de estudio del artículo original",
            "materiales": [
                {"ancho": 100, "alto": 70, "cantidad": 20, "nombre": "Cartulina 100x70"}
            ],
            "piezas": [
                {"ancho": 43, "alto": 28, "demanda": 50, "nombre": "Pieza A"},
                {"ancho": 33, "alto": 21.6, "demanda": 75, "nombre": "Pieza B"},
                {"ancho": 25, "alto": 18, "demanda": 100, "nombre": "Pieza C"},
                {"ancho": 20, "alto": 15, "demanda": 120, "nombre": "Pieza D"}
            ]
        },
        "ejemplo_vidrio": {
            "nombre": "Vidriería básica",
            "descripcion": "Corte de vidrio para ventanas",
            "materiales": [
                {"ancho": 244, "alto": 122, "cantidad": 10, "nombre": "Vidrio estándar"}
            ],
            "piezas": [
                {"ancho": 60, "alto": 90, "demanda": 20, "nombre": "Ventana pequeña"},
                {"ancho": 90, "alto": 120, "demanda": 15, "nombre": "Ventana mediana"},
                {"ancho": 120, "alto": 150, "demanda": 8, "nombre": "Ventana grande"}
            ]
        }
    }
    
    return ejemplos

@app.get("/api/estadisticas")
async def obtener_estadisticas():
    """Estadísticas del sistema"""
    return {
        "sistema": "Optimizador de Corte 2D",
        "version": "1.0.0",
        "optimizaciones_realizadas": optimizer.get_stats()["total_optimizations"],
        "promedio_desperdicio": optimizer.get_stats()["avg_waste"],
        "tiempo_promedio": optimizer.get_stats()["avg_time"],
        "modelo_ml": ml_predictor.get_model_info()
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )