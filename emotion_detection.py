from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def emotion_detector(text_to_analyze):
    """
    Detects emotions in the given text using the Watson NLP Emotion Predict API.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: The text attribute from the response object.
    """
    # Define the API endpoint and headers
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }

    # Create the input JSON payload
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        # Send a POST request to the Emotion Predict API
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()  # Raise an error for HTTP response codes >= 400

        # Extract and return the response JSON
        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/')
def index():
    """
    Route to serve the homepage.
    """
    return render_template('index.html')

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """
    Flask route to handle emotion detection requests.
    Expects JSON input in the format: {"text": "Text to analyze"}
    """
    # Parse input JSON
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input, 'text' field is required"}), 400

    # Call the emotion_detector function
    text_to_analyze = data['text']
    result = emotion_detector(text_to_analyze)

    # Return the result as JSON
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug = True, port=8080)
