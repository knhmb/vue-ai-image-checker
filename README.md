# AI Image Copyright Checker

A Vue + Flask application that lets users upload an image and checks for potential copyright issues using a real AI model from Hugging Face.

---

## Project Structure

```
root/
├── frontend/   # Vue 3 project
├── backend/    # Flask API
└── README.md
```

---

## Getting Started

### Frontend (Vue)

#### Install dependencies

```bash
cd frontend
npm install
```

#### Run the development server

```bash
npm run dev
```

The Vue app should now be running at [http://localhost:5173](http://localhost:5173)

---

### Backend (Flask + Hugging Face AI)

#### Set up Python environment

```bash
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Run the Flask server

```bash
python app.py
```

The Flask API will be available at [http://localhost:5000/upload](http://localhost:5000/upload)

---

### AI Model

This app uses the **[`google/vit-base-patch16-224`](https://huggingface.co/google/vit-base-patch16-224)** Vision Transformer model hosted on Hugging Face for image classification.

Make sure to set your Hugging Face API token in the Flask backend:

```python
HUGGINGFACE_API_TOKEN = "your_token_here"
```

---

## API Integration

### Endpoint: `POST /upload`

**Request:**

- FormData with one field:
  - `image`: uploaded file (JPG/PNG)

**Response (Example):**

```json
{
  "file_id": "abc123",
  "verdict": "Copyright Infringed",
  "confidence": 87.5
}
```

**Error Response (500):**

```json
{
  "error": "Hugging Face API error",
  "details": "..."
}
```

---

## Features

- Upload and preview images
- Validates image file types
- Sends image to real Hugging Face AI model
- Interprets response and gives verdict + confidence
- Displays error messages and feedback

---

## Notes

- Verdict is based on presence of keywords like `comic book`, `cartoon`, or `book jacket` in the AI's predicted labels.
- Confidence is based on the top predicted class from Hugging Face model.

---

## License

MIT — free to use, modify, and build upon.
