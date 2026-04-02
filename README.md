# 🧠 Image Recognition & Deep Learning

이 프로젝트는 인공 신경망(ANN)과 합성곱 신경망(CNN)을 사용하여 기계가 이미지를 어떻게 인식하고 분류하는지 학습하는 과정을 다룹니다.

---

## 01. 🔢 MNIST 손글씨 숫자 분류기 (Simple ANN)
> **"컴퓨터에게 0부터 9까지의 사람이 쓴 숫자를 가르칩니다."**

### 📝 문제 정의
28x28 픽셀 크기의 흑백 손글씨 이미지 70,000장을 학습시켜, 새로운 숫자를 보았을 때 그것이 어떤 숫자인지 맞히는 인공지능 모델을 구축합니다.

### 🔑 핵심 개념
* **Flatten (평탄화):** 2차원 이미지(28x28)를 인공지능이 읽기 좋게 1열(784줄)로 쭉 펼치는 작업입니다.
* **Dense (밀집층):** 뇌세포(뉴런)들이 서로 촘촘하게 연결되어 정보를 전달하는 신경망의 기본 단위입니다.
* **Relu & Softmax:** 인공지능이 판단을 내릴 때 사용하는 활성화 함수입니다. (Softmax는 최종 정답 확률을 알려줍니다.)

### 💻 실습 코드
```python
import tensorflow as tf
from tensorflow.keras import datasets, layers, models

# 1. MNIST 데이터셋 불러오기 (손글씨 데이터)
# x는 이미지 데이터, y는 해당 이미지의 정답(0~9)입니다.
(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

# 2. 데이터 전처리 (정규화)
# 픽셀값은 0~255 사이인데, 이를 0~1 사이의 작은 숫자로 바꿔주면 인공지능이 더 공부를 잘합니다.
train_images, test_images = train_images / 255.0, test_images / 255.0

# 3. 인공 신경망 모델 설계
model = models.Sequential([
    # 28x28 형태의 그림을 1차원 직선(784개)으로 쭉 펼칩니다.
    layers.Flatten(input_shape=(28, 28)),
    # 128개의 인공 뉴런을 배치하여 특징을 학습합니다.
    layers.Dense(128, activation='relu'),
    # 마지막 10개 뉴런은 숫자 0~9까지 각각의 확률을 출력합니다.
    layers.Dense(10, activation='softmax')
])

# 4. 모델 설정 (공부 방법 정하기)
model.compile(optimizer='adam', # 효율적으로 정답을 찾아가는 방법
              loss='sparse_categorical_crossentropy', # 틀린 정도를 계산하는 공식
              metrics=['accuracy']) # 얼마나 맞혔는지(정확도) 기록

# 5. 모델 훈련 (데이터를 5번 반복해서 학습)
model.fit(train_images, train_labels, epochs=5)

# 6. 정확도 평가
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print(f'\n최종 테스트 정확도: {test_acc*100:.2f}%')
```
<img width="597" height="212" alt="image" src="https://github.com/user-attachments/assets/2dc41a1c-9659-4b10-84f5-b45516e9f833" />

---

## 02. 🚗 CIFAR-10 사물 분류 CNN 모델 (Advanced CNN)
> **"비행기, 자동차, 새, 고양이 등 10가지 컬러 사물을 식별합니다."**

### 📝 문제 정의
단순한 숫자를 넘어 실제 세상의 컬러 이미지(32x32x3)를 분류합니다. 사물의 특징(눈, 코, 바퀴 등)을 스스로 추출하는 **CNN(합성곱 신경망)**을 사용합니다.

### 🔑 핵심 개념
* **Conv2D (합성곱):** 이미지 위에 돋보기를 대고 훑으며 사물의 부분적인 특징(선, 면, 무늬)을 찾아냅니다.
* **MaxPooling (풀링):** 중요한 특징만 남기고 이미지 크기를 줄여서 계산 효율을 높입니다.
* **Normalization:** 픽셀값을 0~1로 맞춰 모델의 학습 속도를 올립니다.

### 💻 실습 코드
```python
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np

# 1. CIFAR-10 데이터셋 불러오기 (10가지 사물 컬러 이미지)
(train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()

# 2. 데이터 전처리 (0~255 픽셀값을 0~1 사이로 정규화)
train_images, test_images = train_images / 255.0, test_images / 255.0

# 3. CNN 모델 설계 (특징 추출기 + 분류기)
model = models.Sequential([
    # 첫 번째 특징 추출: 32개의 돋보기(필터)로 이미지의 특징을 찾습니다.
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    # 중요한 정보만 남기고 크기를 절반으로 줄입니다.
    layers.MaxPooling2D((2, 2)),
    # 두 번째 특징 추출: 더 복잡한 특징(바퀴 모양 등)을 찾습니다.
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    # 분류기 단계: 찾은 특징들을 일렬로 펼친 뒤 학습합니다.
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax') # 10개 카테고리 중 하나로 결정
])

# 4. 모델 컴파일 및 훈련
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=10)

# 5. 실제 이미지(dog.jpg) 예측 예시 (가상 코드)
# img = load_and_preprocess('dog.jpg')
# prediction = model.predict(img)
# print(f"이 사진은 {np.argmax(prediction)}번 클래스(개)로 보입니다.")
```
<img width="659" height="393" alt="image" src="https://github.com/user-attachments/assets/eff1e61c-2973-4b74-a5e5-ee8c064a56f0" />

---
