#!/usr/bin/env python3
"""
DEPLOYMENT VPS AUTOMÁTICO - BOT SMC-LIT v2.0
==========================================
Deploy completo con Twitter + Calendario + ML
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class VPSDeployment:
    def __init__(self):
        self.project_name = "bot_smc_lit_v2"
        self.repo_url = "https://github.com/tu-usuario/bot-smc-lit.git"  # Reemplazar con tu repo
        self.vps_path = f"/opt/{self.project_name}"
        self.service_name = "smc-lit-bot"
        
    def print_banner(self):
        """Mostrar banner de deployment"""
        print("🚀" + "=" * 70 + "🚀")
        print("🎯 DEPLOYMENT AUTOMÁTICO VPS - BOT SMC-LIT v2.0")
        print("🚀" + "=" * 70 + "🚀")
        print("📈 CARACTERÍSTICAS:")
        print("  ✅ Twitter + Calendario económico + ML")
        print("  ✅ NASDAQ y S&P 500")
        print("  ✅ Modo automático inteligente")
        print("  ✅ Configuración como servicio systemd")
        print("🚀" + "=" * 70 + "🚀")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀" + "=" * 70 + "🚀")
    
    def check_prerequisites(self):
        """Verificar prerequisitos del sistema"""
        print("\n🔍 VERIFICANDO PREREQUISITOS...")
        
        # Verificar Python 3.8+
        try:
            result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
            python_version = result.stdout.strip()
            print(f"✅ {python_version}")
        except:
            print("❌ Python 3 no encontrado")
            return False
        
        # Verificar git
        try:
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            print("✅ Git disponible")
        except:
            print("❌ Git no encontrado")
            return False
        
        # Verificar pip
        try:
            subprocess.run(['pip3', '--version'], capture_output=True, check=True)
            print("✅ pip3 disponible")
        except:
            print("❌ pip3 no encontrado")
            return False
        
        return True
    
    def setup_environment(self):
        """Configurar entorno de deployment"""
        print("\n🔧 CONFIGURANDO ENTORNO...")
        
        # Crear directorio del proyecto
        if not os.path.exists(self.vps_path):
            os.makedirs(self.vps_path, exist_ok=True)
            print(f"📁 Directorio creado: {self.vps_path}")
        
        # Cambiar al directorio
        os.chdir(self.vps_path)
        print(f"📂 Cambiado a: {os.getcwd()}")
        
        return True
    
    def clone_or_update_repo(self):
        """Clonar o actualizar repositorio"""
        print("\n📦 ACTUALIZANDO CÓDIGO...")
        
        if os.path.exists('.git'):
            print("🔄 Actualizando repositorio existente...")
            try:
                subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
                print("✅ Repositorio actualizado")
            except:
                print("⚠️  Error actualizando, clonando de nuevo...")
                return self.fresh_clone()
        else:
            return self.fresh_clone()
        
        return True
    
    def fresh_clone(self):
        """Clonar repositorio desde cero"""
        try:
            # Limpiar directorio
            subprocess.run(['rm', '-rf', '*'], shell=True)
            
            # Clonar
            subprocess.run(['git', 'clone', self.repo_url, '.'], check=True)
            print("✅ Repositorio clonado")
            return True
        except Exception as e:
            print(f"❌ Error clonando repositorio: {e}")
            return False
    
    def setup_virtual_environment(self):
        """Configurar entorno virtual"""
        print("\n🐍 CONFIGURANDO ENTORNO VIRTUAL...")
        
        # Crear venv si no existe
        if not os.path.exists('.venv'):
            subprocess.run(['python3', '-m', 'venv', '.venv'], check=True)
            print("✅ Entorno virtual creado")
        
        # Activar venv y instalar dependencias
        try:
            # Usar ruta absoluta al pip del venv
            pip_path = os.path.join(self.vps_path, '.venv', 'bin', 'pip')
            subprocess.run([pip_path, 'install', '--upgrade', 'pip'], check=True)
            subprocess.run([pip_path, 'install', '-r', 'requirements.txt'], check=True)
            print("✅ Dependencias instaladas")
            return True
        except Exception as e:
            print(f"❌ Error instalando dependencias: {e}")
            return False
    
    def create_systemd_service(self):
        """Crear servicio systemd"""
        print("\n⚙️  CONFIGURANDO SERVICIO SYSTEMD...")
        
        service_content = f"""[Unit]
Description=SMC-LIT Trading Bot v2.0
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=5
User=root
WorkingDirectory={self.vps_path}
Environment=PATH={self.vps_path}/.venv/bin
ExecStart={self.vps_path}/.venv/bin/python {self.vps_path}/inicio_bot_avanzado.py
StandardOutput=journal
StandardError=journal

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
            
            print(f"✅ Servicio {self.service_name} configurado")
            return True
        except Exception as e:
            print(f"❌ Error configurando servicio: {e}")
            return False
    
    def create_auto_response_script(self):
        """Crear script para respuesta automática"""
        print("\n🤖 CONFIGURANDO RESPUESTA AUTOMÁTICA...")
        
        auto_script = f"""#!/bin/bash
# Auto-respuesta para bot SMC-LIT v2.0
cd {self.vps_path}
echo "mantener" | {self.vps_path}/.venv/bin/python {self.vps_path}/main_advanced_with_indices.py
"""
        
        script_path = os.path.join(self.vps_path, 'start_auto.sh')
        
        try:
            with open(script_path, 'w') as f:
                f.write(auto_script)
            
            os.chmod(script_path, 0o755)
            print("✅ Script de auto-respuesta creado")
            return True
        except Exception as e:
            print(f"❌ Error creando script: {e}")
            return False
    
    def update_systemd_service_for_auto(self):
        """Actualizar servicio para usar script automático"""
        print("\n🔄 ACTUALIZANDO SERVICIO PARA MODO AUTOMÁTICO...")
        
        service_content = f"""[Unit]
Description=SMC-LIT Trading Bot v2.0 (Auto Mode)
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
WorkingDirectory={self.vps_path}
ExecStart=/bin/bash {self.vps_path}/start_auto.sh
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
"""
        
        service_path = f"/etc/systemd/system/{self.service_name}.service"
        
        try:
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            subprocess.run(['systemctl', 'daemon-reload'], check=True)
            print("✅ Servicio actualizado para modo automático")
            return True
        except Exception as e:
            print(f"❌ Error actualizando servicio: {e}")
            return False
    
    def start_service(self):
        """Iniciar servicio"""
        print("\n🚀 INICIANDO SERVICIO...")
        
        try:
            # Parar servicio si está corriendo
            subprocess.run(['systemctl', 'stop', self.service_name], capture_output=True)
            time.sleep(2)
            
            # Iniciar servicio
            subprocess.run(['systemctl', 'start', self.service_name], check=True)
            time.sleep(3)
            
            # Verificar estado
            result = subprocess.run(['systemctl', 'is-active', self.service_name], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip() == 'active':
                print(f"✅ Servicio {self.service_name} iniciado correctamente")
                return True
            else:
                print(f"⚠️  Servicio {self.service_name} no está activo")
                return False
                
        except Exception as e:
            print(f"❌ Error iniciando servicio: {e}")
            return False
    
    def show_status(self):
        """Mostrar estado del deployment"""
        print("\n📊 ESTADO DEL DEPLOYMENT")
        print("=" * 50)
        
        # Estado del servicio
        try:
            result = subprocess.run(['systemctl', 'status', self.service_name], 
                                  capture_output=True, text=True)
            print("🔧 Estado del servicio:")
            print(result.stdout[:500] + "..." if len(result.stdout) > 500 else result.stdout)
        except:
            print("❌ No se pudo obtener estado del servicio")
        
        print("\n📋 COMANDOS ÚTILES:")
        print(f"🔍 Ver logs: journalctl -u {self.service_name} -f")
        print(f"🔄 Reiniciar: systemctl restart {self.service_name}")
        print(f"🛑 Detener: systemctl stop {self.service_name}")
        print(f"📊 Estado: systemctl status {self.service_name}")
        
        print("\n✅ DEPLOYMENT COMPLETADO")
        print("🎯 El bot está funcionando en modo automático")
        print("📈 Incluye: Twitter + Calendario Económico + ML + NASDAQ/S&P 500")
    
    def deploy(self):
        """Ejecutar deployment completo"""
        self.print_banner()
        
        if not self.check_prerequisites():
            print("❌ Prerequisitos no cumplidos")
            return False
        
        if not self.setup_environment():
            print("❌ Error configurando entorno")
            return False
        
        # Usar archivos locales si no hay repo
        print("📁 Usando archivos locales del proyecto")
        
        if not self.setup_virtual_environment():
            print("❌ Error configurando entorno virtual")
            return False
        
        if not self.create_auto_response_script():
            print("❌ Error creando script automático")
            return False
        
        if not self.create_systemd_service():
            print("❌ Error configurando servicio")
            return False
        
        if not self.update_systemd_service_for_auto():
            print("❌ Error actualizando servicio")
            return False
        
        if not self.start_service():
            print("❌ Error iniciando servicio")
            return False
        
        self.show_status()
        return True

def main():
    """Función principal"""
    if os.geteuid() != 0:
        print("❌ Este script debe ejecutarse como root")
        print("💡 Usa: sudo python3 deploy_vps_final.py")
        sys.exit(1)
    
    deployer = VPSDeployment()
    success = deployer.deploy()
    
    if success:
        print("\n🎉 DEPLOYMENT EXITOSO!")
        sys.exit(0)
    else:
        print("\n💥 DEPLOYMENT FALLIDO!")
        sys.exit(1)

if __name__ == "__main__":
    main() 