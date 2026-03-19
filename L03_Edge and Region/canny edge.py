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

