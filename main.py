"""
GestIX - Sistema de Control por Gestos
Punto de entrada principal del sistema

Gestos disponibles:
1. Control de Brillo (BRIGHTNESS):
   - Mano izquierda: 1 dedo levantado (activa el modo)
   - Mano derecha abierta (4+ dedos): Sube el brillo
   - Mano derecha cerrada: Baja el brillo

2. Control de Volumen (VOLUME):
   - Mano izquierda: 2 dedos levantados (activa el modo)
   - Mano derecha abierta (4+ dedos): Sube el volumen
   - Mano derecha cerrada: Baja el volumen

3. Control de Aplicaciones (APPLICATION):
   - Mano izquierda: 3 dedos levantados (activa el modo)
   - Mano derecha con palma abierta (4-5 dedos): Abre Firefox (una vez)
   - Mano derecha con palma cerrada (puño): Cierra Firefox y reinicia el gesto
"""
import argparse
from app.modules.camera.camera import Camera
from app.modules.brightness.brightness_controller import BrightnessController
from app.modules.volume.volume_controller import VolumeController
from app.modules.application.application_controller import ApplicationController
from app.utils.flags import Flags

def main():
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='GestIX - Sistema de Control por Gestos')
    parser.add_argument('--camera', action='store_true', 
                       help='Mostrar la ventana de la cámara (interfaz visual)')
    
    args = parser.parse_args()
    
    print("=== GestIX - Sistema de Control por Gestos ===")
    print("Iniciando sistema...")
    print()
    print("📋 Gestos disponibles:")
    print("  🔆 BRILLO: Mano izq. 1 dedo + Mano der. abierta/cerrada")
    print("  🔊 VOLUMEN: Mano izq. 2 dedos + Mano der. abierta/cerrada")
    print("  🚀 APLICACIONES:")
    print("     • Abrir: Mano izq. 3 dedos + Mano der. palma abierta")
    print("     • Cerrar: Mano izq. 3 dedos + Mano der. palma cerrada (puño)")
    print()
    
    if args.camera:
        print("📷 Modo visual: Ventana de cámara activada")
    else:
        print("🔇 Modo silencioso: Sin interfaz visual")
    
    try:
        # Crear instancias con el parámetro show_window
        camera = Camera(show_window=args.camera)
        brightness_controller = BrightnessController()
        volume_controller = VolumeController()
        application_controller = ApplicationController()
        
        # Registrar controladores
        camera.register_controller(Flags.BRIGHTNESS, brightness_controller)
        camera.register_controller(Flags.VOLUME, volume_controller)
        camera.register_controller(Flags.APPLICATION, application_controller)
        
        print("✅ Sistema iniciado correctamente")
        print("🔆 Controlador de brillo registrado")
        print("🔊 Controlador de volumen registrado")
        print("🚀 Controlador de aplicaciones registrado")
        
        if not args.camera:
            print()
            print("💡 Consejo: Usa --camera para ver la interfaz visual")
            print("⏹️  Presiona Ctrl+C para detener el sistema")

        # Iniciar el bucle principal
        camera.run()
        
    except KeyboardInterrupt:
        print("\n👋 Saliendo del sistema...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que la cámara esté disponible y las dependencias instaladas.")

if __name__ == "__main__":
    main()