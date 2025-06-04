#!/usr/bin/env python3

import threading
import time
import requests
from complete_monitoring_toolkit import CompleteMonitoringToolkit

def test_dashboard():
    print("🌐 PROBANDO DASHBOARD WEB:")
    print("=" * 40)
    
    toolkit = CompleteMonitoringToolkit()
    
    # Instalar dependencias
    if not toolkit.install_dependencies():
        print("❌ Error instalando dependencias")
        return False
    
    # Iniciar dashboard en segundo plano
    print("🚀 Iniciando dashboard...")
    if toolkit.start_monitoring_dashboard():
        print("✅ Dashboard iniciado correctamente")
        
        # Esperar a que inicie
        time.sleep(3)
        
        # Probar conexión al dashboard
        try:
            response = requests.get('http://localhost:5000', timeout=10)
            if response.status_code == 200:
                print("✅ Dashboard respondiendo correctamente")
                print("🌐 Accesible en: http://localhost:5000")
                return True
            else:
                print(f"❌ Dashboard responde con error: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error conectando al dashboard: {e}")
            return False
    else:
        print("❌ Error iniciando dashboard")
        return False

if __name__ == "__main__":
    success = test_dashboard()
    if success:
        print("\n🎯 DASHBOARD FUNCIONANDO CORRECTAMENTE!")
        print("Presiona Ctrl+C para salir...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Dashboard detenido")
    else:
        print("\n❌ DASHBOARD CON PROBLEMAS") 