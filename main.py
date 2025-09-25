"""
GestIX - Sistema de Control por Gestos
Punto de entrada principal del sistema
"""
from app.modules.camera.camera import Camera
from app.modules.brightness.brightness_controller import BrightnessController
from app.utils.flags import Flags

def main():
    print("=== GestIX - Sistema de Control por Gestos ===")
    print("Iniciando sistema...")
    
    try:
        # Crear instancias
        camera = Camera()
        brightness_controller = BrightnessController()
        
        # Registrar controladores
        camera.register_controller(Flags.BRIGHTNESS, brightness_controller)
        
        print("✅ Sistema iniciado correctamente")
        print("📷 Cámara activada")
        print("🔆 Controlador de brillo registrado")

        # Iniciar el bucle principal
        camera.run()
        
    except KeyboardInterrupt:
        print("\n👋 Saliendo del sistema...")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que la cámara esté disponible y las dependencias instaladas.")

if __name__ == "__main__":
    main()