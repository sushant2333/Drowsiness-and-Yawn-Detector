import cv2
import mediapipe as mp
import numpy as np
import pygame

# ---------- Initialize pygame mixer ----------
pygame.mixer.init()
alert_sound = pygame.mixer.Sound("AlertSound.wav")

def play_alert():
    if not pygame.mixer.get_busy():   # play only if not already playing
        alert_sound.play()

# ---------- Helper Functions ----------
def eye_aspect_ratio(landmarks, eye_points):
    A = np.linalg.norm(np.array(landmarks[eye_points[1]]) - np.array(landmarks[eye_points[5]]))
    B = np.linalg.norm(np.array(landmarks[eye_points[2]]) - np.array(landmarks[eye_points[4]]))
    C = np.linalg.norm(np.array(landmarks[eye_points[0]]) - np.array(landmarks[eye_points[3]]))
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(landmarks, mouth_points):
    A = np.linalg.norm(np.array(landmarks[mouth_points[0]]) - np.array(landmarks[mouth_points[1]]))  # vertical
    B = np.linalg.norm(np.array(landmarks[mouth_points[2]]) - np.array(landmarks[mouth_points[3]]))  # horizontal
    return A / B

# ---------- Parameters ----------
EAR_THRESHOLD = 0.22
MAR_THRESHOLD = 0.65
CONSEC_FRAMES = 30
RESET_FRAMES = 25
BLINK_FRAMES = 3
YAWN_FRAMES = 15   # number of frames mouth must stay open

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

# ---------- Variables ----------
counter = 0
reset_counter = 0
status = "Normal"
blink_counter = 0
yawn_counter = 0
eye_closed_frames = 0
mouth_open_frames = 0
yawning = False   # track if currently yawning

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in face_landmarks.landmark]

            # Eye & Mouth indices
            left_eye = [33, 160, 158, 133, 153, 144]
            right_eye = [362, 385, 387, 263, 373, 380]
            mouth = [13, 14, 78, 308]

            # EAR & MAR
            leftEAR = eye_aspect_ratio(landmarks, left_eye)
            rightEAR = eye_aspect_ratio(landmarks, right_eye)
            ear = (leftEAR + rightEAR) / 2.0
            mar = mouth_aspect_ratio(landmarks, mouth)

            # ----- Blink detection -----
            if ear < EAR_THRESHOLD:
                eye_closed_frames += 1
            else:
                if eye_closed_frames >= BLINK_FRAMES:
                    blink_counter += 1
                eye_closed_frames = 0

            # ----- Yawn detection -----
            if mar > MAR_THRESHOLD:
                mouth_open_frames += 1
                if mouth_open_frames >= YAWN_FRAMES and not yawning:
                    yawn_counter += 1
                    yawning = True
                    status = "Yawning"
                    play_alert()
            else:
                mouth_open_frames = 0
                yawning = False

            # ----- Drowsiness Logic -----
            if ear < EAR_THRESHOLD:
                counter += 1
                reset_counter = 0
                if counter >= CONSEC_FRAMES:
                    if status != "Drowsy":
                        play_alert()
                    status = "Drowsy"
            elif not yawning:  # only reset if not yawning
                counter = 0
                reset_counter += 1
                if reset_counter >= RESET_FRAMES:
                    status = "Normal"

            # ----- Draw bounding box -----
            x_coords = [lm[0] for lm in landmarks]
            y_coords = [lm[1] for lm in landmarks]
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            if status == "Normal":
                color = (0, 255, 0)
            elif status == "Drowsy":
                color = (0, 0, 255)
            else:  # Yawning
                color = (0, 255, 255)

            cv2.rectangle(frame, (x_min - 20, y_min - 20), (x_max + 20, y_max + 20), color, 3)

            # ----- Show Text -----
            cv2.putText(frame, f"Status: {status}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"EAR: {ear:.2f}", (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"MAR: {mar:.2f}", (30, 140),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(frame, f"Blinks: {blink_counter}", (30, 180),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)
            cv2.putText(frame, f"Yawns: {yawn_counter}", (30, 220),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 200, 255), 2)

    cv2.imshow("Drowsiness & Yawning Detector", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()