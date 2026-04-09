01. 🏃 SORT 알고리즘을 활용한 다중 객체 추적 (Multi-Object Tracking)
"검출된 객체에 ID를 부여하고, 다음 프레임에서도 같은 물체인지 찾아냅니다."

📝 문제 정의
단순히 "사람이 있다"를 넘어, "1번 사람", "2번 사람"을 구분하여 비디오 내내 추적합니다. 객체 검출기(YOLO)가 찾은 정보를 바탕으로 칼만 필터(예측)와 헝가리안 알고리즘(매칭)을 사용하여 추적기를 구현합니다.

🔑 핵심 개념
Kalman Filter: 물체의 이전 속도와 방향을 보고 "다음엔 여기쯤 있겠군" 하고 예측하는 수학 모델입니다.

Hungarian Algorithm: 새로 검출된 박스와 기존에 추적하던 박스 중 어떤 것끼리 같은 물체인지 가장 최적의 짝을 지어줍니다.

IoU (Intersection over Union): 두 박스가 얼마나 겹치는지를 계산하여 매칭의 근거로 사용합니다.

💻 실습 코드
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

<img width="648" height="399" alt="image" src="https://github.com/user-attachments/assets/e58ac945-7d54-48dc-86f3-bad593248ba1" />


02. 👺 Mediapipe를 활용한 얼굴 랜드마크 추출 (Face Mesh)
"얼굴에 468개의 점을 찍어 미세한 움직임과 표정을 포착합니다."

📝 문제 정의
웹캠 영상을 통해 얼굴을 실시간으로 감지하고, 눈, 코, 입, 얼굴 윤곽 등 총 468개의 정밀한 랜드마크 좌표를 추출하여 시각화합니다.

🔑 핵심 개념
Face Mesh: 딥러닝을 통해 얼굴의 3D 기하학적 구조를 추정하는 모델입니다.

정규화된 좌표 (Normalized Coordinates): 모델은 0~1 사이의 값으로 좌표를 주므로, 실제 이미지 크기(가로, 세로)를 곱해야 정확한 픽셀 위치가 나옵니다.

💻 실습 코드
Python
import cv2
import mediapipe as mp

# 1. Mediapipe의 FaceMesh 모듈 초기화
mp_face_mesh = mp.solutions.face_mesh
# static_image_mode: False(비디오용), max_num_faces: 최대 얼굴 개수
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)

# 2. 웹캠 캡처 시작
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # Mediapipe는 RGB 이미지를 사용하므로 변환이 필요합니다 (OpenCV는 BGR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 3. 얼굴 랜드마크 검출 수행
    results = face_mesh.process(rgb_frame)

    # 검출된 얼굴이 있다면
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # 4. 468개의 점을 하나씩 돌며 시각화
            for lm in face_landmarks.landmark:
                # lm.x, lm.y는 0~1 사이 값이므로 이미지 가로/세로를 곱해 픽셀 좌표로 변환
                ih, iw, ic = frame.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                
                # OpenCV의 circle 함수로 점 그리기 (반지름 1, 파란색)
                cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)

    # 5. 결과 화면 출력
    cv2.imshow("Face Mesh Landmark", frame)

    # ESC 키(27)를 누르면 프로그램 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
