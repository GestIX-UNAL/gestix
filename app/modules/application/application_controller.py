import cv2
import subprocess
import os
from app.utils.flags import Flags


class ApplicationController:
    """
    Controlador para abrir aplicaciones mediante gestos.
    
    Gestos reconocidos:
    - Mano izquierda con 3 dedos + mano derecha con 1 dedo: Abre Firefox una sola vez
    
    La aplicación solo se abre una vez por cada activación del gesto,
    evitando múltiples aperturas mientras se mantiene el gesto.
    """
    
    def __init__(self):
        """
        Inicializa el controlador de aplicaciones.
        """
        self.firefox_opened = False  # Control para abrir Firefox solo una vez
        self.gesture_active = False  # Control para detectar cuando el gesto termina
        
    def process_gesture(self, frame, hand_landmarks_list, hand_labels):
        """
        Procesa los gestos específicos de aplicaciones y retorna el frame modificado y mensaje.
        
        Args:
            frame: Frame de la cámara
            hand_landmarks_list: Lista de landmarks de las manos detectadas
            hand_labels: Lista de etiquetas (Left/Right) de las manos
            
        Returns:
            tuple: (frame modificado, mensaje de estado)
        """
        # Detectar gestos específicos de aplicaciones
        gesture_detected, message = self.detect_application_gesture(hand_landmarks_list, hand_labels)
        
        # Dibujar información en el frame
        frame = self.draw_application_info(frame)
        
        if gesture_detected:
            # El gesto específico ya fue procesado en detect_application_gesture
            pass
        else:
            # Si no hay gesto activo, resetear el control
            if self.gesture_active:
                self.gesture_active = False
                self.firefox_opened = False
            
        return frame, message
        
    def detect_application_gesture(self, hand_landmarks_list, hand_labels):
        """
        Detecta gestos específicos para abrir aplicaciones:
        - Mano izquierda con 3 dedos + mano derecha con 1 dedo: Abre Firefox
        
        Args:
            hand_landmarks_list: Lista de landmarks de las manos detectadas
            hand_labels: Lista de etiquetas (Left/Right) de las manos
            
        Returns:
            tuple: (gesto_detectado, mensaje)
        """
        left_three_fingers = False
        right_one_finger = False
        
        for hand_landmarks, label in zip(hand_landmarks_list, hand_labels):
            if label == "Left":  # Mano izquierda en vista espejo
                # Contar dedos de la mano izquierda
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) == 3:
                    left_three_fingers = True
                    
            elif label == "Right":  # Mano derecha en vista espejo
                # Contar dedos de la mano derecha
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) == 1:
                    right_one_finger = True
        
        # Lógica para abrir Firefox
        if left_three_fingers and right_one_finger:
            self.gesture_active = True
            if not self.firefox_opened:
                self.open_firefox()
                self.firefox_opened = True
                return True, "Abriendo Firefox"
            else:
                return True, "Firefox ya abierto (gesto activo)"
        
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
        
        # Pulgar (Thumb) - comparación en eje X
        if landmarks[4].x > landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
            
        # Otros dedos - comparación en eje Y
        for tip_id in [8, 12, 16, 20]:  # Índice, medio, anular, meñique
            if landmarks[tip_id].y < landmarks[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
                
        return fingers
        
    def open_firefox(self):
        """
        Abre Firefox usando subprocess y xdg-open.
        
        Como el script se ejecuta con sudo, necesitamos ejecutar Firefox
        como el usuario real (no como root) usando sudo -u.
        Esto es necesario porque:
        - Firefox no debe ejecutarse como root por seguridad
        - xdg-open necesita acceso al display del usuario
        
        Intenta obtener el usuario real y abrir Firefox de manera no bloqueante.
        Si falla, imprime un mensaje de error.
        """
        try:
            # Obtener el usuario real (no root) de varias formas
            # SUDO_USER es la variable que contiene el usuario original cuando se usa sudo
            username = os.environ.get('SUDO_USER') or os.environ.get('USER') or os.getlogin()
            
            if not username or username == 'root':
                print("⚠️  Advertencia: Ejecutando como root, Firefox se abrirá como root")
                # Intentar abrir sin sudo si no hay usuario
                subprocess.Popen(
                    ['xdg-open', 'https://www.mozilla.org'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            else:
                # Abrir como el usuario real usando sudo -u
                subprocess.Popen(
                    ['sudo', '-u', username, 'xdg-open', 'https://www.mozilla.org'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
            
            print(f"✅ Firefox abierto correctamente para el usuario: {username}")
            
        except FileNotFoundError:
            print("❌ Error: xdg-open no está disponible")
            print("💡 Intenta instalar: sudo apt install xdg-utils")
        except Exception as e:
            print(f"❌ Error al abrir Firefox: {e}")
            print("💡 Asegúrate de ejecutar con: sudo .venv/bin/python main.py --camera")
        
    def draw_application_info(self, frame):
        """
        Dibuja información específica del control de aplicaciones en el frame.
        
        Args:
            frame: Frame de la cámara
            
        Returns:
            Frame modificado con la información visual
        """
        # Información principal del estado
        status_text = "Firefox: Abierto" if self.firefox_opened else "Firefox: Listo"
        color = (0, 255, 0) if self.firefox_opened else (255, 255, 255)
        
        cv2.putText(frame, status_text, (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Indicador visual de gesto activo
        if self.gesture_active:
            cv2.putText(frame, "Gesto Activo", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Instrucciones
        cv2.putText(frame, "L:3 dedos + R:1 dedo = Firefox", (10, 210), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return frame
        
if __name__ == "__main__":
    # Ejemplo de uso directo (no recomendado, usar main.py en su lugar)
    from app.modules.camera.camera import Camera
    
    camera = Camera()
    application_controller = ApplicationController()
    camera.register_controller(Flags.APPLICATION, application_controller)
    camera.run()
