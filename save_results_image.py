import os
import time
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

def save_result_image(fig, directory, filename):
    if fig is None: # 예외처리
        return None
    
    img_path = os.path.join(directory, f"{filename}_{int(time.time())}.png")
    print("이미지가 저장되었습니다.:", img_path)  # 추가
    
    fig.savefig(img_path)
    plt.close(fig)  # 그림 객체 닫기
    return img_path