#!/bin/bash
# INICIO AGRESIVO - BOT SMC-LIT SIN LIMITACIONES
# ============================================

cd /home/smc-lit-bot
source venv/bin/activate

echo "🤖 INICIANDO BOT SMC-LIT - MODO SIN LIMITACIONES"
echo "==============================================="
echo "💰 Cuenta Demo: $1,000 USD"
echo "⚡ Modo Agresivo: ACTIVADO"
echo "🎯 Sin límites de trading"
echo "==============================================="

# Variables de entorno para operación agresiva
export DEMO_MODE=true
export UNLIMITED_TRADING=true
export AGGRESSIVE_MODE=true
export AUTO_RESTART=true
export RISK_PERCENT=2.0
export MAX_TRADES_PER_DAY=50
export SCALPING_MODE=true

# Iniciar bot con configuración agresiva
python3 main.py --demo --unlimited --aggressive --symbol EURUSD --risk 2.0 --max-trades 50

# Si el bot se detiene, reiniciar automáticamente
while true; do
    echo "🔄 REINICIANDO BOT AUTOMÁTICAMENTE..."
    sleep 5
    python3 main.py --demo --unlimited --aggressive --symbol EURUSD --risk 2.0 --max-trades 50
done
