import cv2
import mediapipe as mp

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
        self.brightness = 50
        
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
        
    def is_hand_open(self, landmarks):
        fingers = self.count_fingers(landmarks)
        return sum(fingers) >= 4
        
    def detect_gestures(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, "No frame captured"
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        message = ""
        left_hand_detected = False
        right_hand_detected = False
        left_one_finger = False
        right_hand_open = False
        
        if results.multi_hand_landmarks:
            for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = hand_info.classification[0].label
                
                if label == "Left":  # Left hand in mirrored view
                    left_hand_detected = True
                    fingers = self.count_fingers(hand_landmarks.landmark)
                    if sum(fingers) == 1:
                        left_one_finger = True
                        message = "brillo"
                    
                elif label == "Right":  # Right hand in mirrored view
                    right_hand_detected = True
                    if self.is_hand_open(hand_landmarks.landmark):
                        right_hand_open = True
                
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        
        # Adjust brightness based on gestures
        if left_one_finger and right_hand_open:
            self.brightness = min(100, self.brightness + 2)
        elif left_one_finger and not right_hand_open and right_hand_detected:
            self.brightness = max(0, self.brightness - 2)
        
        # Display brightness value
        cv2.putText(frame, f"Brightness: {self.brightness}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        if message:
            cv2.putText(frame, message, (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame, message
        
    def run(self):
        while True:
            frame, message = self.detect_gestures()
            if frame is not None:
                cv2.imshow('Hand Gesture Detection', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        self.cap.release()
        cv2.destroyAllWindows()
        
if __name__ == "__main__":
    camera = Camera()
    camera.run()