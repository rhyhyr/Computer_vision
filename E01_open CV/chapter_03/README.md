**문제**

<img width="579" height="395" alt="Image" src="https://github.com/user-attachments/assets/be8df22d-7531-4ce2-99f6-43a57952b750" />

**핵심 개념**
1. Numpy 슬라이싱 (roi = img[y1:y2, x1:x2])
OpenCV 이미지는 사실상 Numpy 배열입니다. 따라서 특정 영역을 잘라낼 때는 이미지[행(y)범위, 열(x)범위] 형식을 사용합니다.
2. 잔상 제거 (img_draw = img.copy())
드래그 중에 cv.rectangle을 그냥 실행하면, 마우스가 움직이는 경로마다 사각형이 겹쳐서 그려지게 됩니다. 이를 방지하기 위해 매 프레임마다 깨끗한 원본 복사본 위에 사각형을 그려서 보여주는 테크닉이 필요합니다.
3. 좌표 정렬 (min, max)
사용자가 왼쪽 위에서 오른쪽 아래로만 드래그한다는 보장이 없습니다. 반대 방향으로 드래그해도 정상적으로 슬라이싱이 되도록 min()과 max()를 사용해 항상 작은 값이 시작점이 되도록 보정했습니다.

**전체 코드**

<img width="740" height="1174" alt="Image" src="https://github.com/user-attachments/assets/f947f7b7-93c2-478f-8bcf-dee4d479301e" />

**실행 결과**

<img width="1445" height="979" alt="Image" src="https://github.com/user-attachments/assets/80333237-009e-448d-8898-4a2a4387b14d" />
