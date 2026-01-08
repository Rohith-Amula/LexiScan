from flask import Flask, request, jsonify
from streamlit_app.utils.corrector import correct_text  # Ensure this path is correct
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "✅ LexiScan Grammar Correction API is running."

@app.route('/correct', methods=['POST'])
def correct():
    data = request.get_json()
    text = data.get("text", "")
    corrected = correct_text(text)
    return jsonify({"corrected": corrected})

if __name__ == '__main__':
    app.run(debug=True)
