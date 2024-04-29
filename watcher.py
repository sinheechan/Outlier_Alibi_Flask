import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import os
import client

# Target : 감시하는 폴더 
class Target:
    watchDir = os.getcwd()
    watchDir = 'C:\sinheechan.github.io-master\Outlier_Alibi_MLops\image' # watcher.py 감시 디렉토리

    def __init__(self):
        self.observer = Observer() # observer 감시

    def run(self):
        print('Watcher가 정상 실행되었습니다.')
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDir, 
                               recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Error가 발생하여 Stop을 실행합니다.")
            self.observer.join()

class Handler(FileSystemEventHandler):

# FileSystemEventHandler 클래스를 상속받음.
# 아래 핸들러들을 오버라이드 => 파일, 디렉터리 행동에 따른 정의
    
    # Case 1.파일이 움직일 때 실행
    '''
    def on_moved(self, event): 
        print(event)
    
    '''
    # Case 2.파일, 디렉터리가 생성되면 실행

    def on_created(self, event):
        print(event)
        file_path = event.src_path
        if os.path.isfile(file_path):
            client.send_img(file_path)   
        print("파일 생성이 감지되었습니다.")

    # Case 3.파일, 디렉터리가 삭제되면 실행 
       
    '''
    def on_deleted(self, event):
        print(event)
    '''
    # Case 4. 파일,디렉터리가 수정되면 실행

    '''
    def on_modified(self, event):
        print(event)
    '''

# 본 파일에서 실행될 때만 실행되도록 함
if __name__ == "__main__":
    w = Target()
    w.run()

