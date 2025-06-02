#!/usr/bin/env python3
"""
DESPLIEGUE AUTOMÁTICO AL VPS - BOT SMC-LIT SIN LIMITACIONES
===========================================================
Script para desplegar y ejecutar el bot en modo agresivo en VPS
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime

# Configuración del VPS
VPS_CONFIG = {
    'host': 'tu-vps-ip',  # Reemplazar con IP del VPS
    'user': 'root',
    'port': 22,
    'bot_dir': '/home/smc-lit-bot',
    'python_path': '/usr/bin/python3'
}

# Configuración del bot sin limitaciones
BOT_CONFIG = {
    'demo_mode': True,
    'unlimited_trading': True,
    'aggressive_mode': True,
    'risk_per_trade': 2.0,
    'max_trades_per_day': 100,
    'auto_restart': True,
    'scalping_mode': True,
    'high_frequency': True
}

def create_vps_deployment_package():
    """Crear paquete de despliegue para VPS"""
    print("📦 Creando paquete de despliegue...")
    
    # Archivos esenciales para el VPS
    essential_files = [
        'main_unlimited.py',
        'config_vps_unlimited.json',
        'start_unlimited_bot.sh',
        'requirements.txt',
        'src/',
        'install_complete.sh'
    ]
    
    # Crear directorio temporal
    os.makedirs('vps_deploy', exist_ok=True)
    
    # Copiar archivos esenciales
    for file in essential_files:
        if os.path.exists(file):
            if os.path.isdir(file):
                subprocess.run(['cp', '-r', file, 'vps_deploy/'], check=True)
            else:
                subprocess.run(['cp', file, 'vps_deploy/'], check=True)
    
    # Crear script de instalación específico para VPS
    vps_install_script = """#!/bin/bash
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
"""
    
    with open('vps_deploy/install_vps.sh', 'w') as f:
        f.write(vps_install_script)
    
    # Crear script de monitoreo
    monitor_script = """#!/bin/bash
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
"""
    
    with open('vps_deploy/monitor_bot.sh', 'w') as f:
        f.write(monitor_script)
    
    # Hacer ejecutables los scripts
    subprocess.run(['chmod', '+x', 'vps_deploy/install_vps.sh'], check=True)
    subprocess.run(['chmod', '+x', 'vps_deploy/monitor_bot.sh'], check=True)
    
    print("✅ Paquete de despliegue creado en: vps_deploy/")
    return True

def create_deployment_instructions():
    """Crear instrucciones de despliegue"""
    instructions = """
# INSTRUCCIONES DE DESPLIEGUE AL VPS
=====================================

## 1. SUBIR ARCHIVOS AL VPS
```bash
# Comprimir archivos
tar -czf smc-lit-bot.tar.gz vps_deploy/*

# Subir al VPS (reemplazar IP_VPS con tu IP)
scp smc-lit-bot.tar.gz root@IP_VPS:/tmp/

# Conectar al VPS
ssh root@IP_VPS
```

## 2. INSTALAR EN EL VPS
```bash
# Extraer archivos
cd /tmp
tar -xzf smc-lit-bot.tar.gz
cd vps_deploy

# Ejecutar instalación
./install_vps.sh

# Copiar archivos al directorio final
cp -r * /home/smc-lit-bot/
cd /home/smc-lit-bot
```

## 3. CONFIGURAR CREDENCIALES
Editar el archivo config_vps_unlimited.json con tus credenciales:
```json
{
  "MT5_LOGIN": "164675960",
  "MT5_PASSWORD": "pfbc0en",
  "MT5_SERVER": "MetaQuotes-Demo"
}
```

## 4. INICIAR BOT
```bash
# Iniciar en screen (para mantener ejecutándose)
screen -S smc-bot
source venv/bin/activate
python3 main_unlimited.py

# Salir de screen: Ctrl+A, luego D
# Volver a screen: screen -r smc-bot
```

## 5. MONITOREO
```bash
# Verificar estado
./monitor_bot.sh

# Ver logs en tiempo real
tail -f bot.log

# Verificar procesos
ps aux | grep python
```

## 6. CONFIGURACIÓN AUTOMÁTICA (OPCIONAL)
```bash
# Crear servicio systemd para auto-inicio
sudo nano /etc/systemd/system/smc-bot.service

[Unit]
Description=SMC-LIT Trading Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/smc-lit-bot
Environment=PATH=/home/smc-lit-bot/venv/bin
ExecStart=/home/smc-lit-bot/venv/bin/python main_unlimited.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Habilitar servicio
sudo systemctl enable smc-bot
sudo systemctl start smc-bot
sudo systemctl status smc-bot
```

## COMANDOS ÚTILES
- Iniciar bot: `python3 main_unlimited.py`
- Detener bot: `pkill -f main_unlimited.py`
- Ver estado: `./monitor_bot.sh`
- Ver logs: `tail -f bot.log`
- Reiniciar: `./start_unlimited_bot.sh`
"""
    
    with open('INSTRUCCIONES_VPS.md', 'w') as f:
        f.write(instructions)
    
    print("📋 Instrucciones creadas en: INSTRUCCIONES_VPS.md")

def main():
    print("🚀 PREPARANDO DESPLIEGUE AL VPS - BOT SMC-LIT SIN LIMITACIONES")
    print("=" * 65)
    print(f"💰 Cuenta Demo: $1,000 USD")
    print(f"⚡ Modo Agresivo: ACTIVADO")
    print(f"🎯 Sin limitaciones de trading")
    print("=" * 65)
    
    try:
        # Crear paquete de despliegue
        if create_vps_deployment_package():
            print("✅ Paquete de despliegue creado exitosamente")
        
        # Crear instrucciones
        create_deployment_instructions()
        
        # Comprimir para facilitar transferencia
        print("\n📦 Comprimiendo archivos para transferencia...")
        subprocess.run(['tar', '-czf', 'smc-lit-bot-vps.tar.gz', 'vps_deploy/'], check=True)
        
        print("\n🎉 DESPLIEGUE PREPARADO EXITOSAMENTE")
        print("=" * 50)
        print("📁 Archivos listos en: vps_deploy/")
        print("📦 Archivo comprimido: smc-lit-bot-vps.tar.gz")
        print("📋 Instrucciones: INSTRUCCIONES_VPS.md")
        print("\n🔥 EL BOT ESTÁ LISTO PARA OPERAR SIN LIMITACIONES EN VPS")
        print("💡 Sigue las instrucciones en INSTRUCCIONES_VPS.md")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en el despliegue: {e}")
        return False

if __name__ == "__main__":
    main() 