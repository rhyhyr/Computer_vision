
## 01. 🧭 소벨 에지 검출 (Sobel Edge Detection)

> **이미지의 변화율(기울기)을 측정하여 경계선을 찾습니다.**

### 📝 문제 정의

이미지 내에서 밝기가 급격하게 변하는 부분(경계선)을
x축(세로선)과 y축(가로선) 방향으로 각각 계산하고, 이를 합쳐 전체적인 윤곽선을 추출합니다.

### 🔑 핵심 함수 (Key Functions)

* `cv2.Sobel()`
  → 이미지의 미분을 계산합니다. (`dx`, `dy` 설정을 통해 방향 결정)

* `cv2.magnitude()`
  → x, y축의 미분 값을 합쳐 전체 에지의 세기(강도)를 계산합니다.

* `cv2.convertScaleAbs()`
  → 계산된 실수 값을 8비트 이미지(0~255)로 변환합니다.

### 실습 코드

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 불러오기
# 파일 경로를 실제 이미지 파일명으로 수정하세요 (예: 'edge_test.jpg')
img = cv2.imread('edgeDetectionImage.jpg')

if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    # 2. 그레이스케일로 변환
    # 에지 검출은 밝기 변화만 관찰하므로 흑백 이미지에서 수행하는 것이 효율적입니다.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Sobel 필터를 사용하여 x축과 y축 방향의 에지 검출
    # cv.Sobel(이미지, 데이터타입, x차수, y차수, 커널크기)
    # cv.CV_64F는 정밀한 계산을 위해 64비트 실수형을 사용함을 의미합니다.
    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3) # 수직선 검출
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3) # 수평선 검출

    # 4. cv.magnitude()를 사용하여 에지 강도(기울기 크기) 계산
    # x방향과 y방향의 변화량을 합쳐 전체 에지 강도를 구합니다.
    magnitude = cv2.magnitude(sobel_x, sobel_y)

    # 5. 시각화를 위해 uint8 타입으로 변환
    # 계산된 실수값을 0~255 사이의 8비트 정수형으로 변환합니다.
    sobel_edge = cv2.convertScaleAbs(magnitude)

    # 6. Matplotlib을 사용하여 시각화
    plt.figure(figsize=(12, 6))

    # 원본 이미지 출력
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) # plt는 RGB 순서 사용
    plt.title('Original Image')
    plt.axis('off')

    # 에지 강도 이미지 출력
    plt.subplot(1, 2, 2)
    plt.imshow(sobel_edge, cmap='gray') # 요구사항에 따라 흑백으로 시각화
    plt.title('Sobel Edge Magnitude')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


```

### 실행 결과

<img width="1204" height="666" alt="image" src="https://github.com/user-attachments/assets/44ba1f26-8744-4096-8727-b3e9045a0bc0" />


---

## 02. ✨ 캐니 에지 & 허프 변환 (Canny Edge & Hough Transform)

> **가장 깔끔한 선을 찾고, 그 선이 직선인지 판별합니다.**

### 📝 문제 정의

소벨보다 더 정교하게 잡음을 제거하여 가느다란 에지를 찾고(**Canny**),
그 에지 점들이 모여 하나의 직선을 이루는지 수학적으로 분석(**Hough Transform**)하여
이미지 위에 선으로 표시합니다.

### 🔑 핵심 함수 (Key Functions)

* `cv2.Canny()`
  → 여러 단계의 필터를 거쳐 가장 선명하고 얇은 에지만 추출합니다.

* `cv2.HoughLinesP()`
  → 에지 점들을 연결해 직선의 시작점과 끝점 좌표를 계산합니다.

* `cv2.line()`
  → 검출된 좌표를 따라 이미지 위에 선을 그립니다.

### 실습 코드

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 불러오기
# 'dabo.jpg' 또는 실제 파일 경로로 수정하세요.
img = cv2.imread('dabo.jpg')

if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    # 원본 복사 (직선을 그릴 이미지)
    line_img = img.copy()
    
    # 2. 그레이스케일 변환 (에지 검출 전처리)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. 캐니 에지 검출 (Canny Edge Detection)
    # 요구사항: threshold1=100, threshold2=200
    edges = cv2.Canny(gray, 100, 200)

    # 4. 허프 변환을 사용하여 직선 검출 (Probabilistic Hough Transform)
    # cv.HoughLinesP(이미지, rho, theta, threshold, minLineLength, maxLineGap)
    # rho: 거리 해상도 (1 pixel), theta: 각도 해상도 (1 degree)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                            minLineLength=50, maxLineGap=10)

    # 5. 검출된 직선을 원본 이미지에 빨간색으로 그리기
    # 요구사항: 색상 (0, 0, 255), 두께 2
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # 6. Matplotlib을 사용하여 시각화
    plt.figure(figsize=(12, 6))

    # 왼쪽: 원본 이미지
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    # 오른쪽: 직선이 그려진 이미지
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(line_img, cv2.COLOR_BGR2RGB))
    plt.title('Detected Lines (Hough Transform)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


```

### 실행 결과

<img width="1199" height="663" alt="image" src="https://github.com/user-attachments/assets/65fff96f-3373-4a2e-8ed0-e32407a2baa8" />

---

## 03. 🎯 그랩컷 객체 추출 (GrabCut Segmentation)

> **사각형만 그려주면 배경을 제거하는 '누끼 따기' 기술입니다.**

### 📝 문제 정의

사용자가 객체 주위에 사각형(ROI)을 지정하면,
알고리즘이 사각형 내부는 **객체**, 외부는 **배경**으로 학습하여
복잡한 환경에서도 원하는 물체만 추출합니다.

### 🔑 핵심 함수 (Key Functions)

* `cv2.grabCut()`
  → 반복적인 연산을 통해 배경과 전경(객체)을 분리합니다.

* `np.where()`
  → 마스크 값을 기준으로 배경(0)은 제거하고 객체(1)만 남깁니다.

* `cv2.GC_INIT_WITH_RECT`
  → 사용자가 지정한 사각형을 기반으로 초기 학습을 수행하도록 설정합니다.

### 실습 코드

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 이미지 불러오기
# 'coffee_cup.jpg' 또는 실제 파일 경로로 수정하세요.
img = cv2.imread('coffee cup.jpg')

if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    # 연산을 위한 마스크 생성 (이미지와 동일한 크기)
    mask = np.zeros(img.shape[:2], np.uint8)

    # 알고리즘 내부에서 사용할 임시 배경/전경 모델 초기화
    # 요구사항: np.zeros((1, 65), np.float64)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # 2. 초기 사각형 영역 설정 (x, y, width, height)
    # 이미지 크기에 맞춰 적절히 수정하세요. (예: 컵이 있는 위치)
    rect = (50, 50, img.shape[1]-100, img.shape[0]-100)

    # 3. cv.grabCut()을 사용하여 대화식 분할 수행
    # 5회 반복 연산을 수행하며 사각형 모드(GC_INIT_WITH_RECT)로 시작합니다.
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # 4. 마스크 처리
    # 마스크 값 중 0(배경), 2(확실한 배경)는 0으로, 
    # 1(전경), 3(확실한 전경)은 1로 변환합니다.
    # np.where를 사용하여 0 또는 2인 경우 0, 나머지는 1로 바꿉니다.
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # 5. 배경 제거 (원본 이미지에 마스크 곱하기)
    # 마스크가 1인 영역(전경)만 남기고 0인 영역(배경)은 검은색으로 바뀝니다.
    img_result = img * mask2[:, :, np.newaxis]

    # 6. Matplotlib을 사용하여 원본, 마스크, 결과 이미지 시각화
    plt.figure(figsize=(15, 5))

    # 왼쪽: 원본 이미지
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    # 가운데: 마스크 이미지 (추출된 영역을 흑백으로 표시)
    plt.subplot(1, 3, 2)
    plt.imshow(mask2, cmap='gray')
    plt.title('Mask Image')
    plt.axis('off')

    # 오른쪽: 배경이 제거된 결과 이미지
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(img_result, cv2.COLOR_BGR2RGB))
    plt.title('GrabCut Result')
    plt.axis('off')

    plt.tight_layout()
    plt.show()


```

### 실행 결과

<img width="1498" height="560" alt="image" src="https://github.com/user-attachments/assets/e8edbf54-b024-4627-9074-1e23035f1abd" />


---
