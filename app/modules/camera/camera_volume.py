"""
Módulo de Cámara con Control de Volumen - GestIX
Reconocimiento gestual para control de volumen y brillo del sistema
Universidad Nacional de Colombia - Computación Visual
"""

import cv2
import mediapipe as mp
import time
from typing import Tuple, Optional, Dict

# Importar módulos del proyecto
from core.modules.brightness.brightness import Brightness
from core.modules.volume.volume import Volume
from app.utils.flags import Flags, GestureMode, GesturePatterns


class CameraVolumeController:
    """
    Controlador de cámara avanzado para reconocimiento gestual
    con soporte para control de volumen y brillo del sistema.
    """
    
    def __init__(self, camera_id: int = 0):
        """
        Inicializa el controlador de cámara y los módulos de sistema.
        
        Args:
            camera_id (int): ID de la cámara a utilizar (default: 0)
        """
        # Configuración de cámara
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(camera_id)
        
        # Configuración de MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,  # Mayor confianza para mejor precisión
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Controladores del sistema
        try:
            self.brightness_controller = Brightness()
            self.volume_controller = Volume()
            print("✅ Controladores de sistema inicializados correctamente")
        except Exception as e:
            print(f"❌ Error al inicializar controladores: {e}")
            raise
        
        # Estado del sistema
        self.current_brightness = self.brightness_controller.getBrightness()
        self.current_volume = self.volume_controller.getVolume()
        self.current_mode = GestureMode.BRIGHTNESS_CONTROL
        
        # Control de tiempo para evitar cambios muy rápidos
        self.last_gesture_time = 0
        self.gesture_cooldown = 0.1  # 100ms entre gestos
        
        # Control de estabilidad de gestos
        self.gesture_stability_frames = 3
        self.current_gesture_count = 0
        self.last_detected_gesture = None
        
        # Configuración visual
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.7
        self.font_thickness = 2
        
        print(f"🎥 Cámara inicializada - Modo: {self.current_mode.value}")
        print(f"🔆 Brillo inicial: {self.current_brightness}%")
        print(f"🔊 Volumen inicial: {self.current_volume}%")
    
    def count_fingers(self, landmarks) -> list:
        """
        Cuenta los dedos extendidos en una mano.
        
        Args:
            landmarks: Landmarks de la mano detectada
            
        Returns:
            list: Lista de estados de dedos [pulgar, índice, medio, anular, meñique]
        """
        fingers = []
        
        # IDs de las puntas de los dedos
        tip_ids = [4, 8, 12, 16, 20]
        
        # Pulgar (lógica especial por orientación)
        if landmarks[tip_ids[0]].x > landmarks[tip_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)
        
        # Otros dedos (índice, medio, anular, meñique)
        for id in range(1, 5):
            if landmarks[tip_ids[id]].y < landmarks[tip_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        
        return fingers
    
    def classify_hand_gesture(self, landmarks) -> str:
        """
        Clasifica el gesto de una mano.
        
        Args:
            landmarks: Landmarks de la mano
            
        Returns:
            str: Tipo de gesto detectado
        """
        fingers = self.count_fingers(landmarks)
        fingers_up = sum(fingers)
        
        if fingers_up == 0:
            return "closed"
        elif fingers_up == 1 and fingers[1] == 1:  # Solo índice
            return "one_finger"
        elif fingers_up == 2 and fingers[1] == 1 and fingers[2] == 1:  # Índice y medio (V)
            return "two_fingers"
        elif fingers_up >= 4:
            return "open"
        else:
            return "partial"
    
    def detect_combined_gesture(self, left_gesture: str, right_gesture: str) -> Optional[str]:
        """
        Detecta gestos combinados usando ambas manos.
        
        Args:
            left_gesture (str): Gesto de la mano izquierda
            right_gesture (str): Gesto de la mano derecha
            
        Returns:
            Optional[str]: Patrón de gesto detectado o None
        """
        if self.current_mode == GestureMode.BRIGHTNESS_CONTROL:
            # Gestos para control de brillo
            if left_gesture == "one_finger" and right_gesture == "open":
                return GesturePatterns.BRIGHTNESS_UP.value
            elif left_gesture == "one_finger" and right_gesture == "closed":
                return GesturePatterns.BRIGHTNESS_DOWN.value
                
        elif self.current_mode == GestureMode.VOLUME_CONTROL:
            # Gestos para control de volumen
            if right_gesture == "one_finger" and left_gesture == "open":
                return GesturePatterns.VOLUME_UP.value
            elif right_gesture == "one_finger" and left_gesture == "closed":
                return GesturePatterns.VOLUME_DOWN.value
        
        # Gestos globales
        if left_gesture == "closed" and right_gesture == "closed":
            return GesturePatterns.MUTE_TOGGLE.value
        elif left_gesture == "two_fingers" and right_gesture == "two_fingers":
            return GesturePatterns.MODE_SWITCH.value
        
        return None
    
    def execute_gesture_action(self, gesture_pattern: str):
        """
        Ejecuta la acción correspondiente al gesto detectado.
        
        Args:
            gesture_pattern (str): Patrón de gesto a ejecutar
        """
        try:
            if gesture_pattern == GesturePatterns.BRIGHTNESS_UP.value:
                self.current_brightness = min(100, self.current_brightness + 3)
                self.brightness_controller.setBrightness(self.current_brightness)
                
            elif gesture_pattern == GesturePatterns.BRIGHTNESS_DOWN.value:
                self.current_brightness = max(0, self.current_brightness - 3)
                self.brightness_controller.setBrightness(self.current_brightness)
                
            elif gesture_pattern == GesturePatterns.VOLUME_UP.value:
                self.current_volume = min(100, self.current_volume + 3)
                self.volume_controller.setVolume(self.current_volume)
                
            elif gesture_pattern == GesturePatterns.VOLUME_DOWN.value:
                self.current_volume = max(0, self.current_volume - 3)
                self.volume_controller.setVolume(self.current_volume)
                
            elif gesture_pattern == GesturePatterns.MUTE_TOGGLE.value:
                if self.volume_controller.isMuted():
                    self.volume_controller.unmute()
                else:
                    self.volume_controller.mute()
                    
            elif gesture_pattern == GesturePatterns.MODE_SWITCH.value:
                # Cambiar entre modos
                if self.current_mode == GestureMode.BRIGHTNESS_CONTROL:
                    self.current_mode = GestureMode.VOLUME_CONTROL
                    print("🔄 Modo cambiado a: CONTROL DE VOLUMEN")
                else:
                    self.current_mode = GestureMode.BRIGHTNESS_CONTROL
                    print("🔄 Modo cambiado a: CONTROL DE BRILLO")
                    
                # Cooldown más largo para cambio de modo
                self.last_gesture_time = time.time() + 1.0
                
        except Exception as e:
            print(f"❌ Error ejecutando acción: {e}")
    
    def is_gesture_stable(self, gesture: str) -> bool:
        """
        Verifica si un gesto es estable durante varios frames.
        
        Args:
            gesture (str): Gesto a verificar
            
        Returns:
            bool: True si el gesto es estable
        """
        if gesture == self.last_detected_gesture:
            self.current_gesture_count += 1
        else:
            self.current_gesture_count = 1
            self.last_detected_gesture = gesture
        
        return self.current_gesture_count >= self.gesture_stability_frames
    
    def draw_ui_overlay(self, frame) -> None:
        """
        Dibuja la interfaz de usuario en el frame.
        
        Args:
            frame: Frame de video donde dibujar
        """
        height, width = frame.shape[:2]
        
        # Fondo semi-transparente para el panel de información
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (400, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        # Información del modo actual
        mode_text = f"Modo: {self.current_mode.value.upper()}"
        cv2.putText(frame, mode_text, (20, 35), self.font, self.font_scale, (0, 255, 255), self.font_thickness)
        
        # Información de brillo
        brightness_text = f"Brillo: {self.current_brightness}%"
        color = (0, 255, 0) if self.current_mode == GestureMode.BRIGHTNESS_CONTROL else (100, 100, 100)
        cv2.putText(frame, brightness_text, (20, 65), self.font, self.font_scale, color, self.font_thickness)
        
        # Información de volumen
        volume_text = f"Volumen: {self.current_volume}%"
        muted_text = " (MUTED)" if self.volume_controller.isMuted() else ""
        volume_text += muted_text
        color = (0, 255, 0) if self.current_mode == GestureMode.VOLUME_CONTROL else (100, 100, 100)
        cv2.putText(frame, volume_text, (20, 95), self.font, self.font_scale, color, self.font_thickness)
        
        # Instrucciones
        instructions = [
            "Gestos:",
            "Brillo: Izq(1) + Der(abrir/cerrar)",
            "Volumen: Der(1) + Izq(abrir/cerrar)",
            "Cambio: Ambas(V)  |  Mute: Ambas(cerrar)"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = height - 100 + (i * 25)
            cv2.putText(frame, instruction, (20, y_pos), self.font, 0.5, (255, 255, 255), 1)
    
    def process_frame(self) -> Tuple[Optional[object], str]:
        """
        Procesa un frame de la cámara y detecta gestos.
        
        Returns:
            Tuple[Optional[object], str]: (frame procesado, mensaje de estado)
        """
        ret, frame = self.cap.read()
        if not ret:
            return None, "❌ Error: No se pudo capturar frame"
        
        # Voltear frame horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        
        # Convertir a RGB para MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        message = ""
        left_gesture = None
        right_gesture = None
        
        # Procesar manos detectadas
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                # Dibujar landmarks
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                    self.mp_draw.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2)
                )
                
                # Clasificar gesto
                gesture = self.classify_hand_gesture(hand_landmarks.landmark)
                label = hand_info.classification[0].label
                
                if label == "Left":
                    left_gesture = gesture
                elif label == "Right":
                    right_gesture = gesture
        
        # Detectar gestos combinados
        if left_gesture and right_gesture:
            combined_gesture = self.detect_combined_gesture(left_gesture, right_gesture)
            
            if combined_gesture and self.is_gesture_stable(combined_gesture):
                current_time = time.time()
                if current_time - self.last_gesture_time > self.gesture_cooldown:
                    self.execute_gesture_action(combined_gesture)
                    self.last_gesture_time = current_time
                    message = f"✅ Ejecutando: {combined_gesture}"
        
        # Actualizar valores actuales
        self.current_brightness = self.brightness_controller.getBrightness()
        self.current_volume = self.volume_controller.getVolume()
        
        # Dibujar interfaz
        self.draw_ui_overlay(frame)
        
        return frame, message
    
    def run(self):
        """
        Ejecuta el bucle principal de captura y procesamiento de gestos.
        """
        print("🚀 Iniciando detección de gestos...")
        print("📋 Controles:")
        print("   - Presiona 'q' para salir")
        print("   - Presiona 'm' para cambiar modo manualmente")
        print("   - Presiona 'r' para resetear valores")
        
        try:
            while True:
                frame, message = self.process_frame()
                
                if frame is not None:
                    # Mostrar mensaje de estado
                    if message:
                        cv2.putText(frame, message, (10, frame.shape[0] - 20), 
                                  self.font, 0.6, (0, 255, 0), 2)
                    
                    cv2.imshow('GestIX - Control por Gestos', frame)
                
                # Manejar teclas
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("👋 Cerrando aplicación...")
                    break
                elif key == ord('m'):
                    # Cambio manual de modo
                    if self.current_mode == GestureMode.BRIGHTNESS_CONTROL:
                        self.current_mode = GestureMode.VOLUME_CONTROL
                        print("🔄 Modo cambiado manualmente a: CONTROL DE VOLUMEN")
                    else:
                        self.current_mode = GestureMode.BRIGHTNESS_CONTROL
                        print("🔄 Modo cambiado manualmente a: CONTROL DE BRILLO")
                elif key == ord('r'):
                    # Reset de valores
                    self.brightness_controller.setBrightness(50)
                    self.volume_controller.setVolume(50)
                    print("🔄 Valores reseteados: Brillo=50%, Volumen=50%")
                
        except KeyboardInterrupt:
            print("\n⏹️ Aplicación interrumpida por el usuario")
        except Exception as e:
            print(f"❌ Error durante la ejecución: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """
        Limpia los recursos utilizados.
        """
        print("🧹 Liberando recursos...")
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        print("✅ Recursos liberados correctamente")


# Función principal para pruebas
if __name__ == "__main__":
    """
    Ejecución principal del módulo de control gestual.
    """
    try:
        # Crear y ejecutar el controlador
        controller = CameraVolumeController()
        controller.run()
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        print("💡 Asegúrate de tener:")
        print("   - Una cámara conectada y funcional")
        print("   - Las dependencias instaladas (pip install -r requirements.txt)")
        print("   - Permisos para controlar el volumen del sistema")