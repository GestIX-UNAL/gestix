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
        
        Gestos:
        - Palma abierta (4-5 dedos): Abre aplicación (una sola vez)
        - Palma cerrada (0 dedos/puño): Cierra aplicación y permite volver a abrirla
        """
        self.application_opened = False  # Control para saber si la aplicación está abierta
        self.palm_open_activated = False  # Control para abrir solo una vez con palma abierta
        self.palm_closed_activated = False  # Control para cerrar solo una vez con palma cerrada
        self.application_process = None  # Referencia al proceso de la aplicación (si es posible)
        
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
            
        return frame, message
        
    def detect_application_gesture(self, hand_landmarks_list, hand_labels):
        """
        Detecta gestos específicos para controlar aplicaciones:
        - Mano izquierda con 3 dedos + mano derecha con palma abierta (4-5 dedos): Abre aplicación
        - Mano izquierda con 3 dedos + mano derecha con palma cerrada (0 dedos): Cierra aplicación
        
        Args:
            hand_landmarks_list: Lista de landmarks de las manos detectadas
            hand_labels: Lista de etiquetas (Left/Right) de las manos
            
        Returns:
            tuple: (gesto_detectado, mensaje)
        """
        left_three_fingers = False
        right_palm_open = False
        right_palm_closed = False
        
        for hand_landmarks, label in zip(hand_landmarks_list, hand_labels):
            if label == "Left":  # Mano izquierda en vista espejo
                # Contar dedos de la mano izquierda
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) == 3:
                    left_three_fingers = True
                    
            elif label == "Right":  # Mano derecha en vista espejo
                # Contar dedos de la mano derecha
                fingers = self.count_fingers(hand_landmarks.landmark)
                finger_count = sum(fingers)
                
                # Palma abierta: 4 o 5 dedos levantados
                if finger_count >= 4:
                    right_palm_open = True
                # Palma cerrada: 0 dedos (puño cerrado)
                elif finger_count == 0:
                    right_palm_closed = True
        
        # Lógica para ABRIR aplicación con palma abierta
        if left_three_fingers and right_palm_open:
            # Si la palma está abierta y la aplicación no está abierta
            if not self.application_opened and not self.palm_open_activated:
                self.open_application()
                self.application_opened = True
                self.palm_open_activated = True
                self.palm_closed_activated = False  # Resetear el estado de cerrado
                return True, "Abriendo aplicacion con palma abierta"
            elif self.application_opened:
                return True, "Aplicacion ya esta abierta"
            else:
                return True, "Gesto de palma abierta activo"
        
        # Lógica para CERRAR aplicación con palma cerrada
        elif left_three_fingers and right_palm_closed:
            # Si la palma está cerrada y la aplicación está abierta
            if self.application_opened and not self.palm_closed_activated:
                self.close_application()
                self.application_opened = False
                self.palm_closed_activated = True
                self.palm_open_activated = False  # Resetear el estado de abierto
                return True, "Cerrando aplicacion con palma cerrada"
            elif not self.application_opened:
                return True, "Aplicacion ya esta cerrada"
            else:
                return True, "Gesto de palma cerrada activo"
        
        # Si no se detecta ningún gesto, resetear los estados de activación
        else:
            if not left_three_fingers:
                # Cuando dejas de hacer el gesto base, resetear todo
                self.palm_open_activated = False
                self.palm_closed_activated = False
        
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
        
    def open_application(self):
        """
        Abre la aplicación (Firefox) usando subprocess y xdg-open.
        
        Como el script se ejecuta con sudo, necesitamos ejecutar la aplicación
        como el usuario real (no como root) usando sudo -u.
        Esto es necesario porque:
        - Las aplicaciones no deben ejecutarse como root por seguridad
        - xdg-open necesita acceso al display del usuario
        
        Intenta obtener el usuario real y abrir la aplicación de manera no bloqueante.
        Si falla, imprime un mensaje de error.
        """
        try:
            # Obtener el usuario real (no root) de varias formas
            # SUDO_USER es la variable que contiene el usuario original cuando se usa sudo
            username = os.environ.get('SUDO_USER') or os.environ.get('USER') or os.getlogin()
            
            if not username or username == 'root':
                print("⚠️  Advertencia: Ejecutando como root, la aplicación se abrirá como root")
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
            
            print(f"✅ Aplicación (Firefox) abierta correctamente para el usuario: {username}")
            
        except FileNotFoundError:
            print("❌ Error: xdg-open no está disponible")
            print("💡 Intenta instalar: sudo apt install xdg-utils")
        except Exception as e:
            print(f"❌ Error al abrir la aplicación: {e}")
            print("💡 Asegúrate de ejecutar con: sudo .venv/bin/python main.py --camera")
    
    def close_application(self):
        """
        Cierra la aplicación (Firefox) usando pkill.
        
        Este método busca y cierra todos los procesos de Firefox.
        Intenta usar el usuario real si se ejecuta con sudo.
        """
        try:
            # Obtener el usuario real
            username = os.environ.get('SUDO_USER') or os.environ.get('USER') or os.getlogin()
            
            if not username or username == 'root':
                print("⚠️  Advertencia: Intentando cerrar la aplicación como root")
                # Intentar cerrar sin sudo si no hay usuario
                subprocess.run(
                    ['pkill', '-f', 'firefox'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Cerrar como el usuario real usando sudo -u
                subprocess.run(
                    ['sudo', '-u', username, 'pkill', '-f', 'firefox'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            print(f"✅ Aplicación (Firefox) cerrada correctamente para el usuario: {username}")
            
        except FileNotFoundError:
            print("❌ Error: pkill no está disponible")
        except Exception as e:
            print(f"❌ Error al cerrar la aplicación: {e}")
        
    def draw_application_info(self, frame):
        """
        Dibuja información específica del control de aplicaciones en el frame.
        
        Args:
            frame: Frame de la cámara
            
        Returns:
            Frame modificado con la información visual
        """
        # Información principal del estado
        status_text = "App: ABIERTA" if self.application_opened else "App: CERRADA"
        color = (0, 255, 0) if self.application_opened else (255, 50, 50)
        
        cv2.putText(frame, status_text, (10, 150), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        
        # Indicador visual de gestos activos
        if self.palm_open_activated:
            cv2.putText(frame, "Palma Abierta (Abrir)", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        elif self.palm_closed_activated:
            cv2.putText(frame, "Palma Cerrada (Cerrar)", (10, 180), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
        
        # Instrucciones
        cv2.putText(frame, "L:3 dedos + R:Palma abierta = Abrir", (10, 210), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(frame, "L:3 dedos + R:Palma cerrada = Cerrar", (10, 240), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        return frame
        
if __name__ == "__main__":
    # Ejemplo de uso directo (no recomendado, usar main.py en su lugar)
    from app.modules.camera.camera import Camera
    
    camera = Camera()
    application_controller = ApplicationController()
    camera.register_controller(Flags.APPLICATION, application_controller)
    camera.run()
