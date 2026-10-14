import os, urllib.request
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
import cv2, numpy as np

WHEEL_PT = "wheel.pt"

# Download wheel detection model from github if not found in the directory already.
if not os.path.exists(WHEEL_PT):
    print("[INFO] Downloading andBabaev wheel-detector yolov11n.pt...")
    url = "https://github.com/andBabaev/wheel-detector/releases/download/v1.0/yolov11n.pt"
    urllib.request.urlretrieve(url, WHEEL_PT)
    print(f"[INFO] Saved to {WHEEL_PT}")

print("[INFO] Loading...")
wheel_detector = YOLO(WHEEL_PT)
chain_model = load_model("snow_chain_detector.keras")

cap = cv2.VideoCapture("test_video_2.mp4")

while True:
    ret, frame = cap.read()
    if not ret: break

    # DIRECT WHEEL DETECTION
    results = wheel_detector(frame, conf=0.4, verbose=False)[0]

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        crop = frame[y1:y2, x1:x2]
        if crop.size == 0: continue

        img = cv2.resize(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), (224,224))
        img = np.expand_dims(preprocess_input(img_to_array(img)), 0)
        with_chain, without = chain_model.predict(img, verbose=0)[0]

        has = with_chain > without
        label = f"{'With Chain : Allowed' if has else 'No Chain : Not allowed'} {max(with_chain,without)*100:.0f}%"
        color = (0,255,0) if has else (0,0,255)

        cv2.rectangle(frame, (x1,y1), (x2,y2), color, 2)
        cv2.putText(frame, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    cv2.imshow("Snow Chain Detector - Press Q to stop", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()