#!/bin/bash
# INSTALACIÓN COMPLETA BOT SMC-LIT
# =================================

echo "🚀 INSTALANDO BOT SMC-LIT PARA OPERACIÓN 24/7"
echo "============================================="

# Actualizar sistema
echo "📦 Actualizando sistema..."
apt update && apt upgrade -y

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias..."
apt install -y python3 python3-pip python3-venv python3-dev
apt install -y build-essential curl wget git htop screen tmux
apt install -y libssl-dev libffi-dev python3-setuptools

# Crear directorio del bot
echo "📁 Configurando directorio..."
mkdir -p /home/smc-lit-bot
cd /home/smc-lit-bot

# Crear entorno virtual
echo "🐍 Configurando entorno Python..."
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip setuptools wheel

# Instalar dependencias específicas para trading
echo "📈 Instalando librerías de trading..."
pip install MetaTrader5 pandas numpy scikit-learn
pip install xgboost lightgbm catboost
pip install matplotlib seaborn plotly
pip install requests urllib3 websocket-client
pip install python-dotenv joblib pickle5
pip install ta-lib TA-Lib technical-indicators
pip install yfinance backtrader

# Instalar dependencias adicionales
pip install -r requirements.txt

# Configurar permisos
chmod +x *.py *.sh

# Crear servicio systemd para auto-inicio
cat > /etc/systemd/system/smc-lit-unlimited.service << EOF
[Unit]
Description=SMC-LIT Trading Bot - Modo Sin Limitaciones
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/smc-lit-bot
Environment=PATH=/home/smc-lit-bot/venv/bin
ExecStart=/home/smc-lit-bot/start_unlimited_bot.sh
Restart=always
RestartSec=10
StandardOutput=append:/home/smc-lit-bot/bot_output.log
StandardError=append:/home/smc-lit-bot/bot_error.log

[Install]
WantedBy=multi-user.target
EOF

# Configurar timezone
timedatectl set-timezone UTC

# Configurar logs
touch /home/smc-lit-bot/bot_output.log
touch /home/smc-lit-bot/bot_error.log
chmod 666 /home/smc-lit-bot/*.log

echo "✅ INSTALACIÓN COMPLETADA"
echo "========================"
echo "📁 Bot instalado en: /home/smc-lit-bot"
echo "🚀 Para iniciar manualmente: ./start_unlimited_bot.sh"
echo "🔄 Para auto-inicio: systemctl start smc-lit-unlimited"
echo "📊 Para ver logs: tail -f /home/smc-lit-bot/bot_output.log"
echo "⚠️  El bot operará SIN LIMITACIONES en modo demo"
