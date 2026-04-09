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
img = load_and_preprocess('dog.jpg')
prediction = model.predict(img)
print(f"이 사진은 {np.argmax(prediction)}번 클래스(개)로 보입니다.")