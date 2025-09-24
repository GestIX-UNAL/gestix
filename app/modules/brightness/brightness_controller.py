import cv2
from app.utils.flags import Flags
from core.modules.brightness.brightness import Brightness

class BrightnessController:
    def __init__(self):
        # Usar la clase Brightness del core para controlar realmente el brillo
        self.brightness_core = Brightness()
        # Obtener el brillo actual del sistema
        try:
            current_brightness = self.brightness_core.getBrightness()
            # Manejar el caso donde getBrightness retorna una lista
            if isinstance(current_brightness, list):
                self.brightness = current_brightness[0] if current_brightness else 50
            else:
                self.brightness = current_brightness
        except Exception as e:
            print(f"Warning: No se pudo obtener el brillo actual: {e}")
            self.brightness = 50  # Valor por defecto
        
        self.min_brightness = 0
        self.max_brightness = 100
        self.brightness_step = 2
        
    def process_gesture(self, frame, hand_landmarks_list, hand_labels):
        """
        Procesa los gestos específicos de brillo y retorna el frame modificado y mensaje
        """
        # Sincronizar con el brillo actual del sistema ocasionalmente
        # (evitar hacerlo en cada frame para no impactar el rendimiento)
        import time
        if not hasattr(self, '_last_sync') or time.time() - self._last_sync > 5:
            self.sync_brightness()
            self._last_sync = time.time()
        
        # Detectar gestos específicos de brillo
        gesture_detected, message = self.detect_brightness_gesture(hand_landmarks_list, hand_labels)
        
        # Dibujar información del brillo en el frame
        frame = self.draw_brightness_info(frame)
        
        if gesture_detected:
            # Aplicar el brillo al sistema
            self.apply_brightness()
            
        return frame, message
        
    def detect_brightness_gesture(self, hand_landmarks_list, hand_labels):
        """
        Detecta gestos específicos para el control de brillo:
        - Mano izquierda con 1 dedo + mano derecha abierta: subir brillo
        - Mano izquierda con 1 dedo + mano derecha cerrada: bajar brillo
        """
        left_hand_detected = False
        right_hand_detected = False
        left_one_finger = False
        right_hand_open = False
        
        for hand_landmarks, label in zip(hand_landmarks_list, hand_labels):
            if label == "Left":  # Mano izquierda en vista espejo
                left_hand_detected = True
                # La detección del dedo ya se hace en Camera.detect_flag()
                # Aquí solo confirmamos que es el gesto de brillo
                left_one_finger = True
                    
            elif label == "Right":  # Mano derecha en vista espejo
                right_hand_detected = True
                # Necesitamos importar el método is_hand_open de Camera
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) >= 4:
                    right_hand_open = True
        
        # Lógica específica del control de brillo
        if left_one_finger and right_hand_open:
            self.brightness = min(self.max_brightness, self.brightness + self.brightness_step)
            return True, f"Subiendo brillo: {self.brightness}"
        elif left_one_finger and not right_hand_open and right_hand_detected:
            self.brightness = max(self.min_brightness, self.brightness - self.brightness_step)
            return True, f"Bajando brillo: {self.brightness}"
        
        return False, None
    
    def count_fingers(self, landmarks):
        """
        Método helper para contar dedos (copiado de Camera para no crear dependencia)
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
        
    def apply_brightness(self):
        """
        Aplica el brillo al sistema usando la clase Brightness del core
        """
        try:
            # Aplicar el brillo real al sistema
            self.brightness_core.setBrightness(int(self.brightness))
            print(f"✅ Brillo aplicado: {self.brightness}%")
            return self.brightness
        except Exception as e:
            print(f"❌ Error al aplicar brillo: {e}")
            return None
    
    def sync_brightness(self):
        """
        Sincroniza el valor interno con el brillo actual del sistema
        """
        try:
            current_brightness = self.brightness_core.getBrightness()
            if isinstance(current_brightness, list):
                # Si hay múltiples monitores, tomar el primero
                current_brightness = current_brightness[0] if current_brightness else 50
            self.brightness = current_brightness
            return self.brightness
        except Exception as e:
            print(f"Warning: No se pudo sincronizar el brillo: {e}")
            return self.brightness
    
    def get_available_monitors(self):
        """
        Obtiene la lista de monitores disponibles
        """
        try:
            monitors = self.brightness_core.getMonitors()
            return monitors
        except Exception as e:
            print(f"Warning: No se pudo obtener la lista de monitores: {e}")
            return []
        
    def draw_brightness_info(self, frame):
        """
        Dibuja información específica del control de brillo en el frame
        """
        # Información principal del brillo
        cv2.putText(frame, f"Brightness: {self.brightness}%", (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        
        # Información adicional sobre el estado
        try:
            monitors = self.get_available_monitors()
            if monitors:
                cv2.putText(frame, f"Monitors: {len(monitors)}", (10, 180), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        except:
            cv2.putText(frame, "Monitor info: N/A", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Barra visual del brillo
        bar_width = 200
        bar_height = 20
        bar_x = 250
        bar_y = 135
        
        # Fondo de la barra
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
        
        # Barra de progreso
        progress_width = int((self.brightness / self.max_brightness) * bar_width)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 255), -1)
        
        # Borde de la barra
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 1)
        
        return frame
        
if __name__ == "__main__":
    # Ejemplo de uso directo (no recomendado, usar main.py en su lugar)
    from app.modules.camera.camera import Camera
    
    camera = Camera()
    brightness_controller = BrightnessController()
    camera.register_controller(Flags.BRIGHTNESS, brightness_controller)
    camera.run()
