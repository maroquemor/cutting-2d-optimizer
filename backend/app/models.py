"""
Modelos Pydantic para la API
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# Modelos de entrada (request)

class MaterialInput(BaseModel):
    """Modelo para material de entrada"""
    ancho: float = Field(..., gt=0, description="Ancho del material en cm")
    alto: float = Field(..., gt=0, description="Alto del material en cm")
    cantidad: int = Field(..., gt=0, description="Cantidad disponible")
    nombre: Optional[str] = Field(None, description="Nombre identificador")

class PieceInput(BaseModel):
    """Modelo para pieza de entrada"""
    ancho: float = Field(..., gt=0, description="Ancho de la pieza en cm")
    alto: float = Field(..., gt=0, description="Alto de la pieza en cm")
    demanda: int = Field(..., gt=0, description="Cantidad requerida")
    nombre: Optional[str] = Field(None, description="Nombre identificador")

class OptimizationConfig(BaseModel):
    """Configuración de optimización"""
    usar_sustitucion: bool = Field(True, description="Usar variantes de sustitución")
    max_patrones: int = Field(1000, description="Máximo número de patrones a generar")
    tiempo_limite: int = Field(300, description="Tiempo límite en segundos")

class OptimizationRequest(BaseModel):
    """Request completo para optimización"""
    materiales: List[MaterialInput]
    piezas: List[PieceInput]
    config: Optional[OptimizationConfig] = None

# Modelos de salida (response)

class CuttingPattern(BaseModel):
    """Patrón de corte individual"""
    id: int
    material_id: int
    piezas: List[dict]
    desperdicio: float
    instrucciones: List[str]

class OptimizationResult(BaseModel):
    """Resultado de optimización"""
    optimizacion_id: str
    desperdicio_total: float
    tiempo_ejecucion: float
    patrones_utilizados: int
    utilizacion_material: float
    fecha: datetime

class OptimizationResponse(BaseModel):
    """Response principal"""
    success: bool
    desperdicio: float
    tiempo_ejecucion: float
    patrones_utilizados: int
    instrucciones: List[str]
    visualizacion_url: Optional[str] = None
    resumen: dict