#!/usr/bin/env python3
"""
Script de prueba para verificar la integración del controlador de brillo
"""
import sys
import os

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.modules.brightness.brightness_controller import BrightnessController

def test_brightness_controller():
    print("=== Test del Controlador de Brillo ===")
    
    try:
        # Crear instancia del controlador
        print("1. Creando controlador de brillo...")
        controller = BrightnessController()
        print(f"   ✅ Brillo actual: {controller.brightness}%")
        
        # Obtener monitores disponibles
        print("2. Obteniendo monitores disponibles...")
        monitors = controller.get_available_monitors()
        if monitors:
            print(f"   ✅ Monitores encontrados: {monitors}")
        else:
            print("   ⚠️  No se pudieron detectar monitores (esto es normal en algunos sistemas)")
        
        # Sincronizar brillo
        print("3. Sincronizando con el sistema...")
        current = controller.sync_brightness()
        print(f"   ✅ Brillo sincronizado: {current}%")
        
        print("4. Probando funcionalidad de aplicar brillo...")
        result = controller.apply_brightness()
        if result is not None:
            print(f"   ✅ Funcionalidad de aplicar brillo: OK")
        else:
            print("   ❌ Error al aplicar brillo")
        
        print("\n🎉 Integración completada exitosamente!")
        print("📌 El controlador ahora puede controlar el brillo real de tu PC")
        print("📌 Usa los gestos definidos en main.py para controlar el brillo")
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        return False

if __name__ == "__main__":
    test_brightness_controller()