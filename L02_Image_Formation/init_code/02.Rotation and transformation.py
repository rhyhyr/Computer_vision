import cv2
import numpy as np

# 1. 이미지 로드
img = cv2.imread('images/rose.png')
if img is None:
    print("이미지를 불러올 수 없습니다.")
    exit()

h, w = img.shape[:2]
center = (w // 2, h // 2) # 이미지의 중심점

# 2. 회전 및 크기 조절 행렬 생성
# cv2.getRotationMatrix2D(중심점, 각도, 배율)
# +각도는 반시계 방향 회전
matrix = cv2.getRotationMatrix2D(center, 30, 0.8)

# 3. 평행이동(Translation) 반영
# matrix는 2x3 행렬: [[alpha, beta, tx], [ -beta, alpha, ty]]
# 마지막 열(tx, ty)에 이동하고 싶은 픽셀 값을 더해줍니다.
matrix[0, 2] += 80  # x축 이동 (+80px)
matrix[1, 2] -= 40  # y축 이동 (-40px)

# 4. 최종 변환 적용 (Warp Affine)
# cv2.warpAffine(이미지, 변환행렬, 출력크기)
dst = cv2.warpAffine(img, matrix, (w, h))

# 5. 결과 시각화
cv2.imshow('Original', img)
cv2.imshow('Transformation Result', dst)

cv2.waitKey(0)
cv2.destroyAllWindows()