# AI Interview Prep Coach

This is a web application designed to help job seekers practice for interviews. It uses speech recognition to capture a user's answer and leverages an AI language model (via the OpenAI API) to provide instant, constructive feedback on their communication skills.

---

### Key Features

*   **Random Question Generation:** Serves a random interview question each time the user visits.
*   **Voice-to-Text Transcription:** Uses the browser's Web Speech API to transcribe user answers in real-time.
*   **AI-Powered Feedback:** Sends the transcribed answer to the OpenAI API (GPT-3.5) to analyze for clarity, structure, and tone.
*   **Interview History:** Saves every practice session (question, answer, and feedback) to a local SQLite database for future review.

---

### Tech Stack

*   **Frontend:** Vue.js
*   **Backend:** Python with Flask
*   **AI Integration:** OpenAI API
*   **Speech Recognition:** Web Speech API
*   **Database:** SQLite
*   **API Communication:** Axios

---

### How to Run Locally

To run this project on your own machine:

1.  **Prerequisites:** You need Node.js and Python 3 installed.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sri-sucheta/interview-prep-coach.git
    cd interview-prep-coach
    ```
3.  **Setup Backend:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt # We will create this file next
    cp .env.example .env # We will create .env.example next
    # Add your OpenAI API key to the .env file
    python app.py
    ```
4.  **Setup Frontend:** (In a new terminal)
    ```bash
    cd frontend
    npm install
    npm run dev
    ```