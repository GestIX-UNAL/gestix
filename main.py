"""
GestIX - Sistema de Control por Gestos
Punto de entrada principal del sistema
"""
import argparse
from app.modules.camera.camera import Camera
from app.modules.brightness.brightness_controller import BrightnessController
from app.utils.flags import Flags

def main():
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='GestIX - Sistema de Control por Gestos')
    parser.add_argument('--camera', action='store_true', 
                       help='Mostrar la ventana de la cámara (interfaz visual)')
    
    args = parser.parse_args()
    
    print("=== GestIX - Sistema de Control por Gestos ===")
    print("Iniciando sistema...")
    
    if args.camera:
        print("📷 Modo visual: Ventana de cámara activada")
    else:
        print("🔇 Modo silencioso: Sin interfaz visual")
    
    try:
        # Crear instancias con el parámetro show_window
        camera = Camera(show_window=args.camera)
        brightness_controller = BrightnessController()
        
        # Registrar controladores
        camera.register_controller(Flags.BRIGHTNESS, brightness_controller)
        
        print("✅ Sistema iniciado correctamente")
        print("� Controlador de brillo registrado")
        
        if not args.camera:
            print("💡 Consejo: Usa --camera para ver la interfaz visual")
            print("� Presiona Ctrl+C para detener el sistema")

        # Iniciar el bucle principal
        camera.run()
        
    except KeyboardInterrupt:
        print("\n👋 Saliendo del sistema...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que la cámara esté disponible y las dependencias instaladas.")

if __name__ == "__main__":
    main()