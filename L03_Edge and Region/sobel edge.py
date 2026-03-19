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

