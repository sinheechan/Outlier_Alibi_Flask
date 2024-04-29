# Outlier_Alibi_MLops

< img src= "outlier_scratch_result.png">

## Object

Alibi는 데이터의 이상 감지를 위한 오픈소스 라이브러리입니다.
우리는 흔히 공정 과정에 현장에 불량 데이터가 적발되었을 시 신속한 체크를 필요로 합니다.
이 모델은 공정 감시 CCTV의 데이터를 가졌다고 가정하였을 때 이상탐지를 알려주는 역할을 수행합니다.

<br /><br /> 
## Dataset

- 본 모델 테스트를 위해 [Kaggle] Surface Crack Detection 데이터셋을 활용합니다.

<br /><br /> 
## Libraries used

- tensorflow
- alibi-detect
- pillow
- scikit-learn
- flask

<br /><br /> 
## WorkFlow

- Alibi 모델을 활용한 이상탐지 모델을 구축합니다.
- app.py 모듈을 통해 Web Application 사이트를 생성합니다.
- 사용자는 생성된 사이트를 통해 원하는 데이터셋을 업로드하여 이상이 있는지 판별할 수 있습니다.
- Watch.py, Client.py 모델은 데이터가 image 폴더에 들어오게 되면 자동으로 이미지 데이터를 분석합니다.
- 본 모델은 임계값(임의) 0.05 기준으로 '이상감지' or '이상없음' 텍스트를 출력합니다.
- 따라서 추후 실시간 카메라 데이터 image 폴더와 연동한다면 실시간으로 이상탐지 유무를 식별할 수 있을 것입니다.  

<br /><br /> 
## Result

- Alibi 모델의 학습 결과 ma-loss 값이 크게 감소하였으나 정확도 개선을 위해 다른 이상탐지 모델과 비교가 필요합니다.
- 많은 기업들이 이상탐지 모델을 필요로 하고 구축하는데 드는 비용을 고려하였을 때에는 완벽한 성능을 기대하기는 어렵습니다.
- 하지만, Alibi 모델은 Negative(결함없음) 데이터셋만을 학습하여 positive(결함있음) 데이터를 식별할 수 있는데에 큰 장점을 가집니다.
- 결론적으로, CCTV, 카메라 데이터를 이용한 실 사례 테스트를 해봄으로서 정확도 성능을 개선할 예정입니다.
  
