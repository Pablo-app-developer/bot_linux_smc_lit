#!/usr/bin/env python3
"""
VERIFICADOR DEL SISTEMA SMC-LIT
==============================
Verifica que todo esté correctamente configurado
"""

import os
import sys
import importlib
from datetime import datetime

def imprimir_banner():
    """Banner del verificador"""
    print("=" * 60)
    print("🔍 VERIFICADOR DEL SISTEMA SMC-LIT")
    print("=" * 60)
    print("✅ Verificando configuración completa...")
    print("=" * 60)

def verificar_archivos_principales():
    """Verifica que todos los archivos principales existan"""
    print("\n📁 VERIFICANDO ARCHIVOS PRINCIPALES:")
    
    archivos_requeridos = [
        'config_seguro.py',
        'iniciar_bot_seguro.py', 
        'configurar_credenciales.py',
        'deploy_a_vps.py',
        'main.py',
        'start_bot.py',
        'requirements.txt',
        'INSTRUCCIONES_COMPLETAS.md'
    ]
    
    todos_ok = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_ok = False
    
    return todos_ok

def verificar_directorio_src():
    """Verifica el directorio src"""
    print("\n📂 VERIFICANDO DIRECTORIO SRC:")
    
    if not os.path.exists('src'):
        print("❌ Directorio src/ no encontrado")
        return False
    
    archivos_src = [
        'src/mt5_connector.py',
        'src/mt5_trader.py',
        'src/strategy.py',
        'src/features.py',
        'src/mt5_simulator.py'
    ]
    
    todos_ok = True
    for archivo in archivos_src:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_ok = False
    
    return todos_ok

def verificar_dependencias():
    """Verifica dependencias Python"""
    print("\n🐍 VERIFICANDO DEPENDENCIAS PYTHON:")
    
    dependencias = [
        'pandas',
        'numpy', 
        'sklearn',
        'xgboost',
        'matplotlib',
        'seaborn',
        'joblib'
    ]
    
    todos_ok = True
    for dep in dependencias:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NO INSTALADO")
            todos_ok = False
    
    return todos_ok

def verificar_configuracion_segura():
    """Verifica la configuración de seguridad"""
    print("\n🛡️  VERIFICANDO CONFIGURACIÓN DE SEGURIDAD:")
    
    try:
        from config_seguro import CONFIGURACION_SEGURA, validar_configuracion_segura
        
        # Verificar configuración
        if validar_configuracion_segura():
            print("✅ Configuración de seguridad OK")
            
            # Verificar valores clave
            if CONFIGURACION_SEGURA['DEMO_MODE']:
                print("✅ DEMO_MODE activado")
            else:
                print("❌ DEMO_MODE desactivado - PELIGRO")
                return False
            
            if CONFIGURACION_SEGURA['PAPER_TRADING']:
                print("✅ PAPER_TRADING activado")
            else:
                print("❌ PAPER_TRADING desactivado - PELIGRO")
                return False
            
            if CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE'] <= 1.0:
                print(f"✅ Riesgo por trade: {CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE']}%")
            else:
                print(f"❌ Riesgo por trade muy alto: {CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE']}%")
                return False
            
            return True
        else:
            print("❌ Configuración de seguridad FALLÓ")
            return False
            
    except ImportError:
        print("❌ No se pudo cargar config_seguro.py")
        return False

def verificar_optimizacion():
    """Verifica archivos de optimización"""
    print("\n🎯 VERIFICANDO SISTEMA DE OPTIMIZACIÓN:")
    
    archivos_optimizacion = [
        'advanced_auto_optimizer.py',
        'bayesian_optimizer.py', 
        'master_optimization_system.py',
        'implement_optimized_strategy.py'
    ]
    
    todos_ok = True
    for archivo in archivos_optimizacion:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTANTE")
            todos_ok = False
    
    return todos_ok

def verificar_resultados_previos():
    """Verifica si hay resultados de optimización"""
    print("\n📊 VERIFICANDO RESULTADOS PREVIOS:")
    
    # Buscar archivos de resultados
    archivos_resultados = []
    for archivo in os.listdir('.'):
        if any(x in archivo for x in ['results', 'strategy', 'backtest']) and archivo.endswith(('.json', '.csv')):
            archivos_resultados.append(archivo)
    
    if archivos_resultados:
        print(f"✅ Encontrados {len(archivos_resultados)} archivos de resultados:")
        for archivo in archivos_resultados[:5]:  # Mostrar solo los primeros 5
            print(f"  • {archivo}")
        if len(archivos_resultados) > 5:
            print(f"  • ... y {len(archivos_resultados) - 5} más")
    else:
        print("ℹ️  No hay resultados previos (normal en primera ejecución)")
    
    return True

def verificar_permisos():
    """Verifica permisos de archivos"""
    print("\n🔐 VERIFICANDO PERMISOS:")
    
    archivos_ejecutables = [
        'config_seguro.py',
        'iniciar_bot_seguro.py',
        'configurar_credenciales.py',
        'deploy_a_vps.py'
    ]
    
    todos_ok = True
    for archivo in archivos_ejecutables:
        if os.path.exists(archivo):
            if os.access(archivo, os.X_OK):
                print(f"✅ {archivo} - Ejecutable")
            else:
                print(f"⚠️  {archivo} - No ejecutable (chmod +x requerido)")
                todos_ok = False
        else:
            print(f"❌ {archivo} - No encontrado")
            todos_ok = False
    
    return todos_ok

def mostrar_estado_mercado():
    """Muestra el estado del mercado"""
    print("\n📈 ESTADO DEL MERCADO:")
    
    now = datetime.now()
    dia_semana = now.weekday()  # 0=Lunes, 6=Domingo
    
    if dia_semana < 5:  # Lunes a Viernes
        print(f"✅ Mercado Forex: ABIERTO")
        print(f"📅 Día: {['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'][dia_semana]}")
    else:
        print(f"❌ Mercado Forex: CERRADO (fin de semana)")
        print(f"📅 Día: {['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'][dia_semana]}")
    
    print(f"🕐 Hora local: {now.strftime('%H:%M:%S')}")

def mostrar_resumen_final(resultados):
    """Muestra el resumen final"""
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    total_checks = len(resultados)
    passed_checks = sum(resultados.values())
    
    for nombre, resultado in resultados.items():
        emoji = "✅" if resultado else "❌"
        print(f"{emoji} {nombre}")
    
    print("\n" + "-" * 60)
    print(f"📊 RESULTADO: {passed_checks}/{total_checks} verificaciones pasadas")
    
    if passed_checks == total_checks:
        print("🎉 ¡SISTEMA COMPLETAMENTE VERIFICADO!")
        print("🚀 Listo para ejecutar el bot")
        print("\n💡 SIGUIENTE PASO:")
        print("   python3 configurar_credenciales.py")
        return True
    else:
        print("⚠️  Algunas verificaciones fallaron")
        print("🔧 Revisa los errores arriba antes de continuar")
        return False

def main():
    """Función principal"""
    try:
        imprimir_banner()
        
        # Ejecutar todas las verificaciones
        resultados = {
            "Archivos principales": verificar_archivos_principales(),
            "Directorio src": verificar_directorio_src(), 
            "Dependencias Python": verificar_dependencias(),
            "Configuración segura": verificar_configuracion_segura(),
            "Sistema optimización": verificar_optimizacion(),
            "Resultados previos": verificar_resultados_previos(),
            "Permisos archivos": verificar_permisos()
        }
        
        # Mostrar estado del mercado
        mostrar_estado_mercado()
        
        # Resumen final
        sistema_ok = mostrar_resumen_final(resultados)
        
        if sistema_ok:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Verificación interrumpida")
    except Exception as e:
        print(f"\n❌ Error durante verificación: {e}")

if __name__ == "__main__":
    main() 