from enum import Enum

class Flags(Enum):
    BRIGHTNESS = "BRILLO"
    VOLUME = "VOLUMEN"
    WINDOW = "VENTANA"
    CONTROLLER = "CONTROLADOR"

class GestureMode(Enum):
    BRIGHTNESS_CONTROL = "brightness"
    VOLUME_CONTROL = "volume"
    WINDOW_CONTROL = "window"
    MIXED_CONTROL = "mixed"

class GesturePatterns(Enum):
    # Gestos para brillo
    BRIGHTNESS_UP = "brightness_up"      # Mano izq. 1 dedo + mano der. abierta
    BRIGHTNESS_DOWN = "brightness_down"  # Mano izq. 1 dedo + mano der. cerrada
    
    # Gestos para volumen
    VOLUME_UP = "volume_up"              # Mano der. 1 dedo + mano izq. abierta
    VOLUME_DOWN = "volume_down"          # Mano der. 1 dedo + mano izq. cerrada
    MUTE_TOGGLE = "mute_toggle"          # Ambas manos cerradas
    
    # Gestos para cambio de modo
    MODE_SWITCH = "mode_switch"          # Ambas manos con 2 dedos (V)