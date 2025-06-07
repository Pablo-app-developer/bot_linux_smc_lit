#!/usr/bin/env python3
# Dashboard VPS Simple - Puerto 5003
# ==================================

import sqlite3
import json
import paramiko
from flask import Flask, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Template HTML integrado
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌐 Dashboard VPS - Bot SMC-LIT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #fff; }
        .header { background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%); padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric-card { background: #1a1a1a; border: 1px solid #333; border-radius: 10px; padding: 20px; text-align: center; }
        .metric-value { font-size: 2.5em; font-weight: bold; margin: 10px 0; }
        .metric-label { color: #aaa; font-size: 0.9em; }
        .trades-table { background: #1a1a1a; border-radius: 10px; overflow: hidden; }
        .table-header { background: #333; padding: 15px; font-weight: bold; }
        .trade-row { padding: 10px 15px; border-bottom: 1px solid #333; display: grid; grid-template-columns: 1fr 1fr 1fr 1fr 1fr 1fr; gap: 10px; }
        .profit { color: #4caf50; }
        .loss { color: #f44336; }
        .refresh-btn { background: #ff7e5f; border: none; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 20px 0; }
        .vps-status { background: #2a2a2a; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
        .status-online { color: #4caf50; }
        .status-offline { color: #f44336; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Dashboard VPS - Bot SMC-LIT</h1>
        <p>Puerto 5003 - Operaciones VPS (107.174.133.202)</p>
    </div>
    
    <div class="container">
        <div class="vps-status" id="vps-status">
            <!-- Estado VPS se cargará aquí -->
        </div>
        
        <div class="metrics" id="metrics">
            <!-- Métricas se cargarán aquí -->
        </div>
        
        <button class="refresh-btn" onclick="refreshData()">🔄 Actualizar VPS</button>
        
        <div class="trades-table">
            <div class="table-header">
                🌐 Últimas Operaciones VPS
            </div>
            <div id="trades-list">
                <!-- Operaciones se cargarán aquí -->
            </div>
        </div>
    </div>

    <script>
        async function loadVPSStatus() {
            try {
                const response = await fetch('/api/vps-status');
                const data = await response.json();
                
                document.getElementById('vps-status').innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>Estado VPS:</strong> 
                            <span class="${data.status === 'online' ? 'status-online' : 'status-offline'}">
                                ${data.status === 'online' ? '🟢 ONLINE' : '🔴 OFFLINE'}
                            </span>
                        </div>
                        <div>
                            <strong>Última actualización:</strong> ${data.last_update}
                        </div>
                    </div>
                `;
            } catch (error) {
                console.error('Error loading VPS status:', error);
            }
        }
        
        async function loadMetrics() {
            try {
                const response = await fetch('/api/metrics');
                const data = await response.json();
                
                document.getElementById('metrics').innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">${data.total_trades}</div>
                        <div class="metric-label">Total Operaciones</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$${data.total_profit.toFixed(2)}</div>
                        <div class="metric-label">Profit Total</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${data.win_rate.toFixed(1)}%</div>
                        <div class="metric-label">Win Rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${data.signals_today}</div>
                        <div class="metric-label">Señales Hoy</div>
                    </div>
                `;
            } catch (error) {
                console.error('Error loading metrics:', error);
            }
        }
        
        async function loadTrades() {
            try {
                const response = await fetch('/api/trades');
                const trades = await response.json();
                
                const tradesHtml = trades.map(trade => `
                    <div class="trade-row">
                        <div>${trade.symbol}</div>
                        <div>${trade.type}</div>
                        <div>$${trade.profit.toFixed(2)}</div>
                        <div class="${trade.profit >= 0 ? 'profit' : 'loss'}">
                            ${trade.profit >= 0 ? '✅' : '❌'}
                        </div>
                        <div>${trade.timestamp}</div>
                        <div>🌐 VPS</div>
                    </div>
                `).join('');
                
                document.getElementById('trades-list').innerHTML = tradesHtml || '<div style="padding: 20px; text-align: center;">No hay operaciones VPS disponibles</div>';
            } catch (error) {
                console.error('Error loading trades:', error);
            }
        }
        
        function refreshData() {
            loadVPSStatus();
            loadMetrics();
            loadTrades();
        }
        
        // Cargar datos al inicio
        refreshData();
        
        // Auto-refresh cada 60 segundos
        setInterval(refreshData, 60000);
    </script>
</body>
</html>
'''

class VPSDataManager:
    def __init__(self):
        self.vps_config = {
            'host': '107.174.133.202',
            'username': 'root',
            'password': 'ASDqwe123++'
        }
    
    def test_vps_connection(self):
        """Probar conexión con VPS"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.vps_config['host'],
                username=self.vps_config['username'],
                password=self.vps_config['password'],
                timeout=10
            )
            ssh.close()
            return True, "Conexión exitosa"
        except Exception as e:
            return False, str(e)
    
    def get_vps_trades(self):
        """Obtener operaciones del VPS"""
        try:
            conn = sqlite3.connect('vps_trading_history.db')
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM operations ORDER BY id DESC LIMIT 50')
            rows = cursor.fetchall()
            
            # Obtener nombres de columnas
            cursor.execute("PRAGMA table_info(operations)")
            columns = [col[1] for col in cursor.fetchall()]
            
            trades = []
            for row in rows:
                trade_data = dict(zip(columns, row))
                
                trade = {
                    'symbol': trade_data.get('symbol', trade_data.get('pair', 'UNKNOWN')),
                    'type': trade_data.get('type', trade_data.get('action', 'UNKNOWN')),
                    'profit': float(trade_data.get('profit_usd', trade_data.get('profit', 0))),
                    'timestamp': trade_data.get('timestamp', trade_data.get('created_at', 'Unknown')),
                    'source': 'VPS'
                }
                trades.append(trade)
            
            conn.close()
            return trades
            
        except Exception as e:
            print(f"Error obteniendo trades VPS: {e}")
            return []
    
    def get_vps_metrics(self):
        """Calcular métricas VPS"""
        trades = self.get_vps_trades()
        
        # Contar señales del día
        signals_today = len([t for t in trades if t['timestamp'].startswith(datetime.now().strftime('%Y-%m-%d'))])
        
        # Operaciones con profit
        profit_trades = [t for t in trades if t['profit'] != 0]
        
        if not profit_trades:
            return {
                'total_trades': len(trades),
                'total_profit': 0.0,
                'win_rate': 0.0,
                'signals_today': signals_today
            }
        
        total_profit = sum(trade['profit'] for trade in profit_trades)
        winning_trades = sum(1 for trade in profit_trades if trade['profit'] > 0)
        win_rate = (winning_trades / len(profit_trades) * 100) if profit_trades else 0
        
        return {
            'total_trades': len(profit_trades),
            'total_profit': total_profit,
            'win_rate': win_rate,
            'signals_today': signals_today
        }

vps_manager = VPSDataManager()

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/vps-status')
def api_vps_status():
    online, message = vps_manager.test_vps_connection()
    return jsonify({
        'status': 'online' if online else 'offline',
        'message': message,
        'last_update': datetime.now().strftime('%H:%M:%S')
    })

@app.route('/api/metrics')
def api_metrics():
    return jsonify(vps_manager.get_vps_metrics())

@app.route('/api/trades')
def api_trades():
    return jsonify(vps_manager.get_vps_trades())

if __name__ == '__main__':
    print("🌐 DASHBOARD VPS INICIADO")
    print("=" * 40)
    print("🌐 URL: http://localhost:5003")
    print("📊 Datos: Solo operaciones VPS")
    print("🔗 VPS: 107.174.133.202")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5003, debug=False) 