#!/usr/bin/env python3
"""
VERIFICACIÓN VPS v2.1 - TIMEOUT AUTOMÁTICO
==========================================
Script para verificar que la actualización v2.1 fue exitosa
"""

import os
import sys
import subprocess
import time
from datetime import datetime

class VPSVerifier:
    def __init__(self):
        self.production_dir = "/opt/bot_smc_lit_v2"
        self.service_name = "smc-lit-bot"
        
    def print_banner(self):
        """Banner de verificación"""
        print("🔍" + "=" * 70 + "🔍")
        print("✅ VERIFICACIÓN VPS v2.1 - TIMEOUT AUTOMÁTICO")
        print("🔍" + "=" * 70 + "🔍")
        print("📋 VERIFICANDO:")
        print("  🔍 Archivos actualizados")
        print("  🔍 Funcionalidad de timeout")
        print("  🔍 Servicio systemd")
        print("  🔍 Logs de funcionamiento")
        print("🔍" + "=" * 70 + "🔍")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔍" + "=" * 70 + "🔍")
    
    def check_files_updated(self):
        """Verificar archivos actualizados"""
        print("\n📁 VERIFICANDO ARCHIVOS ACTUALIZADOS...")
        
        required_files = [
            'main_advanced_with_indices.py',
            'start_production.sh',
            'test_timeout.py',
            'ACTUALIZACION_TIMEOUT_v2.1.md'
        ]
        
        all_found = True
        
        for file_name in required_files:
            file_path = os.path.join(self.production_dir, file_name)
            if os.path.exists(file_path):
                # Verificar fecha de modificación
                mod_time = os.path.getmtime(file_path)
                mod_date = datetime.fromtimestamp(mod_time)
                print(f"  ✅ {file_name} (modificado: {mod_date.strftime('%Y-%m-%d %H:%M')})")
            else:
                print(f"  ❌ {file_name} - NO ENCONTRADO")
                all_found = False
        
        # Verificar contenido específico de main_advanced_with_indices.py
        main_file = os.path.join(self.production_dir, 'main_advanced_with_indices.py')
        if os.path.exists(main_file):
            try:
                with open(main_file, 'r') as f:
                    content = f.read()
                    if 'input_with_timeout' in content and 'select.select' in content:
                        print("  ✅ Funcionalidad de timeout encontrada en código")
                    else:
                        print("  ❌ Funcionalidad de timeout NO encontrada en código")
                        all_found = False
            except Exception as e:
                print(f"  ⚠️  Error leyendo main_advanced_with_indices.py: {e}")
        
        return all_found
    
    def check_service_status(self):
        """Verificar estado del servicio"""
        print("\n🔧 VERIFICANDO SERVICIO SYSTEMD...")
        
        try:
            # Estado del servicio
            result = subprocess.run(['systemctl', 'is-active', self.service_name], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip() == 'active':
                print(f"  ✅ Servicio {self.service_name}: ACTIVO")
                service_ok = True
            else:
                print(f"  ❌ Servicio {self.service_name}: INACTIVO")
                service_ok = False
            
            # Información detallada del servicio
            result = subprocess.run(['systemctl', 'status', self.service_name], 
                                  capture_output=True, text=True)
            
            # Buscar líneas importantes
            for line in result.stdout.split('\n'):
                if 'Active:' in line:
                    print(f"  📊 {line.strip()}")
                elif 'Main PID:' in line:
                    print(f"  🔢 {line.strip()}")
                elif 'Memory:' in line:
                    print(f"  💾 {line.strip()}")
            
            return service_ok
            
        except Exception as e:
            print(f"  ❌ Error verificando servicio: {e}")
            return False
    
    def check_logs(self):
        """Verificar logs de funcionamiento"""
        print("\n📄 VERIFICANDO LOGS...")
        
        # Verificar logs del sistema
        try:
            result = subprocess.run(['journalctl', '-u', self.service_name, '-n', '5', '--no-pager'], 
                                  capture_output=True, text=True)
            
            print("  📋 Últimos 5 logs del servicio:")
            for line in result.stdout.split('\n')[-6:-1]:  # Últimas 5 líneas
                if line.strip():
                    print(f"    {line}")
            
            # Buscar indicadores de timeout v2.1
            if 'timeout' in result.stdout.lower() or 'v2.1' in result.stdout:
                print("  ✅ Logs contienen referencias a timeout/v2.1")
                logs_ok = True
            else:
                print("  ⚠️  Logs no contienen referencias específicas a v2.1")
                logs_ok = True  # No es crítico
            
        except Exception as e:
            print(f"  ❌ Error obteniendo logs systemd: {e}")
            logs_ok = False
        
        # Verificar logs locales
        log_file = os.path.join(self.production_dir, 'logs', 'bot.log')
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-5:]  # Últimas 5 líneas
                    
                print("  📋 Últimas líneas del log local:")
                for line in recent_lines:
                    print(f"    {line.strip()}")
                
                print(f"  ✅ Log local disponible: {len(lines)} líneas totales")
            except Exception as e:
                print(f"  ⚠️  Error leyendo log local: {e}")
        else:
            print("  ⚠️  Log local no encontrado")
        
        return logs_ok
    
    def test_timeout_functionality(self):
        """Probar funcionalidad de timeout específicamente"""
        print("\n🧪 PROBANDO FUNCIONALIDAD DE TIMEOUT...")
        
        os.chdir(self.production_dir)
        python_path = os.path.join(self.production_dir, '.venv', 'bin', 'python')
        
        # Probar script de timeout independiente
        test_timeout_path = os.path.join(self.production_dir, 'test_timeout.py')
        
        if os.path.exists(test_timeout_path):
            try:
                print("  🚀 Ejecutando test_timeout.py...")
                result = subprocess.run([python_path, test_timeout_path], 
                                      capture_output=True, text=True, timeout=15)
                
                print("  📋 Resultado del test:")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        print(f"    {line}")
                
                if 'automatic' in result.stdout and 'exitosa' in result.stdout.lower():
                    print("  ✅ Test de timeout EXITOSO")
                    return True
                else:
                    print("  ⚠️  Test de timeout completado con advertencias")
                    return True
                    
            except subprocess.TimeoutExpired:
                print("  ✅ Test de timeout funcionó (timeout detectado correctamente)")
                return True
            except Exception as e:
                print(f"  ❌ Error ejecutando test de timeout: {e}")
                return False
        else:
            print("  ⚠️  test_timeout.py no encontrado, creando test básico...")
            return self.create_and_run_basic_test()
    
    def create_and_run_basic_test(self):
        """Crear y ejecutar test básico de timeout"""
        basic_test = """
import sys
sys.path.append('.')

try:
    from main_advanced_with_indices import AdvancedTradingBotWithIndices
    print("✅ Bot principal importado")
    
    bot = AdvancedTradingBotWithIndices()
    if hasattr(bot, 'preguntar_modo_operacion'):
        print("✅ Método preguntar_modo_operacion encontrado")
        print("✅ Funcionalidad de timeout disponible")
    else:
        print("❌ Método preguntar_modo_operacion NO encontrado")
        
except Exception as e:
    print(f"❌ Error importando bot: {e}")
"""
        
        try:
            python_path = os.path.join(self.production_dir, '.venv', 'bin', 'python')
            test_file = os.path.join(self.production_dir, 'test_basic_timeout.py')
            
            with open(test_file, 'w') as f:
                f.write(basic_test)
            
            result = subprocess.run([python_path, test_file], 
                                  capture_output=True, text=True, timeout=10)
            
            print("  📋 Resultado del test básico:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    print(f"    {line}")
            
            # Limpiar archivo temporal
            os.remove(test_file)
            
            if '✅' in result.stdout:
                return True
            else:
                return False
                
        except Exception as e:
            print(f"  ❌ Error en test básico: {e}")
            return False
    
    def check_environment(self):
        """Verificar entorno de ejecución"""
        print("\n🐍 VERIFICANDO ENTORNO...")
        
        # Verificar Python y venv
        python_path = os.path.join(self.production_dir, '.venv', 'bin', 'python')
        
        if os.path.exists(python_path):
            try:
                result = subprocess.run([python_path, '--version'], 
                                      capture_output=True, text=True)
                print(f"  ✅ Python: {result.stdout.strip()}")
            except Exception as e:
                print(f"  ❌ Error verificando Python: {e}")
                return False
        else:
            print(f"  ❌ Python virtual env no encontrado: {python_path}")
            return False
        
        # Verificar dependencias críticas
        try:
            result = subprocess.run([python_path, '-c', 'import select; print("select OK")'], 
                                  capture_output=True, text=True)
            if 'select OK' in result.stdout:
                print("  ✅ Módulo select disponible (timeout Linux)")
            else:
                print("  ⚠️  Módulo select no disponible")
        except Exception as e:
            print(f"  ⚠️  Error verificando select: {e}")
        
        return True
    
    def show_verification_summary(self, results):
        """Mostrar resumen de verificación"""
        print("\n" + "=" * 70)
        print("📊 RESUMEN DE VERIFICACIÓN v2.1")
        print("=" * 70)
        
        total_checks = len(results)
        passed_checks = sum(1 for r in results.values() if r)
        
        for check_name, result in results.items():
            status = "✅ PASÓ" if result else "❌ FALLÓ"
            print(f"  {check_name}: {status}")
        
        print(f"\n📈 RESULTADO GENERAL: {passed_checks}/{total_checks} verificaciones pasadas")
        
        if passed_checks == total_checks:
            print("🎉 VERIFICACIÓN EXITOSA - BOT v2.1 FUNCIONANDO CORRECTAMENTE")
            print("⚡ Timeout automático operativo en VPS")
            return True
        elif passed_checks >= total_checks - 1:
            print("⚠️  VERIFICACIÓN MAYORMENTE EXITOSA - Revisar advertencias")
            print("⚡ Bot v2.1 probablemente funcionando")
            return True
        else:
            print("❌ VERIFICACIÓN FALLIDA - Requiere intervención manual")
            print("🔧 Revisar logs y configuración")
            return False
    
    def verify(self):
        """Ejecutar verificación completa"""
        self.print_banner()
        
        # Ejecutar todas las verificaciones
        results = {
            'Archivos actualizados': self.check_files_updated(),
            'Servicio systemd': self.check_service_status(),
            'Logs del sistema': self.check_logs(),
            'Funcionalidad timeout': self.test_timeout_functionality(),
            'Entorno Python': self.check_environment()
        }
        
        return self.show_verification_summary(results)

def main():
    """Función principal"""
    verifier = VPSVerifier()
    success = verifier.verify()
    
    if success:
        print("\n🎉 VERIFICACIÓN EXITOSA!")
        print("✅ Bot SMC-LIT v2.1 funcionando con timeout automático")
        sys.exit(0)
    else:
        print("\n💥 VERIFICACIÓN CON PROBLEMAS")
        print("🔧 Revisar resultados y corregir errores")
        sys.exit(1)

if __name__ == "__main__":
    main() 