"""
Script de prueba para el módulo de control de volumen
GestIX - Universidad Nacional de Colombia
"""

import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.modules.volume.volume import Volume


def test_volume_control():
    """
    Función de prueba para el control de volumen.
    """
    print("🔊 === PRUEBA DEL MÓDULO DE VOLUMEN ===")
    
    try:
        # Inicializar controlador de volumen
        print("🚀 Inicializando controlador de volumen...")
        volume = Volume()
        
        # Obtener información inicial
        current_volume = volume.getVolume()
        is_muted = volume.isMuted()
        
        print(f"📊 Estado inicial:")
        print(f"   - Volumen actual: {current_volume}%")
        print(f"   - Estado de silencio: {'🔇 Silenciado' if is_muted else '🔊 Audible'}")
        print(f"   - Sistema operativo: {volume.system}")
        
        # Prueba de establecer volumen específico
        print(f"\n🎚️ Estableciendo volumen a 50%...")
        volume.setVolume(50)
        new_volume = volume.getVolume()
        print(f"   - Volumen después del cambio: {new_volume}%")
        
        # Prueba de incremento
        print(f"\n⬆️ Aumentando volumen en 10%...")
        volume.volumeUp(10)
        volume_after_up = volume.getVolume()
        print(f"   - Volumen después de aumentar: {volume_after_up}%")
        
        # Prueba de decremento
        print(f"\n⬇️ Disminuyendo volumen en 5%...")
        volume.volumeDown(5)
        volume_after_down = volume.getVolume()
        print(f"   - Volumen después de disminuir: {volume_after_down}%")
        
        # Prueba de silencio
        print(f"\n🔇 Probando función de silencio...")
        volume.mute()
        print(f"   - Estado después de silenciar: {'🔇 Silenciado' if volume.isMuted() else '🔊 Audible'}")
        
        # Reactivar audio
        print(f"\n🔊 Reactivando audio...")
        volume.unmute()
        print(f"   - Estado después de reactivar: {'🔇 Silenciado' if volume.isMuted() else '🔊 Audible'}")
        
        # Restaurar volumen original
        print(f"\n🔄 Restaurando volumen original ({current_volume}%)...")
        volume.setVolume(current_volume)
        final_volume = volume.getVolume()
        print(f"   - Volumen final: {final_volume}%")
        
        print(f"\n✅ Prueba completada exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        print(f"💡 Posibles soluciones:")
        print(f"   - Verificar que las dependencias estén instaladas")
        print(f"   - Ejecutar como administrador si es necesario")
        print(f"   - Verificar que el sistema de audio esté funcionando")
        return False
    
    return True


def interactive_volume_test():
    """
    Prueba interactiva del control de volumen.
    """
    print("\n🎮 === PRUEBA INTERACTIVA ===")
    print("Comandos disponibles:")
    print("  up <valor>    - Aumentar volumen")
    print("  down <valor>  - Disminuir volumen")
    print("  set <valor>   - Establecer volumen específico")
    print("  mute          - Silenciar/Activar audio")
    print("  status        - Mostrar estado actual")
    print("  quit          - Salir")
    
    try:
        volume = Volume()
        
        while True:
            command = input("\n🎚️ Comando: ").strip().lower()
            
            if command == "quit":
                break
            elif command == "status":
                print(f"📊 Volumen: {volume.getVolume()}% | Silenciado: {volume.isMuted()}")
            elif command == "mute":
                if volume.isMuted():
                    volume.unmute()
                    print("🔊 Audio activado")
                else:
                    volume.mute()
                    print("🔇 Audio silenciado")
            elif command.startswith("up"):
                try:
                    parts = command.split()
                    value = int(parts[1]) if len(parts) > 1 else 5
                    volume.volumeUp(value)
                    print(f"⬆️ Volumen aumentado. Actual: {volume.getVolume()}%")
                except (ValueError, IndexError):
                    print("❌ Formato: up <valor>")
            elif command.startswith("down"):
                try:
                    parts = command.split()
                    value = int(parts[1]) if len(parts) > 1 else 5
                    volume.volumeDown(value)
                    print(f"⬇️ Volumen disminuido. Actual: {volume.getVolume()}%")
                except (ValueError, IndexError):
                    print("❌ Formato: down <valor>")
            elif command.startswith("set"):
                try:
                    parts = command.split()
                    value = int(parts[1])
                    volume.setVolume(value)
                    print(f"🎚️ Volumen establecido a: {volume.getVolume()}%")
                except (ValueError, IndexError):
                    print("❌ Formato: set <valor>")
            else:
                print("❌ Comando no reconocido")
                
    except Exception as e:
        print(f"❌ Error en la prueba interactiva: {e}")


if __name__ == "__main__":
    """
    Ejecutar pruebas del módulo de volumen.
    """
    print("🔊 GestIX - Pruebas del Módulo de Volumen")
    print("=" * 50)
    
    # Ejecutar prueba automática
    success = test_volume_control()
    
    if success:
        # Ofrecer prueba interactiva
        response = input("\n¿Deseas ejecutar la prueba interactiva? (s/n): ").lower()
        if response in ['s', 'si', 'yes', 'y']:
            interactive_volume_test()
    
    print("\n👋 ¡Gracias por probar GestIX!")