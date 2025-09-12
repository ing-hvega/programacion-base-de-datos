#!/bin/bash

# Script para construir la imagen Docker para backend-idat

# Colores para la salida
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Construyendo imagen de backend-idat ===${NC}"

# Directorio actual (donde está este script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Verificar si existe el directorio backend-idat
if [ ! -d "$SCRIPT_DIR/backend-idat" ]; then
    echo -e "${YELLOW}Error: No se encontró el directorio backend-idat${NC}"
    exit 1
fi

# Cambiar al directorio backend-idat
cd "$SCRIPT_DIR/backend-idat"

# Construir la imagen Docker
echo -e "${YELLOW}Construyendo imagen Docker...${NC}"
docker build -t backend-idat:latest .

# Verificar si la compilación fue exitosa
if [ $? -eq 0 ]; then
    echo -e "${GREEN}¡Imagen construida con éxito!${NC}"
else
    echo -e "${YELLOW}Error: No se pudo construir la imagen Docker${NC}"
    exit 1
fi
