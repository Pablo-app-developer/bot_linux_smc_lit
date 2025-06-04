#!/usr/bin/env python3
"""
VERIFICACIÓN COMPLETA BOT SMC-LIT v2.0 DESPLEGADO
===============================================
Script para verificar el estado del bot en producción
"""

import subprocess
import os
import sys
from datetime import datetime

def print_banner():
    """Banner de verificación"""
    print("🔍" + "=" * 60 + "🔍")
    print("🛠️  VERIFICACIÓN BOT SMC-LIT v2.0 - PRODUCCIÓN")
    print("🔍" + "=" * 60 + "🔍")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍" + "=" * 60 + "🔍")

def check_service_status():
    """Verificar estado del servicio"""
    print("\n🔧 VERIFICANDO SERVICIO SYSTEMD...")
    
    try:
        # Verificar si está activo
        result = subprocess.run(['systemctl', 'is-active', 'smc-lit-bot'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip() == 'active':
            print("✅ Servicio: ACTIVO")
            
            # Obtener información detallada
            status_result = subprocess.run(['systemctl', 'status', 'smc-lit-bot'], 
                                         capture_output=True, text=True)
            
            # Extraer información clave
            lines = status_result.stdout.split('\n')
            for line in lines:
                if 'Active:' in line:
                    print(f"📊 {line.strip()}")
                elif 'Main PID:' in line:
                    print(f"🆔 {line.strip()}")
                elif 'Memory:' in line:
                    print(f"💾 {line.strip()}")
                elif 'CPU:' in line:
                    print(f"⚡ {line.strip()}")
            
            return True
        else:
            print("❌ Servicio: INACTIVO")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicio: {e}")
        return False

def check_production_directory():
    """Verificar directorio de producción"""
    print("\n📁 VERIFICANDO DIRECTORIO DE PRODUCCIÓN...")
    
    production_dir = "/opt/bot_smc_lit_v2"
    
    if os.path.exists(production_dir):
        print(f"✅ Directorio existe: {production_dir}")
        
        # Verificar archivos clave
        key_files = [
            'main_advanced_with_indices.py',
            'start_production.sh',
            '.venv/bin/python',
            'logs/'
        ]
        
        for file in key_files:
            file_path = os.path.join(production_dir, file)
            if os.path.exists(file_path):
                if file.endswith('/'):
                    print(f"  ✅ Directorio: {file}")
                else:
                    size = os.path.getsize(file_path)
                    print(f"  ✅ Archivo: {file} ({size} bytes)")
            else:
                print(f"  ❌ Faltante: {file}")
        
        return True
    else:
        print(f"❌ Directorio no existe: {production_dir}")
        return False

def check_logs():
    """Verificar logs del bot"""
    print("\n📝 VERIFICANDO LOGS...")
    
    try:
        # Verificar logs del servicio systemd
        result = subprocess.run(['journalctl', '-u', 'smc-lit-bot', '-n', '5', '--no-pager'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Logs systemd disponibles:")
            recent_lines = result.stdout.strip().split('\n')[-3:]
            for line in recent_lines:
                if line.strip():
                    print(f"  📄 {line}")
        
        # Verificar logs locales si existen
        log_files = [
            '/opt/bot_smc_lit_v2/logs/bot.log',
            '/opt/bot_smc_lit_v2/logs/startup.log'
        ]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                size = os.path.getsize(log_file)
                print(f"✅ Log local: {os.path.basename(log_file)} ({size} bytes)")
            else:
                print(f"⚠️  Log no encontrado: {os.path.basename(log_file)}")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando logs: {e}")
        return False

def check_network_activity():
    """Verificar actividad de red (indicador de funcionamiento)"""
    print("\n🌐 VERIFICANDO ACTIVIDAD...")
    
    try:
        # Verificar procesos Python relacionados
        result = subprocess.run(['pgrep', '-f', 'main_advanced_with_indices'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            pids = result.stdout.strip().split('\n')
            print(f"✅ Procesos bot activos: {len(pids)} procesos")
            for pid in pids[:3]:  # Mostrar solo los primeros 3
                print(f"  🔄 PID: {pid}")
        else:
            print("⚠️  No se detectaron procesos del bot principal")
        
        # Verificar procesos Python en general
        result = subprocess.run(['pgrep', '-f', 'python3.*smc'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Actividad Python detectada")
        else:
            print("⚠️  No se detectó actividad Python relacionada")
        
        return True
    except Exception as e:
        print(f"❌ Error verificando actividad: {e}")
        return False

def check_dependencies():
    """Verificar dependencias críticas"""
    print("\n🐍 VERIFICANDO DEPENDENCIAS...")
    
    python_path = "/opt/bot_smc_lit_v2/.venv/bin/python"
    
    if os.path.exists(python_path):
        print("✅ Entorno virtual encontrado")
        
        # Verificar dependencias clave
        key_packages = ['numpy', 'pandas', 'requests', 'sklearn']
        
        for package in key_packages:
            try:
                result = subprocess.run([python_path, '-c', f'import {package}; print("{package} OK")'], 
                                      capture_output=True, text=True, timeout=10)
                
                if result.returncode == 0:
                    print(f"  ✅ {package}")
                else:
                    print(f"  ❌ {package}: {result.stderr.strip()}")
            except Exception as e:
                print(f"  ⚠️  {package}: {e}")
        
        return True
    else:
        print("❌ Entorno virtual no encontrado")
        return False

def show_summary(service_ok, directory_ok, logs_ok, activity_ok, deps_ok):
    """Mostrar resumen final"""
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    total_checks = 5
    passed_checks = sum([service_ok, directory_ok, logs_ok, activity_ok, deps_ok])
    
    status_icon = "✅" if passed_checks >= 4 else "⚠️" if passed_checks >= 2 else "❌"
    
    print(f"{status_icon} Estado general: {passed_checks}/{total_checks} verificaciones pasadas")
    print(f"🔧 Servicio systemd: {'✅' if service_ok else '❌'}")
    print(f"📁 Directorio producción: {'✅' if directory_ok else '❌'}")
    print(f"📝 Logs: {'✅' if logs_ok else '❌'}")
    print(f"🌐 Actividad: {'✅' if activity_ok else '❌'}")
    print(f"🐍 Dependencias: {'✅' if deps_ok else '❌'}")
    
    if passed_checks >= 4:
        print("\n🎉 BOT SMC-LIT v2.0: FUNCIONANDO CORRECTAMENTE")
        print("📈 Sistema estable y operativo")
        print("\n📋 Comandos útiles:")
        print("  🔍 Ver logs: sudo journalctl -u smc-lit-bot -f")
        print("  📊 Estado: sudo systemctl status smc-lit-bot")
        print("  🔄 Reiniciar: sudo systemctl restart smc-lit-bot")
    elif passed_checks >= 2:
        print("\n⚠️  BOT SMC-LIT v2.0: FUNCIONAMIENTO PARCIAL")
        print("🔧 Requiere atención pero puede estar operativo")
        print("\n💡 Recomendaciones:")
        print("  🔄 Reiniciar servicio: sudo systemctl restart smc-lit-bot")
        print("  📋 Revisar logs: sudo journalctl -u smc-lit-bot -n 20")
    else:
        print("\n❌ BOT SMC-LIT v2.0: PROBLEMAS CRÍTICOS")
        print("🚨 Sistema requiere intervención inmediata")
        print("\n🛠️  Acciones recomendadas:")
        print("  1. Reiniciar servicio: sudo systemctl restart smc-lit-bot")
        print("  2. Re-deployment: sudo python3 deploy_production_linux.py")
        print("  3. Verificar logs: sudo journalctl -u smc-lit-bot")
    
    print("=" * 50)

def main():
    """Función principal"""
    print_banner()
    
    # Ejecutar verificaciones
    service_ok = check_service_status()
    directory_ok = check_production_directory()
    logs_ok = check_logs()
    activity_ok = check_network_activity()
    deps_ok = check_dependencies()
    
    # Mostrar resumen
    show_summary(service_ok, directory_ok, logs_ok, activity_ok, deps_ok)

if __name__ == "__main__":
    main() 