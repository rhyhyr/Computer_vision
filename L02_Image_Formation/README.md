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

```

---

## 4. 실행 결과
 <img width="1294" height="488" alt="image" src="https://github.com/user-attachments/assets/9e9b742d-c9d0-4101-853c-020398204c53" />

