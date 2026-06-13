import speech_recognition as sr
from sender import Sender

sender = Sender(host="172.20.10.4", port=9000)
sender.connect()

r = sr.Recognizer()

print("음성 인식 시작...")

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:
        try:
            print("말하세요...")
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio, language="ko-KR")
            print(f"인식됨: {text}")

            for char in text:
                sender.send(f"VOICE:{char}")

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            print("인식 실패")
        except KeyboardInterrupt:
            break

sender.close()