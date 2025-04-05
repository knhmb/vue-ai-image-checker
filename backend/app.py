from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HUGGINGFACE_API_TOKEN = "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"  # Replace with your token
MODEL_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    file_id = str(uuid.uuid4())[:8]  # generate a short random ID like 'abc123'
    image_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(image_path)

    # Send to Hugging Face model
    with open(image_path, "rb") as f:
        response = requests.post(MODEL_URL, headers=HEADERS, data=f)

    os.remove(image_path)

    if response.status_code != 200:
        return jsonify({'error': 'Hugging Face API error', 'details': response.text}), 500

    predictions = response.json()

    # Basic logic based on labels returned
    labels = [item['label'] for item in predictions]
    scores = [item['score'] for item in predictions]
    top_score = max(scores) * 100  # convert to percentage

    if any(label.lower() in ['comic book', 'cartoon', 'book jacket'] for label in labels):
        verdict = "Copyright Infringed"
    else:
        verdict = "No Issue"

    return jsonify({
        "file_id": file_id,
        "verdict": verdict,
        "confidence": round(top_score, 1)
    })

if __name__ == '__main__':
    app.run(debug=True)
