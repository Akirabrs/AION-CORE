#!/bin/bash

# Cores para o terminal (Estética Hacker)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}====================================================================${NC}"
echo -e "${BLUE}       🚀 AION-CORE: INITIALIZING SYSTEM SEQUENCE...               ${NC}"
echo -e "${BLUE}====================================================================${NC}"

# 1. Instalação de Dependências
echo -e "\n${GREEN}[1/3] 📦 Instalando Dependências do Cérebro Neural...${NC}"
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "✅ Dependências instaladas com sucesso."
else
    echo -e "${RED}❌ Falha na instalação. Verifique o Python.${NC}"
    exit 1
fi

# 2. Verificação de Integridade
echo -e "\n${GREEN}[2/3] 🧠 Verificando Integridade do NPE (Professor)...${NC}"
if [ -f "npe/brain.py" ]; then
    echo -e "✅ Cérebro detectado: npe/brain.py"
else
    echo -e "${RED}❌ ERRO CRÍTICO: Cérebro não encontrado!${NC}"
    exit 1
fi

# 3. Execução do Benchmark
echo -e "\n${GREEN}[3/3] ⚔️  Iniciando Benchmark: PID Clássico vs AION-CORE...${NC}"
python experiments/benchmark_vde.py

echo -e "\n${BLUE}====================================================================${NC}"
echo -e "${BLUE}       ✨ SISTEMA OPERACIONAL. VERIFIQUE 'benchmark_result.png'    ${NC}"
echo -e "${BLUE}====================================================================${NC}"
