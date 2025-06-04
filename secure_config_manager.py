#!/usr/bin/env python3
"""
GESTOR SEGURO DE CONFIGURACIÓN - BOT SMC-LIT
===========================================
Sistema profesional para manejo seguro de credenciales y configuración.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass
import base64
from cryptography.fernet import Fernet

@dataclass
class VPSCredentials:
    host: str
    user: str
    password: str
    port: int = 22

@dataclass 
class MT5Credentials:
    login: str
    password: str
    server: str

@dataclass
class BotSettings:
    demo_balance: float = 1000.0
    max_risk_per_trade: float = 0.02
    monitoring_interval: int = 30
    dashboard_port: int = 5000

class SecureConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config_template = "config.json.template"
        self.encrypted_file = "config.encrypted"
        self.key_file = ".config_key"
        self.logger = self._setup_logging()
        
    def _setup_logging(self):
        """Configurar logging seguro"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('config_manager.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger('SecureConfig')
    
    def _generate_key(self) -> bytes:
        """Generar clave de encriptación"""
        return Fernet.generate_key()
    
    def _save_key(self, key: bytes):
        """Guardar clave de forma segura"""
        with open(self.key_file, 'wb') as f:
            f.write(key)
        # Hacer el archivo solo legible por el propietario
        os.chmod(self.key_file, 0o600)
    
    def _load_key(self) -> Optional[bytes]:
        """Cargar clave de encriptación"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as f:
                    return f.read()
            return None
        except Exception as e:
            self.logger.error(f"Error loading encryption key: {e}")
            return None
    
    def encrypt_config(self, config_data: Dict[str, Any]) -> bool:
        """Encriptar archivo de configuración"""
        try:
            # Generar nueva clave si no existe
            key = self._load_key()
            if not key:
                key = self._generate_key()
                self._save_key(key)
            
            fernet = Fernet(key)
            
            # Convertir a JSON y encriptar
            json_data = json.dumps(config_data, indent=2).encode()
            encrypted_data = fernet.encrypt(json_data)
            
            # Guardar archivo encriptado
            with open(self.encrypted_file, 'wb') as f:
                f.write(encrypted_data)
            
            # Hacer archivo solo legible por propietario
            os.chmod(self.encrypted_file, 0o600)
            
            self.logger.info("Configuration encrypted successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error encrypting config: {e}")
            return False
    
    def decrypt_config(self) -> Optional[Dict[str, Any]]:
        """Desencriptar archivo de configuración"""
        try:
            key = self._load_key()
            if not key:
                self.logger.error("Encryption key not found")
                return None
            
            if not os.path.exists(self.encrypted_file):
                self.logger.error("Encrypted config file not found")
                return None
            
            fernet = Fernet(key)
            
            # Leer y desencriptar
            with open(self.encrypted_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            config_data = json.loads(decrypted_data.decode())
            
            return config_data
            
        except Exception as e:
            self.logger.error(f"Error decrypting config: {e}")
            return None
    
    def load_config(self) -> Dict[str, Any]:
        """Cargar configuración desde múltiples fuentes (prioridad: ENV > archivo encriptado > archivo plano)"""
        config = {}
        
        # 1. Intentar variables de entorno primero
        env_config = self._load_from_environment()
        if env_config:
            self.logger.info("Configuration loaded from environment variables")
            return env_config
        
        # 2. Intentar archivo encriptado
        encrypted_config = self.decrypt_config()
        if encrypted_config:
            self.logger.info("Configuration loaded from encrypted file")
            return encrypted_config
        
        # 3. Intentar archivo de configuración plano
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                self.logger.info("Configuration loaded from plain file")
                return config
            except Exception as e:
                self.logger.error(f"Error loading plain config: {e}")
        
        # 4. Si no hay configuración, crear template
        self._create_config_template()
        self.logger.warning("No configuration found. Template created.")
        return {}
    
    def _load_from_environment(self) -> Optional[Dict[str, Any]]:
        """Cargar configuración desde variables de entorno"""
        try:
            # Verificar si existen las variables principales
            required_env_vars = [
                'BOT_VPS_HOST', 'BOT_VPS_USER', 'BOT_VPS_PASSWORD',
                'BOT_MT5_LOGIN', 'BOT_MT5_PASSWORD', 'BOT_MT5_SERVER'
            ]
            
            missing_vars = [var for var in required_env_vars if not os.getenv(var)]
            if missing_vars:
                return None
            
            config = {
                "vps_credentials": {
                    "host": os.getenv('BOT_VPS_HOST'),
                    "user": os.getenv('BOT_VPS_USER'),
                    "password": os.getenv('BOT_VPS_PASSWORD'),
                    "port": int(os.getenv('BOT_VPS_PORT', '22'))
                },
                "mt5_credentials": {
                    "login": os.getenv('BOT_MT5_LOGIN'),
                    "password": os.getenv('BOT_MT5_PASSWORD'),
                    "server": os.getenv('BOT_MT5_SERVER')
                },
                "bot_settings": {
                    "demo_balance": float(os.getenv('BOT_DEMO_BALANCE', '1000.0')),
                    "max_risk_per_trade": float(os.getenv('BOT_MAX_RISK', '0.02')),
                    "monitoring_interval": int(os.getenv('BOT_MONITORING_INTERVAL', '30')),
                    "dashboard_port": int(os.getenv('BOT_DASHBOARD_PORT', '5000'))
                },
                "notifications": {
                    "telegram_bot_token": os.getenv('BOT_TELEGRAM_TOKEN', ''),
                    "telegram_chat_id": os.getenv('BOT_TELEGRAM_CHAT_ID', ''),
                    "email_smtp_server": os.getenv('BOT_EMAIL_SMTP', 'smtp.gmail.com'),
                    "email_port": int(os.getenv('BOT_EMAIL_PORT', '587')),
                    "email_user": os.getenv('BOT_EMAIL_USER', ''),
                    "email_password": os.getenv('BOT_EMAIL_PASSWORD', '')
                }
            }
            
            return config
            
        except Exception as e:
            self.logger.error(f"Error loading environment config: {e}")
            return None
    
    def _create_config_template(self):
        """Crear template de configuración si no existe"""
        if not os.path.exists(self.config_template):
            template = {
                "vps_credentials": {
                    "host": "YOUR_VPS_IP_HERE",
                    "user": "YOUR_USERNAME_HERE",
                    "password": "YOUR_PASSWORD_HERE",
                    "port": 22
                },
                "mt5_credentials": {
                    "login": "YOUR_MT5_LOGIN_HERE",
                    "password": "YOUR_MT5_PASSWORD_HERE",
                    "server": "YOUR_MT5_SERVER_HERE"
                },
                "bot_settings": {
                    "demo_balance": 1000.0,
                    "max_risk_per_trade": 0.02,
                    "monitoring_interval": 30,
                    "dashboard_port": 5000
                },
                "notifications": {
                    "telegram_bot_token": "YOUR_TELEGRAM_TOKEN_HERE",
                    "telegram_chat_id": "YOUR_CHAT_ID_HERE",
                    "email_smtp_server": "smtp.gmail.com",
                    "email_port": 587,
                    "email_user": "your_email@gmail.com",
                    "email_password": "your_email_password"
                }
            }
            
            with open(self.config_template, 'w') as f:
                json.dump(template, f, indent=2)
            
            self.logger.info(f"Configuration template created: {self.config_template}")
    
    def get_vps_credentials(self) -> Optional[VPSCredentials]:
        """Obtener credenciales VPS de forma segura"""
        config = self.load_config()
        if 'vps_credentials' in config:
            creds = config['vps_credentials']
            return VPSCredentials(
                host=creds['host'],
                user=creds['user'],
                password=creds['password'],
                port=creds.get('port', 22)
            )
        return None
    
    def get_mt5_credentials(self) -> Optional[MT5Credentials]:
        """Obtener credenciales MT5 de forma segura"""
        config = self.load_config()
        if 'mt5_credentials' in config:
            creds = config['mt5_credentials']
            return MT5Credentials(
                login=creds['login'],
                password=creds['password'],
                server=creds['server']
            )
        return None
    
    def get_bot_settings(self) -> BotSettings:
        """Obtener configuración del bot"""
        config = self.load_config()
        if 'bot_settings' in config:
            settings = config['bot_settings']
            return BotSettings(
                demo_balance=settings.get('demo_balance', 1000.0),
                max_risk_per_trade=settings.get('max_risk_per_trade', 0.02),
                monitoring_interval=settings.get('monitoring_interval', 30),
                dashboard_port=settings.get('dashboard_port', 5000)
            )
        return BotSettings()
    
    def setup_environment_variables(self):
        """Guía para configurar variables de entorno"""
        print("🔒 CONFIGURACIÓN SEGURA DE VARIABLES DE ENTORNO")
        print("=" * 60)
        print("Para usar variables de entorno, agrega estas líneas a tu ~/.bashrc:")
        print()
        print("# Bot SMC-LIT Configuration")
        print("export BOT_VPS_HOST='tu_ip_vps'")
        print("export BOT_VPS_USER='tu_usuario'") 
        print("export BOT_VPS_PASSWORD='tu_password'")
        print("export BOT_VPS_PORT='22'")
        print()
        print("export BOT_MT5_LOGIN='tu_login_mt5'")
        print("export BOT_MT5_PASSWORD='tu_password_mt5'")
        print("export BOT_MT5_SERVER='tu_servidor_mt5'")
        print()
        print("export BOT_DEMO_BALANCE='1000.0'")
        print("export BOT_MAX_RISK='0.02'")
        print()
        print("Luego ejecuta: source ~/.bashrc")
        print("=" * 60)

def main():
    """Configurador interactivo"""
    config_manager = SecureConfigManager()
    
    print("🔒 GESTOR SEGURO DE CONFIGURACIÓN - BOT SMC-LIT")
    print("=" * 60)
    print("1. Configurar variables de entorno (Recomendado)")
    print("2. Crear archivo de configuración encriptado") 
    print("3. Mostrar guía de variables de entorno")
    print("4. Verificar configuración actual")
    print("5. Salir")
    
    choice = input("\nSelecciona una opción: ").strip()
    
    if choice == "1":
        config_manager.setup_environment_variables()
    
    elif choice == "2":
        print("📝 Creando configuración encriptada...")
        print("Edita config.json.template con tus credenciales y ejecútame de nuevo")
        config_manager._create_config_template()
    
    elif choice == "3":
        config_manager.setup_environment_variables()
    
    elif choice == "4":
        config = config_manager.load_config()
        if config:
            print("✅ Configuración cargada exitosamente")
            print("🔒 Fuente: Variables de entorno o archivo encriptado")
        else:
            print("❌ No se pudo cargar la configuración")
    
    elif choice == "5":
        print("👋 ¡Hasta luego!")
    
    else:
        print("❌ Opción no válida")

if __name__ == "__main__":
    main() 