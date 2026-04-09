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