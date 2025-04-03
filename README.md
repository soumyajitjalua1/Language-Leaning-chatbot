# 🌍 Language Learning Chatbot

A conversational AI-powered language learning assistant that helps users practice their language skills through realistic conversations and provides immediate feedback on mistakes.

![Language Learning Chatbot Architecture](https://github.com/soumyajitjalua1/Language-Leaning-chatbot/blob/main/Screenshot%202025-04-03%20162942.png)

## 📋 Features

- **Personalized Language Learning:** Practice in your target language with conversations tailored to your proficiency level
- **Real-time Corrections:** Get immediate feedback on your mistakes with explanations
- **Realistic Scenarios:** Practice language in real-world contexts like restaurants, shopping, or job interviews
- **Session Summaries:** Receive a detailed summary of your session with grouped mistakes and improvement suggestions
- **Progress Tracking:** All sessions and corrections are stored to help you track your improvement over time

## 🛠️ Technologies Used

- **Frontend & Backend:** Streamlit
- **Language Model:** OpenAI GPT-4
- **Framework:** LangChain
- **Database:** SQLite
- **Language Processing:** Regular expressions for error detection

# 🚀 Getting Started
## Prerequisites

Python 3.8+
OpenAI API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/language-learning-chatbot.git
cd language-learning-chatbot
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a **.env** file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your-api-key-here
```

## Running the Application
Run the Streamlit app:
```bash
streamlit run app.py
```
The application will be available at **http://localhost:8501**
## 📱 Usage

1. Start a New Session:

- Select your native language
- Choose the language you want to learn
- Set your proficiency level
- Pick a conversation scenario

2. Practice Your Language Skills:

- Engage in a natural conversation with the AI tutor
- Receive gentle corrections when you make mistakes
- Learn proper phrasing and grammar in context

3. Review Your Session:

- End the conversation to see a summary of your mistakes
- Get personalized suggestions for improvement
- Start a new session with a different scenario

📂 Project Structure
```
language-learning-chatbot/
├── app.py # Main Streamlit application
├── chatbot.py # Language learning bot implementation
├── database.py # Database operations
├── language_bot.db # SQLite database
├── .env # Environment variables
└── README.md # Project documentation
```



## 💻 Key Components
### 1. **app.py** 
The main Streamlit application that handles the user interface, session management, and coordinates between the database and chatbot components.
### 2. chatbot.py
Contains the LanguageLearningBot class that manages conversations, analyzes responses for mistakes, and generates session summaries using LangChain and OpenAI.
### 3. database.py
Provides functions for database initialization, session creation/tracking, and mistake recording.
### 🔄 How It Works

### 1. **Session Initialization:**

- User provides language preferences and selects a scenario
- System creates a new session in the database
- The chatbot configures a specialized prompt based on user parameters

### 2. **Conversation Flow:**

- User sends messages in their learning language
- AI responds in the learning language and identifies mistakes
- Corrections are formatted with [Correction] tags and explanations
- Mistakes are analyzed and stored in the database

### 3. **Session Summary:**

- When the user ends the session, the system analyzes all mistakes
- Mistakes are grouped by type (grammar, vocabulary, etc.)
- The AI generates personalized improvement suggestions
- A comprehensive summary is displayed to the user

## 🛣️ Future Improvements

- Voice recognition and pronunciation feedback
- Custom lesson plans based on common mistakes
- Multiple language tutors with different teaching styles
- Spaced repetition system for previously corrected mistakes
- Export functionality for review materials
- Progress visualization dashboards

## 🔒 Privacy Note
All conversation data and mistakes are stored locally in the SQLite database. No data is sent to external servers except for the conversation content sent to OpenAI's API.
## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
##🙏 Acknowledgements
- OpenAI for providing the GPT-4 API
- LangChain for the conversation framework
- Streamlit for the easy-to-use web application framework


**Created with ❤️ for language learners worldwide**


