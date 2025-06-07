#!/usr/bin/env python3
# Dashboard Local Simple - Puerto 5002
# ====================================

import sqlite3
import json
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
    <title>📊 Dashboard Local - Bot SMC-LIT</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0a0a0a; color: #fff; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; }
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
        .refresh-btn { background: #667eea; border: none; color: white; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Dashboard Local - Bot SMC-LIT</h1>
        <p>Puerto 5002 - Operaciones Locales</p>
    </div>
    
    <div class="container">
        <div class="metrics" id="metrics">
            <!-- Métricas se cargarán aquí -->
        </div>
        
        <button class="refresh-btn" onclick="refreshData()">🔄 Actualizar</button>
        
        <div class="trades-table">
            <div class="table-header">
                📈 Últimas Operaciones Locales
            </div>
            <div id="trades-list">
                <!-- Operaciones se cargarán aquí -->
            </div>
        </div>
    </div>

    <script>
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
                        <div class="metric-value">$${data.balance.toFixed(2)}</div>
                        <div class="metric-label">Balance</div>
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
                        <div>${trade.source}</div>
                    </div>
                `).join('');
                
                document.getElementById('trades-list').innerHTML = tradesHtml;
            } catch (error) {
                console.error('Error loading trades:', error);
            }
        }
        
        function refreshData() {
            loadMetrics();
            loadTrades();
        }
        
        // Cargar datos al inicio
        refreshData();
        
        // Auto-refresh cada 30 segundos
        setInterval(refreshData, 30000);
    </script>
</body>
</html>
'''

def get_local_trades():
    """Obtener operaciones locales"""
    try:
        # Priorizar base de datos de trading real del bot
        databases = ['local_real_trades.db', 'real_executions.db', 'trading_bot.db', 'real_profits.db', 'unified_trading.db']
        
        for db_name in databases:
            try:
                conn = sqlite3.connect(db_name)
                cursor = conn.cursor()
                
                # Intentar diferentes esquemas de tabla
                tables = ['real_trades', 'real_executions', 'trades', 'operations', 'real_profits', 'trading_operations']
                
                for table in tables:
                    try:
                        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                        if cursor.fetchone():
                            cursor.execute(f"SELECT * FROM {table} ORDER BY id DESC LIMIT 50")
                            rows = cursor.fetchall()
                            
                            # Obtener nombres de columnas
                            cursor.execute(f"PRAGMA table_info({table})")
                            columns = [col[1] for col in cursor.fetchall()]
                            
                            trades = []
                            for row in rows:
                                trade_data = dict(zip(columns, row))
                                
                                # Normalizar formato
                                trade = {
                                    'symbol': trade_data.get('symbol', trade_data.get('pair', 'UNKNOWN')),
                                    'type': trade_data.get('action', trade_data.get('trade_type', trade_data.get('type', 'UNKNOWN'))),
                                    'profit': float(trade_data.get('profit', trade_data.get('profit_usd', trade_data.get('pnl', 0)))),
                                    'timestamp': trade_data.get('timestamp', trade_data.get('created_at', 'Unknown')),
                                    'source': 'LOCAL_BOT_REAL' if db_name == 'local_real_trades.db' else 'LOCAL'
                                }
                                trades.append(trade)
                            
                            conn.close()
                            return trades
                            
                    except sqlite3.Error:
                        continue
                
                conn.close()
                
            except sqlite3.Error:
                continue
        
        return []
        
    except Exception as e:
        print(f"Error obteniendo trades: {e}")
        return []

def get_local_metrics():
    """Calcular métricas locales"""
    trades = get_local_trades()
    
    if not trades:
        return {
            'total_trades': 0,
            'total_profit': 0.0,
            'win_rate': 0.0,
            'balance': 3000.0
        }
    
    total_trades = len(trades)
    total_profit = sum(trade['profit'] for trade in trades)
    winning_trades = sum(1 for trade in trades if trade['profit'] > 0)
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
    balance = 3000.0 + total_profit
    
    return {
        'total_trades': total_trades,
        'total_profit': total_profit,
        'win_rate': win_rate,
        'balance': balance
    }

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/metrics')
def api_metrics():
    return jsonify(get_local_metrics())

@app.route('/api/trades')
def api_trades():
    return jsonify(get_local_trades())

if __name__ == '__main__':
    print("📊 DASHBOARD LOCAL INICIADO")
    print("=" * 40)
    print("🌐 URL: http://localhost:5002")
    print("📊 Datos: Solo operaciones locales")
    print("=" * 40)
    
    app.run(host='0.0.0.0', port=5002, debug=False) 