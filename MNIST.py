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