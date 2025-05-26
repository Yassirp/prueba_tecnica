#!/bin/bash

# Colores para el output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running Ruff linter...${NC}"
ruff check ./src/

echo -e "\n${YELLOW}Running Ruff formatter...${NC}"
ruff format ./src/

echo -e "\n${YELLOW}Running MyPy type checker...${NC}"
mypy_output=$(mypy ./src/ 2>&1)
mypy_exit_code=$?

# Formatear el output de mypy
if [ $mypy_exit_code -eq 0 ]; then
    echo -e "${GREEN}[OK] No type errors found${NC}"
else
    echo -e "${RED}Type errors found:${NC}"
    echo "$mypy_output" | while IFS= read -r line; do
        if [[ $line =~ error: ]]; then
            file_line=$(echo "$line" | sed -E 's/^(.*?):.*/\1/')
            error_msg=$(echo "$line" | sed -E 's/.*?error: //')
            echo -e "\n${RED}$file_line -${NC}"
            echo -e "  ${YELLOW}Error: $error_msg${NC}"
        elif [[ $line =~ note: ]]; then
            note_msg=$(echo "$line" | sed -E 's/.*?note: //')
            echo -e "    ${YELLOW}Note: $note_msg${NC}"
        elif [[ $line =~ Found ]]; then
            echo -e "\n${RED}$line${NC}"
        fi
    done
fi

# Ejecutar tests si existe la carpeta
if [ -d "./src/tests" ]; then
    echo -e "\n${YELLOW}Running tests...${NC}"
    pytest ./src/tests/ -v
else
    echo -e "\n${YELLOW}No tests folder found, skipping tests.${NC}"
fi

echo -e "\n${GREEN}Análisis completado${NC}"