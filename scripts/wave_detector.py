import cv2
import mediapipe as mp
import numpy as np

# Initialize Mediapipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Function to detect waving motion
def is_waving(hand_landmarks, prev_positions):
    if len(prev_positions) < 2:
        return False

    curr_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
    prev_x = prev_positions[-1]

    motion = abs(curr_x - prev_x)
    return motion > 0.05  # Threshold for significant movement

# Open the webcam
cap = cv2.VideoCapture(0)

prev_positions = []  # Track wrist positions for motion detection

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame for a mirror effect
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame with Mediapipe
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detect waving gesture
            if is_waving(hand_landmarks, prev_positions):
                cv2.putText(frame, "Waving Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Update wrist position
            wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
            prev_positions.append(wrist_x)
            if len(prev_positions) > 10:
                prev_positions.pop(0)  # Keep only the last few positions

    # Display the frame
    cv2.imshow("Hand Gesture Recognition", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
