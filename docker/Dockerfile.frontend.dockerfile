FROM node:18-alpine as build

WORKDIR /app

# Copiar package.json
COPY frontend/package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código
COPY frontend/ .

# Construir
RUN npm run build

# Servir con nginx
FROM nginx:alpine

# Copiar build
COPY --from=build /app/dist /usr/share/nginx/html

# Configuración nginx
COPY docker/nginx.conf /etc/nginx/nginx.conf

# Puerto
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]