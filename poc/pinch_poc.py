#!/usr/bin/env python3
# PoC: detección visual del gesto "pinch" (pulgar + índice)
import cv2
import mediapipe as mp
import numpy as np
import yaml

with open("poc/config.yaml") as f:
    cfg = yaml.safe_load(f)

CAM_INDEX = cfg["camera"]["index"]
MIRROR = cfg["camera"]["mirror"]
UMBRAL = cfg["gesture"]["pinch_threshold"]
DRAW = cfg["gesture"]["draw_landmarks"]

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

print("✅ Ejecutando PoC de gesto 'pinch' (pulgar+índice)")
print("Presiona 'q' para salir")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    texto = "No pinch"
    color = (0, 0, 255)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0].landmark
        thumb_tip = np.array([lm[4].x * w, lm[4].y * h])
        index_tip = np.array([lm[8].x * w, lm[8].y * h])
        dist = np.linalg.norm(thumb_tip - index_tip)
        norm = dist / np.sqrt(w*w + h*h)

        if norm < UMBRAL:
            texto = f"PINCH! ({norm:.3f})"
            color = (0, 255, 0)

        if DRAW:
            mp_drawing.draw_landmarks(
                frame,
                res.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

        # dibuja línea entre pulgar e índice
        cv2.line(frame,
                 tuple(thumb_tip.astype(int)),
                 tuple(index_tip.astype(int)),
                 color, 2)

    cv2.putText(frame, texto, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    cv2.imshow("Pinch PoC", frame)

    key = cv2.waitKeyEx(10)
    if key == ord('q') or key == 27:  # 'q' o ESC
        print("Saliendo...")
        break

# salir limpio
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(100)  # fuerza cierre en algunos sistemas
