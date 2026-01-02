"""
Entrenamiento del modelo de Machine Learning
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import json

def generate_training_data():
    """Generar datos de entrenamiento basados en el artículo"""
    
    # Datos basados en el estudio
    data = []
    
    # Configuraciones típicas
    configs = [
        # Ejemplo simple
        {
            'num_materiales': 1,
            'num_piezas': 2,
            'area_total_materiales': 7000,
            'area_total_piezas': 5000,
            'utilizacion_estimada': 0.71,
            'waste': 2000
        },
        # Ejemplo mediano
        {
            'num_materiales': 2,
            'num_piezas': 4,
            'area_total_materiales': 15000,
            'area_total_piezas': 12000,
            'utilizacion_estimada': 0.80,
            'waste': 3000
        },
        # Ejemplo del artículo
        {
            'num_materiales': 1,
            'num_piezas': 4,
            'area_total_materiales': 140000,  # 20 placas de 100x70
            'area_total_piezas': 120000,     # Suma de áreas de piezas
            'utilizacion_estimada': 0.857,
            'waste': 20000
        }
    ]
    
    # Generar variaciones
    for config in configs:
        for _ in range(50):  # 50 variaciones por configuración
            variation = config.copy()
            
            # Añadir ruido aleatorio
            variation['waste'] *= np.random.uniform(0.9, 1.1)
            variation['utilizacion_estimada'] *= np.random.uniform(0.95, 1.05)
            
            data.append(variation)
    
    return pd.DataFrame(data)

def train_model():
    """Entrenar modelo de predicción de desperdicio"""
    
    print("🔧 Entrenando modelo de Machine Learning...")
    
    # Generar datos
    df = generate_training_data()
    print(f"📊 Datos generados: {len(df)} muestras")
    
    # Separar características y target
    features = ['num_materiales', 'num_piezas', 'area_total_materiales', 
                'area_total_piezas', 'utilizacion_estimada']
    X = df[features]
    y = df['waste']
    
    # Dividir en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"  Training set: {len(X_train)} muestras")
    print(f"  Test set: {len(X_test)} muestras")
    
    # Entrenar modelo
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluar
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"✅ Modelo entrenado")
    print(f"📈 MAE: {mae:.2f}")
    print(f"📈 R² Score: {r2:.4f}")
    
    # Importancia de características
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n📊 Importancia de características:")
    print(feature_importance.to_string(index=False))
    
    # Guardar modelo
    model_path = '../models/waste_predictor.pkl'
    joblib.dump(model, model_path)
    
    # Guardar metadata
    metadata = {
        'features': features,
        'performance': {
            'mae': float(mae),
            'r2': float(r2)
        },
        'training_samples': len(df),
        'model_type': 'RandomForestRegressor'
    }
    
    with open('../models/model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"💾 Modelo guardado en: {model_path}")
    
    return model, mae, r2

if __name__ == '__main__':
    train_model()