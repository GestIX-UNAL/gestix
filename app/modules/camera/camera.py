import cv2
import mediapipe as mp
from app.utils.flags import Flags

class Camera:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.controllers = {}  # Dictionary para almacenar los controladores
        
    def count_fingers(self, landmarks):
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
        
    def register_controller(self, flag, controller):
        """
        Registra un controlador para una flag específica
        """
        self.controllers[flag] = controller
        
    def is_hand_open(self, landmarks):
        fingers = self.count_fingers(landmarks)
        return sum(fingers) >= 4
        
    def register_controller(self, flag, controller):
        """
        Registra un controlador para una flag específica
        """
        self.controllers[flag] = controller
        
    def detect_flag(self, hand_landmarks_list, hand_labels):
        """
        Detecta qué flag/gesto se está realizando basado en las manos detectadas
        Retorna la flag detectada o None
        """
        # Detectar gesto de brillo: mano izquierda con 1 dedo
        for hand_landmarks, label in zip(hand_landmarks_list, hand_labels):
            if label == "Left":  # Mano izquierda en vista espejo
                fingers = self.count_fingers(hand_landmarks.landmark)
                if sum(fingers) == 1:  # Solo un dedo levantado
                    return Flags.BRIGHTNESS
        
        # Aquí se pueden agregar más detecciones para otras flags
        # Por ejemplo:
        # - Detección de gesto para WINDOW
        # - Detección de gesto para CONTROLLER
        # etc.
        
        return None
        
    def detect_hands(self):
        """
        Detecta manos en el frame y retorna el frame procesado junto con
        la información de las manos detectadas para que otros módulos
        puedan implementar su propia lógica de gestos.
        
        Returns:
            tuple: (frame, hand_landmarks_list, hand_labels)
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, [], []
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        hand_landmarks_list = []
        hand_labels = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = hand_info.classification[0].label
                
                # Agregar landmarks y etiquetas a las listas
                hand_landmarks_list.append(hand_landmarks)
                hand_labels.append(label)
                
                # Dibujar las conexiones de la mano
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        return frame, hand_landmarks_list, hand_labels
        
    def run(self):
        """
        Bucle principal que detecta flags y delega a los controladores específicos
        """
        while True:
            frame, hand_landmarks_list, hand_labels = self.detect_hands()
            
            if frame is not None:
                # Detectar qué flag/gesto se está realizando
                detected_flag = self.detect_flag(hand_landmarks_list, hand_labels)
                
                if detected_flag and detected_flag in self.controllers:
                    # Delegar al controlador específico
                    controller = self.controllers[detected_flag]
                    frame, message = controller.process_gesture(frame, hand_landmarks_list, hand_labels)
                    
                    # Mostrar mensaje del controlador
                    if message:
                        cv2.putText(frame, message, (10, 110), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Mostrar información básica
                cv2.putText(frame, f"Hands detected: {len(hand_landmarks_list)}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                
                if detected_flag:
                    cv2.putText(frame, f"Flag: {detected_flag.value}", (10, 70), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
                cv2.imshow('Gesture Control System', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        self.release()
    
    def release(self):
        """
        Libera los recursos de la cámara
        """
        self.cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    camera = Camera()
    camera.run()