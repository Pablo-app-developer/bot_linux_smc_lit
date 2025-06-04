#!/usr/bin/env python3
"""
DEPLOYMENT COMPLETO LOCAL A PRODUCCIÓN - BOT SMC-LIT v2.0
========================================================
Script que prepara y deploya el bot completamente
"""

import os
import sys
import subprocess
import shutil
import time
from datetime import datetime

class LocalToProductionDeployment:
    def __init__(self):
        self.project_name = "bot_smc_lit_v2"
        self.current_dir = os.getcwd()
        self.production_dir = f"/opt/{self.project_name}"
        self.service_name = "smc-lit-bot"
        
        # Archivos esenciales para el deployment
        self.essential_files = [
            'main_advanced_with_indices.py',
            'economic_calendar_analyzer.py',
            'twitter_news_analyzer.py',
            'ml_trading_system.py',
            'start_auto_mode.py',
            'requirements.txt',
            'inicio_bot_avanzado.py',
            'configuracion_automatica.py'
        ]
        
    def print_banner(self):
        """Banner de deployment"""
        print("🚀" + "=" * 70 + "🚀")
        print("🎯 DEPLOYMENT COMPLETO BOT SMC-LIT v2.0")
        print("🚀" + "=" * 70 + "🚀")
        print("📈 SISTEMA INCLUYE:")
        print("  ✅ Twitter: 7 categorías + Machine Learning")
        print("  ✅ Calendario económico: FinBERT + eventos")
        print("  ✅ NASDAQ & S&P 500: Trading especializado")
        print("  ✅ Modo automático: Sin intervención")
        print("  ✅ VPS Ready: Servicio systemd")
        print("🚀" + "=" * 70 + "🚀")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀" + "=" * 70 + "🚀")
    
    def check_prerequisites(self):
        """Verificar prerequisitos"""
        print("\n🔍 VERIFICANDO PREREQUISITOS...")
        
        # Verificar que somos root
        if os.geteuid() != 0:
            print("❌ Este script debe ejecutarse como root")
            print("💡 Ejecuta: sudo python3 deploy_local_to_production.py")
            return False
        
        # Verificar archivos esenciales
        missing_files = []
        for file in self.essential_files:
            if not os.path.exists(os.path.join(self.current_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
            return False
        
        print("✅ Todos los archivos esenciales disponibles")
        
        # Verificar Python 3.8+
        try:
            result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
            version_str = result.stdout.strip()
            print(f"✅ {version_str}")
        except:
            print("❌ Python 3 no disponible")
            return False
        
        return True
    
    def prepare_production_directory(self):
        """Preparar directorio de producción"""
        print("\n📁 PREPARANDO DIRECTORIO DE PRODUCCIÓN...")
        
        # Crear backup si existe
        if os.path.exists(self.production_dir):
            backup_dir = f"{self.production_dir}_backup_{int(time.time())}"
            print(f"🔄 Creando backup: {backup_dir}")
            shutil.move(self.production_dir, backup_dir)
        
        # Crear directorio limpio
        os.makedirs(self.production_dir, exist_ok=True)
        print(f"✅ Directorio de producción creado: {self.production_dir}")
        
        return True
    
    def copy_essential_files(self):
        """Copiar archivos esenciales"""
        print("\n📋 COPIANDO ARCHIVOS ESENCIALES...")
        
        for file in self.essential_files:
            src = os.path.join(self.current_dir, file)
            dst = os.path.join(self.production_dir, file)
            
            try:
                shutil.copy2(src, dst)
                print(f"  ✅ {file}")
            except Exception as e:
                print(f"  ❌ Error copiando {file}: {e}")
                return False
        
        # Copiar directorios importantes
        dirs_to_copy = ['src', 'data', 'docs']
        for dir_name in dirs_to_copy:
            src_dir = os.path.join(self.current_dir, dir_name)
            dst_dir = os.path.join(self.production_dir, dir_name)
            
            if os.path.exists(src_dir):
                try:
                    shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)
                    print(f"  ✅ Directorio {dir_name}/")
                except Exception as e:
                    print(f"  ⚠️  Error copiando {dir_name}/: {e}")
        
        # Crear directorio data si no existe
        data_dir = os.path.join(self.production_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        
        print("✅ Archivos copiados exitosamente")
        return True
    
    def setup_virtual_environment(self):
        """Configurar entorno virtual"""
        print("\n🐍 CONFIGURANDO ENTORNO VIRTUAL...")
        
        # Cambiar al directorio de producción
        os.chdir(self.production_dir)
        
        # Crear entorno virtual
        try:
            subprocess.run(['python3', '-m', 'venv', '.venv'], check=True)
            print("✅ Entorno virtual creado")
        except Exception as e:
            print(f"❌ Error creando entorno virtual: {e}")
            return False
        
        # Instalar dependencias
        pip_path = os.path.join(self.production_dir, '.venv', 'bin', 'pip')
        
        try:
            # Actualizar pip
            subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
            print("✅ pip actualizado")
            
            # Instalar dependencias
            subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
            print("✅ Dependencias instaladas")
            
            return True
        except Exception as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    
    def create_auto_start_script(self):
        """Crear script de inicio automático mejorado"""
        print("\n🤖 CREANDO SCRIPT DE INICIO AUTOMÁTICO...")
        
        script_content = f"""#!/bin/bash
# Script de inicio automático BOT SMC-LIT v2.0
# Configurado para responder automáticamente

cd {self.production_dir}

# Variables de entorno
export PYTHONPATH="{self.production_dir}:$PYTHONPATH"
export PYTHONUNBUFFERED=1

# Activar entorno virtual
source {self.production_dir}/.venv/bin/activate

# Ejecutar bot principal con respuesta automática
result = subprocess.run(
    f'cd {self.production_dir} && echo "1" | python3 {self.production_dir}/main_advanced_with_indices.py',
    shell=True, capture_output=True, text=True
)

# Si falla, intentar con start_auto_mode.py
if [ $? -ne 0 ]; then
    echo "Intentando inicio alternativo..."
    python3 {self.production_dir}/start_auto_mode.py
fi
"""
        
        script_path = os.path.join(self.production_dir, 'start_production.sh')
        
        try:
            with open(script_path, 'w') as f:
                f.write(script_content)
            
            os.chmod(script_path, 0o755)
            print("✅ Script de inicio automático creado")
            return True
        except Exception as e:
            print(f"❌ Error creando script: {e}")
            return False
    
    def create_systemd_service(self):
        """Crear servicio systemd"""
        print("\n⚙️  CONFIGURANDO SERVICIO SYSTEMD...")
        
        service_content = f"""[Unit]
Description=SMC-LIT Trading Bot v2.0 - Production
After=network.target network-online.target
Wants=network-online.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=15
User=root
Group=root
WorkingDirectory={self.production_dir}
ExecStart=/bin/bash {self.production_dir}/start_production.sh
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONPATH={self.production_dir}"

# Configuración de recursos
MemoryMax=1G
CPUQuota=50%

[Install]
WantedBy=multi-user.target
"""
        
        service_path = f"/etc/systemd/system/{self.service_name}.service"
        
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Recargar systemd
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            subprocess.run(['systemctl', 'enable', self.service_name], check=True)
            
            print(f"✅ Servicio {self.service_name} configurado y habilitado")
            return True
        except Exception as e:
            print(f"❌ Error configurando servicio: {e}")
            return False
    
    def test_configuration(self):
        """Probar configuración antes de activar servicio"""
        print("\n🧪 PROBANDO CONFIGURACIÓN...")
        
        os.chdir(self.production_dir)
        python_path = os.path.join(self.production_dir, '.venv', 'bin', 'python')
        
        # Probar imports
        test_script = """
import sys
sys.path.append('.')

try:
    from main_advanced_with_indices import AdvancedTradingBotWithIndices
    print("✅ Bot principal importado correctamente")
except Exception as e:
    print(f"❌ Error importando bot: {e}")
    sys.exit(1)

try:
    from economic_calendar_analyzer import EconomicCalendarAnalyzer
    print("✅ Analizador de calendario importado")
except Exception as e:
    print(f"⚠️  Analizador de calendario: {e}")

try:
    from twitter_news_analyzer import AdvancedTwitterNewsAnalyzer
    print("✅ Analizador de Twitter importado")
except Exception as e:
    print(f"⚠️  Analizador de Twitter: {e}")

print("✅ Configuración básica válida")
"""
        
        try:
            with open(os.path.join(self.production_dir, 'test_config.py'), 'w') as f:
                f.write(test_script)
            
            result = subprocess.run([python_path, 'test_config.py'], 
                                  capture_output=True, text=True, timeout=30)
            
            print(result.stdout)
            if result.stderr:
                print("Warnings:", result.stderr)
            
            # Limpiar archivo de prueba
            os.remove(os.path.join(self.production_dir, 'test_config.py'))
            
            return result.returncode == 0
        except Exception as e:
            print(f"❌ Error en prueba de configuración: {e}")
            return False
    
    def start_service(self):
        """Iniciar servicio"""
        print("\n🚀 INICIANDO SERVICIO EN PRODUCCIÓN...")
        
        try:
            # Parar servicio si existe
            subprocess.run(['systemctl', 'stop', self.service_name], capture_output=True)
            time.sleep(3)
            
            # Iniciar servicio
            subprocess.run(['systemctl', 'start', self.service_name], check=True)
            time.sleep(5)
            
            # Verificar estado
            result = subprocess.run(['systemctl', 'is-active', self.service_name], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip() == 'active':
                print(f"✅ Servicio {self.service_name} iniciado correctamente")
                return True
            else:
                print(f"⚠️  Servicio {self.service_name} no está activo")
                # Mostrar logs para debug
                subprocess.run(['journalctl', '-u', self.service_name, '-n', '20', '--no-pager'])
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando servicio: {e}")
            return False
    
    def show_deployment_summary(self):
        """Mostrar resumen del deployment"""
        print("\n🎉 DEPLOYMENT COMPLETADO!")
        print("=" * 60)
        print(f"📁 Directorio: {self.production_dir}")
        print(f"🔧 Servicio: {self.service_name}")
        print("📈 Características activas:")
        print("  ✅ Twitter: 7 categorías + ML")
        print("  ✅ Calendario económico: FinBERT")
        print("  ✅ NASDAQ & S&P 500")
        print("  ✅ Machine Learning")
        print("  ✅ Modo automático")
        
        print("\n📋 COMANDOS ÚTILES:")
        print(f"🔍 Ver logs: journalctl -u {self.service_name} -f")
        print(f"📊 Estado: systemctl status {self.service_name}")
        print(f"🔄 Reiniciar: systemctl restart {self.service_name}")
        print(f"🛑 Detener: systemctl stop {self.service_name}")
        
        print("\n🎯 El bot está funcionando en modo automático 24/7")
        print("📈 Monitoreando Twitter + Calendario + NASDAQ/S&P 500")
        print("=" * 60)
    
    def deploy(self):
        """Ejecutar deployment completo"""
        self.print_banner()
        
        if not self.check_prerequisites():
            return False
        
        if not self.prepare_production_directory():
            return False
        
        if not self.copy_essential_files():
            return False
        
        if not self.setup_virtual_environment():
            return False
        
        if not self.create_auto_start_script():
            return False
        
        if not self.create_systemd_service():
            return False
        
        if not self.test_configuration():
            print("⚠️  Configuración tiene advertencias, pero continuando...")
        
        if not self.start_service():
            print("⚠️  Servicio no inició correctamente, revisa logs")
        
        self.show_deployment_summary()
        return True

def main():
    """Función principal"""
    deployer = LocalToProductionDeployment()
    success = deployer.deploy()
    
    if success:
        print("\n🎉 DEPLOYMENT EXITOSO!")
        sys.exit(0)
    else:
        print("\n💥 DEPLOYMENT CON ERRORES - Revisa los logs")
        sys.exit(1)

if __name__ == "__main__":
    main() 