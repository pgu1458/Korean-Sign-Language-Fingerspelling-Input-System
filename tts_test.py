import win32com.client

speaker = win32com.client.Dispatch("SAPI.SpVoice")
import time
time.sleep(0.5)  # 초기화 대기
speaker.Speak("아니 안녕하세요")
print("완료")