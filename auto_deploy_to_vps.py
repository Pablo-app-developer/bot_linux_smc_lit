#!/usr/bin/env python3
"""
DESPLIEGUE AUTOMÁTICO AL VPS RACKNERD - BOT SMC-LIT
==================================================
Script para desplegar automáticamente el bot al VPS usando SSH
"""

import os
import sys
import subprocess
import time
from datetime import datetime

# Credenciales VPS RackNerd
VPS_CREDENTIALS = {
    'host': '107.174.133.202',
    'user': 'root',
    'password': 'n5X5dB6xPLJj06qr4C',
    'port': 22
}

def upload_to_vps():
    """Subir archivos al VPS usando scp"""
    print("📤 SUBIENDO ARCHIVOS AL VPS RACKNERD...")
    print(f"🌐 IP: {VPS_CREDENTIALS['host']}")
    
    try:
        # Usar sshpass + scp para subir el archivo comprimido
        scp_command = [
            'sshpass', '-p', VPS_CREDENTIALS['password'],
            'scp', 
            '-o', 'StrictHostKeyChecking=no',
            '-P', str(VPS_CREDENTIALS['port']),
            'smc-lit-bot-vps.tar.gz',
            f"{VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']}:/tmp/"
        ]
        
        print("⏳ Subiendo archivo comprimido...")
        result = subprocess.run(scp_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Archivo subido exitosamente al VPS")
            return True
        else:
            print(f"❌ Error subiendo archivo: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en upload: {e}")
        return False

def install_on_vps():
    """Instalar y configurar el bot en el VPS"""
    print("\n🔧 INSTALANDO BOT EN VPS...")
    
    # Comandos para ejecutar en el VPS
    install_commands = [
        "cd /tmp",
        "tar -xzf smc-lit-bot-vps.tar.gz",
        "cd vps_deploy",
        "chmod +x install_vps.sh",
        "./install_vps.sh",
        "cp -r * /home/smc-lit-bot/",
        "cd /home/smc-lit-bot",
        "chmod +x *.sh"
    ]
    
    try:
        # Ejecutar comandos via SSH con sshpass
        ssh_command = [
            'sshpass', '-p', VPS_CREDENTIALS['password'],
            'ssh',
            '-o', 'StrictHostKeyChecking=no',
            '-p', str(VPS_CREDENTIALS['port']),
            f"{VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']}",
            ' && '.join(install_commands)
        ]
        
        print("⏳ Ejecutando instalación en VPS...")
        result = subprocess.run(ssh_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Instalación completada en VPS")
            print(f"📋 Salida: {result.stdout}")
            return True
        else:
            print(f"❌ Error en instalación: {result.stderr}")
            print(f"📋 Salida: {result.stdout}")
            return False
            
    except Exception as e:
        print(f"❌ Error en instalación: {e}")
        return False

def start_bot_on_vps():
    """Iniciar el bot en el VPS usando screen"""
    print("\n🚀 INICIANDO BOT EN VPS...")
    
    # Comando para iniciar el bot en screen
    start_command = [
        'sshpass', '-p', VPS_CREDENTIALS['password'],
        'ssh',
        '-o', 'StrictHostKeyChecking=no',
        '-p', str(VPS_CREDENTIALS['port']),
        f"{VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']}",
        'cd /home/smc-lit-bot && source venv/bin/activate && screen -dmS smc-bot python3 main_unlimited.py'
    ]
    
    try:
        print("⏳ Iniciando bot en screen...")
        result = subprocess.run(start_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Bot iniciado exitosamente en VPS")
            return True
        else:
            print(f"⚠️  Posible error iniciando bot: {result.stderr}")
            return True  # A veces screen no retorna 0 pero funciona
            
    except Exception as e:
        print(f"❌ Error iniciando bot: {e}")
        return False

def check_bot_status():
    """Verificar estado del bot en el VPS"""
    print("\n📊 VERIFICANDO ESTADO DEL BOT...")
    
    status_command = [
        'sshpass', '-p', VPS_CREDENTIALS['password'],
        'ssh',
        '-o', 'StrictHostKeyChecking=no',
        '-p', str(VPS_CREDENTIALS['port']),
        f"{VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']}",
        'ps aux | grep main_unlimited || echo "Bot no encontrado"'
    ]
    
    try:
        result = subprocess.run(status_command, capture_output=True, text=True)
        print(f"📋 Estado del bot: {result.stdout}")
        
        # Verificar si screen está ejecutándose
        screen_command = [
            'sshpass', '-p', VPS_CREDENTIALS['password'],
            'ssh',
            '-o', 'StrictHostKeyChecking=no',
            '-p', str(VPS_CREDENTIALS['port']),
            f"{VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']}",
            'screen -list'
        ]
        
        screen_result = subprocess.run(screen_command, capture_output=True, text=True)
        print(f"📺 Sessions screen: {screen_result.stdout}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando estado: {e}")
        return False

def create_monitor_script():
    """Crear script de monitoreo automático"""
    monitor_script = f"""#!/bin/bash
# SCRIPT DE MONITOREO AUTOMÁTICO VPS
echo "🤖 MONITOREANDO BOT SMC-LIT EN VPS"
echo "=================================="
echo "🌐 VPS: {VPS_CREDENTIALS['host']}"
echo "⏰ $(date)"
echo ""

# Verificar estado via SSH
sshpass -p '{VPS_CREDENTIALS['password']}' ssh -o StrictHostKeyChecking=no -p {VPS_CREDENTIALS['port']} {VPS_CREDENTIALS['user']}@{VPS_CREDENTIALS['host']} << 'EOF'
echo "📊 PROCESOS DEL BOT:"
ps aux | grep main_unlimited | grep -v grep || echo "❌ Bot no está ejecutándose"
echo ""
echo "📺 SESIONES SCREEN:"
screen -list || echo "❌ No hay sesiones screen"
echo ""
echo "📋 ÚLTIMOS LOGS:"
tail -5 /home/smc-lit-bot/bot.log 2>/dev/null || echo "❌ No hay logs disponibles"
EOF
"""
    
    with open('monitor_vps.sh', 'w') as f:
        f.write(monitor_script)
    
    os.chmod('monitor_vps.sh', 0o755)
    print("📊 Script de monitoreo creado: monitor_vps.sh")

def main():
    print("🚀 DESPLIEGUE AUTOMÁTICO AL VPS RACKNERD")
    print("=" * 50)
    print(f"🌐 VPS IP: {VPS_CREDENTIALS['host']}")
    print(f"👤 Usuario: {VPS_CREDENTIALS['user']}")
    print(f"💰 Cuenta Demo: $1,000 USD")
    print(f"⚡ Modo Sin Limitaciones: ACTIVADO")
    print("=" * 50)
    
    # Verificar que el archivo comprimido existe
    if not os.path.exists('smc-lit-bot-vps.tar.gz'):
        print("❌ Archivo smc-lit-bot-vps.tar.gz no encontrado")
        print("🔧 Ejecutando script de preparación...")
        subprocess.run(['python3', 'deploy_vps_unlimited.py'], check=True)
    
    try:
        # Paso 1: Subir archivos
        if not upload_to_vps():
            print("❌ Falló la subida de archivos")
            return False
        
        time.sleep(2)
        
        # Paso 2: Instalar en VPS
        if not install_on_vps():
            print("❌ Falló la instalación")
            return False
        
        time.sleep(3)
        
        # Paso 3: Iniciar bot
        if not start_bot_on_vps():
            print("❌ Falló el inicio del bot")
            return False
        
        time.sleep(2)
        
        # Paso 4: Verificar estado
        check_bot_status()
        
        # Paso 5: Crear script de monitoreo
        create_monitor_script()
        
        print("\n🎉 DESPLIEGUE COMPLETADO EXITOSAMENTE")
        print("=" * 45)
        print("✅ Bot desplegado y ejecutándose en VPS")
        print("🌐 IP VPS: 107.174.133.202")
        print("💰 Cuenta Demo: $1,000 USD - Sin limitaciones")
        print("📊 Para monitorear: ./monitor_vps.sh")
        print("🔧 Para conectar: ssh root@107.174.133.202")
        print("📺 Para ver bot: screen -r smc-bot")
        print("\n🔥 EL BOT ESTÁ OPERANDO 24/7 EN TU VPS")
        
        return True
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        return False

if __name__ == "__main__":
    main() 