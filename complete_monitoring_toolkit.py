#!/usr/bin/env python3
"""
TOOLKIT COMPLETO DE MONITOREO PROFESIONAL - BOT SMC-LIT
=======================================================
Herramienta todo-en-uno para monitoreo, versionado y evaluaciones del bot.
Sistema seguro de credenciales implementado.
"""

import os
import sys
import json
import subprocess
import time
import threading
from datetime import datetime
import logging

# Importar sistemas seguros
try:
    from professional_monitoring_system import ProfessionalMonitoringSystem
    from version_management_system import VersionManagementSystem
    from secure_config_manager import SecureConfigManager, VPSCredentials
except ImportError:
    print("⚠️  Módulos no encontrados. Ejecutando desde archivos locales...")

class CompleteMonitoringToolkit:
    def __init__(self):
        # Usar gestor seguro de configuración
        self.config_manager = SecureConfigManager()
        self.vps_credentials = self._get_secure_credentials()
        
        self.monitoring_system = None
        self.version_manager = None
        self.setup_logging()
        
    def _get_secure_credentials(self) -> dict:
        """Obtener credenciales de forma segura"""
        vps_creds = self.config_manager.get_vps_credentials()
        
        if not vps_creds:
            print("⚠️  CREDENCIALES NO CONFIGURADAS")
            print("   Ejecuta: python3 secure_config_manager.py")
            print("   Para configurar credenciales seguras.")
            # Usar credenciales temporales de fallback (solo para demo)
            return {
                'host': 'PLEASE_CONFIGURE',
                'user': 'PLEASE_CONFIGURE', 
                'password': 'PLEASE_CONFIGURE',
                'port': 22
            }
        
        return {
            'host': vps_creds.host,
            'user': vps_creds.user,
            'password': vps_creds.password,
            'port': vps_creds.port
        }
        
    def setup_logging(self):
        """Configurar logging centralizado"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('complete_monitoring.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('CompleteToolkit')
        
        # Log seguro (sin credenciales)
        self.logger.info(f"Toolkit initialized for VPS: {self.vps_credentials['host']}")
    
    def install_dependencies(self):
        """Instalar dependencias necesarias"""
        print("📦 Instalando dependencias del sistema de monitoreo...")
        try:
            subprocess.run([
                sys.executable, '-m', 'pip', 'install', 
                'flask', 'plotly', 'pandas', 'requests', 'cryptography'
            ], check=True, capture_output=True)
            print("✅ Dependencias instaladas correctamente")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    
    def start_monitoring_dashboard(self):
        """Iniciar dashboard de monitoreo en segundo plano"""
        try:
            if not self.monitoring_system:
                from professional_monitoring_system import ProfessionalMonitoringSystem
                self.monitoring_system = ProfessionalMonitoringSystem(self.vps_credentials)
            
            print("🚀 Iniciando dashboard de monitoreo...")
            print("🌐 Accede a: http://localhost:5000")
            
            # Ejecutar en thread separado
            dashboard_thread = threading.Thread(
                target=self.monitoring_system.run_dashboard,
                daemon=True
            )
            dashboard_thread.start()
            
            return True
            
        except Exception as e:
            print(f"❌ Error iniciando dashboard: {e}")
            return False
    
    def quick_bot_status(self):
        """Estado rápido del bot"""
        try:
            status_command = f"""
            sshpass -p '{self.vps_credentials['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps_credentials['port']} {self.vps_credentials['user']}@{self.vps_credentials['host']} '
                echo "=== BOT STATUS ===" &&
                ps aux | grep main_unlimited | grep -v grep | wc -l &&
                echo "=== LAST ACTIVITY ===" &&
                tail -3 /home/smc-lit-bot/*.log 2>/dev/null | grep "Análisis" | tail -1 &&
                echo "=== SYSTEM LOAD ===" &&
                uptime | awk "{{print \\$3, \\$4, \\$5}}"
            '
            """
            
            result = subprocess.run(status_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                bot_running = int(lines[1]) > 0 if len(lines) > 1 else False
                
                print("\n📊 ESTADO RÁPIDO DEL BOT")
                print("=" * 30)
                print(f"🤖 Bot Status: {'🟢 RUNNING' if bot_running else '🔴 STOPPED'}")
                print(f"📈 Última actividad: {lines[3] if len(lines) > 3 else 'No disponible'}")
                print(f"⚡ Carga del sistema: {lines[5] if len(lines) > 5 else 'No disponible'}")
                print("=" * 30)
                
                return bot_running
            else:
                print(f"❌ Error obteniendo estado: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def get_metrics_for_evaluation(self):
        """Obtener métricas completas para evaluación con asistente"""
        try:
            # Comando simplificado que sabemos que funciona
            metrics_command = [
                'sshpass', '-p', self.vps_credentials['password'],
                'ssh', '-o', 'StrictHostKeyChecking=no',
                '-p', str(self.vps_credentials['port']),
                f"{self.vps_credentials['user']}@{self.vps_credentials['host']}",
                'echo "=== BOT STATUS ===" && ps aux | grep main_unlimited | grep -v grep && echo "=== SYSTEM METRICS ===" && free -h && echo "=== CPU USAGE ===" && top -bn1 | grep "Cpu(s)" && echo "=== UPTIME ===" && uptime && echo "=== TIMESTAMP ===" && date'
            ]
            
            result = subprocess.run(metrics_command, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'vps_ip': self.vps_credentials['host'],
                    'raw_metrics': result.stdout,
                    'collection_success': True
                }
            else:
                return {
                    'timestamp': datetime.now().isoformat(),
                    'error': result.stderr,
                    'collection_success': False
                }
                
        except Exception as e:
            return {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'collection_success': False
            }
    
    def create_evaluation_report(self, request_description: str = "Evaluación general"):
        """Crear reporte completo para evaluación"""
        print(f"📊 Generando reporte de evaluación: {request_description}")
        
        # Obtener métricas completas
        metrics = self.get_metrics_for_evaluation()
        
        # Análisis básico
        analysis = {
            'request': request_description,
            'vps_info': {
                'ip': self.vps_credentials['host'],
                'status': 'operational' if metrics['collection_success'] else 'error'
            },
            'metrics_collected': metrics,
            'recommendations': [],
            'timestamp': datetime.now().isoformat()
        }
        
        # Guardar reporte
        report_file = f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print(f"📋 Reporte guardado: {report_file}")
        print("\n🤖 DATOS PARA EVALUACIÓN CON ASISTENTE:")
        print("=" * 50)
        print(f"📊 Estado de recolección: {'✅ Exitoso' if metrics['collection_success'] else '❌ Error'}")
        print(f"⏰ Timestamp: {analysis['timestamp']}")
        print(f"🌐 VPS IP: {self.vps_credentials['host']}")
        print(f"📝 Solicitud: {request_description}")
        print("=" * 50)
        
        return analysis
    
    def update_bot_version(self, version: str = None, description: str = None):
        """Actualizar versión del bot"""
        try:
            if not self.version_manager:
                from version_management_system import VersionManagementSystem
                self.version_manager = VersionManagementSystem(self.vps_credentials)
            
            if not version:
                version = input("Número de versión (ej: 1.1.0): ")
            if not description:
                description = input("Descripción de cambios: ")
            
            changes = input("Lista de cambios (separados por coma): ").split(',')
            changes = [change.strip() for change in changes if change.strip()]
            
            print(f"🚀 Creando release v{version}...")
            package = self.version_manager.create_release_package(version, description, changes)
            
            print(f"📦 Desplegando al VPS...")
            result = self.version_manager.deploy_to_vps(package)
            
            if result.success:
                print("✅ Actualización exitosa!")
                print(f"📋 Versión: {result.version}")
                print(f"💾 Backup creado: {'Sí' if result.backup_created else 'No'}")
                return True
            else:
                print("❌ Actualización falló:")
                for error in result.errors:
                    print(f"   - {error}")
                
                if result.rollback_available:
                    rollback = input("¿Hacer rollback automático? (y/n): ")
                    if rollback.lower() == 'y':
                        if self.version_manager.rollback_to_backup():
                            print("✅ Rollback exitoso")
                        else:
                            print("❌ Rollback falló")
                return False
                
        except Exception as e:
            print(f"❌ Error en actualización: {e}")
            return False
    
    def interactive_menu(self):
        """Menú interactivo principal"""
        while True:
            print("\n🤖 TOOLKIT COMPLETO - BOT SMC-LIT")
            print("=" * 40)
            print("1. 📊 Estado rápido del bot")
            print("2. 🌐 Iniciar dashboard web")
            print("3. 📋 Generar reporte de evaluación")
            print("4. 🔄 Actualizar versión del bot")
            print("5. 📈 Métricas para evaluación")
            print("6. 🔧 Reiniciar bot")
            print("7. 💾 Hacer backup")
            print("8. 🚪 Salir")
            
            choice = input("\nSelecciona una opción (1-8): ").strip()
            
            if choice == "1":
                self.quick_bot_status()
            
            elif choice == "2":
                if self.install_dependencies():
                    self.start_monitoring_dashboard()
                    input("Presiona Enter para continuar...")
            
            elif choice == "3":
                request = input("Describe qué quieres evaluar: ")
                self.create_evaluation_report(request or "Evaluación general")
            
            elif choice == "4":
                self.update_bot_version()
            
            elif choice == "5":
                metrics = self.get_metrics_for_evaluation()
                print("\n📊 MÉTRICAS PARA COPIAR AL ASISTENTE:")
                print("=" * 45)
                print(json.dumps(metrics, indent=2))
            
            elif choice == "6":
                print("🔄 Reiniciando bot...")
                restart_cmd = f"""
                sshpass -p '{self.vps_credentials['password']}' ssh -o StrictHostKeyChecking=no {self.vps_credentials['user']}@{self.vps_credentials['host']} '
                    pkill -f main_unlimited.py &&
                    cd /home/smc-lit-bot &&
                    source venv/bin/activate &&
                    screen -dmS smc-bot python3 main_unlimited.py
                '
                """
                result = subprocess.run(restart_cmd, shell=True, capture_output=True)
                print("✅ Bot reiniciado" if result.returncode == 0 else "❌ Error reiniciando")
            
            elif choice == "7":
                print("💾 Creando backup...")
                if not self.version_manager:
                    from version_management_system import VersionManagementSystem
                    self.version_manager = VersionManagementSystem(self.vps_credentials)
                
                if self.version_manager.backup_current_version():
                    print("✅ Backup creado exitosamente")
                else:
                    print("❌ Error creando backup")
            
            elif choice == "8":
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción no válida")

def main():
    """Función principal"""
    toolkit = CompleteMonitoringToolkit()
    
    print("🚀 TOOLKIT COMPLETO DE MONITOREO - BOT SMC-LIT")
    print("=" * 55)
    print("🌐 VPS: 107.174.133.202")
    print("🤖 Bot: main_unlimited.py")
    print("💰 Demo: $1,000 USD - Sin limitaciones")
    print("=" * 55)
    
    # Verificar estado inicial
    if toolkit.quick_bot_status():
        print("✅ Bot está funcionando correctamente")
    else:
        print("⚠️  Bot podría necesitar atención")
    
    # Iniciar menú interactivo
    toolkit.interactive_menu()

if __name__ == "__main__":
    main() 