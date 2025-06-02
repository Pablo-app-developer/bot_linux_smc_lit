# 🚀 Guía de Despliegue - Bot SMC-LIT en VPS Ubuntu con XFCE

## 📋 Prerequisitos en la VPS

### 1. Actualizar el sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Python 3.8+ y herramientas
```bash
sudo apt install python3 python3-pip python3-venv git wget curl -y
```

### 3. Verificar versión de Python
```bash
python3 --version  # Debe ser 3.8 o superior
```

## 📦 Transferir archivos del bot

### Opción A: Usar git (recomendado)
```bash
cd /home/ubuntu  # o tu directorio home
git clone <tu-repositorio> bot-smc-lit
cd bot-smc-lit
```

### Opción B: Transferir archivos con scp
```bash
# Desde tu máquina local:
scp -r bot-smc-lit/ usuario@tu-vps-ip:/home/ubuntu/
```

### Opción C: Comprimir y transferir
```bash
# Desde tu máquina local:
tar -czf bot-smc-lit.tar.gz bot-smc-lit/
scp bot-smc-lit.tar.gz usuario@tu-vps-ip:/home/ubuntu/

# En la VPS:
tar -xzf bot-smc-lit.tar.gz
```

## 🔧 Configuración del entorno

### 1. Crear entorno virtual
```bash
cd bot-smc-lit
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configurar credenciales
```bash
# Crear archivo .env con tus credenciales reales
nano .env
```

Contenido del `.env`:
```bash
# === CREDENCIALES METATRADER 5 ===
MT5_LOGIN=164675960
MT5_PASSWORD=pfbc0en
MT5_SERVER=MetaQuotes-Demo

# === CONFIGURACIÓN DE TRADING ===
SYMBOL=EURUSD
TIMEFRAME=M5
RISK_PERCENT=1.0
MAX_TRADES=5

# === NOTIFICACIONES ===
ENABLE_CONSOLE_NOTIFICATIONS=true
ENABLE_FILE_LOGGING=true
```

## 🖥️ Configuración para XFCE

### 1. Instalar herramientas gráficas (opcional)
```bash
sudo apt install xfce4-terminal firefox -y
```

### 2. Crear script de inicio
```bash
nano start_bot_vps.sh
```

Contenido del script:
```bash
#!/bin/bash
cd /home/ubuntu/bot-smc-lit
source .venv/bin/activate
python start_bot.py
```

### 3. Hacer ejecutable el script
```bash
chmod +x start_bot_vps.sh
```

## 🔄 Crear servicio systemd (auto-start)

### 1. Crear archivo de servicio
```bash
sudo nano /etc/systemd/system/smc-lit-bot.service
```

Contenido del servicio:
```ini
[Unit]
Description=SMC-LIT Trading Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/bot-smc-lit
Environment=PATH=/home/ubuntu/bot-smc-lit/.venv/bin
ExecStart=/home/ubuntu/bot-smc-lit/.venv/bin/python start_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Habilitar y iniciar el servicio
```bash
sudo systemctl daemon-reload
sudo systemctl enable smc-lit-bot.service
sudo systemctl start smc-lit-bot.service
```

### 3. Verificar estado del servicio
```bash
sudo systemctl status smc-lit-bot.service
```

## 📊 Monitoreo y Logs

### 1. Ver logs del bot
```bash
# Logs del servicio systemd
sudo journalctl -u smc-lit-bot.service -f

# Logs del archivo del bot
tail -f /home/ubuntu/bot-smc-lit/smc_lit_bot_*.log
```

### 2. Comandos útiles del servicio
```bash
# Detener el bot
sudo systemctl stop smc-lit-bot.service

# Reiniciar el bot
sudo systemctl restart smc-lit-bot.service

# Deshabilitar auto-start
sudo systemctl disable smc-lit-bot.service
```

## 🖥️ Ejecución manual en XFCE

### 1. Abrir terminal en XFCE
- Presiona `Ctrl+Alt+T` o usa el menú Applications > Terminal

### 2. Ejecutar el bot manualmente
```bash
cd bot-smc-lit
source .venv/bin/activate
python start_bot.py
```

### 3. Crear acceso directo en escritorio (opcional)
```bash
nano ~/Desktop/SMC-LIT-Bot.desktop
```

Contenido:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=SMC-LIT Bot
Comment=Algorithmic Trading Bot
Exec=/home/ubuntu/bot-smc-lit/start_bot_vps.sh
Icon=applications-science
Terminal=true
Categories=Office;
```

```bash
chmod +x ~/Desktop/SMC-LIT-Bot.desktop
```

## 🔒 Seguridad y mejores prácticas

### 1. Configurar firewall
```bash
sudo ufw enable
sudo ufw allow ssh
sudo ufw allow 443  # HTTPS si usas APIs web
```

### 2. Configurar backup automático
```bash
# Crear script de backup
nano backup_bot.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "bot_backup_$DATE.tar.gz" bot-smc-lit/
# Opcional: subir a cloud storage
```

### 3. Monitoreo de recursos
```bash
# Instalar htop para monitoreo
sudo apt install htop -y

# Ver recursos en tiempo real
htop
```

## 📱 Configuración de notificaciones (opcional)

### 1. Para notificaciones por email
```bash
sudo apt install mailutils -y
```

### 2. Para notificaciones Telegram (agregar al .env)
```bash
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
```

## 🚀 Lista de verificación final

- [ ] ✅ Python 3.8+ instalado
- [ ] ✅ Entorno virtual creado y activado
- [ ] ✅ Dependencias instaladas
- [ ] ✅ Archivo .env configurado
- [ ] ✅ Bot funciona manualmente
- [ ] ✅ Servicio systemd configurado (opcional)
- [ ] ✅ Logs funcionando correctamente
- [ ] ✅ Acceso SSH configurado
- [ ] ✅ Firewall configurado

## 🆘 Resolución de problemas

### Error: ModuleNotFoundError
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

### Error: Permission denied
```bash
chmod +x start_bot_vps.sh
sudo chown -R ubuntu:ubuntu bot-smc-lit/
```

### Bot no inicia automáticamente
```bash
sudo systemctl status smc-lit-bot.service
sudo journalctl -u smc-lit-bot.service -n 50
```

### Verificar conexión a internet
```bash
ping google.com
curl -I https://www.google.com
```

---

## 📞 Comandos rápidos de administración

```bash
# Estado del bot
sudo systemctl status smc-lit-bot

# Reiniciar bot
sudo systemctl restart smc-lit-bot

# Ver logs en tiempo real
sudo journalctl -u smc-lit-bot -f

# Actualizar bot (si usas git)
cd bot-smc-lit
git pull
sudo systemctl restart smc-lit-bot
```

¡Tu bot SMC-LIT estará funcionando 24/7 en tu VPS! 🎯 