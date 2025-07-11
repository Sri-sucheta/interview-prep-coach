import os
import random
from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
# It automatically reads the OPENAI_API_KEY from the environment
try:
    client = OpenAI()
    print("OpenAI client initialized successfully.")
except Exception as e:
    print(f"Error initializing OpenAI client: {e}")
    client = None

app = Flask(__name__)
CORS(app) # Enable Cross-Origin Resource Sharing

# --- A list of interview questions ---
INTERVIEW_QUESTIONS = [
    { "id": 1, "text": "Tell me about yourself." },
    { "id": 2, "text": "What are your biggest strengths and weaknesses?" },
    { "id": 3, "text": "Tell me about a challenging project you've worked on." },
    { "id": 4, "text": "Where do you see yourself in 5 years?" },
    { "id": 5, "text": "Why do you want to work for this company?" }
]

@app.route('/api/question')
def get_question():
    """Provides a random interview question."""
    random_question = random.choice(INTERVIEW_QUESTIONS)
    return jsonify(random_question)

@app.route('/api/feedback', methods=['POST'])
def get_feedback():
    """Receives text, gets feedback from OpenAI, and returns it."""
    if not client:
        return jsonify({"error": "OpenAI client is not initialized."}), 500

    data = request.json
    user_answer = data.get('answer')
    interview_question = data.get('question')

    if not user_answer:
        return jsonify({"error": "No answer provided"}), 400

    try:
        # This is the instruction for the AI model
        system_prompt = (
            "You are an expert interview coach. Your task is to provide clear, "
            "constructive, and friendly feedback on a user's answer to an interview question. "
            "Analyze their answer for clarity, structure (like the STAR method), and tone. "
            "Keep your feedback concise (around 3-4 sentences). "
            "Start with one positive point and then suggest one area for improvement."
        )

        # Make the API call to OpenAI
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"The question was: '{interview_question}'. My answer is: '{user_answer}'"}
            ]
        )

        feedback_text = completion.choices[0].message.content
        return jsonify({"feedback": feedback_text})

    except Exception as e:
        print(f"An error occurred during OpenAI API call: {e}")
        return jsonify({"error": "Failed to generate feedback from AI service."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)