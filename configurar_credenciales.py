#!/usr/bin/env python3
"""
CONFIGURADOR DE CREDENCIALES DEMO
================================
Script para configurar credenciales de MetaTrader 5 DEMO
IMPORTANTE: Solo usar cuentas DEMO - nunca cuentas reales
"""

import os
import sys
import json
from datetime import datetime

def imprimir_banner():
    """Banner del configurador"""
    print("=" * 60)
    print("🔧 CONFIGURADOR DE CREDENCIALES DEMO")
    print("=" * 60)
    print("🛡️  SOLO PARA CUENTAS DEMO DE METATRADER 5")
    print("❌ NUNCA USAR CREDENCIALES DE CUENTA REAL")
    print("=" * 60)

def explicar_como_obtener_demo():
    """Explica cómo obtener cuenta demo"""
    print("""
📋 CÓMO OBTENER UNA CUENTA DEMO DE MT5:

1. 🌐 Descarga MetaTrader 5 desde: https://www.metatrader5.com/
2. 📱 Instala la aplicación en tu computadora
3. 🆕 Abre MT5 y selecciona "Abrir cuenta demo"
4. 🏢 Elige un broker (ejemplo: MetaQuotes Software Corp)
5. 📝 Llena el formulario con datos ficticios
6. 💰 Selecciona depósito inicial: $1,000 - $10,000 USD
7. ✅ Confirma y obtén tus credenciales

🔐 CREDENCIALES QUE NECESITAS:
• Número de cuenta (Login)
• Contraseña
• Servidor (ej: MetaQuotes-Demo)

⚠️  IMPORTANTE: 
- Usa SOLO cuentas DEMO
- Nunca compartas credenciales reales
- Las cuentas demo son gratuitas y seguras
""")

def solicitar_credenciales():
    """Solicita credenciales al usuario"""
    print("\n🔐 INGRESA TUS CREDENCIALES DEMO:")
    print("-" * 40)
    
    # Login
    while True:
        login = input("📧 Login (número de cuenta demo): ").strip()
        if login.isdigit() and len(login) >= 6:
            break
        print("❌ Login debe ser numérico y tener al menos 6 dígitos")
    
    # Password
    while True:
        password = input("🔑 Contraseña: ").strip()
        if len(password) >= 4:
            break
        print("❌ Contraseña debe tener al menos 4 caracteres")
    
    # Servidor
    servidores_comunes = [
        "MetaQuotes-Demo",
        "MetaQuotes Software Corp-Demo",
        "Alpari-Demo",
        "XM-Demo",
        "FXTM-Demo"
    ]
    
    print("\n🖥️  SERVIDORES DEMO COMUNES:")
    for i, servidor in enumerate(servidores_comunes, 1):
        print(f"  {i}. {servidor}")
    
    while True:
        servidor_input = input("\n🌐 Servidor (escribe el nombre o número): ").strip()
        
        if servidor_input.isdigit():
            idx = int(servidor_input) - 1
            if 0 <= idx < len(servidores_comunes):
                servidor = servidores_comunes[idx]
                break
        elif servidor_input:
            servidor = servidor_input
            break
        
        print("❌ Por favor ingresa un servidor válido")
    
    return login, password, servidor

def confirmar_credenciales(login, password, servidor):
    """Confirma las credenciales con el usuario"""
    print("\n✅ CREDENCIALES CONFIGURADAS:")
    print("-" * 30)
    print(f"📧 Login: {login}")
    print(f"🔑 Contraseña: {'*' * len(password)}")
    print(f"🌐 Servidor: {servidor}")
    
    while True:
        confirmacion = input("\n¿Son correctas? (si/no): ").lower().strip()
        if confirmacion in ['si', 'sí', 's', 'yes', 'y']:
            return True
        elif confirmacion in ['no', 'n']:
            return False
        print("❌ Por favor responde 'si' o 'no'")

def guardar_credenciales(login, password, servidor):
    """Guarda las credenciales en archivo de configuración"""
    try:
        # Actualizar config_seguro.py
        config_lines = []
        with open('config_seguro.py', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            if "'MT5_LOGIN':" in line:
                config_lines.append(f"    'MT5_LOGIN': '{login}',\n")
            elif "'MT5_PASSWORD':" in line:
                config_lines.append(f"    'MT5_PASSWORD': '{password}',\n")
            elif "'MT5_SERVER':" in line:
                config_lines.append(f"    'MT5_SERVER': '{servidor}',\n")
            else:
                config_lines.append(line)
        
        with open('config_seguro.py', 'w', encoding='utf-8') as f:
            f.writelines(config_lines)
        
        print("✅ Credenciales guardadas en config_seguro.py")
        
        # Crear archivo .env adicional para compatibilidad
        env_content = f"""# CREDENCIALES MT5 DEMO - GENERADO AUTOMÁTICAMENTE
MT5_LOGIN={login}
MT5_PASSWORD={password}
MT5_SERVER={servidor}
DEMO_MODE=true
PAPER_TRADING=true
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado para compatibilidad")
        
        return True
        
    except Exception as e:
        print(f"❌ Error guardando credenciales: {e}")
        return False

def verificar_conexion():
    """Verifica la conexión con MT5"""
    print("\n🔍 VERIFICANDO CONEXIÓN...")
    
    try:
        # Intentar importar y conectar MT5
        import MetaTrader5 as mt5
        
        if not mt5.initialize():
            print("❌ Error inicializando MT5")
            return False
        
        # Cargar credenciales guardadas
        from config_seguro import CONFIGURACION_SEGURA
        
        login = int(CONFIGURACION_SEGURA['MT5_LOGIN'])
        password = CONFIGURACION_SEGURA['MT5_PASSWORD']
        servidor = CONFIGURACION_SEGURA['MT5_SERVER']
        
        # Intentar login
        if mt5.login(login, password, servidor):
            print("✅ Conexión exitosa con MT5")
            
            # Mostrar información de la cuenta
            account_info = mt5.account_info()
            if account_info:
                print(f"💰 Balance: ${account_info.balance:.2f}")
                print(f"📊 Cuenta: {account_info.name}")
                print(f"🏢 Compañía: {account_info.company}")
            
            mt5.shutdown()
            return True
        else:
            print("❌ Error de login. Verifica tus credenciales")
            mt5.shutdown()
            return False
            
    except ImportError:
        print("⚠️  MetaTrader5 package no instalado")
        print("💡 Instala con: pip install MetaTrader5")
        return False
    except Exception as e:
        print(f"❌ Error verificando conexión: {e}")
        return False

def mostrar_siguiente_paso():
    """Muestra instrucciones para el siguiente paso"""
    print("""
🎉 ¡CONFIGURACIÓN COMPLETADA!

🚀 SIGUIENTE PASO - INICIAR EL BOT:
================================

1. 📁 Asegúrate de que MetaTrader 5 esté abierto
2. 🔗 Verifica que esté conectado a tu cuenta demo
3. ▶️  Ejecuta el bot con:

   python iniciar_bot_seguro.py

🛡️  RECORDATORIOS DE SEGURIDAD:
• El bot solo usará tu cuenta DEMO
• Capital virtual: $1,000 USD
• Riesgo máximo: 0.5% por trade
• Máximo 10 trades por día
• Stops automáticos activados

📊 MONITOREO:
• Los logs se guardarán automáticamente
• Presiona Ctrl+C para detener el bot
• Revisa resultados en archivos .log y .csv

¡Buena suerte con tu trading automatizado! 🚀
""")

def main():
    """Función principal"""
    try:
        imprimir_banner()
        
        # Verificar si ya hay configuración
        if os.path.exists('config_seguro.py'):
            try:
                from config_seguro import CONFIGURACION_SEGURA
                if (CONFIGURACION_SEGURA['MT5_LOGIN'] != 'TU_LOGIN_DEMO' and
                    CONFIGURACION_SEGURA['MT5_PASSWORD'] != 'TU_PASSWORD_DEMO'):
                    
                    print("✅ Ya hay credenciales configuradas")
                    reconfigurar = input("¿Deseas reconfigurarlas? (si/no): ").lower().strip()
                    if reconfigurar not in ['si', 'sí', 's', 'yes', 'y']:
                        if verificar_conexion():
                            mostrar_siguiente_paso()
                        return
            except ImportError:
                pass
        
        # Explicar proceso
        explicar_como_obtener_demo()
        
        continuar = input("\n¿Ya tienes una cuenta demo de MT5? (si/no): ").lower().strip()
        if continuar not in ['si', 'sí', 's', 'yes', 'y']:
            print("👋 Primero obtén una cuenta demo y luego regresa")
            return
        
        # Configurar credenciales
        while True:
            login, password, servidor = solicitar_credenciales()
            
            if confirmar_credenciales(login, password, servidor):
                if guardar_credenciales(login, password, servidor):
                    break
            else:
                print("🔄 Reingresando credenciales...")
        
        # Verificar conexión
        if verificar_conexion():
            mostrar_siguiente_paso()
        else:
            print("\n⚠️  Conexión falló, pero puedes intentar ejecutar el bot")
            print("💡 Asegúrate de que MT5 esté abierto y conectado")
        
    except KeyboardInterrupt:
        print("\n\n👋 Configuración cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 