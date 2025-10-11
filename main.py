"""
GestIX - Sistema de Interacción Gestual
Universidad Nacional de Colombia - Computación Visual

Punto de entrada principal del sistema de control gestual
para brillo y volumen del sistema mediante reconocimiento de gestos.
"""

import sys
import argparse
from core.modules.brightness.brightness import Brightness
from core.modules.volume.volume import Volume


def test_basic_functionality():
    """
    Prueba las funcionalidades básicas del sistema.
    """
    print("🧪 === PRUEBA DE FUNCIONALIDADES BÁSICAS ===")
    
    try:
        # Probar control de brillo
        print("\n🔆 Probando control de brillo...")
        brightness = Brightness()
        current_brightness = brightness.getBrightness()
        print(f"   - Brillo actual: {current_brightness}%")
        
        brightness.setBrightness(65)
        new_brightness = brightness.getBrightness()
        print(f"   - Brillo establecido a: {new_brightness}%")
        
        # Restaurar brillo original
        brightness.setBrightness(current_brightness)
        print(f"   - Brillo restaurado a: {brightness.getBrightness()}%")
        
        # Probar control de volumen
        print("\n🔊 Probando control de volumen...")
        volume = Volume()
        current_volume = volume.getVolume()
        print(f"   - Volumen actual: {current_volume}%")
        print(f"   - Estado de silencio: {'🔇 Silenciado' if volume.isMuted() else '🔊 Audible'}")
        
        volume.setVolume(50)
        new_volume = volume.getVolume()
        print(f"   - Volumen establecido a: {new_volume}%")
        
        # Restaurar volumen original
        volume.setVolume(current_volume)
        print(f"   - Volumen restaurado a: {volume.getVolume()}%")
        
        print("\n✅ Todas las funcionalidades básicas funcionan correctamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en las pruebas: {e}")
        return False


def run_gesture_control():
    """
    Ejecuta el sistema de control gestual completo.
    """
    print("🚀 === INICIANDO CONTROL GESTUAL ===")
    
    try:
        # Importar el controlador de cámara (solo si se va a usar)
        from app.modules.camera.camera_volume import CameraVolumeController
        
        print("📷 Inicializando cámara y controladores...")
        controller = CameraVolumeController()
        
        print("🎯 Sistema listo. Iniciando detección de gestos...")
        controller.run()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de haber instalado todas las dependencias:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error al inicializar el control gestual: {e}")


def main():
    """
    Función principal con opciones de ejecución.
    """
    parser = argparse.ArgumentParser(
        description="GestIX - Sistema de Interacción Gestual",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py                    # Ejecutar control gestual completo
  python main.py --test            # Probar funcionalidades básicas
  python main.py --test-volume     # Probar solo el módulo de volumen
  python main.py --test-brightness # Probar solo el módulo de brillo
        """
    )
    
    parser.add_argument(
        '--test', 
        action='store_true',
        help='Ejecutar pruebas de funcionalidades básicas'
    )
    
    parser.add_argument(
        '--test-volume',
        action='store_true', 
        help='Ejecutar pruebas específicas del módulo de volumen'
    )
    
    parser.add_argument(
        '--test-brightness',
        action='store_true',
        help='Ejecutar pruebas específicas del módulo de brillo'
    )
    
    args = parser.parse_args()
    
    print("🎮 GestIX - Sistema de Interacción Gestual")
    print("🏛️ Universidad Nacional de Colombia")
    print("=" * 50)
    
    if args.test:
        # Ejecutar pruebas básicas
        test_basic_functionality()
        
    elif args.test_volume:
        # Ejecutar pruebas específicas de volumen
        try:
            from test_volume import test_volume_control
            test_volume_control()
        except ImportError:
            print("❌ No se pudo importar el módulo de pruebas de volumen")
            
    elif args.test_brightness:
        # Ejecutar pruebas específicas de brillo
        try:
            brightness = Brightness()
            print("🔆 Prueba del módulo de brillo:")
            print(f"   - Brillo actual: {brightness.getBrightness()}%")
            
            # Obtener lista de monitores
            monitors = brightness.getMonitors()
            if monitors:
                print(f"   - Monitores disponibles: {len(monitors)}")
                for i, monitor in enumerate(monitors):
                    print(f"     [{i}] {monitor}")
            else:
                print("   - Monitor principal detectado")
                
        except Exception as e:
            print(f"❌ Error en la prueba de brillo: {e}")
            
    else:
        # Ejecutar el sistema completo
        print("🎯 Iniciando sistema completo...")
        
        # Primero verificar que las funcionalidades básicas funcionen
        if test_basic_functionality():
            print("\n" + "="*50)
            run_gesture_control()
        else:
            print("\n❌ Las pruebas básicas fallaron. Revisa la configuración.")
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Aplicación interrumpida por el usuario")
        print("👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}")
        sys.exit(1)