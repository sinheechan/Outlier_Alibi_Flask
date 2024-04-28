import matplotlib
# matplotlib.use('Agg')  # 백엔드를 Agg로 설정 => Flask 충돌우려로 인한 주석처리
from flask import Flask, request, render_template, jsonify
from alibi_detect.utils.saving import load_detector
from alibi_detect.od import OutlierVAE
from alibi_detect.utils.visualize import plot_instance_score, plot_feature_outlier_image
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
import time

# 서버를 구축하는 모듈입니다.

app = Flask(__name__)

# train.py 결과 모델 로드
od = load_detector('outlier_detection_model')

# 결과를 저장할 폴더 경로
results_folder = 'C:/sinheechan.github.io-master/Mlops-outlier-detection_lee/results_folder'

# result 폴더가 없는 경우 신규 폴더 생성
if not os.path.exists(results_folder):
    os.makedirs(results_folder)

# 파일로 결과를 저장
def save_result_image(fig, filename_prefix):
    if fig is None: # 예외처리
        return None
    
    img_path = os.path.join(results_folder, f"{filename_prefix}_{int(time.time())}.png")
    print("이미지가 저장되었습니다.:", img_path)
    
    fig.savefig(img_path)
    plt.close(fig)
    
    return img_path

# 파일을 업로드하면 분석결과 출력
@app.route('/', methods=['GET', 'POST'])

def home():
    if request.method == 'POST':
        
        # 예외처리1 => 파일을 아예 제출하지 않은 경우
        if 'file' not in request.files:
            return render_template('index.html', prediction="제출 된 파일이 없습니다. 파일을 다시 제출해주세요")

        file = request.files['file']

        # 예외처리2 => 파일 업로드 폼에서 파일을 선택하지 않은 경우
        if file.filename == '':
            return render_template('index.html', prediction="선택한 파일없음")

        # 정상 파일 제출 시 => 이미지로 변환하는 역할
        if file:
            img = Image.open(file.stream).convert('RGB')
            img = img.resize((64, 64))
            img = np.asarray(img)
            img = img.astype(np.float32) / 255. # 정규화
            img = img.reshape(1, 64, 64, 3)

            # 이미지 데이터 => 이상 탐지 모델에서 재구성
            x_recon = od.vae(img).numpy()

            # 예측 수행
            # od.predict : 이미지가 얼마나 정상적인지를 나타내는 값 반환
            od_preds = od.predict(img, outlier_type='instance', return_feature_score=True, return_instance_score=True)

            # 결과를 시각화, 시각화된 결과를 이미지 파일로 저장
            instance_score_plot = plot_instance_score(od_preds, [0], ['normal', 'outlier'], od.threshold)
            instance_score_plot_path = save_result_image(instance_score_plot, 'instance_score_plot')

            feature_outlier_image = plot_feature_outlier_image(od_preds, img, X_recon=x_recon, max_instances=5, outliers_only=False)
            feature_outlier_image_path = save_result_image(feature_outlier_image, 'feature_outlier_image')

            return render_template('index.html', prediction="Anomaly Score: {:.4f}".format(od_preds['data']['instance_score'][0]), instance_score_plot=instance_score_plot_path, feature_outlier_image=feature_outlier_image_path)
    else:
        return render_template('index.html', prediction=None)
