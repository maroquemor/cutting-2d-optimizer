#!/bin/bash

echo "🚀 Iniciando Sistema de Optimización de Corte 2D"
echo "=============================================="

# Función para limpiar al salir
cleanup() {
    echo -e "\n🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✅ Servicios detenidos"
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT SIGTERM

# Iniciar backend
echo "🌐 Iniciando backend..."
cd backend
python run.py &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend inicie
sleep 3

# Iniciar frontend
echo "🎨 Iniciando frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo -e "\n✅ Sistema iniciado correctamente"
echo "================================="
echo "🌐 Backend API: http://localhost:8000"
echo "📚 Documentación: http://localhost:8000/api/docs"
echo "🎨 Frontend: http://localhost:5173"
echo -e "\n📝 Presiona Ctrl+C para detener"

# Mantener el script ejecutándose
wait $BACKEND_PID $FRONTEND_PID