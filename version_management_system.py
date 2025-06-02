#!/usr/bin/env python3
"""
SISTEMA DE VERSIONADO Y ACTUALIZACIÓN - BOT SMC-LIT
==================================================
Sistema profesional para manejar versiones, actualizaciones automáticas
y rollbacks del bot en el VPS.
"""

import os
import sys
import json
import subprocess
import time
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

@dataclass
class Version:
    version_number: str
    release_date: datetime
    description: str
    changes: List[str]
    files_hash: str
    rollback_supported: bool
    performance_baseline: Dict[str, float]

@dataclass
class DeploymentResult:
    success: bool
    version: str
    deployment_time: datetime
    errors: List[str]
    backup_created: bool
    rollback_available: bool

class VersionManagementSystem:
    def __init__(self, vps_credentials: Dict[str, str], local_bot_path: str = "."):
        self.vps = vps_credentials
        self.local_path = local_bot_path
        self.version_file = "version_info.json"
        self.backup_dir = "backups"
        self.setup_logging()
        self.ensure_directories()
    
    def setup_logging(self):
        """Configurar sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('version_management.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def ensure_directories(self):
        """Crear directorios necesarios"""
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs("releases", exist_ok=True)
    
    def calculate_files_hash(self, file_paths: List[str]) -> str:
        """Calcular hash de archivos para verificar integridad"""
        hasher = hashlib.sha256()
        
        for file_path in sorted(file_paths):
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    hasher.update(f.read())
        
        return hasher.hexdigest()
    
    def get_current_version(self) -> Optional[Version]:
        """Obtener versión actual del bot"""
        try:
            if os.path.exists(self.version_file):
                with open(self.version_file, 'r') as f:
                    data = json.load(f)
                    return Version(
                        version_number=data['version_number'],
                        release_date=datetime.fromisoformat(data['release_date']),
                        description=data['description'],
                        changes=data['changes'],
                        files_hash=data['files_hash'],
                        rollback_supported=data['rollback_supported'],
                        performance_baseline=data['performance_baseline']
                    )
        except Exception as e:
            self.logger.error(f"Error reading version info: {e}")
        
        return None
    
    def save_version_info(self, version: Version):
        """Guardar información de versión"""
        version_data = {
            'version_number': version.version_number,
            'release_date': version.release_date.isoformat(),
            'description': version.description,
            'changes': version.changes,
            'files_hash': version.files_hash,
            'rollback_supported': version.rollback_supported,
            'performance_baseline': version.performance_baseline
        }
        
        with open(self.version_file, 'w') as f:
            json.dump(version_data, f, indent=2)
    
    def create_release_package(self, version_number: str, description: str, changes: List[str]) -> str:
        """Crear paquete de release con nueva versión"""
        release_dir = f"releases/v{version_number}"
        os.makedirs(release_dir, exist_ok=True)
        
        # Archivos principales del bot
        core_files = [
            'main_unlimited.py',
            'config_vps_unlimited.json',
            'start_unlimited_bot.sh',
            'requirements.txt',
            'src/'
        ]
        
        # Copiar archivos al directorio de release
        copied_files = []
        for file_path in core_files:
            if os.path.exists(file_path):
                dest_path = os.path.join(release_dir, os.path.basename(file_path))
                if os.path.isdir(file_path):
                    shutil.copytree(file_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(file_path, dest_path)
                copied_files.append(file_path)
        
        # Calcular hash de archivos
        files_hash = self.calculate_files_hash(copied_files)
        
        # Crear información de versión
        version = Version(
            version_number=version_number,
            release_date=datetime.now(),
            description=description,
            changes=changes,
            files_hash=files_hash,
            rollback_supported=True,
            performance_baseline={}
        )
        
        # Guardar metadatos del release
        with open(os.path.join(release_dir, 'release_info.json'), 'w') as f:
            json.dump(version.__dict__, f, default=str, indent=2)
        
        # Crear archivo comprimido
        release_package = f"releases/smc-lit-bot-v{version_number}.tar.gz"
        subprocess.run(['tar', '-czf', release_package, '-C', 'releases', f'v{version_number}'], check=True)
        
        self.logger.info(f"Release package created: {release_package}")
        return release_package
    
    def backup_current_version(self) -> bool:
        """Crear backup de la versión actual en el VPS"""
        try:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            backup_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                cd /home &&
                tar -czf {backup_name}.tar.gz smc-lit-bot/ &&
                mkdir -p /home/backups &&
                mv {backup_name}.tar.gz /home/backups/ &&
                echo "Backup created: {backup_name}.tar.gz"
            '
            """
            
            result = subprocess.run(backup_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"Backup created successfully: {backup_name}")
                return True
            else:
                self.logger.error(f"Backup failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
            return False
    
    def deploy_to_vps(self, release_package: str, perform_backup: bool = True) -> DeploymentResult:
        """Desplegar nueva versión al VPS"""
        deployment_start = datetime.now()
        errors = []
        backup_created = False
        
        try:
            # 1. Crear backup si se solicita
            if perform_backup:
                backup_created = self.backup_current_version()
                if not backup_created:
                    errors.append("Failed to create backup")
            
            # 2. Detener bot actual
            self.logger.info("Stopping current bot...")
            stop_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                pkill -f main_unlimited.py || true &&
                screen -S smc-bot -X quit || true
            '
            """
            subprocess.run(stop_command, shell=True, capture_output=True)
            
            # 3. Subir nuevo release
            self.logger.info("Uploading new release...")
            upload_command = [
                'sshpass', '-p', self.vps['password'],
                'scp', '-o', 'StrictHostKeyChecking=no', '-P', str(self.vps['port']),
                release_package,
                f"{self.vps['user']}@{self.vps['host']}:/tmp/"
            ]
            
            result = subprocess.run(upload_command, capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Upload failed: {result.stderr}")
                raise Exception("Upload failed")
            
            # 4. Extraer y aplicar nueva versión
            self.logger.info("Extracting and applying new version...")
            release_filename = os.path.basename(release_package)
            deploy_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                cd /tmp &&
                tar -xzf {release_filename} &&
                cd v* &&
                cp -r * /home/smc-lit-bot/ &&
                cd /home/smc-lit-bot &&
                chmod +x *.sh &&
                chmod +x *.py
            '
            """
            
            result = subprocess.run(deploy_command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Deployment failed: {result.stderr}")
                raise Exception("Deployment failed")
            
            # 5. Reiniciar bot con nueva versión
            self.logger.info("Starting bot with new version...")
            start_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                cd /home/smc-lit-bot &&
                source venv/bin/activate &&
                screen -dmS smc-bot python3 main_unlimited.py
            '
            """
            
            result = subprocess.run(start_command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                errors.append(f"Bot start failed: {result.stderr}")
            
            # 6. Verificar que el bot esté funcionando
            time.sleep(5)
            verify_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                ps aux | grep main_unlimited | grep -v grep | wc -l
            '
            """
            
            result = subprocess.run(verify_command, shell=True, capture_output=True, text=True)
            bot_running = int(result.stdout.strip()) > 0
            
            if not bot_running:
                errors.append("Bot is not running after deployment")
            
            success = len(errors) == 0 and bot_running
            
            return DeploymentResult(
                success=success,
                version=os.path.basename(release_package),
                deployment_time=deployment_start,
                errors=errors,
                backup_created=backup_created,
                rollback_available=backup_created
            )
            
        except Exception as e:
            errors.append(str(e))
            return DeploymentResult(
                success=False,
                version=os.path.basename(release_package),
                deployment_time=deployment_start,
                errors=errors,
                backup_created=backup_created,
                rollback_available=backup_created
            )
    
    def rollback_to_backup(self, backup_name: str = None) -> bool:
        """Hacer rollback a una versión anterior"""
        try:
            if not backup_name:
                # Usar el backup más reciente
                list_backups_command = f"""
                sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                    ls -t /home/backups/*.tar.gz | head -1
                '
                """
                result = subprocess.run(list_backups_command, shell=True, capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    backup_path = result.stdout.strip()
                    backup_name = os.path.basename(backup_path)
                else:
                    self.logger.error("No backups found")
                    return False
            
            self.logger.info(f"Rolling back to backup: {backup_name}")
            
            # Detener bot actual
            stop_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                pkill -f main_unlimited.py || true &&
                screen -S smc-bot -X quit || true
            '
            """
            subprocess.run(stop_command, shell=True, capture_output=True)
            
            # Restaurar backup
            rollback_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                cd /home &&
                rm -rf smc-lit-bot &&
                tar -xzf /home/backups/{backup_name} &&
                cd smc-lit-bot &&
                source venv/bin/activate &&
                screen -dmS smc-bot python3 main_unlimited.py
            '
            """
            
            result = subprocess.run(rollback_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info("Rollback completed successfully")
                return True
            else:
                self.logger.error(f"Rollback failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error during rollback: {e}")
            return False
    
    def list_available_backups(self) -> List[str]:
        """Listar backups disponibles en el VPS"""
        try:
            list_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                ls -la /home/backups/*.tar.gz 2>/dev/null || echo "No backups found"
            '
            """
            
            result = subprocess.run(list_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0 and "No backups found" not in result.stdout:
                backups = []
                for line in result.stdout.strip().split('\n'):
                    if '.tar.gz' in line:
                        backup_name = line.split()[-1]
                        backups.append(os.path.basename(backup_name))
                return backups
            else:
                return []
                
        except Exception as e:
            self.logger.error(f"Error listing backups: {e}")
            return []
    
    def get_vps_bot_status(self) -> Dict[str, any]:
        """Obtener estado actual del bot en el VPS"""
        try:
            status_command = f"""
            sshpass -p '{self.vps['password']}' ssh -o StrictHostKeyChecking=no -p {self.vps['port']} {self.vps['user']}@{self.vps['host']} '
                echo "=== BOT STATUS ===" &&
                ps aux | grep main_unlimited | grep -v grep | wc -l &&
                echo "=== VERSION INFO ===" &&
                cat /home/smc-lit-bot/version_info.json 2>/dev/null || echo "No version info" &&
                echo "=== UPTIME ===" &&
                uptime &&
                echo "=== DISK SPACE ===" &&
                df -h /home
            '
            """
            
            result = subprocess.run(status_command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                bot_running = int(lines[1]) > 0 if len(lines) > 1 else False
                
                return {
                    'bot_running': bot_running,
                    'raw_output': result.stdout,
                    'status': 'RUNNING' if bot_running else 'STOPPED'
                }
            else:
                return {'error': result.stderr, 'status': 'ERROR'}
                
        except Exception as e:
            return {'error': str(e), 'status': 'ERROR'}

def create_easy_deployment_script():
    """Crear script simplificado para uso fácil"""
    script_content = """#!/usr/bin/env python3
'''
SCRIPT SIMPLIFICADO DE DESPLIEGUE
=================================
Uso: python3 easy_deploy.py [version] [description]
'''

import sys
from version_management_system import VersionManagementSystem

def main():
    if len(sys.argv) < 3:
        print("Uso: python3 easy_deploy.py [version] [description]")
        print("Ejemplo: python3 easy_deploy.py 1.2.0 'Mejoras en estrategia SMC'")
        return
    
    version = sys.argv[1]
    description = sys.argv[2]
    changes = sys.argv[3:] if len(sys.argv) > 3 else ["Actualización general"]
    
    vps_credentials = {
        'host': '107.174.133.202',
        'user': 'root',
        'password': 'n5X5dB6xPLJj06qr4C',
        'port': 22
    }
    
    vms = VersionManagementSystem(vps_credentials)
    
    print(f"🚀 Creando release v{version}...")
    package = vms.create_release_package(version, description, changes)
    
    print(f"📦 Desplegando al VPS...")
    result = vms.deploy_to_vps(package)
    
    if result.success:
        print(f"✅ Despliegue exitoso!")
        print(f"📋 Versión: {result.version}")
        print(f"⏰ Tiempo: {result.deployment_time}")
        print(f"💾 Backup: {'Sí' if result.backup_created else 'No'}")
    else:
        print(f"❌ Despliegue falló:")
        for error in result.errors:
            print(f"   - {error}")
        
        if result.rollback_available:
            rollback = input("¿Hacer rollback? (y/n): ")
            if rollback.lower() == 'y':
                if vms.rollback_to_backup():
                    print("✅ Rollback exitoso")
                else:
                    print("❌ Rollback falló")

if __name__ == "__main__":
    main()
"""
    
    with open('easy_deploy.py', 'w') as f:
        f.write(script_content)
    
    os.chmod('easy_deploy.py', 0o755)

def main():
    """Función principal de demostración"""
    vps_credentials = {
        'host': '107.174.133.202',
        'user': 'root',
        'password': 'n5X5dB6xPLJj06qr4C',
        'port': 22
    }
    
    vms = VersionManagementSystem(vps_credentials)
    
    print("🚀 SISTEMA DE VERSIONADO Y ACTUALIZACIÓN")
    print("=" * 50)
    print("📋 Opciones disponibles:")
    print("1. Ver estado actual del bot")
    print("2. Crear nueva versión")
    print("3. Listar backups disponibles")
    print("4. Hacer rollback")
    print("5. Crear script de despliegue fácil")
    
    choice = input("\nSelecciona una opción (1-5): ")
    
    if choice == "1":
        status = vms.get_vps_bot_status()
        print(f"\n📊 Estado del bot: {status}")
    
    elif choice == "2":
        version = input("Número de versión (ej: 1.1.0): ")
        description = input("Descripción: ")
        changes = input("Cambios (separados por coma): ").split(',')
        
        package = vms.create_release_package(version, description, changes)
        
        deploy = input("¿Desplegar al VPS? (y/n): ")
        if deploy.lower() == 'y':
            result = vms.deploy_to_vps(package)
            if result.success:
                print("✅ Despliegue exitoso!")
            else:
                print(f"❌ Errores: {result.errors}")
    
    elif choice == "3":
        backups = vms.list_available_backups()
        print(f"\n📁 Backups disponibles: {backups}")
    
    elif choice == "4":
        backups = vms.list_available_backups()
        if backups:
            print("📁 Backups disponibles:")
            for i, backup in enumerate(backups):
                print(f"  {i+1}. {backup}")
            
            choice = input("Selecciona backup (número o nombre): ")
            if choice.isdigit() and int(choice) <= len(backups):
                backup_name = backups[int(choice)-1]
            else:
                backup_name = choice
            
            if vms.rollback_to_backup(backup_name):
                print("✅ Rollback exitoso")
            else:
                print("❌ Rollback falló")
        else:
            print("❌ No hay backups disponibles")
    
    elif choice == "5":
        create_easy_deployment_script()
        print("✅ Script easy_deploy.py creado")
        print("Uso: python3 easy_deploy.py 1.1.0 'Nueva funcionalidad'")

if __name__ == "__main__":
    main() 