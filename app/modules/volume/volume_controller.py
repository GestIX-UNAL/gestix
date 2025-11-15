import cv2
from app.utils.flags import Flags
from core.modules.volume.volume import Volume

class VolumeController:
    """
    Controlador para ajustar el volumen del sistema mediante gestos.
    
    Gestos reconocidos:
    - Mano izquierda con 2 dedos: Activa el modo de control de volumen
    - Mano izquierda con 2 dedos + mano derecha abierta (4+ dedos): Sube el volumen
    - Mano izquierda con 2 dedos + mano derecha cerrada (puño): Baja el volumen
    
    El volumen se ajusta en pasos de 3% y se sincroniza con el sistema operativo.
    """
    
    def __init__(self):
        """
        Inicializa el controlador de volumen.
        Obtiene el volumen actual del sistema y configura los parámetros.
        """
        # Usar la clase Volume del core para controlar realmente el volumen
        self.volume_core = Volume()
        # Obtener el volumen actual del sistema
        try:
            current_volume = self.volume_core.getVolume()
            # Manejar el caso donde getVolume retorna un valor
            if isinstance(current_volume, list):
                self.volume = current_volume[0] if current_volume else 50
            else:
                self.volume = current_volume
        except Exception as e:
            print(f"Warning: No se pudo obtener el volumen actual: {e}")
            self.volume = 50  # Valor por defecto
        
        self.min_volume = 0
        self.max_volume = 100
        self.volume_step = 3
        
    def process_gesture(self, frame, hand_landmarks_list, hand_labels):
        """
        Procesa los gestos específicos de volumen y retorna el frame modificado y mensaje.
        
        Args:
            frame: Frame de la cámara
            hand_landmarks_list: Lista de landmarks de las manos detectadas
            hand_labels: Lista de etiquetas (Left/Right) de las manos
            
        Returns:
            tuple: (frame modificado, mensaje de estado)
        """
        # Sincronizar con el volumen actual del sistema ocasionalmente
        # (evitar hacerlo en cada frame para no impactar el rendimiento)
        import time
        if not hasattr(self, '_last_sync') or time.time() - self._last_sync > 5:
            self.sync_volume()
            self._last_sync = time.time()
        
        # Detectar gestos específicos de volumen
        gesture_detected, message = self.detect_volume_gesture(hand_landmarks_list, hand_labels)
        
        # Dibujar información del volumen en el frame
        frame = self.draw_volume_info(frame)
        
        if gesture_detected:
            # Aplicar el volumen al sistema
            self.apply_volume()
            
        return frame, message
        
    def detect_volume_gesture(self, hand_landmarks_list, hand_labels):
        """
        Detecta gestos específicos para el control de volumen:
        - Mano izquierda con 2 dedos + mano derecha abierta (4+ dedos): Subir volumen
        - Mano izquierda con 2 dedos + mano derecha cerrada: Bajar volumen
        
        Args:
            hand_landmarks_list: Lista de landmarks de las manos detectadas
            hand_labels: Lista de etiquetas (Left/Right) de las manos
            
        Returns:
            tuple: (gesto_detectado, mensaje)
        """
        left_hand_detected = False
        right_hand_detected = False
        left_two_fingers = False
        right_hand_open = False
        
        for hand_landmarks, label in zip(hand_landmarks_list, hand_labels):
            if label == "Left":  # Mano izquierda en vista espejo
                left_hand_detected = True
                # La detección de los dedos ya se hace en Camera.detect_flag()
                # Aquí solo confirmamos que es el gesto de volumen
                left_two_fingers = True
                    
            elif label == "Right":  # Mano derecha en vista espejo
                right_hand_detected = True
                # Contar dedos de la mano derecha
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) >= 4:
                    right_hand_open = True
        
        # Lógica específica del control de volumen
        if left_two_fingers and right_hand_open:
            self.volume = min(self.max_volume, self.volume + self.volume_step)
            return True, f"Subiendo volumen: {self.volume}%"
        elif left_two_fingers and not right_hand_open and right_hand_detected:
            self.volume = max(self.min_volume, self.volume - self.volume_step)
            return True, f"Bajando volumen: {self.volume}%"
        
        return False, None
    
    def count_fingers(self, landmarks):
        """
        Cuenta el número de dedos levantados en una mano.
        
        Args:
            landmarks: Landmarks de la mano detectada
            
        Returns:
            list: Lista con 1 (levantado) o 0 (no levantado) para cada dedo
        """
        fingers = []
        # Thumb
        if landmarks[4].x > landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
        # Other fingers
        for tip_id in [8, 12, 16, 20]:
            if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
        
    def apply_volume(self):
        """
        Aplica el volumen al sistema usando la clase Volume del core.
        
        Returns:
            int or None: El valor de volumen aplicado o None si hay error
        """
        try:
            # Aplicar el volumen real al sistema
            self.volume_core.setVolume(int(self.volume))
            print(f"🔊 Volumen aplicado: {self.volume}%")
            return self.volume
        except Exception as e:
            print(f"❌ Error al aplicar volumen: {e}")
            return None
            
    def sync_volume(self):
        """
        Sincroniza el volumen interno con el volumen actual del sistema.
        Útil para detectar cambios externos al volumen.
        
        Returns:
            int or None: El volumen sincronizado o None si hay error
        """
        try:
            current_volume = self.volume_core.getVolume()
            if isinstance(current_volume, list):
                self.volume = current_volume[0] if current_volume else self.volume
            else:
                self.volume = current_volume
            return self.volume
        except Exception as e:
            print(f"Warning: No se pudo sincronizar el volumen: {e}")
            return None
            
    def draw_volume_info(self, frame):
        """
        Dibuja información del volumen en el frame.
        
        Args:
            frame: Frame de la cámara
            
        Returns:
            frame modificado con información del volumen
        """
        h, w, c = frame.shape
        
        # Dibujar barra de volumen
        bar_x = 50
        bar_y = h - 100
        bar_width = 300
        bar_height = 30
        
        # Fondo de la barra
        cv2.rectangle(frame, (bar_x, bar_y), 
                     (bar_x + bar_width, bar_y + bar_height),
                     (50, 50, 50), -1)
        
        # Barra de progreso del volumen
        volume_width = int((self.volume / 100) * bar_width)
        color = (0, 255, 0) if self.volume > 30 else (0, 165, 255)
        cv2.rectangle(frame, (bar_x, bar_y),
                     (bar_x + volume_width, bar_y + bar_height),
                     color, -1)
        
        # Borde de la barra
        cv2.rectangle(frame, (bar_x, bar_y),
                     (bar_x + bar_width, bar_y + bar_height),
                     (255, 255, 255), 2)
        
        # Texto del volumen
        volume_text = f"Volumen: {int(self.volume)}%"
        cv2.putText(frame, volume_text, (bar_x, bar_y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Icono de volumen
        icon_text = "🔊" if self.volume > 50 else "🔉" if self.volume > 0 else "🔇"
        cv2.putText(frame, icon_text, (bar_x + bar_width + 20, bar_y + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
        
        return frame
    
    def get_volume(self):
        """
        Obtiene el valor actual del volumen.
        
        Returns:
            int: Nivel de volumen actual (0-100)
        """
        return self.volume
    
    def set_volume(self, value):
        """
        Establece el valor del volumen.
        
        Args:
            value (int): Nivel de volumen deseado (0-100)
        """
        self.volume = max(self.min_volume, min(self.max_volume, value))
        self.apply_volume()
