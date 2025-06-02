# 🤖 SMC-LIT TRADING BOT - INSTRUCCIONES COMPLETAS

## 🛡️ MODO SEGURO ACTIVADO - SIN RIESGO FINANCIERO

Este bot está configurado para operar **ÚNICAMENTE** en modo DEMO, protegiendo tu dinero real.

---

## 📋 PASOS PARA USAR EL BOT HOY

### 1. 🔧 CONFIGURAR CREDENCIALES DEMO (OBLIGATORIO)

**Primero necesitas una cuenta DEMO de MetaTrader 5:**

```bash
python3 configurar_credenciales.py
```

Este script te guiará para:
- Obtener una cuenta demo gratuita de MT5
- Configurar credenciales de forma segura
- Verificar la conexión

### 2. 🚀 INICIAR EL BOT

**Una vez configuradas las credenciales:**

```bash
python3 iniciar_bot_seguro.py
```

### 3. 📊 MONITOREAR RESULTADOS

El bot generará automáticamente:
- **Logs en tiempo real**: `*.log`
- **Resultados CSV**: `*.csv` 
- **Gráficos de rendimiento**: `*.png`

---

## 🎯 CONFIGURACIÓN ACTUAL DEL BOT

### 💰 CONFIGURACIÓN FINANCIERA
- **Capital virtual**: $1,000 USD (no real)
- **Riesgo por operación**: 0.5% (máximo $5 por trade)
- **Riesgo diario máximo**: 2% ($20)
- **Trades máximos por día**: 10
- **Drawdown máximo**: 5%

### 📈 CONFIGURACIÓN DE TRADING  
- **Símbolo principal**: EURUSD
- **Timeframe**: M5 (5 minutos)
- **Horario**: 08:00 - 18:00 UTC
- **Días**: Lunes a Viernes

### 🎯 PARÁMETROS OPTIMIZADOS
El bot usa parámetros optimizados por IA:
- **BOS threshold**: 0.0003
- **CHOCH threshold**: 0.0005  
- **Liquidity threshold**: 0.0004
- **RSI period**: 14
- **ATR multiplier**: 2.0
- **Risk/Reward mínimo**: 1.5
- **Probabilidades SMC**: 65%-80%

---

## 📊 VERIFICACIÓN DE RENDIMIENTO

### 🧪 EJECUTAR BACKTEST DE PRUEBA
```bash
python3 quick_backtest.py
```

### 📈 RESULTADOS ESPERADOS (HISTÓRICOS)
Basado en optimizaciones previas:
- **Win Rate objetivo**: 75-85%
- **Profit Factor**: >1.5
- **Sharpe Ratio**: >1.0
- **Max Drawdown**: <5%

---

## 🌐 DESPLIEGUE AL VPS (OPCIONAL)

Para ejecutar el bot 24/7 en tu VPS:

```bash
python3 deploy_a_vps.py
```

**Información del VPS:**
- **IP**: 107.174.133.202
- **Usuario**: root  
- **Contraseña**: n5X5dB6xPLJj06qr4C

---

## 🔍 COMANDOS DE MONITOREO

### Ver logs en tiempo real:
```bash
tail -f *.log
```

### Ver estadísticas:
```bash
python3 -c "
from config_seguro import CONFIGURACION_SEGURA
print('📊 CONFIGURACIÓN ACTUAL:')
for k, v in CONFIGURACION_SEGURA.items():
    print(f'{k}: {v}')
"
```

### Estado del mercado:
```bash
python3 -c "
from datetime import datetime
import time
now = datetime.now()
print(f'🕐 Hora actual: {now}')
print(f'📈 Mercado Forex: {'ABIERTO' if now.weekday() < 5 else 'CERRADO'}')
"
```

---

## ⚠️ PROTECCIONES DE SEGURIDAD

### 🛡️ VALIDACIONES AUTOMÁTICAS
- ✅ Solo cuentas DEMO permitidas
- ✅ Riesgo limitado por configuración
- ✅ Stops automáticos activados
- ✅ Monitoreo de drawdown continuo
- ✅ Validación antes de cada trade

### 🚨 SEÑALES DE ALERTA
El bot se detiene automáticamente si:
- Drawdown > 5%
- Pérdidas diarias > $20
- Más de 10 trades en un día
- Error de conexión con MT5

---

## 📱 NOTIFICACIONES Y LOGS

### 📋 ARCHIVOS GENERADOS
- `smc_lit_bot_YYYYMMDD.log` - Log principal
- `backtest_results_YYYYMMDD.csv` - Resultados de backtesting  
- `optimization_results_YYYYMMDD.json` - Parámetros optimizados
- `trading_session_YYYYMMDD.csv` - Historial de trades

### 📊 MÉTRICAS MONITOREADAS
- Win Rate en tiempo real
- Profit Factor acumulado
- Sharpe Ratio del período
- Drawdown máximo
- Trades ejecutados/día
- Balance de cuenta demo

---

## 🚀 INICIO RÁPIDO (RESUMEN)

```bash
# 1. Configurar credenciales demo
python3 configurar_credenciales.py

# 2. Iniciar bot seguro  
python3 iniciar_bot_seguro.py

# 3. Monitorear en otra terminal
tail -f *.log
```

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### ❌ Error de conexión MT5
```bash
# Verificar que MT5 esté abierto y conectado
# Revisar credenciales en config_seguro.py
python3 configurar_credenciales.py
```

### ❌ Dependencias faltantes
```bash
pip install -r requirements.txt
```

### ❌ Bot no ejecuta trades
- Verificar horario de trading
- Comprobar que el mercado esté abierto
- Revisar logs para errores específicos

---

## 📞 VERIFICACIÓN FINAL

### ✅ CHECKLIST ANTES DE INICIAR
- [ ] MetaTrader 5 instalado y abierto
- [ ] Cuenta DEMO configurada
- [ ] Credenciales configuradas con `configurar_credenciales.py`
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Configuración segura verificada

### ✅ VERIFICACIÓN POST-INICIO
- [ ] Bot muestra "MODO SEGURO ACTIVADO"
- [ ] Logs se generan correctamente
- [ ] No hay errores de conexión
- [ ] Balance inicial = $1,000 USD (virtual)

---

## 🏆 EXPECTATIVAS REALISTAS

### 📈 RENDIMIENTO ESPERADO (DEMO)
- **Trades por día**: 3-8 (promedio 5)
- **Win Rate**: 70-80% (optimizado)
- **Ganancia diaria promedio**: $10-30 (virtual)
- **Drawdown típico**: 1-3%

### ⏱️ TIEMPO DE EJECUCIÓN
- **Análisis por vela**: <1 segundo
- **Decisión de trade**: <3 segundos  
- **Ejecución de orden**: <5 segundos
- **Optimización automática**: 1 vez/día

---

## 🎯 OBJETIVOS DEL SISTEMA

1. **Demostrar eficacia** del algoritmo SMC-LIT
2. **Validar parámetros optimizados** en tiempo real
3. **Generar estadísticas** para análisis 
4. **Probar estabilidad** del sistema 24/7
5. **Preparar para trading real** (cuando estés listo)

---

**🚨 IMPORTANTE: Este bot está configurado para NO usar dinero real. Todas las operaciones son virtuales en cuenta demo.**

**💡 Una vez que veas resultados consistentes en demo durante semanas/meses, podrás considerar pasar a trading real con supervisión.** 