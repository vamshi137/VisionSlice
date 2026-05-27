import cv2  # type: ignore
import mediapipe as mp  # type: ignore
from mediapipe.tasks import python  # type: ignore
from mediapipe.tasks.python import vision  # type: ignore
import os
import urllib.request

# Download model if not exists
model_path = "hand_landmarker.task"
if not os.path.exists(model_path):
    print("Downloading hand tracking model... please wait")
    url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Model downloaded successfully")

# Setup AI detector
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7
)
detector = vision.HandLandmarker.create_from_options(options)

# Trail storage
trail_points = []
MAX_TRAIL_LENGTH = 20

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened")
else:
    print("Camera opened successfully")

cv2.namedWindow("VisionSlice - Finger Motion", cv2.WINDOW_NORMAL)

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.resize(frame, (1280, 720))

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    results = detector.detect(mp_image)

    if results.hand_landmarks:
        for hand in results.hand_landmarks:

            # Get index fingertip - point 8
            index_tip = hand[8]
            tip_x = int(index_tip.x * 1280)
            tip_y = int(index_tip.y * 720)

            # Add to trail
            trail_points.append((tip_x, tip_y))

            # Keep trail at max length
            if len(trail_points) > MAX_TRAIL_LENGTH:
                trail_points.pop(0)

            # Draw trail
            for i in range(1, len(trail_points)):
                thickness = max(1, int((i / MAX_TRAIL_LENGTH) * 8))
                alpha = int((i / MAX_TRAIL_LENGTH) * 255)
                color = (0, alpha, 255)
                cv2.line(frame, trail_points[i - 1], trail_points[i], color, thickness)

            # Draw circle on fingertip
            cv2.circle(frame, (tip_x, tip_y), 10, (0, 255, 255), -1)

    else:
        trail_points.clear()

    cv2.imshow("VisionSlice - Finger Motion", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()