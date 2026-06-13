import pickle
import numpy as np
import warnings
warnings.filterwarnings('ignore')

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

def classify(landmarks):
    lm = landmarks.landmark
    row = np.array([[val for lm_pt in lm for val in [lm_pt.x, lm_pt.y, lm_pt.z]]])
    proba = model.predict_proba(row)[0]
    max_idx = np.argmax(proba)
    confidence = proba[max_idx]
    char = model.classes_[max_idx]
    return char, confidence  # 글자 + 신뢰도 같이 반환