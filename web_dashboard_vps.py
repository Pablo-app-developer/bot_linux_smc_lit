#!/usr/bin/env python3
# Dashboard Web para Datos VPS - SMC-LIT Trading Analytics
# ========================================================

from flask import Flask, render_template, jsonify, request
import json
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.utils
from trading_analytics_system import TradingAnalytics
import os

app = Flask(__name__)
app.secret_key = 'smc-lit-vps-dashboard-2024'

# Usar base de datos del VPS
analytics = TradingAnalytics("vps_trading_history.db")

@app.route('/')
def dashboard():
    """Página principal del dashboard VPS"""
    return render_template('dashboard_vps.html')

@app.route('/api/metrics')
def get_metrics():
    """API para obtener métricas de rendimiento del VPS"""
    try:
        metrics = analytics.calculate_metrics()
        if 'error' not in metrics:
            # Agregar información VPS
            metrics['data_source'] = 'VPS'
            metrics['vps_ip'] = '107.174.133.202'
        return jsonify(metrics)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/trades')
def get_trades():
    """API para obtener historial de operaciones del VPS"""
    try:
        limit = request.args.get('limit', 50, type=int)
        
        # Usar la conexión directa para obtener los datos
        conn = sqlite3.connect(analytics.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, symbol, type, entry_price, exit_price, lot_size, 
                   profit, status, entry_time, exit_time, comment
            FROM trades 
            ORDER BY id DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convertir a formato JSON
        trades = []
        for row in rows:
            trades.append({
                'id': row[0],
                'symbol': row[1],
                'type': row[2],
                'entry_price': row[3],
                'exit_price': row[4],
                'lot_size': row[5],
                'profit': row[6],
                'status': row[7] if row[7] else 'OPEN',
                'entry_time': row[8],
                'exit_time': row[9],
                'comment': row[10]
            })
        
        return jsonify(trades)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/profit-chart')
def get_profit_chart():
    """API para obtener gráfica de profit del VPS"""
    try:
        conn = sqlite3.connect(analytics.db_path)
        
        # Obtener datos de operaciones cerradas
        df = pd.read_sql_query('''
            SELECT exit_time, profit FROM trades 
            WHERE status = 'CLOSED' AND exit_time IS NOT NULL
            ORDER BY exit_time
        ''', conn)
        
        conn.close()
        
        if df.empty:
            return jsonify({"error": "No hay operaciones cerradas del VPS"})
            
        df['exit_time'] = pd.to_datetime(df['exit_time'])
        df['cumulative_profit'] = df['profit'].cumsum()
        
        # Crear gráfica
        fig = go.Figure()
        
        # Línea de profit acumulado
        fig.add_trace(go.Scatter(
            x=df['exit_time'],
            y=df['cumulative_profit'],
            mode='lines+markers',
            name='Profit Acumulado VPS',
            line=dict(color='blue', width=3),
            marker=dict(size=6)
        ))
        
        # Barras de profit por operación
        colors = ['green' if p > 0 else 'red' for p in df['profit']]
        fig.add_trace(go.Bar(
            x=df['exit_time'],
            y=df['profit'],
            name='Profit por Trade VPS',
            marker_color=colors,
            opacity=0.6,
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='📊 Análisis de Profit VPS - SMC-LIT Bot',
            xaxis_title='Fecha',
            yaxis_title='Profit Acumulado ($)',
            yaxis2=dict(
                title='Profit por Trade ($)',
                overlaying='y',
                side='right'
            ),
            template='plotly_white',
            height=500
        )
        
        return jsonify(json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig)))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/drawdown-chart')
def get_drawdown_chart():
    """API para obtener gráfica de drawdown del VPS"""
    try:
        conn = sqlite3.connect(analytics.db_path)
        
        df = pd.read_sql_query('''
            SELECT exit_time, profit FROM trades 
            WHERE status = 'CLOSED' AND exit_time IS NOT NULL
            ORDER BY exit_time
        ''', conn)
        
        conn.close()
        
        if df.empty:
            return jsonify({"error": "No hay operaciones para calcular drawdown del VPS"})
            
        df['exit_time'] = pd.to_datetime(df['exit_time'])
        df['cumulative_profit'] = df['profit'].cumsum()
        df['running_max'] = df['cumulative_profit'].expanding().max()
        df['drawdown'] = df['cumulative_profit'] - df['running_max']
        
        fig = go.Figure()
        
        # Línea de profit acumulado
        fig.add_trace(go.Scatter(
            x=df['exit_time'],
            y=df['cumulative_profit'],
            mode='lines',
            name='Profit Acumulado VPS',
            line=dict(color='blue', width=3)
        ))
        
        # Línea de máximo histórico
        fig.add_trace(go.Scatter(
            x=df['exit_time'],
            y=df['running_max'],
            mode='lines',
            name='Máximo Histórico VPS',
            line=dict(color='green', width=2, dash='dash')
        ))
        
        # Área de drawdown
        fig.add_trace(go.Scatter(
            x=df['exit_time'],
            y=df['drawdown'],
            mode='lines',
            name='Drawdown VPS',
            fill='tonexty',
            fillcolor='rgba(255, 0, 0, 0.3)',
            line=dict(color='red', width=2)
        ))
        
        fig.update_layout(
            title='📉 Análisis de Drawdown VPS - SMC-LIT Bot',
            xaxis_title='Fecha',
            yaxis_title='Profit ($)',
            template='plotly_white',
            height=500
        )
        
        return jsonify(json.loads(plotly.utils.PlotlyJSONEncoder().encode(fig)))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/performance-summary')
def get_performance_summary():
    """API para obtener resumen de rendimiento del VPS por períodos"""
    try:
        conn = sqlite3.connect(analytics.db_path)
        
        # Performance por día
        daily_df = pd.read_sql_query('''
            SELECT DATE(exit_time) as date, 
                   COUNT(*) as trades_count,
                   SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) as wins,
                   SUM(profit) as daily_profit
            FROM trades 
            WHERE status = 'CLOSED' AND exit_time IS NOT NULL
            GROUP BY DATE(exit_time)
            ORDER BY date DESC
            LIMIT 30
        ''', conn)
        
        # Performance por símbolo
        symbol_df = pd.read_sql_query('''
            SELECT symbol,
                   COUNT(*) as trades_count,
                   SUM(CASE WHEN profit > 0 THEN 1 ELSE 0 END) as wins,
                   SUM(profit) as total_profit,
                   AVG(profit) as avg_profit
            FROM trades 
            WHERE status = 'CLOSED'
            GROUP BY symbol
            ORDER BY total_profit DESC
        ''', conn)
        
        conn.close()
        
        # Convertir a formato JSON
        daily_performance = daily_df.to_dict('records') if not daily_df.empty else []
        symbol_performance = symbol_df.to_dict('records') if not symbol_df.empty else []
        
        return jsonify({
            'daily_performance': daily_performance,
            'symbol_performance': symbol_performance
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/vps-status')
def get_vps_status():
    """API para obtener estado del VPS"""
    try:
        # Información del VPS
        vps_info = {
            'ip': '107.174.133.202',
            'status': 'Conectado',
            'last_sync': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'bot_status': 'Activo',
            'data_source': 'VPS Logs'
        }
        
        return jsonify(vps_info)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/sync-now', methods=['POST'])
def sync_now():
    """API para sincronizar datos del VPS ahora"""
    try:
        # Importar y ejecutar sincronización
        from vps_data_sync import VPSDataSync
        
        sync = VPSDataSync(
            vps_ip='107.174.133.202',
            vps_user='root',
            vps_password='n5X5dB6xPLJj06qr4C',
            vps_bot_dir='/home/smc-lit-bot'
        )
        
        success = sync.full_sync()
        
        if success:
            return jsonify({"success": True, "message": "Sincronización completada"})
        else:
            return jsonify({"success": False, "message": "Error en sincronización"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("🚀 Iniciando Dashboard Web VPS SMC-LIT Trading Analytics")
    print("📊 Accede a: http://localhost:5002")
    print("🔗 Datos sincronizados desde VPS: 107.174.133.202")
    
    app.run(debug=False, host='0.0.0.0', port=5002) 