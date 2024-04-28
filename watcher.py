# image 파일이 업로드 될 때 마다 이상 탐지 모듈 가동

import requests

# 이미지 파일을 HTTP POST 요청을 통해 서버로 보내고, 서버에서 반환된 결과를 처리하는 역할
def send_img(img):
    file_path = img
    target_url = 'http://127.0.0.1:5000/predict' # 주소

    with open(file_path, 'rb') as f: # 이미지파일 읽기 : rb
        files = {'file' : f}
        res = requests.post(target_url, files=files)

    if res.status_code == 200: # 정상여부 : 200
        res = res.json() # 응답 Json

        anomaly_score = res['prediction'] # 점수 가져오기
        if float(anomaly_score.split(': ')[1]) >= 0.005:
            print('이상 감지')
        else :
            print('이상 없음')
    else :
        print('Error :', res.text) # 예외처리 : Error

# watcher 실행 시 단일 이미지 테스트용, 모듈 정상실행 테스트 목적
if __name__ == '__main__':
    file_path = 'Positive/00062.jpg' # 보낼 이미지 파일 경로

    target_url = 'http://127.0.0.1:5000/predict' 

    with open(file_path, 'rb') as f:
        files = {'file' : f}
        res = requests.post(target_url, files=files)

    if res.status_code == 200:
        res = res.json()
        print(res)

        anomaly_score = res['prediction']
        if float(anomaly_score.split(': ')[1]) >= 0.005:
            print('이상 감지')
        else :
            print('이상 없음')
    else :
        print('error :', res.text)