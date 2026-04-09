Python
import cv2
import numpy as np
# SORT 라이브러리가 설치되어 있어야 합니다 (sort.py)
from sort import * # 1. 객체 검출을 위한 YOLO 모델 로드 (OpenCV DNN 사용)
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# 2. SORT 추적기 초기화
# max_age: 물체가 사라진 후 몇 프레임까지 기억할 것인가
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

# 비디오 파일 또는 카메라 읽기
cap = cv2.VideoCapture("video.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 3. YOLO 객체 검출 수행
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    detections = [] # 이번 프레임에서 찾은 박스들 저장용
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5: # 신뢰도가 50% 이상인 것만 사용
                # 박스 좌표 계산 (중심점 -> 왼쪽 위 x, y)
                center_x, center_y = int(detection[0] * frame.shape[1]), int(detection[1] * frame.shape[0])
                w, h = int(detection[2] * frame.shape[1]), int(detection[3] * frame.shape[0])
                x, y = int(center_x - w / 2), int(center_y - h / 2)
                # [x1, y1, x2, y2, score] 형식으로 저장
                detections.append([x, y, x + w, y + h, confidence])

    # 4. SORT 추적기에 검출 결과 전달
    # 추적기는 기존 객체와 대조하여 고유 ID가 포함된 정보를 반환합니다.
    track_bbs_ids = tracker.update(np.array(detections))

    # 5. 결과 시각화
    for track in track_bbs_ids:
        x1, y1, x2, y2, obj_id = map(int, track) # 정수로 변환
        # 객체에 박스 그리기
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 고유 ID 표시 (예: "ID 1")
        cv2.putText(frame, f"ID {obj_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Multi-Object Tracking", frame)
    if cv2.waitKey(1) == 27: break # ESC 누르면 종료

cap.release()
cv2.destroyAllWindows()