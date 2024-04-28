# Row 데이터 가져오기

import zipfile
import os

# Kaggle : Surface Crack Detection 데이터셋
# https://www.kaggle.com/datasets/arunrk7/surface-crack-detection
def scratch_dataset():
    zip_file_path = r'C:/sinheechan.github.io-master/Mlops-outlier-detection_lee/archive.zip'
    extract_to_path = r'C:/sinheechan.github.io-master/Mlops-outlier-detection_lee/row_data'

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to_path)
        print("Zip 파일이 성공적으로 추출되었습니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")



# 함수 호출 버튼
scratch_dataset()