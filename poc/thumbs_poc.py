#!/usr/bin/env python3
# PoC: detección de gesto "Thumbs Up / Down"
import cv2
import mediapipe as mp
import numpy as np
import yaml

# === Configuración ===
cfg_path = "poc/config.yaml"
try:
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
except Exception as e:
    print(f"Error leyendo {cfg_path}: {e}")
    exit(1)

CAM_INDEX = cfg.get("camera", {}).get("index", 0)
MIRROR = cfg.get("camera", {}).get("mirror", True)
DRAW = cfg.get("gesture", {}).get("draw_landmarks", True)
ANGLE_THRESHOLD = cfg.get("gesture", {}).get("thumb_angle_threshold", 20)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    print("❌ No se pudo abrir la cámara")
    exit(1)

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

print("✅ Ejecutando PoC de gesto 'Thumbs Up / Down'")
print("Presiona 'q' o 'ESC' para salir")

def get_thumb_angle(landmarks):
    """Calcula el ángulo del pulgar respecto al eje Y."""
    thumb_tip = np.array([landmarks[4].x, landmarks[4].y])
    thumb_base = np.array([landmarks[2].x, landmarks[2].y])
    vec = thumb_tip - thumb_base
    angle = np.degrees(np.arctan2(-vec[1], vec[0]))
    return angle

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if MIRROR:
        frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    texto = "No thumb gesture"
    color = (0, 0, 255)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0].landmark
        angle = get_thumb_angle(lm)

        # Determinar orientación del pulgar
        if angle > (90 - ANGLE_THRESHOLD) and angle < (90 + ANGLE_THRESHOLD):
            texto = "Thumb → (Horizontal)"
            color = (255, 255, 0)
        elif angle < -45:
            texto = "THUMBS DOWN"
            color = (0, 0, 255)
        elif angle > 45:
            texto = "THUMBS UP"
            color = (0, 255, 0)

        if DRAW:
            mp_drawing.draw_landmarks(
                frame,
                res.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

        # Dibuja vector del pulgar
        thumb_tip = (int(lm[4].x * w), int(lm[4].y * h))
        thumb_base = (int(lm[2].x * w), int(lm[2].y * h))
        cv2.line(frame, thumb_base, thumb_tip, color, 3)

    cv2.putText(frame, texto, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.imshow("Thumbs PoC", frame)

    key = cv2.waitKeyEx(10)
    if key == ord('q') or key == 27 or cv2.getWindowProperty("Thumbs PoC", cv2.WND_PROP_VISIBLE) < 1:
        print("Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()
