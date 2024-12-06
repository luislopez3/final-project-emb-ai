from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

def emotion_detector(text_to_analyze):
    """
    Detects emotions in the given text using the Watson NLP Emotion Predict API.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: Dictionary containing emotion scores and the dominant emotion.
    """
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=input_json, timeout=10)
        response.raise_for_status()

        # Parse the API response JSON
        response_data = response.json()

        # Extract the emotion predictions
        predictions = response_data.get('emotionPredictions', [])
        if not predictions:
            return {"error": "No emotion predictions found in the response"}

        # Get the primary emotion scores
        emotions = predictions[0].get('emotion', {})
        required_emotions = {key: emotions.get(key, 0.0) for key in ['anger', 'disgust', 'fear', 'joy', 'sadness']}

        # Handle all-zero scores
        if all(score == 0.0 for score in required_emotions.values()):
            required_emotions['dominant_emotion'] = 'None'
        else:
            # Find the dominant emotion
            dominant_emotion = max(required_emotions, key=required_emotions.get)
            required_emotions['dominant_emotion'] = dominant_emotion

        return required_emotions

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    except KeyError:
        return {"error": "Unexpected response format from the API"}

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
