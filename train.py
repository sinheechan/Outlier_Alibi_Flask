import tensorflow as tf
from tensorflow.keras.layers import Conv2D, Conv2DTranspose, Dense, Layer, Reshape, InputLayer
from alibi_detect.models.tensorflow.losses import elbo
from alibi_detect.od import OutlierVAE
import numpy as np
from PIL import Image
from sklearn.model_selection import train_test_split
from glob import glob
from alibi_detect.utils.saving import save_detector

# 이 모듈은 이상 탐지 모델을 학습하고 저장하는 역할을 수행합니다.

# 이미지 파일 경로에 따라 해당 이미지들을 넘파이 배열로 변환 => RGB 형식 반환
def img_to_np(fpaths, resize=True):  
    img_array = []
    for fname in fpaths:
        try:
            img = Image.open(fname).convert('RGB')
            if resize: 
                img = img.resize((64, 64))
            img_array.append(np.asarray(img))
        except:
            continue
    images = np.array(img_array)
    return images

# Data 불러오기, Split, 정규화
Negative_data = "C:/sinheechan.github.io-master/Outlier_Alibi_MLops/dataset_file/Negative/*.jpg" # 경로
img_list = glob(Negative_data) # 불러오기 => 리스트 저장
train_img_list, val_img_list = train_test_split(img_list, test_size=0.1, random_state=2024) # split
x_train = img_to_np(train_img_list[:1000]) # 훈련데이터 1,000개 이미지를 넘파이로 반환
x_train = x_train.astype(np.float32) / 255. # 이미지 정규화

# Encoder 네트워크 정의
latent_dim = 1024
encoder_net = tf.keras.Sequential([
    InputLayer(input_shape=(64, 64, 3)),
    Conv2D(64, 4, strides=2, padding='same', activation=tf.nn.relu),
    Conv2D(128, 4, strides=2, padding='same', activation=tf.nn.relu),
    Conv2D(512, 4, strides=2, padding='same', activation=tf.nn.relu)
])

# Decoder 네트워크 정의
decoder_net = tf.keras.Sequential([
    InputLayer(input_shape=(latent_dim,)),
    Dense(4 * 4 * 128),
    Reshape(target_shape=(4, 4, 128)),
    Conv2DTranspose(256, 4, strides=2, padding='same', activation=tf.nn.relu),
    Conv2DTranspose(64, 4, strides=2, padding='same', activation=tf.nn.relu),
    Conv2DTranspose(32, 4, strides=2, padding='same', activation=tf.nn.relu),
    Conv2DTranspose(3, 4, strides=2, padding='same', activation='sigmoid')
])

# 이상 탐지 모델 훈련
od = OutlierVAE(
    threshold=.005, # 임계값 : 0.005 설정
    score_type='mse', # MSE 평가지표_메뉴얼
    encoder_net=encoder_net,
    decoder_net=decoder_net,
    latent_dim=latent_dim,
)
od.fit(x_train, epochs=10, verbose=True) # epochs = 1

# 모델 저장
save_detector(od, 'outlier_Scratch_model')
