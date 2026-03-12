# 📸 Camera Calibration with OpenCV

이 프로젝트는 OpenCV를 사용하여 카메라의 고유 파라미터를 계산하고, 렌즈로 인해 발생하는 이미지 왜곡을 보정하는 프로세스를 담고 있습니다.

## 1. 개요: 왜 카메라 캘리브레이션이 필요한가?

우리가 사용하는 대부분의 카메라는 핀홀 모델을 기반으로 하지만, 실제 제조 과정에서 렌즈의 물리적 특성으로 인해 **주변부가 둥글게 휘는 왜곡**이 발생합니다. 특히 광각 렌즈일수록 이러한 현상이 심하며, 이를 보정해야 컴퓨터가 이미지상의 픽셀을 실제 세상의 좌표로 정확하게 인식할 수 있습니다.

### 🛠 카메라 파라미터의 종류

* **내부 파라미터 (Intrinsic Parameters):** 카메라 자체의 고유한 특성
* **초점 거리 ($f_x, f_y$):** 렌즈와 센서 사이의 거리 (픽셀 단위)
* **주점 ($c_x, c_y$):** 렌즈의 중심이 이미지 센서에 맺히는 좌표
* **왜곡 계수 ($k_1, k_2, p_1, p_2...$):** 렌즈의 굴절 특성


* **외부 파라미터 (Extrinsic Parameters):** 실제 세계 좌표계와 카메라 사이의 관계
* 카메라의 **회전(Rotation)** 및 **이동(Translation)** 상태



---

## 2. 주요 개념

### 🆔 카메라 내부 행렬 (Camera Matrix, $K$)

이미지의 픽셀 좌표를 실제 좌표계와 연결해 주는 '카메라의 주민등록증' 같은 값입니다.


$$K = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix}$$

### 🌀 왜곡 계수 (Distortion Coefficients)

* **방사 왜곡 (Radial Distortion):** $k_1, k_2, k_3$ 등. 직선이 볼록(배럴 왜곡)하거나 오목(핀쿠션 왜곡)하게 보이는 정도를 결정합니다.
* **접선 왜곡 (Tangential Distortion):** $p_1, p_2$. 카메라 렌즈와 센서가 완벽하게 평행하지 않을 때 발생하는 비틀림을 보정합니다.

---

## 3. 구현 코드
<img width="731" height="970" alt="image" src="https://github.com/user-attachments/assets/29c42cad-d0d9-42b4-9827-c53c6e582e55" />
<img width="738" height="527" alt="image" src="https://github.com/user-attachments/assets/bf55b797-c005-442d-9e5c-70c6be063b06" />


---

## 4. 실행 결과
<img width="1294" height="488" alt="스크린샷 2026-03-12 160419" src="https://github.com/user-attachments/assets/4814ab53-166d-421f-a33e-af630879c2a2" />

깃허브 리드미에 추가하기 좋은 두 번째 주제, **이미지 변환(Image Transformation)** 내용을 정리해 드립니다. 이번 주제는 카메라로 찍은 이미지를 기하학적으로 어떻게 조작하는지(Affine Transformation)를 다룹니다.

---

# 🔄 Image Rotation & Transformation

이 프로젝트는 이미지 처리의 기초인 **어파인 변환(Affine Transformation)**을 활용하여 이미지의 회전, 크기 조절, 평행이동을 동시에 적용하는 방법을 다룹니다.

## 1. 개요: 어파인 변환(Affine Transformation)이란?

어파인 변환은 선의 평행성을 유지하면서 이미지를 변형시키는 방법입니다. 변환 행렬 $M$을 이용하여 이미지의 각 픽셀 $(x, y)$를 새로운 좌표 $(x', y')$로 이동시킵니다.

$$\begin{bmatrix} x' \\ y' \end{bmatrix} = M \begin{bmatrix} x \\ y \\ 1 \end{bmatrix}$$

이 프로젝트에서는 **회전(Rotation)**, **스케일링(Scaling)**, **평행이동(Translation)**을 하나의 행렬에 담아 처리합니다.

---

## 2. 주요 단계 및 요구사항

1. **회전:** 이미지 중심을 기준으로 **+30도** 회전
2. **크기 조절:** 회전과 동시에 크기를 **0.8배**로 축소
3. **평행이동:** 결과물을 **x축 +80px, y축 -40px** 이동

---

## 3. 구현 코드

<img width="555" height="684" alt="image" src="https://github.com/user-attachments/assets/b7cb2c7f-a1e0-4bb0-a114-09d90141a814" />

---

## 4. 핵심 함수 설명

### 🛠 `cv2.getRotationMatrix2D(center, angle, scale)`

회전을 위한 2x3 변환 행렬을 생성합니다.

* **center:** 회전의 중심축 (x, y)
* **angle:** 회전 각도 (양수는 반시계 방향)
* **scale:** 이미지 배율 (1.0은 원본 크기)

### 🛠 `cv2.warpAffine(src, M, dsize)`

생성된 행렬 $M$을 실제 이미지에 적용합니다.

* **src:** 원본 이미지
* **M:** 2x3 변환 행렬
* **dsize:** 출력 이미지 크기 (가로, 세로)

---

## 5. 실행 결과 요약

* 이미지가 중앙에서 **30도** 돌아가며 약간 작아졌습니다.
* 동시에 오른쪽으로 **80픽셀**, 위쪽으로 **40픽셀** 이동하여 배치됩니다.

---

## 4. 실행 결과
<img width="2371" height="823" alt="image" src="https://github.com/user-attachments/assets/e9974566-0775-4807-8207-dda388dbcb26" />


# 📐 Stereo Disparity & Depth Estimation

이 프로젝트는 좌/우 두 장의 스테레오 이미지를 분석하여 물체의 입체감을 계산하고, 실제 거리(Depth)를 추정하는 과정을 다룹니다.

## 1. 핵심 이론

* **Disparity (시차, $d$):** 왼쪽 이미지와 오른쪽 이미지에서 동일한 물체의 픽셀 위치 차이입니다. 물체가 가까울수록 시차는 커집니다.
* **Depth (깊이, $Z$):** 카메라로부터 물체까지의 실제 거리입니다. 시차와 반비례 관계를 가집니다.
* 공식: 
$$Z = \frac{f \times B}{d}$$


* $f$: 초점 거리 (Focal length)
* $B$: 두 카메라 사이의 거리 (Baseline)



---

## 2. 전체 구현 코드

```python
import cv2
import numpy as np
from pathlib import Path

# 출력 폴더 생성
output_dir = Path("./outputs")
output_dir.mkdir(parents=True, exist_ok=True)

# 좌/우 이미지 불러오기
left_color = cv2.imread("images/left.png")
right_color = cv2.imread("images/right.png")

if left_color is None or right_color is None:
    raise FileNotFoundError("좌/우 이미지를 찾지 못했습니다.")


# 카메라 파라미터
f = 700.0
B = 0.12

# ROI 설정
rois = {
    "Painting": (55, 50, 130, 110),
    "Frog": (90, 265, 230, 95),
    "Teddy": (310, 35, 115, 90)
}

# 그레이스케일 변환
left_gray = cv2.cvtColor(left_color, cv2.COLOR_BGR2GRAY)
right_gray = cv2.cvtColor(right_color, cv2.COLOR_BGR2GRAY)

# -----------------------------
# 1. Disparity 계산
# -----------------------------
# numDisparities: 탐색 범위 (16의 배수), blockSize: 비교 윈도우 크기 (홀수)
stereo = cv2.StereoBM_create(numDisparities=64, blockSize=15)
disparity_raw = stereo.compute(left_gray, right_gray).astype(np.float32)

# StereoBM은 결과를 16배 스케일해서 반환하므로 16으로 나눠줌
disparity = disparity_raw / 16.0
# -----------------------------
# 2. Depth 계산
# Z = fB / d
# -----------------------------
# 0으로 나누기 방지 및 유효한 시차(d > 0)만 계산
depth_map = np.zeros_like(disparity)
valid_mask = disparity > 0
depth_map[valid_mask] = (f * B) / disparity[valid_mask]

# -----------------------------
# 3. ROI별 평균 disparity / depth 계산
# -----------------------------
results = {}
for name, (x, y, w, h) in rois.items():
    roi_disp = disparity[y:y+h, x:x+w]
    roi_depth = depth_map[y:y+h, x:x+w]
    
    # ROI 내 유효한 값들만 평균 계산
    valid_roi = roi_disp > 0
    avg_disp = np.mean(roi_disp[valid_roi]) if np.any(valid_roi) else 0
    avg_depth = np.mean(roi_depth[valid_roi]) if np.any(valid_roi) else 0
    
    results[name] = {"disparity": avg_disp, "depth": avg_depth}

# -----------------------------
# 4. 결과 출력 및 해석
# -----------------------------
print(f"{'Region':<10} | {'Avg Disparity':<15} | {'Avg Depth (m)':<15}")
print("-" * 45)
for name, data in results.items():
    print(f"{name:<10} | {data['disparity']:<15.2f} | {data['depth']:<15.4f}")

# 가장 가까운/먼 곳 해석
sorted_depth = sorted(results.items(), key=lambda x: x[1]['depth'])
print(f"\n[해석] 가장 가까운 영역: {sorted_depth[0][0]} ({sorted_depth[0][1]['depth']:.2f}m)")
print(f"[해석] 가장 먼 영역: {sorted_depth[-1][0]} ({sorted_depth[-1][1]['depth']:.2f}m)")
# -----------------------------
# 5. disparity 시각화
# 가까울수록 빨강 / 멀수록 파랑
# -----------------------------
disp_tmp = disparity.copy()
disp_tmp[disp_tmp <= 0] = np.nan

if np.all(np.isnan(disp_tmp)):
    raise ValueError("유효한 disparity 값이 없습니다.")

d_min = np.nanpercentile(disp_tmp, 5)
d_max = np.nanpercentile(disp_tmp, 95)

if d_max <= d_min:
    d_max = d_min + 1e-6

disp_scaled = (disp_tmp - d_min) / (d_max - d_min)
disp_scaled = np.clip(disp_scaled, 0, 1)

disp_vis = np.zeros_like(disparity, dtype=np.uint8)
valid_disp = ~np.isnan(disp_tmp)
disp_vis[valid_disp] = (disp_scaled[valid_disp] * 255).astype(np.uint8)

disparity_color = cv2.applyColorMap(disp_vis, cv2.COLORMAP_JET)

# -----------------------------
# 6. depth 시각화
# 가까울수록 빨강 / 멀수록 파랑
# -----------------------------
depth_vis = np.zeros_like(depth_map, dtype=np.uint8)

if np.any(valid_mask):
    depth_valid = depth_map[valid_mask]

    z_min = np.percentile(depth_valid, 5)
    z_max = np.percentile(depth_valid, 95)

    if z_max <= z_min:
        z_max = z_min + 1e-6

    depth_scaled = (depth_map - z_min) / (z_max - z_min)
    depth_scaled = np.clip(depth_scaled, 0, 1)

    # depth는 클수록 멀기 때문에 반전
    depth_scaled = 1.0 - depth_scaled
    depth_vis[valid_mask] = (depth_scaled[valid_mask] * 255).astype(np.uint8)

depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)

# -----------------------------
# 7. Left / Right 이미지에 ROI 표시
# -----------------------------
left_vis = left_color.copy()
right_vis = right_color.copy()

for name, (x, y, w, h) in rois.items():
    cv2.rectangle(left_vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(left_vis, name, (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.rectangle(right_vis, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(right_vis, name, (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

# -----------------------------
# 8. 저장
# -----------------------------
cv2.imwrite(str(output_dir / "disparity_color.png"), disparity_color)
cv2.imwrite(str(output_dir / "depth_color.png"), depth_color)
cv2.imwrite(str(output_dir / "left_roi.png"), left_vis)
# -----------------------------
# 9. 출력
# -----------------------------
print(f"\n결과 이미지가 '{output_dir}' 폴더에 저장되었습니다.")

```

---

## 3. 핵심 포인트 설명
### 🛠 `cv2.StereoBM_create()`

* **`numDisparities`**: 왼쪽으로 최대 몇 픽셀까지 찾을 것인가를 결정합니다. 물체가 카메라와 아주 가깝다면 이 값을 키워야 합니다.
* **`blockSize`**: 주변의 특징을 얼마나 크게 묶어서 비교할지 정합니다. 값이 작으면 디테일하지만 노이즈가 생기고, 크면 뭉툭하지만 안정적입니다.


## 4. 실행 결과

<img width="916" height="1054" alt="image" src="https://github.com/user-attachments/assets/094c074c-61fc-426d-a348-466cab30715b" />



