#!/usr/bin/env python3
"""
SCRIPT DE DESPLIEGUE A VPS
========================
Despliega automáticamente el bot SMC-LIT al VPS de RackNerd
"""

import os
import sys
import subprocess
import json
from datetime import datetime

# INFORMACIÓN DEL VPS (proporcionada por el usuario)
VPS_INFO = {
    'ip': '107.174.133.202',
    'usuario': 'root',
    'password': 'n5X5dB6xPLJj06qr4C',
    'puerto': 22
}

def imprimir_banner():
    """Banner del script de despliegue"""
    print("=" * 60)
    print("🚀 DESPLIEGUE SMC-LIT BOT A VPS")
    print("=" * 60)
    print(f"🖥️  Servidor: {VPS_INFO['ip']}")
    print(f"👤 Usuario: {VPS_INFO['usuario']}")
    print(f"🔐 Puerto: {VPS_INFO['puerto']}")
    print("=" * 60)

def verificar_dependencias_locales():
    """Verifica dependencias necesarias para el despliegue"""
    print("🔍 Verificando dependencias locales...")
    
    # Verificar si scp/ssh están disponibles
    try:
        subprocess.run(['ssh', '-V'], capture_output=True, check=True)
        print("✅ SSH disponible")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ SSH no disponible. Instala OpenSSH")
        return False
    
    try:
        subprocess.run(['scp', '-h'], capture_output=True)
        print("✅ SCP disponible")
    except FileNotFoundError:
        print("❌ SCP no disponible")
        return False
    
    return True

def crear_archivo_transferencia():
    """Crea lista de archivos a transferir"""
    archivos_esenciales = [
        'main.py',
        'start_bot.py',
        'config_seguro.py',
        'iniciar_bot_seguro.py',
        'configurar_credenciales.py',
        'requirements.txt',
        'src/',
        'advanced_auto_optimizer.py',
        'bayesian_optimizer.py',
        'master_optimization_system.py',
        'implement_optimized_strategy.py'
    ]
    
    archivos_existentes = []
    for archivo in archivos_esenciales:
        if os.path.exists(archivo):
            archivos_existentes.append(archivo)
        else:
            print(f"⚠️  Archivo no encontrado: {archivo}")
    
    return archivos_existentes

def crear_script_instalacion_vps():
    """Crea script de instalación para el VPS"""
    script_contenido = """#!/bin/bash
# Script de instalación automática para VPS
# SMC-LIT Trading Bot

echo "🚀 INICIANDO INSTALACIÓN EN VPS..."
echo "=================================="

# Actualizar sistema
echo "📦 Actualizando sistema..."
apt update && apt upgrade -y

# Instalar Python 3.9+
echo "🐍 Instalando Python..."
apt install -y python3 python3-pip python3-venv python3-dev

# Instalar dependencias del sistema
echo "📚 Instalando dependencias del sistema..."
apt install -y build-essential curl wget git htop screen

# Crear directorio del bot
echo "📁 Configurando directorio..."
cd /home
mkdir -p smc-lit-bot
cd smc-lit-bot

# Crear entorno virtual
echo "🔧 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias Python
echo "📦 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

# Configurar permisos
chmod +x *.py

# Crear servicio systemd
cat > /etc/systemd/system/smc-lit-bot.service << EOF
[Unit]
Description=SMC-LIT Trading Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/smc-lit-bot
Environment=PATH=/home/smc-lit-bot/venv/bin
ExecStart=/home/smc-lit-bot/venv/bin/python iniciar_bot_seguro.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Configurar firewall
echo "🔒 Configurando firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Configurar timezone
timedatectl set-timezone UTC

echo "✅ INSTALACIÓN COMPLETADA"
echo "========================="
echo "📁 Bot instalado en: /home/smc-lit-bot"
echo "🔧 Para configurar credenciales: python3 configurar_credenciales.py"
echo "🚀 Para iniciar: python3 iniciar_bot_seguro.py"
echo "📊 Para ver logs: tail -f *.log"
echo "🔄 Para servicio: systemctl start smc-lit-bot"
"""
    
    with open('install_vps.sh', 'w') as f:
        f.write(script_contenido)
    
    os.chmod('install_vps.sh', 0o755)
    print("✅ Script de instalación VPS creado")

def crear_script_inicio_vps():
    """Crea script de inicio específico para VPS"""
    script_contenido = """#!/bin/bash
# Script de inicio para VPS
cd /home/smc-lit-bot
source venv/bin/activate

echo "🤖 Iniciando SMC-LIT Bot en VPS..."
echo "Presiona Ctrl+C para detener"

python3 iniciar_bot_seguro.py
"""
    
    with open('start_vps.sh', 'w') as f:
        f.write(script_contenido)
    
    os.chmod('start_vps.sh', 0o755)
    print("✅ Script de inicio VPS creado")

def transferir_archivos():
    """Transfiere archivos al VPS"""
    print(f"\n📤 Transfiriendo archivos a {VPS_INFO['ip']}...")
    
    archivos = crear_archivo_transferencia()
    crear_script_instalacion_vps()
    crear_script_inicio_vps()
    
    # Agregar scripts creados
    archivos.extend(['install_vps.sh', 'start_vps.sh'])
    
    # Crear directorio temporal
    subprocess.run(['mkdir', '-p', 'temp_deploy'])
    
    # Copiar archivos a directorio temporal
    for archivo in archivos:
        if os.path.isfile(archivo):
            subprocess.run(['cp', archivo, 'temp_deploy/'])
        elif os.path.isdir(archivo):
            subprocess.run(['cp', '-r', archivo, 'temp_deploy/'])
    
    try:
        # Transferir usando scp
        cmd = [
            'scp', '-r', '-o', 'StrictHostKeyChecking=no',
            'temp_deploy/*',
            f"{VPS_INFO['usuario']}@{VPS_INFO['ip']}:/tmp/"
        ]
        
        print(f"🔄 Ejecutando: {' '.join(cmd)}")
        
        # Usar sshpass si está disponible, sino pedir password manualmente
        try:
            # Intentar con sshpass
            cmd_with_pass = ['sshpass', f"-p{VPS_INFO['password']}"] + cmd
            result = subprocess.run(cmd_with_pass, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, cmd_with_pass)
                
        except FileNotFoundError:
            # sshpass no disponible, usar método manual
            print("⚠️  sshpass no disponible. Ingresa la contraseña manualmente cuando se solicite:")
            print(f"Contraseña: {VPS_INFO['password']}")
            result = subprocess.run(cmd)
        
        print("✅ Archivos transferidos exitosamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error transfiriendo archivos: {e}")
        return False
    finally:
        # Limpiar directorio temporal
        subprocess.run(['rm', '-rf', 'temp_deploy'])

def ejecutar_instalacion_remota():
    """Ejecuta la instalación en el VPS remoto"""
    print(f"\n🔧 Ejecutando instalación en {VPS_INFO['ip']}...")
    
    comandos = [
        'cd /tmp',
        'mkdir -p /home/smc-lit-bot',
        'cp -r * /home/smc-lit-bot/',
        'cd /home/smc-lit-bot',
        'chmod +x *.sh',
        './install_vps.sh'
    ]
    
    comando_completo = ' && '.join(comandos)
    
    try:
        cmd = [
            'ssh', '-o', 'StrictHostKeyChecking=no',
            f"{VPS_INFO['usuario']}@{VPS_INFO['ip']}",
            comando_completo
        ]
        
        # Intentar con sshpass
        try:
            cmd_with_pass = ['sshpass', f"-p{VPS_INFO['password']}"] + cmd
            result = subprocess.run(cmd_with_pass, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Instalación completada exitosamente")
                print("\n📋 SALIDA DE INSTALACIÓN:")
                print(result.stdout)
                return True
            else:
                print(f"❌ Error en instalación: {result.stderr}")
                return False
                
        except FileNotFoundError:
            print("⚠️  sshpass no disponible. Ejecuta manualmente:")
            print(f"ssh {VPS_INFO['usuario']}@{VPS_INFO['ip']}")
            print(f"Contraseña: {VPS_INFO['password']}")
            print(f"Luego ejecuta: {comando_completo}")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando instalación remota: {e}")
        return False

def mostrar_instrucciones_finales():
    """Muestra instrucciones finales para el usuario"""
    print("""
🎉 ¡DESPLIEGUE COMPLETADO!

🖥️  CONEXIÓN AL VPS:
==================
ssh root@107.174.133.202
Contraseña: n5X5dB6xPLJj06qr4C

📁 DIRECTORIO DEL BOT:
===================
cd /home/smc-lit-bot

🔧 CONFIGURAR CREDENCIALES DEMO:
==============================
python3 configurar_credenciales.py

🚀 INICIAR BOT:
=============
python3 iniciar_bot_seguro.py

📊 MONITOREAR BOT:
================
tail -f *.log

🔄 SERVICIO AUTOMÁTICO:
=====================
systemctl enable smc-lit-bot
systemctl start smc-lit-bot
systemctl status smc-lit-bot

⚠️  RECORDATORIOS:
• Solo usar credenciales DEMO
• Monitorear logs regularmente
• El bot se reinicia automáticamente
• Máximo riesgo: 0.5% por trade

¡Tu bot está listo para trading 24/7! 🤖
""")

def main():
    """Función principal"""
    try:
        imprimir_banner()
        
        # Confirmación de usuario
        print("⚠️  Este script desplegará el bot al VPS usando las credenciales proporcionadas")
        confirmar = input("¿Continuar con el despliegue? (si/no): ").lower().strip()
        
        if confirmar not in ['si', 'sí', 's', 'yes', 'y']:
            print("👋 Despliegue cancelado")
            return
        
        # Verificaciones
        if not verificar_dependencias_locales():
            print("❌ Dependencias faltantes para despliegue")
            return
        
        # Transferir archivos
        if not transferir_archivos():
            print("❌ Error transfiriendo archivos")
            return
        
        # Ejecutar instalación
        if not ejecutar_instalacion_remota():
            print("⚠️  Instalación remota falló, pero archivos están transferidos")
        
        # Instrucciones finales
        mostrar_instrucciones_finales()
        
    except KeyboardInterrupt:
        print("\n\n👋 Despliegue interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error en despliegue: {e}")

if __name__ == "__main__":
    main() 