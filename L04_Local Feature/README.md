
## 01. 🔍 SIFT 특징점 검출 (Feature Extraction)
> **"이미지가 회전하거나 크기가 변해도 변하지 않는 핵심 지점을 찾습니다."**

### 📝 문제 정의
사진을 멀리서 찍거나 옆에서 찍어도 동일하게 발견되는 고유의 점들을 찾고, 그 점의 크기와 방향을 시각화합니다.

### 🔑 핵심 개념
* **SIFT:** 크기(Scale)와 회전(Invariant)에 강한 특징 추출 알고리즘입니다.
* **Keypoints:** 이미지에서 특징이 뚜렷한 지점입니다. (코너, 무늬 등)

### 💻 실습 코드
```python
import cv2
import matplotlib.pyplot as plt

# 1. 사진 불러오기
img = cv2.imread('mot_color70.jpg')

# 흑백으로 변경 (특징점은 색상보다 밝기 변화에서 더 잘 찾아져요!)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. SIFT 연산기 만들기 (500개만 뽑아보자!)
sift = cv2.SIFT_create(nfeatures=500)

# 3. 특징점(kp) 찾기 & 그 지점의 특징(des) 계산하기
# kp: 점의 위치 / des: 그 점이 어떻게 생겼는지 설명하는 데이터
kp, des = sift.detectAndCompute(gray, None)

# 4. 사진 위에 특징점 그려보기
# DRAW_RICH_KEYPOINTS: 점의 크기(중요도)와 방향(회전된 정도)까지 원으로 표시
img_with_kp = cv2.drawKeypoints(img, kp, None, 
                                flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# 5. 결과 화면에 띄우기
plt.figure(figsize=(15, 7))
plt.imshow(cv2.cvtColor(img_with_kp, cv2.COLOR_BGR2RGB))
plt.title('SIFT Keypoints (Rich)')
plt.axis('off')
plt.show()
```

### 실행 결과
<img width="1499" height="762" alt="image" src="https://github.com/user-attachments/assets/7247169c-c1d4-4c0b-a550-a7cf2af4e515" />

---

## 02. 🤝 SIFT 특징점 매칭 (Feature Matching)
> **"두 사진에서 서로 같은 부분을 찾아 선으로 연결합니다."**

### 📝 문제 정의
두 장의 사진에서 각각 뽑은 특징점들을 비교하여, 가장 비슷하게 생긴 점끼리 짝을 지어줍니다.

### 🔑 핵심 개념
* **BFMatcher:** 모든 점을 일일이 대조해서 가장 가까운 '짝'을 찾는 무식하지만 확실한 방법(Brute-Force)입니다.
* **Distance:** 두 특징점이 얼마나 닮았는지를 나타내며, 숫자가 작을수록 '도플갱어' 수준으로 닮았다는 뜻입니다.

### 💻 실습 코드
```python
import cv2
import matplotlib.pyplot as plt

# 1. 비교할 두 장의 사진 불러오기
img1 = cv2.imread('mot_color70.jpg')
img2 = cv2.imread('mot_color83.jpg')

# 2. 각각의 사진에서 특징점(kp)과 특징 데이터(des) 추출하기
sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# 3. '짝짓기 매니저' 만들기
# crossCheck=True: 서로가 서로에게 1순위일 때만 커플로 인정! (정확도 UP)
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

# 4. 비슷한 점끼리 매칭하기
matches = bf.match(des1, des2)

# 거리(차이점)가 짧은 순서대로 정렬 (가장 닮은 커플부터!)
matches = sorted(matches, key=lambda x: x.distance)

# 5. 상위 50개 커플만 선으로 이어서 보여주기
res = cv2.drawMatches(img1, kp1, img2, kp2, matches[:50], None, 
                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

plt.figure(figsize=(20, 10))
plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
plt.title('SIFT Feature Matching (Top 50)')
plt.axis('off')
plt.show()
```

### 실행 결과
<img width="2001" height="1035" alt="image" src="https://github.com/user-attachments/assets/5f6a57f1-1757-4b99-b341-155a6cfbcdef" />

---

## 03. 📐 호모그래피 이미지 정합 (Image Alignment)
> **"두 사진의 대응점을 이용해 한 사진을 비틀어서 다른 사진에 딱 붙입니다."**

### 📝 문제 정의
매칭된 점들을 바탕으로 한쪽 사진을 어떻게 비틀어야 다른 사진과 겹칠지 계산(Homography)하고, 실제로 사진을 변형(Warping)하여 정렬합니다.

### 🔑 핵심 개념
* **Homography ($H$):** 한 평면을 다른 평면으로 투영시키는 3x3 변환 행렬입니다.
* **RANSAC:** 잘못 연결된 '가짜 매칭'들을 걸러내고 가장 믿을만한 연결만 사용하는 알고리즘입니다.
* **Warping:** 사진을 사다리꼴 모양 등으로 비틀어 시점을 맞추는 작업입니다.



### 💻 실습 코드
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 사진 불러오기
img1 = cv2.imread('img1.jpg') # 비틀어질 사진
img2 = cv2.imread('img2.jpg') # 기준이 될 사진

sift = cv2.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# 2. KNN 매칭 (가장 닮은 놈 2개씩 후보 뽑기)
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# 3. 진짜 닮은 점만 골라내기 (Lowe's Ratio Test)
# 1순위가 2순위보다 훨씬 압도적으로 닮았을 때만 채택!
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)

# 4. 사진을 붙이기 위한 수학적 계산
if len(good_matches) > 4:
    # 매칭된 점들의 좌표만 추출
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # RANSAC으로 가짜 매칭을 무시하고 '변환 행렬(H)' 찾기
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # 5. 사진 비틀기 (Warping)
    # img1을 H 행렬을 이용해 img2의 시점으로 비틉니다.
    h2, w2 = img2.shape[:2]
    # 도화지를 넓게(w1+w2) 준비해서 붙일 공간 확보
    warped_img = cv2.warpPerspective(img1, H, (img1.shape[1] + img2.shape[1], max(img1.shape[0], img2.shape[0])))

    # 결과 보기
    plt.figure(figsize=(20, 10))
    plt.imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB))
    plt.title('Warped Image (Alignment)')
    plt.axis('off')
    plt.show()
```

### 실행 결과
<img width="1998" height="1061" alt="image" src="https://github.com/user-attachments/assets/2bda12b5-e0d8-4b82-a37e-aa1e12b340a6" />

---
