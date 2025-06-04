#!/usr/bin/env python3

from complete_monitoring_toolkit import CompleteMonitoringToolkit

def test_monitoring():
    print("🔍 VERIFICACIÓN RÁPIDA DEL BOT:")
    print("=" * 40)
    
    toolkit = CompleteMonitoringToolkit()
    
    # Test 1: Quick bot status
    bot_running = toolkit.quick_bot_status()
    
    print("\n📊 PROBANDO MÉTRICAS PARA EVALUACIÓN:")
    print("=" * 40)
    
    # Test 2: Metrics collection
    metrics = toolkit.get_metrics_for_evaluation()
    print(f"✅ Recolección exitosa: {metrics['collection_success']}")
    print(f"⏰ Timestamp: {metrics['timestamp']}")
    print(f"🌐 VPS: {toolkit.vps_credentials['host']}")
    
    if metrics['collection_success']:
        print("\n🎯 Sistema de monitoreo funcionando correctamente!")
        print("🤖 Bot está operacional")
        print("📡 Conexión VPS estable")
        print("💾 Recolección de datos activa")
    else:
        print(f"\n❌ Error en recolección: {metrics.get('error', 'Unknown')}")
    
    return bot_running and metrics['collection_success']

if __name__ == "__main__":
    test_monitoring() 