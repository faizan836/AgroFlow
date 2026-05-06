from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import base64

from ai.soil_predict import predict_soil
from ai.crop_recommend import predict_crop
from ai.weather_ai import get_weather, farmer_advice

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Dashboard Page
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Camera Image Prediction
@app.route("/predict", methods=["POST"])
def predict():

    data = request.json
    image_data = data["image"]
    lat = data["lat"]
    lon = data["lon"]

    # Base64 decode
    image_data = image_data.split(",")[1]
    image_bytes = base64.b64decode(image_data)

    image_path = os.path.join(UPLOAD_FOLDER, "captured.png")

    with open(image_path, "wb") as f:
        f.write(image_bytes)

    # Soil detection AI
    soil_type = predict_soil(image_path)

    # Example values (later sensors / weather API se aa sakta hai)
    N = 90
    P = 42
    K = 43
    temp = 25
    humidity = 70
    ph = 6.5
    rainfall = 200

    # Real Crop AI Model
    crop = predict_crop(N, P, K, temp, humidity, ph, rainfall)

    return jsonify({
    "soil": soil_type,
    "crop": crop,
    "lat": lat,
    "lon": lon
})


# Soil Detection (Direct Upload)
@app.route("/soil", methods=["POST"])
def soil():

    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    soil_type = predict_soil(path)

    return jsonify({"soil_type": soil_type})


# Crop Recommendation API
@app.route("/crop", methods=["POST"])
def crop():

    data = request.json

    crop = predict_crop(
        data["N"],
        data["P"],
        data["K"],
        data["temp"],
        data["humidity"],
        data["ph"],
        data["rainfall"]
    )

    return jsonify({"recommended_crop": crop})


# Weather AI
@app.route("/weather", methods=["POST"])
def weather():

    city = request.json["city"]

    temp, humidity, weather = get_weather(city)

    advice = farmer_advice(temp, humidity, weather)

    return jsonify({
        "temperature": temp,
        "humidity": humidity,
        "weather": weather,
        "advice": advice
    })


# Location Based Crop Suggestion
@app.route("/location_crop", methods=["POST"])
def location_crop():

    data = request.json

    lat = data["lat"]
    lon = data["lon"]

    # Example logic (later ML add kar sakte ho)
    crop = "Rice"

    return jsonify({
        "crop": crop
    })


if __name__ == "__main__":
    app.run(debug=True)