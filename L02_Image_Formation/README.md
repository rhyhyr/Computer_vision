우리가 카메라를 보면 보통 이미지가 왜곡되어 있다.
카메라의 원리가 핀홀 효과를 사용하기 때문에 주변부가 둥글게 왜곡되기 때문이다.
카메라의 내부 파라미터와 외부 파라미터를 보정하여 주변부를 직선이 되도록 펼칠 수 있다.

카메라의 파라미터는 내부 파라미터, 외부 파라미터가 있다
내부 파라미터 - 초점 거리, 광학 중심, 렌즈의 방사 왜곡 계수
외부 파라미터 - 시계 좌표계에 대한 카메라의 방향. 회전, 이동을 나타냄

왜 하는가? (Calibration의 목적)카메라 렌즈는 제조 공정상 미세하게 휘어 있습니다. 특히 광각 렌즈일수록 가장자리가 휘어 보이는 방사 왜곡이 심합니다. 이 왜곡을 해결해야 컴퓨터가 "이미지의 이 점이 실제 세상의 어느 위치인가?"를 정확히 계산할 수 있습니다.② 카메라 내부 행렬 (Camera Matrix, $K$)이미지 속의 픽셀 좌표를 실제 좌표계와 연결해 주는 '카메라의 주민등록증' 같은 값입니다.초점거리 ($f_x, f_y$): 렌즈가 얼마나 이미지를 확대/축소하는지 픽셀 단위로 나타냅니다.주점 ($c_x, c_y$): 렌즈의 정중앙이 이미지의 어느 픽셀에 맺히는지 나타냅니다. 보통 이미지 해상도의 절반 근처입니다.③ 왜곡 계수 (Distortion Coefficients)렌즈의 굴절 특성을 숫자로 표현한 것입니다.$k_1, k_2, k_3$: 직선이 볼록하거나 오목하게 보이는 정도를 결정합니다.$p_1, p_2$: 카메라 렌즈와 센서가 완벽하게 평행하지 않을 때 발생하는 비틀림을 잡아줍니다.

전체 코드 
import cv2
import numpy as np
import glob  # 특정 패턴의 파일 경로들을 리스트로 가져오는 도구

# --- 설정 단계 ---
# 체커보드 내부에서 가로, 세로로 만나는 지점(코너)의 개수 (가로 9개, 세로 6개)
CHECKERBOARD = (9, 6) 
# 체커보드 한 칸의 실제 물리적 크기 (단위: mm)
square_size = 25.0

# 코너 위치를 픽셀 미세 단위까지 찾기 위한 반복 중지 기준 (정밀도 설정)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# --- 실제 세상의 좌표(3D) 준비 ---
# 9x6개의 코너에 대해 (x, y, z) 좌표를 담을 0으로 채워진 행렬 생성
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
# 격자 모양의 인덱스 생성 (0,0,0), (1,0,0), (2,0,0) ... 순서
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
# 인덱스에 실제 크기(25mm)를 곱해 실제 좌표값으로 변환
objp *= square_size

# 실제 좌표(3D)와 이미지상 좌표(2D)를 저장할 리스트
objpoints = [] # 실제 세상의 좌표 (항상 동일한 패턴)
imgpoints = [] # 이미지에서 찾은 코너 좌표 (이미지마다 다름)

# 해당 경로에서 left로 시작하는 모든 이미지를 가져옴
images = glob.glob("images/calibration_images/left*.*") # 경로/확장자 주의!

img_size = None # 이미지 크기를 저장할 변수 초기화

# -----------------------------
# 1. 체크보드 코너 검출 단계
# -----------------------------
for fname in images:
    img = cv2.imread(fname) # 이미지 읽기
    if img is None: continue 
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 연산 속도를 위해 흑백 변환
    
    if img_size is None:
        img_size = gray.shape[::-1] # 이미지의 가로, 세로 크기 저장 (W, H)
    
    # 이미지에서 체커보드 코너 찾기 (성공 시 ret은 True)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    
    if ret == True:
        objpoints.append(objp) # 실제 좌표 추가
        # 찾은 코너 위치를 서브픽셀 단위로 더 정밀하게 다듬기
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2) # 다듬어진 이미지 좌표 추가

# -----------------------------
# 2. 카메라 파라미터 계산 (Calibration)
# -----------------------------
# objpoints와 imgpoints를 비교해 카메라의 특성(내부행렬, 왜곡계수)을 추출
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

print("Camera Matrix K (초점거리, 중심점):")
print(mtx)

print("\nDistortion Coefficients (왜곡 계수):")
print(dist)

# -----------------------------
# 3. 왜곡 보정 및 결과 보기
# -----------------------------
test_img_path = images[0] # 첫 번째 이미지를 테스트용으로 사용
img = cv2.imread(test_img_path)

# 계산된 mtx, dist를 이용해 왜곡이 없는 새로운 이미지 생성
dst = cv2.undistort(img, mtx, dist, None, mtx)

# 원본과 보정본을 가로로 붙여서 비교 시각화
res = np.hstack((img, dst)) 

cv2.imshow('Original (Left) vs Undistorted (Right)', res)
cv2.waitKey(0) # 아무 키나 누를 때까지 대기
cv2.destroyAllWindows()

실행 화면 <img width="1294" height="488" alt="image" src="https://github.com/user-attachments/assets/9e9b742d-c9d0-4101-853c-020398204c53" />

