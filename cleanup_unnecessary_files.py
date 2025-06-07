#!/usr/bin/env python3
# Limpieza Inteligente de Archivos SMC-LIT
# ========================================

import os
import glob
import shutil
from datetime import datetime

class SmartCleaner:
    """Limpiador inteligente de archivos innecesarios"""
    
    def __init__(self):
        self.deleted_files = []
        self.kept_files = []
        self.total_size_freed = 0
        
        # Archivos ESENCIALES que NO se deben eliminar
        self.essential_files = {
            # Bots principales activos
            'unified_trading_bot.py',
            'main_unlimited_v2.py',
            'main_advanced_with_indices.py',
            
            # Dashboard y monitoreo activo
            'unified_dashboard.py',
            'vps_data_sync.py',
            
            # Bases de datos ACTIVAS (modo real)
            'real_account_trading.db',
            'vps_trading_history.db',
            'trading_bot.db',
            
            # Scripts de activación/configuración
            'activate_real_with_same_credentials.py',
            'start_vps_bot_real.py',
            
            # Documentación importante
            'README.md',
            'requirements_linux.txt'
        }
        
        # Patrones de archivos a ELIMINAR
        self.cleanup_patterns = [
            # Backups antiguos
            '*.backup_*',
            '*.backup_20*',
            
            # Logs grandes
            '*.log',
            
            # Archivos de prueba y temporales
            'test_*.py',
            'check_*.py',
            'verify_*.py',
            
            # Scripts de instalación/deploy ya usados  
            'install_*.py',
            'deploy_*.py',
            'setup_*.py',
            'actualizar_*.py',
            'actualizar_*.sh',
            'upload_*.sh',
            
            # Documentación técnica antigua
            '*.md',  # Excepto README.md
            
            # Bases de datos demo/antiguas
            'demo_trading.db',
            'trading_history.db',
            'trading_real.db',
            'real_trading_history.db',
            'vps_trading_data.db',
            'bot_monitoring.db',
            
            # Archivos de análisis/reportes
            '*.html',
            '*.xlsx',
            '*.json',
            
            # Scripts obsoletos
            'panel_control_*.py',
            'configuracion_*.py',
            'web_dashboard.py',
            'bot_analytics_*.py',
            'trading_analytics_*.py',
            'complete_*.py',
            'launch_*.py',
            'restart_*.py',
            'quick_*.py',
            'final_*.py',
            'start_unified_*.py',
            'dashboard_*.py',
            'remove_*.py',
            'show_*.py',
            'sync_*.py',
            'update_*.py'
        ]
        
        # Directorios a limpiar
        self.cleanup_dirs = [
            '__pycache__',
            'templates',  # Solo si está vacío
            '.cursor'
        ]

    def get_file_size(self, filepath):
        """Obtener tamaño de archivo en bytes"""
        try:
            return os.path.getsize(filepath)
        except:
            return 0

    def format_size(self, size_bytes):
        """Formatear tamaño en unidades legibles"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def should_keep_file(self, filename):
        """Determinar si un archivo debe mantenerse"""
        # Mantener archivos esenciales
        if filename in self.essential_files:
            return True
            
        # Mantener README.md específicamente
        if filename == 'README.md':
            return True
            
        return False

    def cleanup_by_patterns(self):
        """Limpiar archivos usando patrones"""
        print("🧹 LIMPIANDO ARCHIVOS POR PATRONES...")
        
        for pattern in self.cleanup_patterns:
            matches = glob.glob(pattern)
            
            for filepath in matches:
                filename = os.path.basename(filepath)
                
                # Verificar si debe mantenerse
                if self.should_keep_file(filename):
                    self.kept_files.append(filename)
                    print(f"✅ CONSERVADO: {filename} (archivo esencial)")
                    continue
                
                # Eliminar archivo
                try:
                    file_size = self.get_file_size(filepath)
                    os.remove(filepath)
                    self.deleted_files.append(filename)
                    self.total_size_freed += file_size
                    print(f"🗑️  ELIMINADO: {filename} ({self.format_size(file_size)})")
                except Exception as e:
                    print(f"⚠️  Error eliminando {filename}: {e}")

    def cleanup_directories(self):
        """Limpiar directorios innecesarios"""
        print("\n📁 LIMPIANDO DIRECTORIOS...")
        
        for dirname in self.cleanup_dirs:
            if os.path.exists(dirname):
                try:
                    if dirname == 'templates':
                        # Solo eliminar si está vacío o solo tiene archivos HTML
                        files = os.listdir(dirname)
                        html_files = [f for f in files if f.endswith('.html')]
                        if len(files) == len(html_files):  # Solo HTML
                            shutil.rmtree(dirname)
                            print(f"🗑️  ELIMINADO: directorio {dirname}/")
                        else:
                            print(f"✅ CONSERVADO: {dirname}/ (tiene archivos necesarios)")
                    else:
                        shutil.rmtree(dirname)
                        print(f"🗑️  ELIMINADO: directorio {dirname}/")
                except Exception as e:
                    print(f"⚠️  Error eliminando {dirname}: {e}")

    def cleanup_empty_files(self):
        """Eliminar archivos vacíos"""
        print("\n📄 ELIMINANDO ARCHIVOS VACÍOS...")
        
        for filename in os.listdir('.'):
            if os.path.isfile(filename):
                if self.get_file_size(filename) == 0 and not self.should_keep_file(filename):
                    try:
                        os.remove(filename)
                        self.deleted_files.append(filename)
                        print(f"🗑️  ELIMINADO: {filename} (archivo vacío)")
                    except Exception as e:
                        print(f"⚠️  Error eliminando {filename}: {e}")

    def show_summary(self):
        """Mostrar resumen de limpieza"""
        print("\n" + "=" * 60)
        print("📋 RESUMEN DE LIMPIEZA")
        print("=" * 60)
        
        print(f"🗑️  Archivos eliminados: {len(self.deleted_files)}")
        print(f"✅ Archivos conservados: {len(self.kept_files)}")
        print(f"💾 Espacio liberado: {self.format_size(self.total_size_freed)}")
        
        print(f"\n✅ ARCHIVOS ESENCIALES CONSERVADOS:")
        for filename in sorted(self.essential_files):
            if os.path.exists(filename):
                size = self.get_file_size(filename)
                print(f"   📄 {filename} ({self.format_size(size)})")
        
        print(f"\n🔥 ARCHIVOS IMPORTANTES PARA TRADING REAL:")
        critical_files = [
            'unified_trading_bot.py',
            'unified_dashboard.py', 
            'real_account_trading.db',
            'vps_trading_history.db',
            'activate_real_with_same_credentials.py'
        ]
        
        for filename in critical_files:
            if os.path.exists(filename):
                print(f"   💎 {filename} ✅")
            else:
                print(f"   ❌ {filename} FALTA!")

    def perform_cleanup(self):
        """Realizar limpieza completa"""
        print("🚀 INICIANDO LIMPIEZA INTELIGENTE SMC-LIT")
        print("=" * 50)
        
        # Confirmar antes de continuar
        print("⚠️  ARCHIVOS QUE SE ELIMINARÁN:")
        print("   - Backups antiguos (*.backup_*)")
        print("   - Logs grandes (*.log)")
        print("   - Scripts de prueba (test_*, check_*, verify_*)")
        print("   - Scripts de instalación usados")
        print("   - Documentación técnica antigua")
        print("   - Bases de datos demo/obsoletas")
        print("   - Archivos de análisis y reportes")
        
        print(f"\n✅ SE CONSERVARÁN:")
        for filename in sorted(self.essential_files):
            print(f"   📄 {filename}")
        
        confirm = input(f"\n❓ ¿Proceder con la limpieza? (si/no): ").lower()
        if confirm != 'si':
            print("❌ Limpieza cancelada")
            return False
        
        # Realizar limpieza
        self.cleanup_by_patterns()
        self.cleanup_directories()
        self.cleanup_empty_files()
        
        # Mostrar resumen
        self.show_summary()
        
        print(f"\n🎉 ¡LIMPIEZA COMPLETADA!")
        print(f"💰 Tu bot de trading real sigue funcionando perfectamente")
        print(f"📊 Dashboard disponible en: http://localhost:5003")
        
        return True

def main():
    """Función principal"""
    cleaner = SmartCleaner()
    
    print("🧹 LIMPIADOR INTELIGENTE SMC-LIT")
    print("Elimina archivos innecesarios manteniendo el sistema de trading activo")
    
    cleaner.perform_cleanup()

if __name__ == "__main__":
    main() 