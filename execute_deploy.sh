#!/bin/bash
# Script de transferencia y ejecución automática

echo "📤 Transfiriendo archivos al VPS..."

# Crear directorio en VPS
sshpass -p 'n5X5dB6xPLJj06qr4C' ssh -o StrictHostKeyChecking=no root@107.174.133.202 "mkdir -p /home/smc-lit-bot"

# Transferir archivos
sshpass -p 'n5X5dB6xPLJj06qr4C' scp -r -o StrictHostKeyChecking=no deploy_temp/* root@107.174.133.202:/home/smc-lit-bot/

# Ejecutar instalación
echo "🔧 Ejecutando instalación en VPS..."
sshpass -p 'n5X5dB6xPLJj06qr4C' ssh -o StrictHostKeyChecking=no root@107.174.133.202 "cd /home/smc-lit-bot && chmod +x *.sh && ./install_complete.sh"

# Iniciar bot
echo "🚀 Iniciando bot en VPS..."
sshpass -p 'n5X5dB6xPLJj06qr4C' ssh -o StrictHostKeyChecking=no root@107.174.133.202 "cd /home/smc-lit-bot && nohup ./start_unlimited_bot.sh > bot_unlimited.log 2>&1 &"

echo "✅ DEPLOYMENT COMPLETADO"
echo "📊 Bot operando sin limitaciones en: 107.174.133.202"
echo "📋 Para ver logs: ssh root@107.174.133.202 'tail -f /home/smc-lit-bot/bot_unlimited.log'"
