import joblib
import numpy as np

model = joblib.load("models/crop_model.pkl")

def predict_crop(N, P, K, temp, humidity, ph, rainfall):

    input_data = np.array([[N, P, K, temp, humidity, ph, rainfall]])

    prediction = model.predict(input_data)

    return prediction[0]