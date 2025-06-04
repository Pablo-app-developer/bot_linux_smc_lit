#!/bin/bash
# SCRIPT DE MONITOREO AUTOMÁTICO VPS
echo "🤖 MONITOREANDO BOT SMC-LIT EN VPS"
echo "=================================="
echo "🌐 VPS: 107.174.133.202"
echo "⏰ $(date)"
echo ""

# Verificar estado via SSH
sshpass -p 'n5X5dB6xPLJj06qr4C' ssh -o StrictHostKeyChecking=no -p 22 root@107.174.133.202 << 'EOF'
echo "📊 PROCESOS DEL BOT:"
ps aux | grep main_unlimited | grep -v grep || echo "❌ Bot no está ejecutándose"
echo ""
echo "📺 SESIONES SCREEN:"
screen -list || echo "❌ No hay sesiones screen"
echo ""
echo "📋 ÚLTIMOS LOGS:"
tail -5 /home/smc-lit-bot/bot.log 2>/dev/null || echo "❌ No hay logs disponibles"
EOF
