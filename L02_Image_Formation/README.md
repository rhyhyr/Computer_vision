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


## 5. 실행 결과
<img width="2371" height="823" alt="image" src="https://github.com/user-attachments/assets/e9974566-0775-4807-8207-dda388dbcb26" />


