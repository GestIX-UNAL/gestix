from enum import Enum

class Flags(Enum):
    """
    Flags que representan los diferentes modos de control por gestos.
    
    Cada flag se activa con un gesto específico:
    - BRIGHTNESS: Mano izquierda con 1 dedo levantado
      Control de brillo de pantalla (subir/bajar con mano derecha)
    
    - APPLICATION: Mano izquierda con 3 dedos levantados
      Abre una aplicación específica (Firefox con mano derecha 1 dedo)
    
    - WINDOW: Reservado para control de ventanas
    
    - CONTROLLER: Reservado para funcionalidades futuras
    """
    BRIGHTNESS = "BRILLO"
    APPLICATION = "APLICACION"
    WINDOW = "VENTANA"
    CONTROLLER = "CONTROLADOR"