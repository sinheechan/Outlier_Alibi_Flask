# 이상 데이터 탐지 및 알림 전송

import requests

def send_img(img):
    file_path = img
    target_url = 'http://127.0.0.1:5000/predict' # 타겟 주소

    with open(file_path, 'rb') as f: # 이미지파일 읽기 : rb
        files = {'file' : f}
        res = requests.post(target_url, files=files)

    if res.status_code == 200: # 정상여부 : 200
        res = res.json() # 응답 Json

        anomaly_score = res['prediction'] # 점수 가져오기
        if float(anomaly_score.split(': ')[1]) >= 0.005: # 임계값과 대조
            print('이상 감지')
        else :
            print('이상 없음')
    else :
        print('Error :', res.text) # 예외처리 : Error