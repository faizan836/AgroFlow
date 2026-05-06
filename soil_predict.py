import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model("models/soil_model.h5")

classes = ["Alluvial Soil","Black Soil","Clay Soil","Red Soil","Sandy Soil"]

def predict_soil(image_path):

    img = cv2.imread(image_path)
    img = cv2.resize(img,(224,224))
    img = img/255.0
    img = np.reshape(img,(1,224,224,3))

    prediction = model.predict(img)

    soil = classes[np.argmax(prediction)]

    return soil