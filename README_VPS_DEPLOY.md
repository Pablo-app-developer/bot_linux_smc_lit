# 🚀 **GUÍA RÁPIDA - DEPLOY VPS BOT SMC-LIT v2.0**

## ⚡ **DEPLOY EN 3 PASOS**

### **📋 REQUISITOS:**
- VPS Ubuntu/Debian con acceso root
- Python 3.8+ instalado
- 2GB RAM mínimo
- 10GB espacio libre

---

## 🎯 **MÉTODO 1: DEPLOY AUTOMÁTICO**

### **1️⃣ Subir archivos al VPS:**
```bash
# En tu PC local
scp -r * usuario@tu-vps-ip:/tmp/bot-smc-lit/

# En el VPS
sudo mv /tmp/bot-smc-lit /opt/
cd /opt/bot-smc-lit
```

### **2️⃣ Ejecutar deploy automático:**
```bash
sudo python3 deploy_vps_final.py
```

### **3️⃣ ¡LISTO! Bot funcionando 24/7:**
```bash
# Ver estado
sudo systemctl status smc-lit-bot

# Ver logs en tiempo real
sudo journalctl -u smc-lit-bot -f
```

---

## 🛠️ **MÉTODO 2: DEPLOY MANUAL**

### **1️⃣ Instalar dependencias:**
```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y Git
sudo apt install python3 python3-pip python3-venv git -y

# Crear directorio
sudo mkdir -p /opt/bot_smc_lit_v2
cd /opt/bot_smc_lit_v2
```

### **2️⃣ Configurar entorno:**
```bash
# Copiar archivos (método que prefieras)
# Luego:
sudo python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### **3️⃣ Crear servicio systemd:**
```bash
sudo nano /etc/systemd/system/smc-lit-bot.service
```

**Contenido del archivo:**
```ini
[Unit]
Description=SMC-LIT Trading Bot v2.0 (Auto Mode)
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=10
User=root
WorkingDirectory=/opt/bot_smc_lit_v2
ExecStart=/opt/bot_smc_lit_v2/.venv/bin/python /opt/bot_smc_lit_v2/start_auto_mode.py
StandardOutput=journal
StandardError=journal
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```

### **4️⃣ Activar servicio:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable smc-lit-bot
sudo systemctl start smc-lit-bot
```

---

## 📊 **COMANDOS DE MONITOREO**

### **🔍 Estado del bot:**
```bash
sudo systemctl status smc-lit-bot
```

### **📝 Ver logs:**
```bash
# Logs en tiempo real
sudo journalctl -u smc-lit-bot -f

# Últimas 100 líneas
sudo journalctl -u smc-lit-bot -n 100

# Logs de hoy
sudo journalctl -u smc-lit-bot --since today
```

### **🔄 Control del servicio:**
```bash
# Reiniciar
sudo systemctl restart smc-lit-bot

# Detener
sudo systemctl stop smc-lit-bot

# Iniciar
sudo systemctl start smc-lit-bot

# Deshabilitar
sudo systemctl disable smc-lit-bot
```

---

## 🎯 **CARACTERÍSTICAS ACTIVADAS**

✅ **Twitter:** Análisis de 7 categorías con ML  
✅ **Calendario económico:** 8 tipos de eventos con FinBERT  
✅ **Machine Learning:** 12 características, aprendizaje continuo  
✅ **NASDAQ & S&P 500:** Trading especializado  
✅ **Modo automático:** Sin intervención manual  
✅ **Reinicio automático:** En caso de error  
✅ **Logs completos:** Monitoreo total  

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **❌ Bot no inicia:**
```bash
# Verificar logs
sudo journalctl -u smc-lit-bot -n 50

# Verificar permisos
sudo chown -R root:root /opt/bot_smc_lit_v2
sudo chmod +x /opt/bot_smc_lit_v2/start_auto_mode.py

# Probar manualmente
cd /opt/bot_smc_lit_v2
sudo .venv/bin/python start_auto_mode.py
```

### **❌ Dependencias faltantes:**
```bash
cd /opt/bot_smc_lit_v2
sudo .venv/bin/pip install -r requirements.txt
```

### **❌ Memoria insuficiente:**
```bash
# Crear swap de 2GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 📈 **RENDIMIENTO ESPERADO**

### **💾 Uso de recursos:**
- **RAM:** 200-500MB
- **CPU:** 5-15%
- **Disco:** 500MB-1GB
- **Red:** 1-5MB/día

### **📊 Actividad:**
- **Análisis Twitter:** Cada 15 minutos
- **Calendario económico:** Cada 30 minutos
- **Trading:** Continuo (30-60 segundos)
- **ML:** Aprendizaje continuo

---

## 🎉 **¡BOT FUNCIONANDO!**

Una vez desplegado, el bot estará:

🔄 **Funcionando 24/7** sin intervención  
📊 **Analizando** Twitter + Calendario económico  
🧠 **Aprendiendo** con Machine Learning  
📈 **Trading** NASDAQ, S&P 500 y Forex  
📝 **Generando logs** completos  

**Ver en tiempo real:**
```bash
sudo journalctl -u smc-lit-bot -f
```

---

**🚀 Bot SMC-LIT v2.0 - Production Ready** 