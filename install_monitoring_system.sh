#!/bin/bash
# INSTALACIÓN AUTOMÁTICA - SISTEMA DE MONITOREO PROFESIONAL
# =========================================================

echo "🚀 INSTALANDO SISTEMA DE MONITOREO PROFESIONAL"
echo "=============================================="

# Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3-pip python3-venv

# Instalar dependencias Python
echo "🐍 Instalando dependencias Python..."
pip3 install flask plotly pandas requests

# Dar permisos de ejecución
echo "🔧 Configurando permisos..."
chmod +x complete_monitoring_toolkit.py
chmod +x professional_monitoring_system.py
chmod +x version_management_system.py

# Crear directorio de templates si no existe
mkdir -p templates

echo "✅ INSTALACIÓN COMPLETADA"
echo "========================="
echo "🌐 Para usar el sistema:"
echo "   python3 complete_monitoring_toolkit.py"
echo ""
echo "📊 Dashboard web: http://localhost:5000"
echo "🔧 VPS: 107.174.133.202"
echo "🤖 Bot: Operando 24/7"
echo "=========================" 