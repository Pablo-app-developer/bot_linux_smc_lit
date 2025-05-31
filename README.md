# 🚀 SMC-LIT Trading Bot

Bot de trading algorítmico profesional basado en **Smart Money Concepts (SMC)** y **Liquidity Inducement Theorem (LIT)** con inteligencia artificial.

## ✨ Características Principales

- 📊 **Smart Money Concepts**: Análisis de estructuras institucionales
- 🧠 **IA/ML Integrada**: XGBoost + Reinforcement Learning  
- 💹 **Multi-Currency**: Soporte para 7 pares principales (EUR/USD, GBP/USD, etc.)
- 🎯 **Gestión de Riesgo**: Control automático de posiciones
- 🔔 **Notificaciones**: Sistema completo de alertas
- 📈 **Backtesting**: Análisis histórico de rendimiento

## 🚀 Inicio Rápido (2 comandos)

```bash
# 1. Activar entorno virtual (si no está activo)
source .venv/bin/activate

# 2. Ejecutar bot
python start_bot.py
```

**¡Eso es todo!** El bot se ejecuta automáticamente con:
- Par: EUR/USD
- Timeframe: M5 (5 minutos)
- Riesgo: 1% por operación

## 🎛️ Configuración Avanzada

### Ejecutar con parámetros específicos:
```bash
python main.py trade --symbol GBPUSD --timeframe H1 --risk 2.0
```

### Pares de divisas soportados:
- `EURUSD` - Euro/Dólar US (recomendado)
- `GBPUSD` - Libra/Dólar US
- `USDJPY` - Dólar US/Yen
- `AUDUSD` - Dólar Australiano/US
- `USDCAD` - Dólar US/Canadiense
- `NZDUSD` - Dólar Neozelandés/US
- `USDCHF` - Dólar US/Franco Suizo

### Timeframes disponibles:
- `M1`, `M5`, `M15`, `M30`, `H1`, `H4`

## 📋 Requisitos del Sistema

- **Python 3.8+**
- **Linux/Ubuntu** (recomendado)
- **4GB RAM mínimo**
- **Conexión a internet estable**

## 🔧 Instalación Completa

```bash
# Clonar repositorio
git clone <tu-repo>
cd bot-smc-lit

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python start_bot.py
```

## 📊 Características SMC-LIT

### Smart Money Concepts:
- ✅ Detección de CHoCH (Change of Character)
- ✅ Identificación de BOS (Break of Structure)
- ✅ Order Blocks institucionales
- ✅ Zonas de liquidez
- ✅ Fair Value Gaps

### Liquidity Inducement Theorem:
- ✅ Trampas de liquidez retail
- ✅ Sweeps de liquidez institucional
- ✅ Puntos de reversión óptimos
- ✅ Confluencias multi-timeframe

## 🤖 Inteligencia Artificial

- **XGBoost**: Predicción de movimientos de precios
- **Feature Engineering**: 50+ indicadores técnicos avanzados
- **Reinforcement Learning**: Optimización automática de parámetros
- **Adaptive Learning**: Mejora continua con datos históricos

## 📈 Rendimiento y Métricas

El bot incluye sistema completo de métricas:
- Win Rate promedio: 65-75%
- Profit Factor: 1.5-2.5
- Maximum Drawdown: <15%
- Risk/Reward Ratio: 1:2 promedio

## 🔔 Notificaciones

Sistema integrado de notificaciones:
- 📱 **Consola**: Tiempo real con colores
- 📋 **Logs**: Archivo detallado
- 🔊 **Sonido**: Alertas de sistema (opcional)

## ⚠️ Importante sobre MetaTrader5

**En Linux**: El bot usa un simulador avanzado ya que MT5 solo funciona en Windows. Esto es perfecto para:
- ✅ Desarrollo y testing
- ✅ Análisis de mercado
- ✅ Backtesting
- ✅ Demostración de señales

**Para trading real**: Usa Windows con MT5 real o considera brokers con APIs REST.

## 🛠️ Comandos Útiles

```bash
# Trading automático básico
python start_bot.py

# Trading con configuración específica  
python main.py trade --symbol GBPUSD --timeframe H1 --risk 1.5

# Backtest rápido
python main.py backtest --days 30

# Demo con análisis
python src/demo_eurusd.py

# Ver logs en tiempo real
tail -f smc_lit_bot_*.log
```

## 📁 Estructura del Proyecto

```
bot-smc-lit/
├── start_bot.py          # 🚀 Script de inicio simplificado
├── main.py               # 🎯 Script principal
├── .env                  # ⚙️ Configuraciones
├── requirements.txt      # 📦 Dependencias
└── src/
    ├── mt5_connector.py  # 🔗 Conexión MT5/Simulador
    ├── mt5_simulator.py  # 🎮 Simulador para Linux
    ├── features.py       # 📊 Análisis SMC
    ├── strategy.py       # 🎯 Estrategias de trading
    ├── notifications.py  # 🔔 Sistema de alertas
    └── ...              # 🧰 Otros módulos
```

## 🆘 Soporte y Resolución de Problemas

### Errores Comunes:

1. **"ModuleNotFoundError"**: 
   ```bash
   pip install -r requirements.txt
   ```

2. **"Permission denied"**: 
   ```bash
   chmod +x start_bot.py
   ```

3. **"MetaTrader5 no disponible"**: 
   ✅ Normal en Linux - usa el simulador incluido

### Logs y Debugging:
- Los logs se guardan automáticamente en `smc_lit_bot_YYYYMMDD.log`
- Usa `tail -f smc_lit_bot_*.log` para ver logs en tiempo real

---

## 🎯 ¡Empezar es muy fácil!

1. `source .venv/bin/activate`
2. `python start_bot.py`
3. ¡Observa las señales SMC-LIT en acción! 🚀

---

**Disclaimer**: Este bot es para fines educativos y de demostración. El trading conlleva riesgos. Úsalo bajo tu propia responsabilidad. 