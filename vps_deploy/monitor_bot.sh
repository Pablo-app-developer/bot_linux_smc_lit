#!/bin/bash
# MONITOREO DEL BOT SMC-LIT
echo "📊 ESTADO DEL BOT SMC-LIT"
echo "========================"

# Verificar si el bot está ejecutándose
if pgrep -f "main_unlimited.py" > /dev/null; then
    echo "✅ Bot EJECUTÁNDOSE"
    echo "🔢 PID: $(pgrep -f main_unlimited.py)"
    echo "⏰ Tiempo activo: $(ps -o etime= -p $(pgrep -f main_unlimited.py))"
else
    echo "❌ Bot NO está ejecutándose"
    echo "🔄 Reiniciando bot..."
    cd /home/smc-lit-bot
    source venv/bin/activate
    nohup python3 main_unlimited.py > bot.log 2>&1 &
    echo "✅ Bot reiniciado"
fi

# Mostrar últimas líneas del log
echo ""
echo "📋 ÚLTIMAS ACTIVIDADES:"
tail -10 /home/smc-lit-bot/bot.log 2>/dev/null || echo "Log no disponible"
