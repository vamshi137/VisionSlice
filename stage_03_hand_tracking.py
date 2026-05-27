import cv2  # type: ignore
import mediapipe as mp  # type: ignore
from mediapipe.tasks import python  # type: ignore
from mediapipe.tasks.python import vision  # type: ignore
import urllib.request
import os

# Download hand tracking model if not exists
model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading hand tracking model... please wait")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Model downloaded successfully")

# Setup hand tracking
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# Drawing connections
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (0,9),(9,10),(10,11),(11,12),
    (0,13),(13,14),(14,15),(15,16),
    (0,17),(17,18),(18,19),(19,20),
    (5,9),(9,13),(13,17)
]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened")
else:
    print("Camera opened successfully")

cv2.namedWindow("VisionSlice - Hand Tracking", cv2.WINDOW_NORMAL)

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.resize(frame, (1280, 720))

    # Convert frame for mediapipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect hands
    results = detector.detect(mp_image)

    # Draw landmarks if hand detected
    if results.hand_landmarks:
        for hand in results.hand_landmarks:
            # Draw dots on each landmark
            for landmark in hand:
                x = int(landmark.x * 1280)
                y = int(landmark.y * 720)
                cv2.circle(frame, (x, y), 6, (0, 255, 0), -1)

            # Draw connections between landmarks
            for connection in HAND_CONNECTIONS:
                x1 = int(hand[connection[0]].x * 1280)
                y1 = int(hand[connection[0]].y * 720)
                x2 = int(hand[connection[1]].x * 1280)
                y2 = int(hand[connection[1]].y * 720)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 200, 255), 2)

    cv2.imshow("VisionSlice - Hand Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()