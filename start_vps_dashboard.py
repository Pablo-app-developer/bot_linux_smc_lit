#!/usr/bin/env python3
# Iniciador del Dashboard VPS - SMC-LIT
# =====================================

import os
import sys
import threading
import time
import subprocess

def print_header():
    """Mostrar header del sistema"""
    print("\n" + "="*60)
    print("🚀 DASHBOARD VPS SMC-LIT TRADING ANALYTICS")
    print("="*60)
    print("📍 VPS: 107.174.133.202")
    print("🌐 Dashboard: http://localhost:5002")
    print("📊 Análisis en tiempo real desde tu VPS")
    print("="*60)

def start_vps_sync():
    """Iniciar sincronización VPS en segundo plano"""
    print("🔄 Iniciando sincronización con VPS...")
    
    try:
        from vps_data_sync import VPSDataSync
        
        # Configuración VPS
        sync = VPSDataSync(
            vps_ip='107.174.133.202',
            vps_user='root',
            vps_password='n5X5dB6xPLJj06qr4C',
            vps_bot_dir='/home/smc-lit-bot'
        )
        
        # Sincronización inicial
        print("⚡ Realizando sincronización inicial...")
        if sync.full_sync():
            print("✅ Sincronización inicial completada")
            
            # Programar auto-sync cada 30 minutos
            sync.schedule_auto_sync(30)
            print("⏰ Auto-sincronización programada cada 30 minutos")
            
        else:
            print("⚠️  Error en sincronización inicial - continuando sin datos VPS")
            
    except Exception as e:
        print(f"❌ Error configurando sincronización: {e}")
        print("💡 Podrás sincronizar manualmente desde el dashboard")

def start_dashboard():
    """Iniciar dashboard web"""
    print("🌐 Iniciando dashboard web VPS...")
    
    try:
        # Cambiar al directorio correcto
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Importar y ejecutar dashboard
        from web_dashboard_vps import app
        
        print("✅ Dashboard iniciado exitosamente")
        print("📊 Accede a: http://localhost:5002")
        print("💡 Presiona Ctrl+C para detener")
        
        app.run(host='0.0.0.0', port=5002, debug=False)
        
    except Exception as e:
        print(f"❌ Error iniciando dashboard: {e}")
        return False
        
    return True

def main():
    """Función principal"""
    print_header()
    
    # Verificar dependencias
    try:
        import paramiko
        import flask
        print("✅ Dependencias verificadas")
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: pip install paramiko flask")
        sys.exit(1)
    
    # Crear directorio templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("📁 Directorio templates creado")
    
    print("\n🚀 INICIANDO SISTEMA VPS...")
    
    # Iniciar sincronización en segundo plano
    sync_thread = threading.Thread(target=start_vps_sync, daemon=True)
    sync_thread.start()
    
    # Esperar un momento para la sincronización inicial
    time.sleep(3)
    
    # Iniciar dashboard
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\n\n🛑 Cerrando dashboard VPS...")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 