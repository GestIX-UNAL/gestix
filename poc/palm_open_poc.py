#!/usr/bin/env python3
import cv2
import mediapipe as mp
import yaml

# Cargar configuración desde YAML
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

# Umbral: cuántos dedos arriba para considerar palma abierta
MIN_FINGERS_OPEN = cfg.get("gesture", {}).get("palm_min_fingers", 4)

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

print("✅ Ejecutando PoC de gesto 'Palm Open'")
print("Presiona 'q' para salir")

def count_fingers_open(landmarks):
    """
    Cuenta dedos extendidos: índice, medio, anular, meñique.
    Retorna número de dedos “abiertos”.
    """
    count = 0
    # Para cada dedo excepto el pulgar:
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    for tip_id, pip_id in zip(tips, pips):
        if landmarks[tip_id].y < landmarks[pip_id].y:
            count += 1
    return count

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if MIRROR:
        frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    texto = "No palm open"
    color = (0, 0, 255)

    if res.multi_hand_landmarks:
        lm = res.multi_hand_landmarks[0].landmark
        fingers_open = count_fingers_open(lm)
        if fingers_open >= MIN_FINGERS_OPEN:
            texto = f"PALM OPEN ({fingers_open})"
            color = (0, 255, 0)

        if DRAW:
            mp_drawing.draw_landmarks(
                frame,
                res.multi_hand_landmarks[0],
                mp_hands.HAND_CONNECTIONS,
                mp_styles.get_default_hand_landmarks_style(),
                mp_styles.get_default_hand_connections_style()
            )

    cv2.putText(frame, texto, (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.imshow("Palm Open PoC", frame)

    key = cv2.waitKeyEx(10)
    if key == ord('q') or key == 27 or cv2.getWindowProperty("Palm Open PoC", cv2.WND_PROP_VISIBLE) < 1:
        print("Saliendo...")
        break

cap.release()
cv2.destroyAllWindows()
