import cv2
import mediapipe as mp
from classifier import classify
from hold_filter import HoldFilter
from sender import Sender
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import threading
import queue
import subprocess
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

tts_queue = queue.Queue()

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        try:
            subprocess.run(
                ['powershell', '-Command',
                 f'Add-Type -AssemblyName System.Speech; '
                 f'$s = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                 f'$s.Volume = 200; '
                 f'$s.Rate = -5; '
                 f'$s.Speak(" {text}")'],
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        except Exception as e:
            print(f"TTS 오류: {e}")

tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

def speak(text):
    if tts_queue.empty():
        tts_queue.put(text)

font = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 60)
font_small = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 25)
font_mode = ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", 30)

def put_korean(frame, text, pos, color=(0, 255, 0), size="big"):
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    if size == "big":
        f = font
    elif size == "small":
        f = font_small
    else:
        f = font_mode
    draw.text(pos, text, font=f, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def is_fist(lm):
    return (lm[8].y > lm[6].y and lm[12].y > lm[10].y and
            lm[16].y > lm[14].y and lm[20].y > lm[18].y)

def is_open(lm):
    return (lm[8].y < lm[6].y and lm[12].y < lm[10].y and
            lm[16].y < lm[14].y and lm[20].y < lm[18].y)

def is_thumb_up(lm):
    return (lm[4].y < lm[2].y and
            lm[8].y > lm[6].y and lm[12].y > lm[10].y and
            lm[16].y > lm[14].y and lm[20].y > lm[18].y)

def get_hand_side(lm):
    return "right" if lm[4].x > lm[17].x else "left"

hold_filter = HoldFilter(hold_time=1.0)
hold_filter_slow = HoldFilter(hold_time=2.0)
sender = Sender(host="192.168.0.24", port=9000)        #llllllllllll
sender.connect()

cap = cv2.VideoCapture(0)
current_confidence = 1.0
last_delete_time = 0
DELETE_INTERVAL = 0.5

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    char = None
    hand_count = 0
    left_lm = None
    right_lm = None

    if result.multi_hand_landmarks:
        hand_count = len(result.multi_hand_landmarks)

        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            lm = hand_landmarks.landmark
            side = get_hand_side(lm)
            if side == "left":
                left_lm = lm
            else:
                right_lm = lm

    # ===== 두 손 = 제스처 명령 모드 =====
    if hand_count == 2 and left_lm and right_lm:

        # 양손 주먹 → 홀딩 (아무것도 안 함)
        if is_fist(left_lm) and is_fist(right_lm):
            frame = put_korean(frame, "홀딩 중...", (10, 10), color=(100, 100, 100), size="mode")

        # 양손 펴기 → DELETE
        elif is_open(left_lm) and is_open(right_lm):
            frame = put_korean(frame, "제스처 명령 모드", (10, 10), color=(0, 200, 255), size="mode")
            now = time.time()
            if now - last_delete_time > DELETE_INTERVAL:
                sender.send("CMD:DELETE")
                speak("삭제")
                last_delete_time = now
            frame = put_korean(frame, "삭제 중...", (50, 100), color=(0, 100, 255), size="mode")

        # 왼손 엄지업 → 스페이스
        elif is_thumb_up(left_lm) and not is_thumb_up(right_lm):
            frame = put_korean(frame, "제스처 명령 모드", (10, 10), color=(0, 200, 255), size="mode")
            sender.send("CMD:SPACE")
            speak("스페이스")
            frame = put_korean(frame, "스페이스!", (50, 100), color=(255, 255, 0), size="mode")

        # 오른손 엄지업 → 전송
        elif is_thumb_up(right_lm) and not is_thumb_up(left_lm):
            frame = put_korean(frame, "제스처 명령 모드", (10, 10), color=(0, 200, 255), size="mode")
            sender.send("CMD:CONFIRM")
            speak("전송")
            frame = put_korean(frame, "전송!", (50, 100), color=(0, 255, 255), size="mode")

        else:
            frame = put_korean(frame, "제스처 명령 모드", (10, 10), color=(0, 200, 255), size="mode")

        hold_filter.update(None)
        hold_filter_slow.update(None)

    # ===== 한 손 = 지문자 인식 모드 =====
    elif hand_count == 1:
        frame = put_korean(frame, "인식 모드", (10, 10), color=(0, 255, 0), size="mode")

        for hand_landmarks in result.multi_hand_landmarks:
            char, confidence = classify(hand_landmarks)
            current_confidence = confidence

            if char:
                if confidence >= 0.9:
                    color = (0, 255, 0)
                elif confidence >= 0.7:
                    color = (0, 255, 255)
                else:
                    color = (0, 0, 255)

                frame = put_korean(frame, char, (50, 60), color=color)
                frame = put_korean(frame, f"{confidence*100:.1f}%", (50, 130), color=color, size="small")

        if current_confidence >= 0.65:
            active_filter = hold_filter
            hold_filter_slow.update(None)
        else:
            active_filter = hold_filter_slow
            hold_filter.update(None)

        progress = active_filter.get_progress()
        bar_max = 120
        bar_height = 10
        x1 = frame.shape[1] - 140
        y1 = 20
        bar_width = int(bar_max * progress)
        cv2.rectangle(frame, (x1, y1), (x1 + bar_max, y1 + bar_height), (50, 50, 50), -1)
        cv2.rectangle(frame, (x1, y1), (x1 + bar_width, y1 + bar_height), (0, 255, 0), -1)

        confirmed = active_filter.update(char)
        if confirmed:
            print(f"확정: {confirmed}")
            sender.send(confirmed)
            speak(confirmed)

    else:
        frame = put_korean(frame, "손을 보여주세요", (10, 10), color=(150, 150, 150), size="mode")
        hold_filter.update(None)
        hold_filter_slow.update(None)

    cv2.imshow("Hand Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
sender.close()
tts_queue.put(None)
cv2.destroyAllWindows()