# 🎛️ **GUÍA COMPLETA - CONFIGURACIÓN Y CONTROL DEL BOT SMC-LIT**

## ✅ **ESTADO ACTUAL: SISTEMA COMPLETO FUNCIONANDO**

### 🎯 **UBICACIÓN DE CONFIGURACIONES Y MODOS**

#### **1. 🔧 Panel de Control Principal**
**Archivo:** `panel_control_bot.py`
```bash
python3 panel_control_bot.py
```

**Funciones disponibles:**
- 🔧 **Configurar Parámetros de Trading**
- 🎯 **Seleccionar Modo de Operación** 
- 💰 **Configurar Gestión de Riesgo**
- 📊 **Configurar Indicadores SMC**
- 🚀 **Desplegar al VPS automáticamente**
- 📈 **Ver Estado del Bot en VPS**
- 🔄 **Reiniciar Bot en VPS**

#### **2. 📊 Parámetros de Trading**
**Ubicación:** Panel de Control → Opción 1

**Configurables:**
- **Símbolos:** EURUSD, GBPUSD, USDJPY, AUDUSD, USDCAD, USDCHF
- **Timeframes:** M1, M5, M15, M30, H1, H4, D1
- **Riesgo por trade:** 0.1% - 10% de la cuenta
- **Max trades diarios:** 1 - 200 operaciones

#### **3. 🎯 Modos de Operación**
**Ubicación:** Panel de Control → Opción 2

**Modos disponibles:**
1. **🛡️ Conservador:** Bajo riesgo, operaciones espaciadas
2. **⚖️ Balanceado:** Riesgo moderado, frecuencia media
3. **⚡ Agresivo:** Alto rendimiento, mayor frecuencia
4. **🚀 Sin Limitaciones:** Máximo rendimiento
5. **🎯 Scalping:** Alta frecuencia, trades rápidos

#### **4. 💰 Gestión de Riesgo**
**Ubicación:** Panel de Control → Opción 3

**Configurables:**
- **Stop Loss:** 5-100 pips
- **Take Profit:** 10-200 pips
- **Trailing Stop:** Activar/Desactivar
- **Max Drawdown:** 5%-50%

#### **5. 📊 Indicadores SMC**
**Ubicación:** Panel de Control → Opción 4

**Configurables:**
- **BOS Threshold:** 0.0001 - 0.001
- **CHoCH Threshold:** 0.0001 - 0.001
- **Liquidity Threshold:** 0.0001 - 0.001
- **RSI Oversold:** 20-40
- **RSI Overbought:** 60-80

---

## 🚀 **CONFIGURACIÓN ACTUAL ACTIVA**

### **📊 Configuración Desplegada:**
```json
{
  "symbol": "GBPUSD",
  "timeframe": "M1", 
  "risk_per_trade": 0.5,
  "max_daily_trades": 50,
  "mode": "scalping",
  "demo_mode": true,
  "aggressive": true,
  "scalping": true,
  "high_frequency": true
}
```

### **🤖 Bot Activo en VPS:**
- **Estado:** ✅ FUNCIONANDO
- **Versión:** 2.0 con configuración dinámica
- **Proceso:** `main_unlimited_v2.py`
- **Screen:** `smc-bot-v2-venv`
- **Configuración:** Carga desde `config_bot_activo.json`

---

## 🔄 **FLUJO DE ACTUALIZACIÓN COMPLETO**

### **Paso 1: Configurar Parámetros**
```bash
python3 panel_control_bot.py
```
1. Seleccionar opción 1-4 para configurar
2. Guardar configuración (opción 8)
3. Ver configuración actual (opción 9)

### **Paso 2: Desplegar Automáticamente**
```bash
# Desde el panel de control:
# Opción 5: 🚀 Desplegar al VPS
```

**El sistema automáticamente:**
1. ✅ Genera archivo `config_bot_activo.json`
2. ✅ Sube configuración al VPS
3. ✅ Detiene bot anterior
4. ✅ Inicia bot con nueva configuración

### **Paso 3: Verificar Estado**
```bash
# Desde el panel de control:
# Opción 6: 📈 Estado del Bot en VPS
# Opción 7: 🔄 Reiniciar Bot en VPS
```

---

## 📁 **ARCHIVOS DE CONFIGURACIÓN**

### **Archivos Principales:**
1. **`panel_control_bot.py`** - Panel de control principal
2. **`main_unlimited_v2.py`** - Bot versión 2.0
3. **`config_bot_activo.json`** - Configuración activa
4. **`config_trading_real.py`** - Configuración para trading real
5. **`src/mt5_simulator.py`** - Simulador MT5

### **Archivos Generados:**
- **`config_bot_YYYYMMDD_HHMMSS.json`** - Backups de configuración
- **`session_stats.json`** - Estadísticas de sesión
- **`bot_status.json`** - Estado del bot

---

## 🎛️ **COMANDOS DIRECTOS DE CONTROL**

### **Configurar y Desplegar:**
```bash
# 1. Panel de control completo
python3 panel_control_bot.py

# 2. Configuración manual
python3 config_trading_real.py

# 3. Bot local para pruebas
python3 main_unlimited_v2.py
```

### **Control VPS:**
```bash
# Estado del bot
sshpass -p 'contraseña' ssh root@107.174.133.202 'ps aux | grep main_unlimited_v2'

# Reiniciar bot
sshpass -p 'contraseña' ssh root@107.174.133.202 'cd /home/smc-lit-bot && pkill -f main_unlimited_v2.py && source venv/bin/activate && screen -dmS smc-bot python3 main_unlimited_v2.py'

# Ver sesión activa
sshpass -p 'contraseña' ssh root@107.174.133.202 'screen -ls'
```

---

## 🎯 **CONFIGURACIONES RECOMENDADAS**

### **Para Principiantes:**
- **Modo:** Conservador
- **Símbolo:** EURUSD
- **Timeframe:** M5
- **Riesgo:** 0.5%
- **Cuenta:** DEMO

### **Para Trading Agresivo:**
- **Modo:** Scalping
- **Símbolo:** GBPUSD
- **Timeframe:** M1
- **Riesgo:** 2.0%
- **Cuenta:** DEMO

### **Para Máximo Rendimiento:**
- **Modo:** Sin Limitaciones
- **Símbolo:** EURUSD
- **Timeframe:** M1
- **Riesgo:** 1.0%
- **Cuenta:** DEMO

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Bot no inicia:**
```bash
# Verificar dependencias en VPS
ssh root@VPS 'cd /home/smc-lit-bot && source venv/bin/activate && pip install pandas numpy'

# Subir archivos faltantes
scp -r src/ root@VPS:/home/smc-lit-bot/
```

### **Configuración no se aplica:**
```bash
# Verificar archivo de configuración
ssh root@VPS 'cat /home/smc-lit-bot/config_bot_activo.json'

# Regenerar y subir configuración
python3 panel_control_bot.py
# Seleccionar opción 5 (Desplegar)
```

### **Bot se detiene:**
```bash
# Reiniciar desde panel
python3 panel_control_bot.py
# Seleccionar opción 7 (Reiniciar)
```

---

## ✅ **RESUMEN EJECUTIVO**

**🎛️ DONDE CONFIGURAR TODO:**
- **Archivo principal:** `panel_control_bot.py`
- **Comando:** `python3 panel_control_bot.py`

**🚀 DONDE DESPLEGAR:**
- **Opción 5 del panel:** Despliegue automático al VPS
- **Actualización completa:** Configuración + Reinicio

**📊 DONDE VER ESTADO:**
- **Opción 6 del panel:** Estado en tiempo real
- **Archivo local:** Configuración guardada

**El sistema está completamente funcional y automatizado. Puedes cambiar cualquier parámetro desde el panel de control y desplegarlo automáticamente al VPS.** 🎉 