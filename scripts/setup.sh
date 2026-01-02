#!/bin/bash

echo "🚀 Configurando Sistema de Optimización de Corte 2D"
echo "================================================="

# Colores para mensajes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en la carpeta correcta
if [ ! -f "README.md" ]; then
    echo -e "${RED}❌ Error: Debes ejecutar este script desde la raíz del proyecto${NC}"
    exit 1
fi

echo -e "${YELLOW}1. Verificando dependencias...${NC}"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no está instalado${NC}"
    echo "Instala Python desde: https://www.python.org/downloads/"
    exit 1
else
    echo -e "${GREEN}✅ Python3 encontrado${NC}"
fi

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️ pip3 no encontrado, instalando...${NC}"
    python3 -m ensurepip --upgrade
fi
echo -e "${GREEN}✅ pip3 listo${NC}"

echo -e "\n${YELLOW}2. Instalando backend...${NC}"
cd backend
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backend instalado${NC}"
    else
        echo -e "${RED}❌ Error instalando backend${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ requirements.txt no encontrado${NC}"
    exit 1
fi
cd ..

echo -e "\n${YELLOW}3. Instalando frontend...${NC}"
cd frontend
if [ -f "package.json" ]; then
    npm install
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Frontend instalado${NC}"
    else
        echo -e "${YELLOW}⚠️ Intentando con npm ci...${NC}"
        npm ci
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Frontend instalado${NC}"
        else
            echo -e "${RED}❌ Error instalando frontend${NC}"
            exit 1
        fi
    fi
else
    echo -e "${RED}❌ package.json no encontrado${NC}"
    exit 1
fi
cd ..

echo -e "\n${YELLOW}4. Entrenando modelo ML...${NC}"
cd ml/training
if [ -f "train_model.py" ]; then
    python3 train_model.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Modelo ML entrenado${NC}"
    else
        echo -e "${YELLOW}⚠️ Modelo ML no pudo ser entrenado (continuando igual)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️ train_model.py no encontrado${NC}"
fi
cd ../..

echo -e "\n${YELLOW}5. Configurando base de datos...${NC}"
if [ ! -d "data" ]; then
    mkdir data
    echo -e "${GREEN}✅ Carpeta data creada${NC}"
fi

echo -e "\n${GREEN}🎉 ¡Instalación completada!${NC}"
echo -e "\n${YELLOW}Para iniciar el sistema:${NC}"
echo "1. Backend: cd backend && python run.py"
echo "2. Frontend: cd frontend && npm run dev"
echo -e "\n${YELLOW}O usar Docker:${NC}"
echo "docker-compose up"
echo -e "\n${YELLOW}Acceso:${NC}"
echo "Frontend: http://localhost:5173"
echo "Backend API: http://localhost:8000"
echo "Documentación API: http://localhost:8000/api/docs"