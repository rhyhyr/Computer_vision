**문제**

<img width="663" height="365" alt="Image" src="https://github.com/user-attachments/assets/4f439e79-0f69-42e7-907f-7421cd5ea9a3" />

**핵심 개념**
cv.setMouseCallback: 마우스가 움직이거나 클릭될 때 특정 함수(draw_circle)를 실행하도록 연결합니다.
flags & cv.EVENT_FLAG_LBUTTON: 드래그 중인 상태에서 어떤 버튼이 눌려있는지 확인하기 위해 비트 연산을 사용합니다.
브러시 크기 제한: min(15, ...)와 max(1, ...)를 사용하여 붓 크기가 지정된 범위(1~15)를 벗어나지 않도록 방어 코드를 작성했습니다.
cv.waitKey(1): 화면을 실시간으로 갱신하면서 키보드 입력을 즉시 감지하기 위해 루프 내부에 배치했습니다.

<img width="671" height="379" alt="Image" src="https://github.com/user-attachments/assets/ec1a853f-de52-46b8-bdeb-40b0daaaee0a" />

**전체 코드**

<img width="796" height="1075" alt="Image" src="https://github.com/user-attachments/assets/95776c76-3dcf-49eb-9c1d-41386549f369" />

**실행 결과**

<img width="1428" height="972" alt="Image" src="https://github.com/user-attachments/assets/be06b742-4bae-4b10-9de6-7c5b6a84063f" />
