import cv2
import matplotlib.pyplot as plt

# 1. 이미지 불러오기
# 'mot_color70.jpg' 또는 실제 파일 경로로 수정하세요.
img = cv2.imread('mot_color70.jpg')

if img is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    # 연산 속도와 정확도를 위해 그레이스케일 변환
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2. SIFT 객체 생성
    # 힌트: nfeatures 값을 조절하여 검출할 특징점 개수를 제한할 수 있습니다.
    sift = cv2.SIFT_create(nfeatures=500)

    # 3. 특징점 검출 및 기술자 계산
    # kp: 특징점 위치 정보, des: 특징점을 설명하는 수학적 데이터(기술자)
    kp, des = sift.detectAndCompute(gray, None)

    # 4. 특징점을 이미지에 시각화
    # 힌트: DRAW_RICH_KEYPOINTS 플래그를 사용하여 특징점의 크기와 방향까지 표시
    img_with_kp = cv2.drawKeypoints(img, kp, None, 
                                    flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # 5. Matplotlib을 사용하여 원본과 결과 시각화
    plt.figure(figsize=(15, 7))

    # 왼쪽: 원본 이미지
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    # 오른쪽: 특징점이 표시된 이미지
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(img_with_kp, cv2.COLOR_BGR2RGB))
    plt.title('SIFT Keypoints (Rich)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    print(f"검출된 특징점 개수: {len(kp)}")