#!/bin/bash
# Script de despliegue automático para VPS Ubuntu

echo "🚀 DESPLIEGUE AUTOMÁTICO BOT SMC-LIT"
echo "=================================="

# Variables (editar según tu VPS)
VPS_IP="TU_VPS_IP"
VPS_USER="ubuntu"
VPS_PATH="/home/ubuntu"

echo "📝 Configuración:"
echo "   VPS IP: $VPS_IP"
echo "   Usuario: $VPS_USER"
echo "   Directorio: $VPS_PATH"

# Verificar conexión SSH
echo -n "🔗 Verificando conexión SSH... "
if ssh -o ConnectTimeout=5 -o BatchMode=yes $VPS_USER@$VPS_IP exit 2>/dev/null; then
    echo "✅ OK"
else
    echo "❌ FALLO"
    echo "Por favor configura tu conexión SSH primero:"
    echo "ssh-copy-id $VPS_USER@$VPS_IP"
    exit 1
fi

# Crear archivo comprimido
echo "📦 Comprimiendo archivos del bot..."
tar -czf bot-smc-lit.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.venv' \
    --exclude='*.log' \
    --exclude='*.pyc' \
    .

# Transferir archivos
echo "📤 Transfiriendo archivos a la VPS..."
scp bot-smc-lit.tar.gz $VPS_USER@$VPS_IP:$VPS_PATH/

# Ejecutar comandos en la VPS
echo "⚙️ Configurando bot en la VPS..."
ssh $VPS_USER@$VPS_IP << 'ENDSSH'
cd /home/ubuntu

# Extraer archivos
echo "📂 Extrayendo archivos..."
rm -rf bot-smc-lit-old
if [ -d "bot-smc-lit" ]; then
    mv bot-smc-lit bot-smc-lit-old
fi
tar -xzf bot-smc-lit.tar.gz -C .
mv bot-smc-lit-* bot-smc-lit 2>/dev/null || true

cd bot-smc-lit

# Verificar Python
echo "🐍 Verificando Python..."
python3 --version

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear script de inicio
echo "📝 Creando script de inicio..."
cat > start_bot_vps.sh << 'EOF'
#!/bin/bash
cd /home/ubuntu/bot-smc-lit
source .venv/bin/activate
python start_bot.py
EOF
chmod +x start_bot_vps.sh

# Crear servicio systemd
echo "🔄 Configurando servicio systemd..."
sudo tee /etc/systemd/system/smc-lit-bot.service > /dev/null << 'EOF'
[Unit]
Description=SMC-LIT Trading Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bot-smc-lit
Environment=PATH=/home/ubuntu/bot-smc-lit/.venv/bin
ExecStart=/home/ubuntu/bot-smc-lit/.venv/bin/python start_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Recargar systemd
sudo systemctl daemon-reload
sudo systemctl enable smc-lit-bot.service

echo "✅ Configuración completada!"
echo ""
echo "📋 PRÓXIMOS PASOS:"
echo "1. Configurar archivo .env con tus credenciales"
echo "2. Iniciar el servicio: sudo systemctl start smc-lit-bot"
echo "3. Ver logs: sudo journalctl -u smc-lit-bot -f"

ENDSSH

# Limpiar archivo temporal
rm bot-smc-lit.tar.gz

echo ""
echo "🎉 ¡DESPLIEGUE COMPLETADO!"
echo ""
echo "📞 Comandos útiles para la VPS:"
echo "   ssh $VPS_USER@$VPS_IP"
echo "   sudo systemctl start smc-lit-bot"
echo "   sudo systemctl status smc-lit-bot"
echo "   sudo journalctl -u smc-lit-bot -f"
echo ""
echo "⚠️  RECUERDA:"
echo "   1. Configurar el archivo .env en la VPS"
echo "   2. Usar credenciales reales de MT5 para trading"
echo "   3. Monitorear los logs regularmente" 