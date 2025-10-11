"""
Configuración del Sistema GestIX
Universidad Nacional de Colombia - Computación Visual
"""

class GestixConfig:
    """
    Configuración centralizada para el sistema GestIX.
    """
    
    # === CONFIGURACIÓN DE CÁMARA ===
    CAMERA_ID = 0
    CAMERA_WIDTH = 640
    CAMERA_HEIGHT = 480
    CAMERA_FPS = 30
    
    # === CONFIGURACIÓN DE MEDIAPIPE ===
    DETECTION_CONFIDENCE = 0.7
    TRACKING_CONFIDENCE = 0.5
    MAX_HANDS = 2
    
    # === CONFIGURACIÓN DE GESTOS ===
    GESTURE_COOLDOWN = 0.1  # Segundos entre gestos
    GESTURE_STABILITY_FRAMES = 3  # Frames para confirmar gesto
    
    # === INCREMENTOS DE CONTROL ===
    BRIGHTNESS_STEP = 3  # Porcentaje por gesto
    VOLUME_STEP = 3      # Porcentaje por gesto
    
    # === RANGOS DE CONTROL ===
    BRIGHTNESS_MIN = 0
    BRIGHTNESS_MAX = 100
    VOLUME_MIN = 0
    VOLUME_MAX = 100
    
    # === CONFIGURACIÓN VISUAL ===
    FONT = 0  # cv2.FONT_HERSHEY_SIMPLEX
    FONT_SCALE = 0.7
    FONT_THICKNESS = 2
    
    # Colores (BGR format)
    COLOR_ACTIVE = (0, 255, 0)      # Verde
    COLOR_INACTIVE = (100, 100, 100)  # Gris
    COLOR_WARNING = (0, 255, 255)   # Amarillo
    COLOR_ERROR = (0, 0, 255)       # Rojo
    COLOR_INFO = (255, 255, 255)    # Blanco
    
    # === CONFIGURACIÓN DE RECONOCIMIENTO ===
    FINGER_TIPS = [4, 8, 12, 16, 20]  # IDs de puntas de dedos
    FINGER_PIPS = [3, 6, 10, 14, 18]  # IDs de articulaciones PIP
    
    # === UMBRALES DE GESTOS ===
    OPEN_HAND_THRESHOLD = 4  # Dedos mínimos para mano abierta
    ONE_FINGER_THRESHOLD = 1  # Exactamente un dedo
    TWO_FINGER_THRESHOLD = 2  # Exactamente dos dedos
    
    # === CONFIGURACIÓN DE MODOS ===
    DEFAULT_MODE = "brightness"  # Modo inicial
    MODE_SWITCH_COOLDOWN = 1.0   # Cooldown para cambio de modo (segundos)
    
    # === CONFIGURACIÓN DE SEGURIDAD ===
    MAX_BRIGHTNESS_CHANGE_PER_SECOND = 20  # Máximo cambio de brillo por segundo
    MAX_VOLUME_CHANGE_PER_SECOND = 20      # Máximo cambio de volumen por segundo
    
    # === CONFIGURACIÓN DE DEBUG ===
    DEBUG_MODE = False
    SHOW_LANDMARKS = True
    SHOW_CONNECTIONS = True
    SHOW_FPS = True
    
    # === MENSAJES DEL SISTEMA ===
    MESSAGES = {
        'init_success': '✅ Sistema inicializado correctamente',
        'init_error': '❌ Error al inicializar el sistema',
        'camera_error': '❌ Error al acceder a la cámara',
        'brightness_control': '🔆 Controlando brillo',
        'volume_control': '🔊 Controlando volumen',
        'mode_switch': '🔄 Cambiando modo',
        'mute_toggle': '🔇 Alternando silencio',
        'gesture_detected': '👋 Gesto detectado',
        'gesture_stable': '✅ Gesto confirmado',
        'cooldown_active': '⏳ Esperando cooldown',
        'exit_app': '👋 Cerrando aplicación'
    }
    
    # === CONFIGURACIÓN DE ARCHIVOS ===
    LOG_FILE = "gestix.log"
    CONFIG_FILE = "gestix_config.json"
    
    @classmethod
    def get_gesture_patterns(cls):
        """
        Obtiene los patrones de gestos configurados.
        
        Returns:
            dict: Diccionario con patrones de gestos
        """
        return {
            'brightness_up': {
                'left_hand': 'one_finger',
                'right_hand': 'open',
                'action': 'increase_brightness',
                'step': cls.BRIGHTNESS_STEP
            },
            'brightness_down': {
                'left_hand': 'one_finger', 
                'right_hand': 'closed',
                'action': 'decrease_brightness',
                'step': cls.BRIGHTNESS_STEP
            },
            'volume_up': {
                'left_hand': 'open',
                'right_hand': 'one_finger',
                'action': 'increase_volume',
                'step': cls.VOLUME_STEP
            },
            'volume_down': {
                'left_hand': 'closed',
                'right_hand': 'one_finger', 
                'action': 'decrease_volume',
                'step': cls.VOLUME_STEP
            },
            'mute_toggle': {
                'left_hand': 'closed',
                'right_hand': 'closed',
                'action': 'toggle_mute'
            },
            'mode_switch': {
                'left_hand': 'two_fingers',
                'right_hand': 'two_fingers',
                'action': 'switch_mode'
            }
        }
    
    @classmethod
    def validate_config(cls):
        """
        Valida la configuración actual.
        
        Returns:
            bool: True si la configuración es válida
        """
        try:
            # Validar rangos
            assert 0 <= cls.BRIGHTNESS_MIN <= cls.BRIGHTNESS_MAX <= 100
            assert 0 <= cls.VOLUME_MIN <= cls.VOLUME_MAX <= 100
            
            # Validar pasos
            assert 0 < cls.BRIGHTNESS_STEP <= 10
            assert 0 < cls.VOLUME_STEP <= 10
            
            # Validar tiempos
            assert 0 < cls.GESTURE_COOLDOWN <= 1.0
            assert 1 <= cls.GESTURE_STABILITY_FRAMES <= 10
            
            # Validar confianza
            assert 0.1 <= cls.DETECTION_CONFIDENCE <= 1.0
            assert 0.1 <= cls.TRACKING_CONFIDENCE <= 1.0
            
            return True
            
        except AssertionError:
            return False
    
    @classmethod
    def print_config(cls):
        """
        Imprime la configuración actual.
        """
        print("🔧 === CONFIGURACIÓN GESTIX ===")
        print(f"📷 Cámara: ID={cls.CAMERA_ID}, Resolución={cls.CAMERA_WIDTH}x{cls.CAMERA_HEIGHT}")
        print(f"🤖 MediaPipe: Detección={cls.DETECTION_CONFIDENCE}, Seguimiento={cls.TRACKING_CONFIDENCE}")
        print(f"👋 Gestos: Cooldown={cls.GESTURE_COOLDOWN}s, Estabilidad={cls.GESTURE_STABILITY_FRAMES} frames")
        print(f"🎚️ Control: Brillo±{cls.BRIGHTNESS_STEP}%, Volumen±{cls.VOLUME_STEP}%")
        print(f"🔍 Debug: {cls.DEBUG_MODE}, Landmarks: {cls.SHOW_LANDMARKS}")
        print("=" * 40)


# Crear instancia global de configuración
config = GestixConfig()

# Validar configuración al importar
if not config.validate_config():
    print("⚠️ ADVERTENCIA: Configuración inválida detectada")
    print("🔧 Usando valores por defecto seguros")


# Configuración específica para desarrollo/producción
class DevelopmentConfig(GestixConfig):
    """Configuración para desarrollo"""
    DEBUG_MODE = True
    GESTURE_COOLDOWN = 0.05  # Más sensible para pruebas
    BRIGHTNESS_STEP = 5
    VOLUME_STEP = 5


class ProductionConfig(GestixConfig):
    """Configuración para producción"""
    DEBUG_MODE = False
    GESTURE_COOLDOWN = 0.15  # Más estable para uso real
    BRIGHTNESS_STEP = 2
    VOLUME_STEP = 2


# Función para cambiar configuración según el entorno
def get_config(environment='production'):
    """
    Obtiene la configuración según el entorno.
    
    Args:
        environment (str): 'development' o 'production'
        
    Returns:
        GestixConfig: Configuración apropiada
    """
    if environment.lower() == 'development':
        return DevelopmentConfig()
    else:
        return ProductionConfig()


if __name__ == "__main__":
    """
    Prueba de la configuración.
    """
    print("🧪 Probando configuración de GestIX...")
    
    # Probar configuración por defecto
    config.print_config()
    
    # Validar configuración
    if config.validate_config():
        print("✅ Configuración válida")
    else:
        print("❌ Configuración inválida")
    
    # Mostrar patrones de gestos
    patterns = config.get_gesture_patterns()
    print(f"\n👋 Patrones de gestos configurados: {len(patterns)}")
    for name, pattern in patterns.items():
        print(f"   - {name}: {pattern['action']}")
    
    print("\n🎯 Configuración lista para usar!")