<template>
  <div id="app">
    <header>
      <h1>AI Interview Coach</h1>
    </header>
    <main>
      <!-- Interview Practice Section -->
      <div class="interview-container">
        <h2>Your Question:</h2>
        <p class="question">{{ question }}</p>
        <button @click="toggleRecording" :class="{ 'is-recording': isRecording }">
          {{ isRecording ? 'Stop Recording' : 'Start Answering' }}
        </button>
        <div v-if="transcript" class="transcript-container">
          <h3>Your Answer:</h3>
          <p>{{ transcript }}</p>
        </div>
        <button @click="submitForFeedback" :disabled="!transcript || isSubmitting">
          {{ isSubmitting ? 'Analyzing...' : 'Get Feedback' }}
        </button>
      </div>

      <!-- Feedback Section -->
      <div v-if="feedback" class="feedback-container">
        <h3>AI Feedback:</h3>
        <p v-html="formattedFeedback"></p> <!-- Use v-html for line breaks -->
      </div>

      <!-- NEW: History Section -->
      <div class="history-container" v-if="history.length > 0">
        <h2>Your Practice History</h2>
        <ul>
          <li v-for="item in history" :key="item.id" class="history-item">
            <p><strong>Question:</strong> {{ item.question }}</p>
            <p><strong>Your Answer:</strong> {{ item.answer }}</p>
            <p><strong>AI Feedback:</strong> {{ item.feedback }}</p>
            <small>{{ new Date(item.timestamp).toLocaleString() }}</small>
          </li>
        </ul>
      </div>
    </main>
  </div>
</template>

<script>
import axios from 'axios';
let recognition;

export default {
  name: 'App',
  data() {
    return {
      question: 'Loading your question...',
      isRecording: false,
      transcript: '',
      feedback: '',
      isSubmitting: false,
      history: []
    };
  },
  // The computed property needs a comma after its closing brace
  computed: {
    formattedFeedback() {
      // Replace newline characters with <br> tags to render them in HTML
      return this.feedback.replace(/\n/g, '<br />');
    }
  },
  // The methods object contains all our functions
  methods: {
    async fetchQuestion() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/question');
        this.question = response.data.text;
      } catch (error) {
        console.error("There was an error fetching the question:", error);
        this.question = 'Failed to load a question. Please try again later.';
      }
    }, // <-- Comma needed between methods

    toggleRecording() {
      if (this.isRecording) {
        recognition.stop();
      } else {
        this.startRecording();
      }
    }, // <-- Comma needed between methods

    startRecording() {
      this.transcript = '';
      this.feedback = '';

      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        alert("Sorry, your browser does not support Speech Recognition.");
        return;
      }

      recognition = new SpeechRecognition();
      recognition.lang = 'en-US';
      recognition.interimResults = true;
      recognition.continuous = true;

      recognition.onstart = () => { this.isRecording = true; };
      recognition.onend = () => { this.isRecording = false; };
      recognition.onerror = (event) => { console.error("Speech recognition error:", event.error); this.isRecording = false; };

      recognition.onresult = (event) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        this.transcript = finalTranscript;
      };

      recognition.start();
    }, // <-- Comma needed between methods

    async submitForFeedback() {
      if (!this.transcript) {
        alert("Please provide an answer first.");
        return;
      }
      this.isSubmitting = true;
      this.feedback = '';

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/feedback', {
          question: this.question,
          answer: this.transcript
        });

        this.feedback = response.data.feedback || `Error: ${response.data.error}`;
        // After getting feedback, refresh the history list
        await this.fetchHistory();

      } catch (error) {
        console.error("Error fetching feedback:", error);
        this.feedback = "Sorry, an error occurred while getting your feedback.";
      } finally {
        this.isSubmitting = false;
      }
    }, // <-- Comma needed between methods

    async fetchHistory() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/history');
        this.history = response.data;
      } catch (error) {
        console.error("Error fetching history:", error);
      }
    }
  },
  // The created hook runs when the component is first loaded
  created() {
    this.fetchQuestion();
    this.fetchHistory();
  }
};
</script>

<style>
  /* ... Your existing styles ... */
  /* NEW/UPDATED Styles for History */
  .feedback-container p {
    white-space: pre-wrap; /* Helps preserve formatting from AI */
  }
  .history-container {
    max-width: 700px;
    margin: 40px auto;
    text-align: left;
  }
  .history-container h2 {
    text-align: center;
  }
  .history-container ul {
    list-style-type: none;
    padding: 0;
  }
  .history-item {
    background-color: #f8f9fa;
    border: 1px solid #dfe1e5;
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 15px;
  }
  .history-item p {
    margin: 5px 0;
  }
  .history-item small {
    color: #5f6368;
  }
</style>