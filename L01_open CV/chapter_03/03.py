import cv2 as cv
import sys

# 1. 초기 설정
img = cv.imread('soccer.jpg')
if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

img_copy = img.copy()  # 원본 보관용 (리셋용)
roi = None             # 잘라낸 이미지를 담을 변수
start_x, start_y = -1, -1
drawing = False

# 2. 마우스 콜백 함수
def draw_roi(event, x, y, flags, param):
    global start_x, start_y, drawing, img, roi

    if event == cv.EVENT_LBUTTONDOWN:   # 시작점 지정
        drawing = True
        start_x, start_y = x, y

    elif event == cv.EVENT_MOUSEMOVE:   # 드래그 중 사각형 그리기
        if drawing:
            img_draw = img.copy() # 잔상 제거를 위해 매번 복사본 생성
            cv.rectangle(img_draw, (start_x, start_y), (x, y), (0, 255, 0), 2)
            cv.imshow('ROI Selection', img_draw)

    elif event == cv.EVENT_LBUTTONUP:   # 마우스를 떼면 ROI 추출
        drawing = False
        # 좌표 정렬 (역방향 드래그 대비)
        x1, x2 = min(start_x, x), max(start_x, x)
        y1, y2 = min(start_y, y), max(start_y, y)

        if x1 != x2 and y1 != y2: # 영역이 유효할 때만
            roi = img[y1:y2, x1:x2].copy() # ROI 추출 (Numpy 슬라이싱)
            cv.imshow('Extracted ROI', roi)
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2) # 원본에 표시

# 3. 메인 루프 및 키보드 이벤트
cv.namedWindow('ROI Selection')
cv.setMouseCallback('ROI Selection', draw_roi)


while True:
    cv.imshow('ROI Selection', img)
    key = cv.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    elif key == ord('r'): # 리셋
        img = img_copy.copy()
        cv.destroyWindow('Extracted ROI')
        print("영역이 초기화되었습니다.")
    elif key == ord('s'): # 저장
        if roi is not None:
            cv.imwrite('extracted_roi.jpg', roi)
            print("ROI가 'extracted_roi.jpg'로 저장되었습니다.")
        else:
            print("저장할 영역이 없습니다. 먼저 드래그하세요.")

cv.destroyAllWindows()