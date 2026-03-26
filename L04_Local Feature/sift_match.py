import cv2
import matplotlib.pyplot as plt

# 1. 두 개의 이미지 불러오기
img1 = cv2.imread('mot_color70.jpg') # 쿼리 이미지 (기준)
img2 = cv2.imread('mot_color83.jpg') # 트레인 이미지 (비교 대상)

if img1 is None or img2 is None:
    print("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
else:
    # 연산 효율을 위한 그레이스케일 변환
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 2. SIFT 객체 생성 및 특징점 추출
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # 3. 매칭 수행 (BFMatcher 사용)
    # NORM_L2: SIFT 기술자 거리 계산 방식
    # crossCheck=True: 서로가 서로에게 최적인 매칭만 남김 (정확도 향상)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    matches = bf.match(des1, des2)

    # 매칭 결과를 거리(유사도) 순으로 정렬
    matches = sorted(matches, key=lambda x: x.distance)

    # 4. 매칭 결과 시각화
    # 상위 50개의 좋은 매칭 결과만 표시 (너무 많으면 선이 복잡해짐)
    res = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, 
                          flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    # 5. Matplotlib을 사용하여 매칭 결과 출력
    plt.figure(figsize=(20, 10))
    plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
    plt.title('SIFT Feature Matching (Top 50)')
    plt.axis('off')
    plt.show()