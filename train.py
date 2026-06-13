import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv("data.csv", encoding="cp949")
X = df.drop("label", axis=1)
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# RandomForest로 교체 (빠르고 정확도도 충분)
model = RandomForestClassifier(
    n_estimators=100,
    n_jobs=-1,        # CPU 전체 사용 → 빠름
    random_state=42
)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f"정확도: {acc * 100:.1f}%")

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("model.pkl 저장 완료!")