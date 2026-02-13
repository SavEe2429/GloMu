import numpy as np
import pandas as pd
import joblib , sys , os , warnings
warnings.filterwarnings("ignore")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__) , "..")))
from backend.tts import speak_number
# -------------------------------------
# 1️⃣ LOAD MODEL
# -------------------------------------

model = joblib.load("./ML/models/randomforest_model.pkl")
print("✓ Model loaded")


# -------------------------------------
# 2️⃣ FEATURE EXTRACTION
# -------------------------------------
signals = ["ax","ay","az","gx","gy","gz","p0","p1","p2","p3"]

def extract_features(window):
    features = []
    for col in signals:
        data = window[col].values

        features.append(np.mean(data))
        features.append(np.std(data))
        features.append(np.max(data))
        features.append(np.min(data))
        features.append(np.max(data) - np.min(data))
        features.append(np.sqrt(np.mean(data**2)))

    acc_mag = np.sqrt(window["ax"]**2 + window["ay"]**2 + window["az"]**2)
    gyro_mag = np.sqrt(window["gx"]**2 + window["gy"]**2 + window["gz"]**2)

    features.append(np.mean(acc_mag))
    features.append(np.mean(gyro_mag))

    return np.array(features)

def predict(data_buffer):
    df = pd.DataFrame(data_buffer , columns=signals)
    features = extract_features(df).reshape(1,-1)
    prediction = model.predict(features)[0]
    prob = np.max(model.predict_proba(features))
    print(f"ข้อมูล : {df} ท่าทางที่ตรวจพบ: {prediction} (ความมั่นใจ: {prob:.2f})")
    speak_number(prediction)

# # -------------------------------------
# # 3️⃣ CREATE EXAMPLE WINDOW
# # -------------------------------------

# WINDOW_SIZE = 50
# example_data = []

# for i in range(WINDOW_SIZE):

#     ax = 1.20
#     ay = 0.41
#     az = 0.67

#     gx = -1.48
#     gy = -1.53
#     gz = -2.98

#     p0 = 3996
#     p1 = 3996
#     p2 = 4095
#     p3 = 4095

#     example_data.append([ax, ay, az, gx, gy, gz, p0, p1, p2, p3])

# df = pd.DataFrame(example_data, columns=[
#     "ax","ay","az","gx","gy","gz","p0","p1","p2","p3"
# ])


# # -------------------------------------
# # 4️⃣ EXTRACT FEATURE
# # -------------------------------------

# features = extract_features(df)
# features = features.reshape(1, -1)

# print("Feature shape:", features.shape)


# # -------------------------------------
# # 5️⃣ PREDICT
# # -------------------------------------

# prediction = model.predict(features)

# print("\nPrediction:", prediction[0])

# # ถ้าเป็น classifier
# if hasattr(model, "predict_proba"):
#     prob = model.predict_proba(features)
#     print("Confidence:", np.max(prob))
