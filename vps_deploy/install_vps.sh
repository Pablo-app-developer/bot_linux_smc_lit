#!/bin/bash
# INSTALACIÓN AUTOMÁTICA EN VPS - BOT SMC-LIT
echo "🚀 INSTALANDO BOT SMC-LIT EN VPS..."

# Actualizar sistema
apt update && apt upgrade -y

# Instalar Python y dependencias
apt install -y python3 python3-pip python3-venv git screen htop

# Crear directorio del bot
mkdir -p /home/smc-lit-bot
cd /home/smc-lit-bot

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Dar permisos de ejecución
chmod +x *.sh
chmod +x main_unlimited.py

echo "✅ INSTALACIÓN COMPLETADA"
echo "🎯 Para iniciar el bot: ./start_unlimited_bot.sh"
