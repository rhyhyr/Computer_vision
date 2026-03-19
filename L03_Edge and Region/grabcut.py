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

