"""
Predictor de Machine Learning para desperdicio
"""
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from typing import Dict
import json
import os

class WastePredictor:
    """Predictor de desperdicio usando ML"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.features = [
            'num_materiales',
            'num_piezas',
            'area_total_materiales',
            'area_total_piezas',
            'utilizacion_estimada'
        ]
        
        # Cargar o crear modelo
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.train_dummy_model()
    
    def train_dummy_model(self):
        """Entrenar modelo de ejemplo"""
        # Datos de ejemplo basados en el artículo
        data = {
            'num_materiales': [1, 2, 1, 3],
            'num_piezas': [2, 4, 3, 5],
            'area_total_materiales': [7000, 15000, 8000, 20000],
            'area_total_piezas': [5000, 12000, 6500, 17000],
            'utilizacion_estimada': [0.71, 0.80, 0.81, 0.85],
            'waste': [2000, 3000, 1500, 3000]
        }
        
        df = pd.DataFrame(data)
        X = df[self.features]
        y = df['waste']
        
        # Entrenar modelo simple
        self.model = RandomForestRegressor(n_estimators=10, random_state=42)
        self.model.fit(X, y)
    
    def predict(self, features: Dict) -> Dict:
        """Predecir desperdicio"""
        try:
            # Preparar características
            X = np.array([[features.get(f, 0) for f in self.features]])
            
            # Predecir
            waste_pred = self.model.predict(X)[0]
            
            # Calcular confianza (simplificado)
            confidence = min(0.95, 0.7 + (features.get('utilizacion_estimada', 0) * 0.3))
            
            # Generar recomendaciones
            recommendations = []
            if features.get('utilizacion_estimada', 0) < 0.7:
                recommendations.append("Considera usar materiales de diferentes tamaños")
            if features.get('num_piezas', 0) > 10:
                recommendations.append("Problema complejo, el tiempo de optimización puede ser mayor")
            
            return {
                "waste": float(waste_pred),
                "confidence": float(confidence),
                "recommendations": recommendations
            }
            
        except Exception as e:
            # Fallback a estimación simple
            estimated_waste = features.get('area_total_materiales', 0) * 0.15
            return {
                "waste": float(estimated_waste),
                "confidence": 0.5,
                "recommendations": ["Usando estimación básica - modelo no disponible"],
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict:
        """Información del modelo"""
        return {
            "type": "RandomForestRegressor",
            "features": self.features,
            "trained": self.model is not None,
            "version": "1.0"
        }
    
    def save_model(self, path: str):
        """Guardar modelo"""
        if self.model:
            joblib.dump(self.model, path)
    
    def load_model(self, path: str):
        """Cargar modelo"""
        self.model = joblib.load(path)