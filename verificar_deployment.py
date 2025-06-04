#!/usr/bin/env python3
"""
VERIFICACIÓN PRE-DEPLOYMENT - BOT SMC-LIT v2.0
============================================
Verifica que todo esté listo para el deployment
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """Banner de verificación"""
    print("🔍" + "=" * 60 + "🔍")
    print("🛠️  VERIFICACIÓN PRE-DEPLOYMENT BOT SMC-LIT v2.0")
    print("🔍" + "=" * 60 + "🔍")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔍" + "=" * 60 + "🔍")

def check_essential_files():
    """Verificar archivos esenciales"""
    print("\n📋 VERIFICANDO ARCHIVOS ESENCIALES...")
    
    essential_files = [
        'main_advanced_with_indices.py',
        'economic_calendar_analyzer.py',
        'twitter_news_analyzer.py',
        'ml_trading_system.py',
        'start_auto_mode.py',
        'requirements.txt',
        'inicio_bot_avanzado.py',
        'configuracion_automatica.py'
    ]
    
    missing_files = []
    for file in essential_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"  ✅ {file} ({size} bytes)")
        else:
            missing_files.append(file)
            print(f"  ❌ {file} - FALTANTE")
    
    return len(missing_files) == 0, missing_files

def check_python_dependencies():
    """Verificar dependencias de Python"""
    print("\n🐍 VERIFICANDO DEPENDENCIAS DE PYTHON...")
    
    try:
        import MetaTrader5
        print("  ✅ MetaTrader5")
    except ImportError:
        print("  ⚠️  MetaTrader5 - Usará simulador")
    
    try:
        import numpy
        print("  ✅ numpy")
    except ImportError:
        print("  ❌ numpy - REQUERIDO")
        return False
    
    try:
        import pandas
        print("  ✅ pandas")
    except ImportError:
        print("  ❌ pandas - REQUERIDO")
        return False
    
    try:
        import requests
        print("  ✅ requests")
    except ImportError:
        print("  ❌ requests - REQUERIDO")
        return False
    
    try:
        import sklearn
        print("  ✅ scikit-learn")
    except ImportError:
        print("  ⚠️  scikit-learn - ML limitado")
    
    try:
        import transformers
        print("  ✅ transformers (FinBERT)")
    except ImportError:
        print("  ⚠️  transformers - FinBERT limitado")
    
    return True

def test_imports():
    """Probar imports críticos"""
    print("\n🧪 PROBANDO IMPORTS CRÍTICOS...")
    
    try:
        from main_advanced_with_indices import AdvancedTradingBotWithIndices
        print("  ✅ Bot principal")
    except Exception as e:
        print(f"  ❌ Bot principal: {e}")
        return False
    
    try:
        from economic_calendar_analyzer import EconomicCalendarAnalyzer
        print("  ✅ Calendario económico")
    except Exception as e:
        print(f"  ⚠️  Calendario económico: {e}")
    
    try:
        from twitter_news_analyzer import AdvancedTwitterNewsAnalyzer
        print("  ✅ Twitter analyzer")
    except Exception as e:
        print(f"  ⚠️  Twitter analyzer: {e}")
    
    try:
        from ml_trading_system import AdvancedMLTradingSystem
        print("  ✅ Sistema ML")
    except Exception as e:
        print(f"  ⚠️  Sistema ML: {e}")
    
    return True

def check_system_requirements():
    """Verificar requisitos del sistema"""
    print("\n🖥️  VERIFICANDO SISTEMA...")
    
    # Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"  ✅ Python {python_version.major}.{python_version.minor}")
    else:
        print(f"  ❌ Python {python_version.major}.{python_version.minor} - Necesita 3.8+")
        return False
    
    # Espacio en disco
    import shutil
    disk_usage = shutil.disk_usage('.')
    free_gb = disk_usage.free / (1024**3)
    if free_gb >= 2:
        print(f"  ✅ Espacio libre: {free_gb:.1f}GB")
    else:
        print(f"  ⚠️  Espacio libre: {free_gb:.1f}GB - Recomendado 2GB+")
    
    # Permisos
    if os.access('.', os.W_OK):
        print("  ✅ Permisos de escritura")
    else:
        print("  ❌ Sin permisos de escritura")
        return False
    
    return True

def test_bot_functionality():
    """Probar funcionalidad básica del bot"""
    print("\n🤖 PROBANDO FUNCIONALIDAD BÁSICA...")
    
    try:
        # Test calendario económico
        from economic_calendar_analyzer import EconomicCalendarAnalyzer
        calendar = EconomicCalendarAnalyzer()
        events = calendar.get_upcoming_events(1)
        print(f"  ✅ Calendario económico: {len(events)} eventos")
    except Exception as e:
        print(f"  ⚠️  Calendario económico: {e}")
    
    try:
        # Test Twitter analyzer
        from twitter_news_analyzer import TwitterNewsAnalyzer
        twitter = TwitterNewsAnalyzer()
        print("  ✅ Twitter analyzer básico")
    except Exception as e:
        print(f"  ⚠️  Twitter analyzer: {e}")
    
    try:
        # Test ML system
        from ml_trading_system import AdvancedMLTradingSystem
        ml_system = AdvancedMLTradingSystem()
        print("  ✅ Sistema ML")
    except Exception as e:
        print(f"  ⚠️  Sistema ML: {e}")
    
    return True

def show_deployment_readiness():
    """Mostrar resumen de preparación"""
    print("\n📊 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    files_ok, missing = check_essential_files()
    deps_ok = check_python_dependencies()
    imports_ok = test_imports()
    system_ok = check_system_requirements()
    functionality_ok = test_bot_functionality()
    
    if files_ok and deps_ok and imports_ok and system_ok:
        print("🎉 LISTO PARA DEPLOYMENT!")
        print("✅ Todos los componentes verificados")
        print("🚀 Puedes ejecutar: sudo python3 deploy_local_to_production.py")
    else:
        print("⚠️  PROBLEMAS DETECTADOS:")
        if not files_ok:
            print(f"  📋 Archivos faltantes: {', '.join(missing)}")
        if not deps_ok:
            print("  🐍 Dependencias faltantes")
        if not imports_ok:
            print("  🧪 Problemas de imports")
        if not system_ok:
            print("  🖥️  Problemas de sistema")
        
        print("\n💡 SOLUCIONES:")
        print("  1. Instalar dependencias: pip install -r requirements.txt")
        print("  2. Verificar permisos del sistema")
        print("  3. Actualizar Python si es necesario")
    
    print("=" * 50)

def main():
    """Función principal"""
    print_banner()
    show_deployment_readiness()

if __name__ == "__main__":
    main() 