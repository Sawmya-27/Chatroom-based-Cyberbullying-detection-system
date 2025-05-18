# File: core/bullying_detector.py

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import librosa

image_model = load_model('/Users/sawmy/Desktop/img project/models/models/image_model.h5')


def detect_bullying_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = image_model.predict(img_array)
    return prediction[0][0] > 0.5

