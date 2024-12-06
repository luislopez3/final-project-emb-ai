"""
Flask application for emotion detection.

Provides routes for analyzing emotions in text and rendering the index page.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_analyzer():
    """
    Route to analyze emotions for the given text.
    """
    # Retrieve the text to analyze from the request arguments
    text_to_analyze = request.args.get('textToAnalyze')
    if not text_to_analyze:
        return "Error: Invalid text! Please try again!"

    # Pass the text to the emotion_detector function
    response = emotion_detector(text_to_analyze)

    # Format the response
    if 'error' in response:
        return f"Error: {response['error']}"

    # Extract emotions and scores
    emotions = ", ".join(
        [f"'{key}': {value}" for key, value in response.items() if key != 'dominant_emotion']
    )
    dominant_emotion = response['dominant_emotion']

    # Return the formatted string
    return (
        f"For the given statement, the system response is {emotions}. "
        f"The dominant emotion is {dominant_emotion}."
    )

@app.route("/")
def render_index_page():
    """
    Route to render the index.html page.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
