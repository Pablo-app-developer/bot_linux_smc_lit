#!/usr/bin/env python3
"""
PANEL DE CONTROL COMPLETO - BOT SMC-LIT
=======================================
Configuración de parámetros, modos y despliegue automático
"""

import json
import os
import subprocess
import sys
from datetime import datetime

class PanelControlBot:
    def __init__(self):
        self.config = {}
        self.vps_credentials = {
            'host': '107.174.133.202',
            'user': 'root',
            'password': 'n5X5dB6xPLJj06qr4C',
            'port': 22
        }
    
    def mostrar_banner(self):
        """Banner del panel de control"""
        print("=" * 70)
        print("🎛️  PANEL DE CONTROL - BOT SMC-LIT")
        print("=" * 70)
        print("🤖 Configuración Completa de Parámetros y Modos")
        print("🚀 Despliegue Automático al VPS")
        print("⚙️  Gestión de Trading en Tiempo Real")
        print("=" * 70)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 VPS: 107.174.133.202")
        print("=" * 70)
    
    def menu_principal(self):
        """Menú principal del panel"""
        while True:
            print("\n🎛️  PANEL DE CONTROL")
            print("=" * 30)
            print("1. 🔧 Configurar Parámetros de Trading")
            print("2. 🎯 Seleccionar Modo de Operación")
            print("3. 💰 Configurar Gestión de Riesgo")
            print("4. 📊 Configurar Indicadores SMC")
            print("5. 🚀 Desplegar al VPS")
            print("6. 📈 Estado del Bot en VPS")
            print("7. 🔄 Reiniciar Bot en VPS")
            print("8. 💾 Guardar/Cargar Configuración")
            print("9. 📋 Ver Configuración Actual")
            print("10. 🚪 Salir")
            
            opcion = input("\nSelecciona una opción (1-10): ").strip()
            
            if opcion == "1":
                self.configurar_parametros_trading()
            elif opcion == "2":
                self.seleccionar_modo_operacion()
            elif opcion == "3":
                self.configurar_gestion_riesgo()
            elif opcion == "4":
                self.configurar_indicadores_smc()
            elif opcion == "5":
                self.desplegar_al_vps()
            elif opcion == "6":
                self.estado_bot_vps()
            elif opcion == "7":
                self.reiniciar_bot_vps()
            elif opcion == "8":
                self.gestionar_configuracion()
            elif opcion == "9":
                self.mostrar_configuracion_actual()
            elif opcion == "10":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")
    
    def configurar_parametros_trading(self):
        """Configurar parámetros básicos de trading"""
        print("\n🔧 CONFIGURACIÓN DE PARÁMETROS DE TRADING")
        print("=" * 50)
        
        # Símbolo
        simbolos = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'USDCHF']
        print("📈 Símbolos disponibles:")
        for i, symbol in enumerate(simbolos, 1):
            print(f"  {i}. {symbol}")
        
        while True:
            try:
                sym_choice = int(input("Selecciona símbolo (1-6): ")) - 1
                if 0 <= sym_choice < len(simbolos):
                    self.config['symbol'] = simbolos[sym_choice]
                    break
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Timeframe
        timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']
        print("\n⏱️  Timeframes disponibles:")
        for i, tf in enumerate(timeframes, 1):
            print(f"  {i}. {tf}")
        
        while True:
            try:
                tf_choice = int(input("Selecciona timeframe (1-7): ")) - 1
                if 0 <= tf_choice < len(timeframes):
                    self.config['timeframe'] = timeframes[tf_choice]
                    break
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Riesgo por trade
        while True:
            try:
                risk = float(input("💰 Riesgo por trade (% de cuenta, ej: 2.0): "))
                if 0.1 <= risk <= 10.0:
                    self.config['risk_per_trade'] = risk
                    break
                else:
                    print("❌ Riesgo debe estar entre 0.1% y 10%")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Máximo trades por día
        while True:
            try:
                max_trades = int(input("📊 Máximo trades por día (ej: 50): "))
                if 1 <= max_trades <= 200:
                    self.config['max_daily_trades'] = max_trades
                    break
                else:
                    print("❌ Debe estar entre 1 y 200")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        print("✅ Parámetros de trading configurados")
    
    def seleccionar_modo_operacion(self):
        """Seleccionar modo de operación del bot"""
        print("\n🎯 MODOS DE OPERACIÓN")
        print("=" * 30)
        print("1. 🛡️  Modo Conservador (Bajo riesgo)")
        print("2. ⚖️  Modo Balanceado (Riesgo moderado)")
        print("3. ⚡ Modo Agresivo (Alto rendimiento)")
        print("4. 🚀 Modo Sin Limitaciones (Máximo)")
        print("5. 🎯 Modo Scalping (Alta frecuencia)")
        
        while True:
            try:
                modo = int(input("Selecciona modo (1-5): "))
                if modo == 1:
                    self.config['mode'] = 'conservative'
                    self.config['aggressive'] = False
                    self.config['scalping'] = False
                    self.config['high_frequency'] = False
                    print("✅ Modo Conservador seleccionado")
                elif modo == 2:
                    self.config['mode'] = 'balanced'
                    self.config['aggressive'] = False
                    self.config['scalping'] = False
                    self.config['high_frequency'] = True
                    print("✅ Modo Balanceado seleccionado")
                elif modo == 3:
                    self.config['mode'] = 'aggressive'
                    self.config['aggressive'] = True
                    self.config['scalping'] = False
                    self.config['high_frequency'] = True
                    print("✅ Modo Agresivo seleccionado")
                elif modo == 4:
                    self.config['mode'] = 'unlimited'
                    self.config['aggressive'] = True
                    self.config['scalping'] = True
                    self.config['high_frequency'] = True
                    print("✅ Modo Sin Limitaciones seleccionado")
                elif modo == 5:
                    self.config['mode'] = 'scalping'
                    self.config['aggressive'] = True
                    self.config['scalping'] = True
                    self.config['high_frequency'] = True
                    print("✅ Modo Scalping seleccionado")
                else:
                    print("❌ Opción inválida")
                    continue
                break
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Tipo de cuenta
        print("\n💳 Tipo de Cuenta:")
        print("1. 📊 Cuenta DEMO (Recomendado)")
        print("2. 💰 Cuenta REAL (¡Cuidado!)")
        
        while True:
            try:
                cuenta = int(input("Selecciona tipo (1-2): "))
                if cuenta == 1:
                    self.config['account_type'] = 'DEMO'
                    self.config['demo_mode'] = True
                    print("✅ Cuenta DEMO seleccionada (Seguro)")
                elif cuenta == 2:
                    print("⚠️  ADVERTENCIA: Cuenta REAL seleccionada")
                    confirm = input("¿Estás seguro? (si/no): ").lower()
                    if confirm in ['si', 'sí', 's', 'yes', 'y']:
                        self.config['account_type'] = 'REAL'
                        self.config['demo_mode'] = False
                        print("⚠️  Cuenta REAL configurada")
                    else:
                        continue
                else:
                    print("❌ Opción inválida")
                    continue
                break
            except ValueError:
                print("❌ Ingresa un número válido")
    
    def configurar_gestion_riesgo(self):
        """Configurar gestión de riesgo"""
        print("\n💰 CONFIGURACIÓN DE GESTIÓN DE RIESGO")
        print("=" * 45)
        
        # Stop Loss
        while True:
            try:
                sl = float(input("🛑 Stop Loss en pips (ej: 20): "))
                if 5 <= sl <= 100:
                    self.config['stop_loss_pips'] = sl
                    break
                else:
                    print("❌ Stop Loss debe estar entre 5 y 100 pips")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Take Profit
        while True:
            try:
                tp = float(input("🎯 Take Profit en pips (ej: 40): "))
                if 10 <= tp <= 200:
                    self.config['take_profit_pips'] = tp
                    break
                else:
                    print("❌ Take Profit debe estar entre 10 y 200 pips")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Trailing Stop
        trailing = input("🔄 ¿Activar Trailing Stop? (si/no): ").lower()
        self.config['trailing_stop'] = trailing in ['si', 'sí', 's', 'yes', 'y']
        
        # Max Drawdown
        while True:
            try:
                dd = float(input("📉 Máximo Drawdown permitido (%, ej: 10): "))
                if 5 <= dd <= 50:
                    self.config['max_drawdown'] = dd
                    break
                else:
                    print("❌ Drawdown debe estar entre 5% y 50%")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        print("✅ Gestión de riesgo configurada")
    
    def configurar_indicadores_smc(self):
        """Configurar indicadores Smart Money Concepts"""
        print("\n📊 CONFIGURACIÓN DE INDICADORES SMC")
        print("=" * 40)
        
        # BOS Threshold
        while True:
            try:
                bos = float(input("🔄 BOS Threshold (ej: 0.0003): "))
                if 0.0001 <= bos <= 0.001:
                    self.config['bos_threshold'] = bos
                    break
                else:
                    print("❌ Debe estar entre 0.0001 y 0.001")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # CHoCH Threshold
        while True:
            try:
                choch = float(input("🔄 CHoCH Threshold (ej: 0.0005): "))
                if 0.0001 <= choch <= 0.001:
                    self.config['choch_threshold'] = choch
                    break
                else:
                    print("❌ Debe estar entre 0.0001 y 0.001")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # Liquidity Threshold
        while True:
            try:
                liq = float(input("💧 Liquidity Threshold (ej: 0.0004): "))
                if 0.0001 <= liq <= 0.001:
                    self.config['liquidity_threshold'] = liq
                    break
                else:
                    print("❌ Debe estar entre 0.0001 y 0.001")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        # RSI Configuración
        while True:
            try:
                rsi_os = int(input("📈 RSI Oversold (ej: 30): "))
                if 20 <= rsi_os <= 40:
                    self.config['rsi_oversold'] = rsi_os
                    break
                else:
                    print("❌ Debe estar entre 20 y 40")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        while True:
            try:
                rsi_ob = int(input("📉 RSI Overbought (ej: 70): "))
                if 60 <= rsi_ob <= 80:
                    self.config['rsi_overbought'] = rsi_ob
                    break
                else:
                    print("❌ Debe estar entre 60 y 80")
            except ValueError:
                print("❌ Ingresa un número válido")
        
        print("✅ Indicadores SMC configurados")
    
    def mostrar_configuracion_actual(self):
        """Mostrar configuración actual"""
        print("\n📋 CONFIGURACIÓN ACTUAL")
        print("=" * 35)
        
        if not self.config:
            print("❌ No hay configuración cargada")
            return
        
        for key, value in self.config.items():
            print(f"• {key}: {value}")
    
    def guardar_configuracion(self):
        """Guardar configuración actual"""
        filename = f"config_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✅ Configuración guardada en: {filename}")
        return filename
    
    def cargar_configuracion(self):
        """Cargar configuración existente"""
        configs = [f for f in os.listdir('.') if f.startswith('config_bot_') and f.endswith('.json')]
        
        if not configs:
            print("❌ No hay configuraciones guardadas")
            return
        
        print("📁 Configuraciones disponibles:")
        for i, config in enumerate(configs, 1):
            print(f"  {i}. {config}")
        
        while True:
            try:
                choice = int(input("Selecciona configuración: ")) - 1
                if 0 <= choice < len(configs):
                    with open(configs[choice], 'r') as f:
                        self.config = json.load(f)
                    print(f"✅ Configuración cargada: {configs[choice]}")
                    break
                else:
                    print("❌ Opción inválida")
            except ValueError:
                print("❌ Ingresa un número válido")
            except FileNotFoundError:
                print("❌ Archivo no encontrado")
    
    def gestionar_configuracion(self):
        """Gestionar configuraciones"""
        print("\n💾 GESTIÓN DE CONFIGURACIÓN")
        print("=" * 35)
        print("1. 💾 Guardar configuración actual")
        print("2. 📁 Cargar configuración existente")
        print("3. 🔄 Volver")
        
        opcion = input("Selecciona opción (1-3): ").strip()
        
        if opcion == "1":
            self.guardar_configuracion()
        elif opcion == "2":
            self.cargar_configuracion()
        elif opcion == "3":
            return
        else:
            print("❌ Opción inválida")
    
    def generar_archivo_configuracion(self):
        """Generar archivo de configuración para el bot"""
        if not self.config:
            print("❌ No hay configuración para generar")
            return None
        
        # Configuración completa con valores por defecto
        config_completa = {
            # Parámetros básicos
            'symbol': self.config.get('symbol', 'EURUSD'),
            'timeframe': self.config.get('timeframe', 'M5'),
            'risk_per_trade': self.config.get('risk_per_trade', 2.0),
            'max_daily_trades': self.config.get('max_daily_trades', 50),
            
            # Modo de operación
            'mode': self.config.get('mode', 'aggressive'),
            'demo_mode': self.config.get('demo_mode', True),
            'aggressive': self.config.get('aggressive', True),
            'scalping': self.config.get('scalping', False),
            'high_frequency': self.config.get('high_frequency', True),
            
            # Gestión de riesgo
            'stop_loss_pips': self.config.get('stop_loss_pips', 20),
            'take_profit_pips': self.config.get('take_profit_pips', 40),
            'trailing_stop': self.config.get('trailing_stop', True),
            'max_drawdown': self.config.get('max_drawdown', 10.0),
            
            # Indicadores SMC
            'bos_threshold': self.config.get('bos_threshold', 0.0003),
            'choch_threshold': self.config.get('choch_threshold', 0.0005),
            'liquidity_threshold': self.config.get('liquidity_threshold', 0.0004),
            'rsi_oversold': self.config.get('rsi_oversold', 30),
            'rsi_overbought': self.config.get('rsi_overbought', 70),
            
            # Credenciales MT5
            'mt5_login': '164675960',
            'mt5_server': 'MetaQuotes-Demo',
            'mt5_password': 'Chevex9292!',
            
            # Timestamp
            'created': datetime.now().isoformat(),
            'version': '2.0'
        }
        
        # Guardar configuración
        with open('config_bot_activo.json', 'w') as f:
            json.dump(config_completa, f, indent=2)
        
        return config_completa
    
    def desplegar_al_vps(self):
        """Desplegar configuración al VPS"""
        print("\n🚀 DESPLEGANDO BOT AL VPS")
        print("=" * 35)
        
        if not self.config:
            print("❌ No hay configuración para desplegar")
            print("💡 Configura los parámetros primero")
            return
        
        # Generar configuración
        config_final = self.generar_archivo_configuracion()
        print("✅ Configuración generada")
        
        # Subir archivos al VPS
        print("📤 Subiendo archivos al VPS...")
        
        try:
            # Comando para subir archivos
            upload_cmd = [
                'sshpass', '-p', self.vps_credentials['password'],
                'scp', '-o', 'StrictHostKeyChecking=no',
                'config_bot_activo.json',
                f"{self.vps_credentials['user']}@{self.vps_credentials['host']}:/home/smc-lit-bot/"
            ]
            
            result = subprocess.run(upload_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Configuración subida al VPS")
            else:
                print(f"❌ Error subiendo: {result.stderr}")
                return
            
            # Reiniciar bot con nueva configuración
            print("🔄 Reiniciando bot con nueva configuración...")
            
            restart_cmd = [
                'sshpass', '-p', self.vps_credentials['password'],
                'ssh', '-o', 'StrictHostKeyChecking=no',
                f"{self.vps_credentials['user']}@{self.vps_credentials['host']}",
                'cd /home/smc-lit-bot && pkill -f main_unlimited.py && sleep 2 && screen -dmS smc-bot-new python3 main_unlimited.py'
            ]
            
            result = subprocess.run(restart_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Bot reiniciado con nueva configuración")
                print("🎯 Bot desplegado exitosamente!")
            else:
                print(f"❌ Error reiniciando: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error en despliegue: {e}")
    
    def estado_bot_vps(self):
        """Verificar estado del bot en VPS"""
        print("\n📈 ESTADO DEL BOT EN VPS")
        print("=" * 30)
        
        try:
            status_cmd = [
                'sshpass', '-p', self.vps_credentials['password'],
                'ssh', '-o', 'StrictHostKeyChecking=no',
                f"{self.vps_credentials['user']}@{self.vps_credentials['host']}",
                'ps aux | grep main_unlimited | grep -v grep && echo "=== LOG RECIENTE ===" && cd /home/smc-lit-bot && tail -5 bot_unlimited.log 2>/dev/null || echo "No hay logs disponibles"'
            ]
            
            result = subprocess.run(status_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("📊 Estado actual:")
                print(result.stdout)
            else:
                print(f"❌ Error obteniendo estado: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def reiniciar_bot_vps(self):
        """Reiniciar bot en VPS"""
        print("\n🔄 REINICIANDO BOT EN VPS")
        print("=" * 30)
        
        try:
            restart_cmd = [
                'sshpass', '-p', self.vps_credentials['password'],
                'ssh', '-o', 'StrictHostKeyChecking=no',
                f"{self.vps_credentials['user']}@{self.vps_credentials['host']}",
                'pkill -f main_unlimited.py && sleep 3 && cd /home/smc-lit-bot && screen -dmS smc-bot-restart python3 main_unlimited.py && echo "Bot reiniciado"'
            ]
            
            result = subprocess.run(restart_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Bot reiniciado exitosamente")
                print(result.stdout)
            else:
                print(f"❌ Error reiniciando: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal"""
    panel = PanelControlBot()
    panel.mostrar_banner()
    panel.menu_principal()

if __name__ == "__main__":
    main() 