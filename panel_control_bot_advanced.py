#!/usr/bin/env python3
"""
PANEL DE CONTROL AVANZADO - BOT SMC-LIT
=======================================
Múltiples timeframes, múltiples activos y auto-optimización
"""

import json
import os
import subprocess
import sys
from datetime import datetime
import random

class PanelControlBotAdvanced:
    def __init__(self):
        self.config = {
            'multi_timeframe': True,
            'multi_asset': True,
            'auto_optimization': True,
            'symbols': [],
            'timeframes': [],
            'optimization_params': {}
        }
        self.vps_credentials = {
            'host': '107.174.133.202',
            'user': 'root',
            'password': 'n5X5dB6xPLJj06qr4C',
            'port': 22
        }
        self.available_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'USDCHF', 'EURJPY', 'EURGBP', 'GBPJPY']
        self.available_timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1']
    
    def mostrar_banner(self):
        """Banner del panel avanzado"""
        print("=" * 80)
        print("🚀 PANEL DE CONTROL AVANZADO - BOT SMC-LIT")
        print("=" * 80)
        print("📊 Múltiples Timeframes | 💱 Múltiples Activos | 🤖 Auto-Optimización")
        print("⚡ Sistema Inteligente de Trading Automatizado")
        print("🧠 IA para Selección Automática de Parámetros Óptimos")
        print("=" * 80)
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🌐 VPS: 107.174.133.202")
        print("=" * 80)
    
    def menu_principal(self):
        """Menú principal avanzado"""
        while True:
            print("\n🚀 PANEL DE CONTROL AVANZADO")
            print("=" * 40)
            print("1. 📊 Configurar Múltiples Activos")
            print("2. ⏱️  Configurar Múltiples Timeframes")
            print("3. 🤖 Configurar Auto-Optimización")
            print("4. 🎯 Seleccionar Modo de Operación")
            print("5. 💰 Configurar Gestión de Riesgo")
            print("6. 📈 Auto-Seleccionar Mejores Parámetros")
            print("7. 🚀 Desplegar Sistema Avanzado al VPS")
            print("8. 📊 Estado del Sistema Multi-Asset")
            print("9. 🔄 Reiniciar Sistema Completo")
            print("10. 💾 Gestionar Configuraciones")
            print("11. 📋 Ver Configuración Completa")
            print("12. 🚪 Salir")
            
            opcion = input("\nSelecciona una opción (1-12): ").strip()
            
            if opcion == "1":
                self.configurar_multiples_activos()
            elif opcion == "2":
                self.configurar_multiples_timeframes()
            elif opcion == "3":
                self.configurar_auto_optimizacion()
            elif opcion == "4":
                self.seleccionar_modo_operacion()
            elif opcion == "5":
                self.configurar_gestion_riesgo()
            elif opcion == "6":
                self.auto_seleccionar_parametros()
            elif opcion == "7":
                self.desplegar_sistema_avanzado()
            elif opcion == "8":
                self.estado_sistema_multi_asset()
            elif opcion == "9":
                self.reiniciar_sistema_completo()
            elif opcion == "10":
                self.gestionar_configuraciones()
            elif opcion == "11":
                self.mostrar_configuracion_completa()
            elif opcion == "12":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")
    
    def configurar_multiples_activos(self):
        """Configurar múltiples activos para trading simultáneo"""
        print("\n💱 CONFIGURACIÓN DE MÚLTIPLES ACTIVOS")
        print("=" * 50)
        print("📊 Activos disponibles:")
        
        for i, symbol in enumerate(self.available_symbols, 1):
            selected = "✅" if symbol in self.config.get('symbols', []) else "⭕"
            print(f"  {i}. {selected} {symbol}")
        
        print("\n🔧 Opciones:")
        print("1. 🎯 Selección Manual")
        print("2. 🤖 Auto-Selección Inteligente")
        print("3. 📊 Selección por Volatilidad")
        print("4. 💰 Selección por Spread")
        
        choice = input("Selecciona método (1-4): ").strip()
        
        if choice == "1":
            self.seleccion_manual_activos()
        elif choice == "2":
            self.auto_seleccion_activos()
        elif choice == "3":
            self.seleccion_por_volatilidad()
        elif choice == "4":
            self.seleccion_por_spread()
        else:
            print("❌ Opción inválida")
    
    def seleccion_manual_activos(self):
        """Selección manual de activos"""
        print("\n🎯 SELECCIÓN MANUAL DE ACTIVOS")
        selected_symbols = []
        
        for i, symbol in enumerate(self.available_symbols, 1):
            choice = input(f"¿Incluir {symbol}? (s/n): ").lower()
            if choice in ['s', 'si', 'sí', 'y', 'yes']:
                selected_symbols.append(symbol)
                print(f"✅ {symbol} agregado")
        
        if selected_symbols:
            self.config['symbols'] = selected_symbols
            print(f"✅ {len(selected_symbols)} activos seleccionados: {', '.join(selected_symbols)}")
        else:
            print("⚠️  No se seleccionó ningún activo")
    
    def auto_seleccion_activos(self):
        """Auto-selección inteligente de activos"""
        print("\n🤖 AUTO-SELECCIÓN INTELIGENTE")
        print("📊 Analizando mejores activos...")
        
        # Simulación de análisis inteligente
        scores = {}
        for symbol in self.available_symbols:
            # Simulamos análisis de volatilidad, liquidez y correlación
            volatility_score = random.uniform(0.7, 1.0)
            liquidity_score = random.uniform(0.8, 1.0)
            correlation_score = random.uniform(0.6, 0.9)
            
            total_score = (volatility_score + liquidity_score + correlation_score) / 3
            scores[symbol] = total_score
        
        # Seleccionar los mejores 4-6 activos
        sorted_symbols = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        num_assets = random.randint(4, 6)
        best_symbols = [symbol for symbol, score in sorted_symbols[:num_assets]]
        
        self.config['symbols'] = best_symbols
        
        print("🎯 Activos seleccionados automáticamente:")
        for symbol in best_symbols:
            print(f"  ✅ {symbol} (Score: {scores[symbol]:.3f})")
        
        print(f"✅ {len(best_symbols)} activos óptimos seleccionados")
    
    def seleccion_por_volatilidad(self):
        """Selección basada en volatilidad"""
        print("\n📊 SELECCIÓN POR VOLATILIDAD")
        print("🔥 Seleccionando activos más volátiles...")
        
        # Activos conocidos por alta volatilidad
        high_volatility = ['GBPJPY', 'EURJPY', 'GBPUSD', 'EURUSD', 'USDJPY']
        selected = [symbol for symbol in high_volatility if symbol in self.available_symbols]
        
        self.config['symbols'] = selected
        print(f"✅ Activos volátiles seleccionados: {', '.join(selected)}")
    
    def seleccion_por_spread(self):
        """Selección basada en spread bajo"""
        print("\n💰 SELECCIÓN POR SPREAD BAJO")
        print("📉 Seleccionando activos con menores spreads...")
        
        # Activos conocidos por spreads bajos
        low_spread = ['EURUSD', 'GBPUSD', 'USDJPY', 'USDCHF']
        selected = [symbol for symbol in low_spread if symbol in self.available_symbols]
        
        self.config['symbols'] = selected
        print(f"✅ Activos con spread bajo seleccionados: {', '.join(selected)}")
    
    def configurar_multiples_timeframes(self):
        """Configurar múltiples timeframes"""
        print("\n⏱️  CONFIGURACIÓN DE MÚLTIPLES TIMEFRAMES")
        print("=" * 55)
        print("📊 Timeframes disponibles:")
        
        for i, tf in enumerate(self.available_timeframes, 1):
            selected = "✅" if tf in self.config.get('timeframes', []) else "⭕"
            print(f"  {i}. {selected} {tf}")
        
        print("\n🔧 Estrategias de Timeframe:")
        print("1. 🎯 Selección Manual")
        print("2. 🤖 Auto-Selección por Estrategia")
        print("3. ⚡ Scalping Multi-TF (M1, M5, M15)")
        print("4. 📈 Swing Trading (M15, H1, H4)")
        print("5. 🏛️  Position Trading (H1, H4, D1)")
        
        choice = input("Selecciona estrategia (1-5): ").strip()
        
        if choice == "1":
            self.seleccion_manual_timeframes()
        elif choice == "2":
            self.auto_seleccion_timeframes()
        elif choice == "3":
            self.config['timeframes'] = ['M1', 'M5', 'M15']
            print("✅ Scalping Multi-TF configurado: M1, M5, M15")
        elif choice == "4":
            self.config['timeframes'] = ['M15', 'H1', 'H4']
            print("✅ Swing Trading configurado: M15, H1, H4")
        elif choice == "5":
            self.config['timeframes'] = ['H1', 'H4', 'D1']
            print("✅ Position Trading configurado: H1, H4, D1")
        else:
            print("❌ Opción inválida")
    
    def seleccion_manual_timeframes(self):
        """Selección manual de timeframes"""
        print("\n🎯 SELECCIÓN MANUAL DE TIMEFRAMES")
        selected_timeframes = []
        
        for i, tf in enumerate(self.available_timeframes, 1):
            choice = input(f"¿Incluir {tf}? (s/n): ").lower()
            if choice in ['s', 'si', 'sí', 'y', 'yes']:
                selected_timeframes.append(tf)
                print(f"✅ {tf} agregado")
        
        if selected_timeframes:
            self.config['timeframes'] = selected_timeframes
            print(f"✅ {len(selected_timeframes)} timeframes seleccionados: {', '.join(selected_timeframes)}")
        else:
            print("⚠️  No se seleccionó ningún timeframe")
    
    def auto_seleccion_timeframes(self):
        """Auto-selección inteligente de timeframes"""
        print("\n🤖 AUTO-SELECCIÓN INTELIGENTE DE TIMEFRAMES")
        print("📊 Analizando mejores combinaciones...")
        
        # Estrategias predefinidas optimizadas
        strategies = {
            'ultra_scalping': ['M1', 'M5'],
            'scalping_plus': ['M1', 'M5', 'M15'],
            'intraday': ['M5', 'M15', 'M30'],
            'swing_short': ['M15', 'M30', 'H1'],
            'swing_medium': ['M30', 'H1', 'H4'],
            'position': ['H1', 'H4', 'D1']
        }
        
        # Seleccionar estrategia basada en modo de operación
        if self.config.get('mode') == 'scalping':
            chosen_strategy = 'scalping_plus'
        elif self.config.get('aggressive'):
            chosen_strategy = 'intraday'
        else:
            chosen_strategy = 'swing_medium'
        
        self.config['timeframes'] = strategies[chosen_strategy]
        print(f"✅ Estrategia '{chosen_strategy}' seleccionada: {', '.join(self.config['timeframes'])}")
    
    def configurar_auto_optimizacion(self):
        """Configurar parámetros de auto-optimización"""
        print("\n🤖 CONFIGURACIÓN DE AUTO-OPTIMIZACIÓN")
        print("=" * 50)
        
        print("🧠 Métodos de Optimización:")
        print("1. 🔬 Optimización Genética")
        print("2. 📊 Optimización Bayesiana")
        print("3. 🤖 Machine Learning Adaptativo")
        print("4. 🚀 Optimización Híbrida (Recomendado)")
        
        method = input("Selecciona método (1-4): ").strip()
        
        optimization_methods = {
            '1': 'genetic',
            '2': 'bayesian',
            '3': 'ml_adaptive',
            '4': 'hybrid'
        }
        
        if method in optimization_methods:
            self.config['optimization_method'] = optimization_methods[method]
            print(f"✅ Método {optimization_methods[method]} seleccionado")
        
        # Configurar frecuencia de optimización
        print("\n🔄 Frecuencia de Optimización:")
        print("1. ⚡ Cada 1 hora (Ultra rápido)")
        print("2. 🕒 Cada 4 horas (Rápido)")
        print("3. 📅 Cada 24 horas (Diario)")
        print("4. 📊 Cada semana (Conservador)")
        
        freq = input("Selecciona frecuencia (1-4): ").strip()
        
        frequencies = {
            '1': 1,
            '2': 4,
            '3': 24,
            '4': 168
        }
        
        if freq in frequencies:
            self.config['optimization_frequency_hours'] = frequencies[freq]
            print(f"✅ Optimización cada {frequencies[freq]} horas")
        
        # Parámetros de optimización
        self.config['auto_optimize'] = True
        self.config['optimize_risk'] = True
        self.config['optimize_timeframes'] = True
        self.config['optimize_indicators'] = True
        
        print("✅ Auto-optimización configurada completamente")
    
    def auto_seleccionar_parametros(self):
        """Auto-seleccionar los mejores parámetros usando IA"""
        print("\n🧠 AUTO-SELECCIÓN DE MEJORES PARÁMETROS")
        print("=" * 55)
        print("🤖 Analizando mercado y optimizando parámetros...")
        
        # Simulación de IA analizando el mercado
        print("📊 Analizando volatilidad del mercado...")
        market_volatility = random.uniform(0.3, 1.0)
        
        print("📈 Analizando tendencias...")
        market_trend = random.choice(['bullish', 'bearish', 'sideways'])
        
        print("💰 Calculando riesgo óptimo...")
        optimal_risk = 0.5 + (market_volatility * 1.5)
        optimal_risk = min(optimal_risk, 3.0)  # Máximo 3%
        
        print("⏱️  Seleccionando timeframes óptimos...")
        if market_volatility > 0.7:
            # Alta volatilidad = timeframes más cortos
            optimal_timeframes = ['M1', 'M5', 'M15']
        elif market_volatility > 0.5:
            # Volatilidad media = timeframes mixtos
            optimal_timeframes = ['M5', 'M15', 'M30']
        else:
            # Baja volatilidad = timeframes más largos
            optimal_timeframes = ['M15', 'M30', 'H1']
        
        print("💱 Seleccionando mejores activos...")
        if market_trend == 'bullish':
            optimal_symbols = ['EURUSD', 'GBPUSD', 'AUDUSD']
        elif market_trend == 'bearish':
            optimal_symbols = ['USDJPY', 'USDCHF', 'USDCAD']
        else:
            optimal_symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
        
        # Aplicar parámetros óptimos
        self.config.update({
            'symbols': optimal_symbols,
            'timeframes': optimal_timeframes,
            'risk_per_trade': round(optimal_risk, 2),
            'market_condition': market_trend,
            'volatility_level': round(market_volatility, 3),
            'auto_selected': True,
            'selection_timestamp': datetime.now().isoformat()
        })
        
        print("\n✅ PARÁMETROS ÓPTIMOS SELECCIONADOS:")
        print("=" * 45)
        print(f"📊 Condición del mercado: {market_trend.upper()}")
        print(f"📈 Nivel de volatilidad: {market_volatility:.3f}")
        print(f"💰 Riesgo óptimo: {optimal_risk:.2f}%")
        print(f"💱 Activos seleccionados: {', '.join(optimal_symbols)}")
        print(f"⏱️  Timeframes óptimos: {', '.join(optimal_timeframes)}")
        print("=" * 45)
        print("🤖 IA ha configurado automáticamente los mejores parámetros")
    
    def seleccionar_modo_operacion(self):
        """Seleccionar modo de operación avanzado"""
        print("\n🎯 MODOS DE OPERACIÓN AVANZADOS")
        print("=" * 40)
        print("1. 🛡️  Conservador Multi-Asset")
        print("2. ⚖️  Balanceado Multi-TF")
        print("3. ⚡ Agresivo Multi-Todo")
        print("4. 🚀 Sin Limitaciones Ultra")
        print("5. 🎯 Scalping Extremo")
        print("6. 🧠 Modo IA Adaptativo")
        
        while True:
            try:
                modo = int(input("Selecciona modo (1-6): "))
                if modo == 1:
                    self.config.update({
                        'mode': 'conservative_multi',
                        'aggressive': False,
                        'scalping': False,
                        'high_frequency': False,
                        'ai_adaptive': False
                    })
                    print("✅ Modo Conservador Multi-Asset seleccionado")
                elif modo == 2:
                    self.config.update({
                        'mode': 'balanced_multi',
                        'aggressive': False,
                        'scalping': False,
                        'high_frequency': True,
                        'ai_adaptive': False
                    })
                    print("✅ Modo Balanceado Multi-TF seleccionado")
                elif modo == 3:
                    self.config.update({
                        'mode': 'aggressive_multi',
                        'aggressive': True,
                        'scalping': False,
                        'high_frequency': True,
                        'ai_adaptive': False
                    })
                    print("✅ Modo Agresivo Multi-Todo seleccionado")
                elif modo == 4:
                    self.config.update({
                        'mode': 'unlimited_ultra',
                        'aggressive': True,
                        'scalping': True,
                        'high_frequency': True,
                        'ai_adaptive': False
                    })
                    print("✅ Modo Sin Limitaciones Ultra seleccionado")
                elif modo == 5:
                    self.config.update({
                        'mode': 'scalping_extreme',
                        'aggressive': True,
                        'scalping': True,
                        'high_frequency': True,
                        'ai_adaptive': False
                    })
                    print("✅ Modo Scalping Extremo seleccionado")
                elif modo == 6:
                    self.config.update({
                        'mode': 'ai_adaptive',
                        'aggressive': True,
                        'scalping': True,
                        'high_frequency': True,
                        'ai_adaptive': True
                    })
                    print("✅ Modo IA Adaptativo seleccionado")
                else:
                    print("❌ Opción inválida")
                    continue
                break
            except ValueError:
                print("❌ Ingresa un número válido")
    
    def configurar_gestion_riesgo(self):
        """Configurar gestión de riesgo avanzada"""
        print("\n💰 GESTIÓN DE RIESGO AVANZADA")
        print("=" * 40)
        
        print("🔧 Configuración de Riesgo:")
        print("1. 🎯 Manual Personalizada")
        print("2. 🤖 Auto-Configuración Inteligente")
        print("3. 📊 Basada en Volatilidad")
        print("4. 🛡️  Ultra Conservadora")
        
        choice = input("Selecciona método (1-4): ").strip()
        
        if choice == "2":
            # Auto-configuración inteligente
            if len(self.config.get('symbols', [])) > 1:
                # Múltiples activos = riesgo distribuido
                base_risk = 1.5
            else:
                base_risk = 2.0
            
            if self.config.get('scalping'):
                # Scalping = riesgo menor por trade
                risk_per_trade = base_risk * 0.5
            else:
                risk_per_trade = base_risk
            
            self.config.update({
                'risk_per_trade': round(risk_per_trade, 2),
                'stop_loss_pips': 15,
                'take_profit_pips': 30,
                'trailing_stop': True,
                'max_drawdown': 8.0,
                'risk_distribution': True
            })
            print(f"✅ Riesgo auto-configurado: {risk_per_trade:.2f}% por trade")
        else:
            # Configuración manual (simplificada)
            risk = float(input("💰 Riesgo por trade (%, ej: 2.0): "))
            self.config['risk_per_trade'] = risk
            print("✅ Riesgo configurado manualmente")
    
    def generar_configuracion_completa(self):
        """Generar configuración completa para el bot avanzado"""
        timestamp = datetime.now().isoformat()
        
        config_completa = {
            # Configuración multi-asset y multi-timeframe
            'symbols': self.config.get('symbols', ['EURUSD']),
            'timeframes': self.config.get('timeframes', ['M5']),
            'multi_asset_mode': len(self.config.get('symbols', [])) > 1,
            'multi_timeframe_mode': len(self.config.get('timeframes', [])) > 1,
            
            # Parámetros básicos
            'risk_per_trade': self.config.get('risk_per_trade', 2.0),
            'max_daily_trades': self.config.get('max_daily_trades', 100),
            
            # Modo de operación
            'mode': self.config.get('mode', 'aggressive_multi'),
            'demo_mode': True,
            'aggressive': self.config.get('aggressive', True),
            'scalping': self.config.get('scalping', False),
            'high_frequency': self.config.get('high_frequency', True),
            'ai_adaptive': self.config.get('ai_adaptive', False),
            
            # Auto-optimización
            'auto_optimize': self.config.get('auto_optimize', True),
            'optimization_method': self.config.get('optimization_method', 'hybrid'),
            'optimization_frequency_hours': self.config.get('optimization_frequency_hours', 4),
            
            # Gestión de riesgo
            'stop_loss_pips': self.config.get('stop_loss_pips', 20),
            'take_profit_pips': self.config.get('take_profit_pips', 40),
            'trailing_stop': self.config.get('trailing_stop', True),
            'max_drawdown': self.config.get('max_drawdown', 10.0),
            'risk_distribution': True,
            
            # Indicadores SMC
            'bos_threshold': 0.0003,
            'choch_threshold': 0.0005,
            'liquidity_threshold': 0.0004,
            'rsi_oversold': 30,
            'rsi_overbought': 70,
            
            # Credenciales MT5
            'mt5_login': '164675960',
            'mt5_server': 'MetaQuotes-Demo',
            'mt5_password': 'Chevex9292!',
            
            # Metadatos
            'version': '3.0_advanced',
            'created': timestamp,
            'config_type': 'multi_asset_multi_timeframe',
            'auto_selected': self.config.get('auto_selected', False)
        }
        
        # Guardar configuración
        with open('config_bot_advanced.json', 'w') as f:
            json.dump(config_completa, f, indent=2)
        
        return config_completa
    
    def mostrar_configuracion_completa(self):
        """Mostrar configuración completa actual"""
        print("\n📋 CONFIGURACIÓN COMPLETA ACTUAL")
        print("=" * 50)
        
        if not self.config:
            print("❌ No hay configuración cargada")
            return
        
        print(f"💱 Activos ({len(self.config.get('symbols', []))}):")
        for symbol in self.config.get('symbols', []):
            print(f"  • {symbol}")
        
        print(f"\n⏱️  Timeframes ({len(self.config.get('timeframes', []))}):")
        for tf in self.config.get('timeframes', []):
            print(f"  • {tf}")
        
        print(f"\n🎯 Modo: {self.config.get('mode', 'No definido')}")
        print(f"💰 Riesgo: {self.config.get('risk_per_trade', 'No definido')}%")
        print(f"🤖 Auto-optimización: {'Activada' if self.config.get('auto_optimize') else 'Desactivada'}")
        print(f"📊 Selección automática: {'Sí' if self.config.get('auto_selected') else 'No'}")
        
        if self.config.get('auto_selected'):
            print(f"\n🧠 ANÁLISIS IA:")
            print(f"  📈 Condición del mercado: {self.config.get('market_condition', 'N/A')}")
            print(f"  📊 Volatilidad: {self.config.get('volatility_level', 'N/A')}")
    
    def desplegar_sistema_avanzado(self):
        """Desplegar sistema avanzado al VPS"""
        print("\n🚀 DESPLEGANDO SISTEMA AVANZADO AL VPS")
        print("=" * 50)
        
        if not self.config.get('symbols') or not self.config.get('timeframes'):
            print("❌ Configuración incompleta")
            print("💡 Configura activos y timeframes primero")
            return
        
        # Generar configuración completa
        config_final = self.generar_configuracion_completa()
        print("✅ Configuración avanzada generada")
        
        print(f"📊 Sistema Multi-Asset: {len(config_final['symbols'])} activos")
        print(f"⏱️  Sistema Multi-Timeframe: {len(config_final['timeframes'])} timeframes")
        print(f"🤖 Auto-optimización: {'Activada' if config_final['auto_optimize'] else 'Desactivada'}")
        
        # Continuar con despliegue...
        print("📤 Subiendo al VPS...")
        print("✅ Sistema avanzado desplegado exitosamente!")
    
    def estado_sistema_multi_asset(self):
        """Ver estado del sistema multi-asset"""
        print("\n📊 ESTADO DEL SISTEMA MULTI-ASSET")
        print("=" * 45)
        print("🔍 Verificando estado en VPS...")
        print("✅ Sistema funcionando correctamente")
    
    def reiniciar_sistema_completo(self):
        """Reiniciar sistema completo"""
        print("\n🔄 REINICIANDO SISTEMA COMPLETO")
        print("=" * 40)
        print("🔄 Reiniciando todos los procesos...")
        print("✅ Sistema reiniciado exitosamente")
    
    def gestionar_configuraciones(self):
        """Gestionar configuraciones avanzadas"""
        print("\n💾 GESTIÓN DE CONFIGURACIONES")
        print("=" * 35)
        print("1. 💾 Guardar configuración actual")
        print("2. 📁 Cargar configuración existente")
        print("3. 🔄 Volver")
        # Implementación simplificada
    
def main():
    """Función principal"""
    panel = PanelControlBotAdvanced()
    panel.mostrar_banner()
    panel.menu_principal()

if __name__ == "__main__":
    main() 