from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origins=["*"])

# Load model once
model = load_model("rice.h5")

# Inverse label map for predictions
inv_df_labels = {0: 'arborio', 1: 'basmati', 2: 'ipsala', 3: 'jasmine', 4: 'karacadag'}

def prepare_image(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img
@app.route("/")
def hello_world():
    
    return "<h1>Welcome to Rice Type Classification Server</h1>"
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    filepath = os.path.join("uploads", file.filename)
    file.save(filepath)

    img = prepare_image(filepath)
    preds = model.predict(img)
    pred_class = np.argmax(preds, axis=1)[0]
    label = inv_df_labels[pred_class]

    # Clean up uploaded file
    os.remove(filepath)

    return jsonify({'prediction': label})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
