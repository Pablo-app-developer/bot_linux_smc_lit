"""
notifications.py - Sistema de notificaciones para el bot SMC-LIT

Proporciona diferentes métodos de notificación:
- Consola (siempre activo)
- Archivo de log
- Sonido del sistema (opcional)
"""

import os
import logging
import time
from datetime import datetime
from enum import Enum

class NotificationType(Enum):
    """Tipos de notificaciones"""
    INFO = "INFO"
    SUCCESS = "SUCCESS" 
    WARNING = "WARNING"
    ERROR = "ERROR"
    TRADE_SIGNAL = "TRADE_SIGNAL"
    TRADE_EXECUTED = "TRADE_EXECUTED"
    TRADE_CLOSED = "TRADE_CLOSED"

class NotificationManager:
    """Gestor de notificaciones del bot"""
    
    def __init__(self, enable_sound=False, enable_file=True):
        """
        Inicializa el gestor de notificaciones
        
        Args:
            enable_sound: Habilitar notificaciones de sonido
            enable_file: Habilitar notificaciones en archivo
        """
        self.enable_sound = enable_sound
        self.enable_file = enable_file
        self.logger = logging.getLogger('notifications')
        
        # Emojis para cada tipo
        self.emojis = {
            NotificationType.INFO: "ℹ️",
            NotificationType.SUCCESS: "✅", 
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
            NotificationType.TRADE_SIGNAL: "📊",
            NotificationType.TRADE_EXECUTED: "💹",
            NotificationType.TRADE_CLOSED: "🏁"
        }
        
        # Colores para consola (códigos ANSI)
        self.colors = {
            NotificationType.INFO: "\033[94m",      # Azul
            NotificationType.SUCCESS: "\033[92m",   # Verde
            NotificationType.WARNING: "\033[93m",   # Amarillo
            NotificationType.ERROR: "\033[91m",     # Rojo
            NotificationType.TRADE_SIGNAL: "\033[96m",    # Cian
            NotificationType.TRADE_EXECUTED: "\033[95m",  # Magenta
            NotificationType.TRADE_CLOSED: "\033[90m"     # Gris
        }
        self.reset_color = "\033[0m"
    
    def notify(self, message, notification_type=NotificationType.INFO, data=None):
        """
        Envía una notificación
        
        Args:
            message: Mensaje de la notificación
            notification_type: Tipo de notificación
            data: Datos adicionales (opcional)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        emoji = self.emojis.get(notification_type, "")
        color = self.colors.get(notification_type, "")
        
        # Formatear mensaje
        formatted_message = f"[{timestamp}] {emoji} {message}"
        
        # Notificación en consola (siempre activa)
        print(f"{color}{formatted_message}{self.reset_color}")
        
        # Notificación en log
        if self.enable_file:
            if notification_type == NotificationType.ERROR:
                self.logger.error(f"{message} | Data: {data}")
            elif notification_type == NotificationType.WARNING:
                self.logger.warning(f"{message} | Data: {data}")
            elif notification_type in [NotificationType.TRADE_SIGNAL, NotificationType.TRADE_EXECUTED]:
                self.logger.info(f"TRADING: {message} | Data: {data}")
            else:
                self.logger.info(f"{message} | Data: {data}")
        
        # Sonido del sistema (opcional)
        if self.enable_sound:
            self._play_sound(notification_type)
    
    def _play_sound(self, notification_type):
        """Reproduce sonido según el tipo de notificación"""
        try:
            if notification_type == NotificationType.ERROR:
                # Sonido de error
                print("\a\a")  # Doble beep
            elif notification_type in [NotificationType.TRADE_EXECUTED, NotificationType.SUCCESS]:
                # Sonido de éxito
                print("\a")  # Un beep
            elif notification_type == NotificationType.WARNING:
                # Sonido de advertencia
                print("\a")
        except:
            pass  # Ignorar errores de sonido
    
    def trade_signal(self, symbol, signal_type, confidence, price, reason=""):
        """Notificación especializada para señales de trading"""
        signal_emoji = "🔼" if signal_type.upper() == "BUY" else "🔽"
        confidence_bar = "█" * int(confidence * 10) + "░" * (10 - int(confidence * 10))
        
        message = f"SEÑAL {signal_type.upper()} | {symbol} @ {price}"
        details = f"Confianza: {confidence:.1%} [{confidence_bar}]"
        if reason:
            details += f" | {reason}"
        
        self.notify(message, NotificationType.TRADE_SIGNAL, details)
        print(f"    └─ {details}")
    
    def trade_executed(self, symbol, order_type, volume, price, sl=None, tp=None):
        """Notificación especializada para trades ejecutados"""
        message = f"TRADE EJECUTADO | {order_type} {volume} {symbol} @ {price}"
        details = {
            'symbol': symbol,
            'type': order_type,
            'volume': volume,
            'price': price,
            'sl': sl,
            'tp': tp
        }
        
        self.notify(message, NotificationType.TRADE_EXECUTED, details)
        if sl:
            print(f"    ├─ Stop Loss: {sl}")
        if tp:
            print(f"    └─ Take Profit: {tp}")
    
    def trade_closed(self, symbol, result, profit, duration=""):
        """Notificación especializada para trades cerrados"""
        result_emoji = "💰" if profit > 0 else "💸" if profit < 0 else "⚖️"
        message = f"TRADE CERRADO | {symbol} {result_emoji} {profit:+.2f} USD"
        details = f"Resultado: {result} | Duración: {duration}"
        
        self.notify(message, NotificationType.TRADE_CLOSED, details)
    
    def system_status(self, status, details=""):
        """Notificación de estado del sistema"""
        if status == "STARTED":
            self.notify(f"🚀 SMC-LIT Bot iniciado | {details}", NotificationType.SUCCESS)
        elif status == "STOPPED":
            self.notify(f"🛑 SMC-LIT Bot detenido | {details}", NotificationType.INFO)
        elif status == "ERROR":
            self.notify(f"💥 Error del sistema | {details}", NotificationType.ERROR)
        elif status == "CONNECTED":
            self.notify(f"🔗 Conectado a MT5 | {details}", NotificationType.SUCCESS)
        elif status == "DISCONNECTED":
            self.notify(f"🔌 Desconectado de MT5 | {details}", NotificationType.WARNING)
    
    def market_analysis(self, symbol, trend, sentiment, volatility):
        """Notificación de análisis de mercado"""
        trend_emoji = "📈" if trend > 0 else "📉" if trend < 0 else "📊"
        message = f"ANÁLISIS | {symbol} {trend_emoji}"
        details = f"Tendencia: {trend:.3f} | Sentimiento: {sentiment:.3f} | Volatilidad: {volatility:.3f}"
        
        self.notify(message, NotificationType.INFO, details)

# Instancia global del gestor de notificaciones
notifier = NotificationManager(
    enable_sound=os.getenv('ENABLE_SOUND_NOTIFICATIONS', 'false').lower() == 'true',
    enable_file=os.getenv('ENABLE_FILE_NOTIFICATIONS', 'true').lower() == 'true'
) 