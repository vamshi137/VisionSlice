import cv2  # type: ignore

cap = cv2.VideoCapture(0)

cv2.namedWindow("VisionSlice - Camera Test", cv2.WINDOW_NORMAL)

while True:
    success, frame = cap.read()

    if not success:
        print("Camera not found")
        break

    frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("VisionSlice - Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()