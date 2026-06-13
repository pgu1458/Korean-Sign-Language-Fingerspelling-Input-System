import cv2
import mediapipe as mp
import csv
import os

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 문제 있는 글자만 집중 수집
LABELS = ["ㅜ","ㅜ"]

DATA_FILE = "data.csv"
TARGET = 500

# CSV 파일 없으면 헤더 생성
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        header = ["label"] + [f"{i}_{axis}" for i in range(21) for axis in ["x","y","z"]]
        writer.writerow(header)

label_idx = 0
current_label = LABELS[label_idx]
count = 0
collecting = False

cap = cv2.VideoCapture(0)

print(f"현재 수집 중: {current_label} | 스페이스: 시작/중지 | N: 다음 | Q: 종료")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    status = "수집중" if collecting else "대기중"
    color = (0, 255, 0) if collecting else (0, 0, 255)

    cv2.putText(frame, f"{current_label} | {count}/{TARGET} | {status}",
                (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, "SPACE:시작/중지 | N:다음 | Q:종료",
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if collecting and count < TARGET:
                lm = hand_landmarks.landmark
                row = [current_label] + [val for lm_pt in lm for val in [lm_pt.x, lm_pt.y, lm_pt.z]]
                with open(DATA_FILE, "a", newline="", encoding="cp949") as f:
                    csv.writer(f).writerow(row)
                count += 1

                if count >= TARGET:
                    collecting = False
                    print(f"{current_label} 수집 완료! N 눌러서 다음으로")

    cv2.imshow("Data Collector", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord(' '):
        collecting = not collecting
        print(f"수집 {'시작' if collecting else '중지'}")
    elif key == ord('n'):
        if label_idx < len(LABELS) - 1:
            label_idx += 1
            current_label = LABELS[label_idx]
            count = 0
            collecting = False
            print(f"다음 글자: {current_label}")
        else:
            print("모든 글자 수집 완료!")

cap.release()
cv2.destroyAllWindows()