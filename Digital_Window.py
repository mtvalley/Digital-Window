import cv2
import numpy as np
import time
import os
from TCPsocket import TCPServer

class FaceTrackerDNN:
    def __init__(self):
        proto_path = "deploy.prototxt.txt"
        model_path = "res10_300x300_ssd_iter_140000.caffemodel"
        if not os.path.exists(proto_path) or not os.path.exists(model_path):
            raise FileNotFoundError("DNN 모델 파일이 누락되었습니다. deploy.prototxt.txt 또는 res10_300x300_ssd_iter_140000.caffemodel")

        self.net = cv2.dnn.readNetFromCaffe(proto_path, model_path)
        self.prev_center = None
        self.lost_count = 0

    def get_face_center(self, frame):
        h, w = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104.0, 177.0, 123.0], False, False)
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x1, y1, x2, y2) = box.astype("int")
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                self.prev_center = center
                self.lost_count = 0
                return center

        self.lost_count += 1
        if self.lost_count > 30:
            self.prev_center = None
            self.lost_count = 0
        return self.prev_center


def main():
    capL = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    capR = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    capL.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capL.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    capR.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    capR.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    trackerL = FaceTrackerDNN()
    trackerR = FaceTrackerDNN()
    server = TCPServer()
    f = 700  # focal length (in pixels)
    B = 6    # baseline (in cm)

    frame_width = int(capL.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capL.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cx = frame_width // 2
    cy = frame_height // 2
    prev_x = prev_y = prev_z = None

    while True:
        retL, frameL = capL.read()
        retR, frameR = capR.read()

        if not retL or not retR or frameL is None or frameR is None:
            print("❌ 카메라 연결 또는 프레임 실패")
            continue

        centerL = trackerL.get_face_center(frameL)
        centerR = trackerR.get_face_center(frameR)

        x = y = z = None

        if centerL and centerR:
            disparity = abs(centerL[0] - centerR[0])
            z = (f * B) / disparity if disparity > 0 else 0  # Z in cm

            raw_x = (centerL[0] + centerR[0]) // 2
            raw_y = (centerL[1] + centerR[1]) // 2

            # 정규화된 중심 좌표 (중앙 기준 0,0) → cm 환산용 스케일 (예: 0.1cm/pixel)
            pixel_to_cm = 0.1
            x = (raw_x - cx) * pixel_to_cm
            y = (raw_y - cy) * pixel_to_cm

            cv2.circle(frameL, centerL, 5, (0, 255, 0), -1)
            cv2.circle(frameR, centerR, 5, (0, 255, 0), -1)

            if prev_x is not None:
                dx = round(x - prev_x, 3)
                dy = round(y - prev_y, 3)
                dz = round(z - prev_z, 3)
                server.send_xyz(dx, dy, dz)
            prev_x, prev_y, prev_z = x, y, z



        combined = cv2.hconcat([frameL, frameR])

        if x is not None and y is not None and z is not None:
            cv2.putText(combined, f"X: {x:.2f}cm Y: {y:.2f}cm Z: {z:.2f}cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.imshow("Stereo Face Tracking (OpenCV DNN)", combined)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    capL.release()
    capR.release()
    cv2.destroyAllWindows()
    time.sleep(0.01)


if __name__ == "__main__":
    main()
