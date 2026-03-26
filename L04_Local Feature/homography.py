import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 두 개의 이미지 불러오기 (샘플 파일 선택)
img1 = cv2.imread('img1.jpg') # 변환될 이미지
img2 = cv2.imread('img2.jpg') # 기준 이미지

if img1 is None or img2 is None:
    print("이미지를 불러올 수 없습니다.")
else:
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 2. SIFT 특징점 검출
    sift = cv2.SIFT_create()
    kp1, des1 = sift.detectAndCompute(gray1, None)
    kp2, des2 = sift.detectAndCompute(gray2, None)

    # 3. 매칭 및 좋은 매칭점 선별 (Lowe's Ratio Test)
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance: # 힌트: 거리 비율 0.7 미만 선별
            good_matches.append(m)

    # 4. 호모그래피 행렬 계산
    if len(good_matches) > 4:
        # 대응점 좌표 추출
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 힌트: RANSAC을 사용하여 이상점 제거 후 행렬 계산
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        # 5. 이미지 변환 및 정합 (Warping)
        h1, w1 = img1.shape[:2]
        h2, w2 = img2.shape[:2]
        
        # 힌트: 출력 크기를 두 이미지를 합친 파노라마 크기로 설정
        res_w = w1 + w2
        res_h = max(h1, h2)
        
        # img1을 img2 기준평면으로 변환
        warped_img = cv2.warpPerspective(img1, H, (res_w, res_h))
        
        # 매칭 결과 시각화 이미지 생성
        match_img = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=2)

        # 6. 결과 출력
        plt.figure(figsize=(20, 10))
        
        plt.subplot(2, 1, 1)
        plt.imshow(cv2.cvtColor(match_img, cv2.COLOR_BGR2RGB))
        plt.title('Matching Result')
        plt.axis('off')

        plt.subplot(2, 1, 2)
        plt.imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB))
        plt.title('Warped Image (Alignment)')
        plt.axis('off')

        plt.tight_layout()
        plt.show()
    else:
        print("충분한 매칭점을 찾지 못했습니다.")