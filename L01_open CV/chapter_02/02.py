import cv2 as cv
import sys

# 1. 초기 설정
img = cv.imread('soccer.jpg')

if img is None: 
    sys.exit('파일을 찾을 수 없습니다.')

brush_size = 5  # 초기 붓 크기
drawing = False # 마우스 클릭 상태 확인용 변수

# 2. 콜백 함수 정의
def draw_circle(event, x, y, flags, param):
    global drawing, brush_size

    if event == cv.EVENT_LBUTTONDOWN:   # 좌클릭 시작
        drawing = True
        cv.circle(img, (x, y), brush_size, (255, 0, 0), -1) # 파란색
        
    elif event == cv.EVENT_RBUTTONDOWN: # 우클릭 시작
        drawing = True
        cv.circle(img, (x, y), brush_size, (0, 0, 255), -1) # 빨간색
        
    elif event == cv.EVENT_MOUSEMOVE:   # 마우스 이동 (드래그)
        if drawing:
            # 좌클릭 드래그 시 파란색, 우클릭 드래그 시 빨간색
            color = (255, 0, 0) if (flags & cv.EVENT_FLAG_LBUTTON) else (0, 0, 255)
            cv.circle(img, (x, y), brush_size, color, -1)
            
    elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP:
        drawing = False # 클릭 해제

# 3. 윈도우 생성 및 콜백 함수 등록
cv.namedWindow('Painting')
cv.setMouseCallback('Painting', draw_circle)

print("사용법: [L버튼-파랑/R버튼-빨강] [+/- 브러시 조절] [q-종료]")

# 4. 루프 처리
while True:
    cv.imshow('Painting', img)
    
    key = cv.waitKey(1) & 0xFF # 키 입력 대기 (1ms)

    if key == ord('q'): # 종료
        break
    elif key == ord('+') or key == ord('='): # 붓 크기 증가 (+는 보통 Shift와 함께 입력되므로 '='도 체크)
        brush_size = min(15, brush_size + 1)
        print(f"현재 붓 크기: {brush_size}")
    elif key == ord('-'): # 붓 크기 감소
        brush_size = max(1, brush_size - 1)
        print(f"현재 붓 크기: {brush_size}")

cv.destroyAllWindows()