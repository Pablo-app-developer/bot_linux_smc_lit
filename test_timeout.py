#!/usr/bin/env python3
"""
PRUEBA DE TIMEOUT - BOT SMC-LIT v2.0
====================================
Script para probar el timeout automático
"""

import sys
import time
import select

def test_timeout():
    """Probar la funcionalidad de timeout"""
    print("🧪 PRUEBA DE TIMEOUT AUTOMÁTICO")
    print("=" * 40)
    print("⏰ El sistema elegirá automáticamente en 10 segundos...")
    print()
    
    def input_with_timeout(prompt, timeout=10):
        print(prompt, end='', flush=True)
        
        # En Windows, usar un método alternativo
        if sys.platform == 'win32':
            import msvcrt
            start_time = time.time()
            input_chars = []
            
            while True:
                if time.time() - start_time > timeout:
                    print()  # Nueva línea
                    return None  # Timeout
                
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    if char == b'\r':  # Enter
                        print()  # Nueva línea
                        return ''.join(input_chars)
                    elif char == b'\x08':  # Backspace
                        if input_chars:
                            input_chars.pop()
                            print('\b \b', end='', flush=True)
                    else:
                        try:
                            decoded_char = char.decode('utf-8')
                            input_chars.append(decoded_char)
                            print(decoded_char, end='', flush=True)
                        except:
                            pass
                
                time.sleep(0.01)  # Pequeña pausa para no saturar CPU
        
        else:
            # En Linux/Unix usar select
            ready, _, _ = select.select([sys.stdin], [], [], timeout)
            if ready:
                return sys.stdin.readline().strip()
            else:
                print()  # Nueva línea después del timeout
                return None  # Timeout
    
    # Probar el timeout
    respuesta = input_with_timeout("Elige opción (1=Automático, 2=Manual): ", timeout=10)
    
    if respuesta is None:
        print("⏰ Timeout alcanzado - Seleccionando MODO AUTOMÁTICO por defecto")
        print("✅ PRUEBA EXITOSA: Sistema funcionó sin intervención")
        return "automatic"
    else:
        if respuesta.strip() == '1':
            print("✅ Opción 1 seleccionada - MODO AUTOMÁTICO")
            return "automatic"
        elif respuesta.strip() == '2':
            print("✅ Opción 2 seleccionada - MODO MANUAL")
            return "manual"
        else:
            print("❌ Opción no válida")
            return "invalid"

if __name__ == "__main__":
    resultado = test_timeout()
    print(f"\n🎯 Resultado: {resultado}")
    print("✅ Prueba completada") 