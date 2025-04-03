import os
import uuid
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import base64
import requests

# Import from our existing modules
from database import init_db, create_session, end_session
from chatbot import LanguageLearningBot

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")

# Function to add background image
def add_bg_from_url(image_url):
    try:
        response = requests.get(image_url)
        background_image = response.content
        background_image_b64 = base64.b64encode(background_image).decode()
        return f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{background_image_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stApp > header {{
            background-color: transparent;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            border-radius: 1rem;
            margin: 1rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }}
        .chat-message {{
            padding: 1.2rem;
            border-radius: 0.8rem;
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            word-wrap: break-word;
            overflow-wrap: break-word;
            width: 100%;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        .chat-message.user {{
            background-color: #DCF8C6;
        }}
        .chat-message.bot {{
            background-color: #E3F2FD;
        }}
        .chat-message .avatar {{
            min-width: 40px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            margin-right: 1rem;
            background-color: #ffffff;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }}
        .chat-message .message {{
            flex-grow: 1;
            overflow-wrap: break-word;
            word-break: break-word;
            max-width: calc(100% - 60px);
        }}
        .correction {{
            background-color: #FFEBEE;
            padding: 0.8rem;
            border-radius: 0.5rem;
            margin-top: 1rem;
            border-left: 4px solid #F44336;
        }}
        .stButton button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 4px;
            cursor: pointer;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .stButton button:hover {{
            background-color: #45a049;
        }}
        /* Improve form styling */
        .stForm {{
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }}
        /* Improve title and header styling */
        h1, h2, h3 {{
            color: #2E7D32;
        }}
        /* Improve chat input area */
        .stChatInputContainer {{
            padding-top: 10px;
            padding-bottom: 10px;
        }}
        </style>
        """
    except Exception as e:
        st.error(f"Error loading background image: {e}")
        return ""

# Initialize the app
def initialize_app():
    if 'bot' not in st.session_state:
        st.session_state.bot = LanguageLearningBot(OPENAI_API_KEY)
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'session_active' not in st.session_state:
        st.session_state.session_active = False
    
    if 'session_summary' not in st.session_state:
        st.session_state.session_summary = None
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())

# Initialize the database
init_db()

# UI Components
def render_message(message, is_user=False):
    if is_user:
        avatar = "👤"
        css_class = "user"
    else:
        avatar = "🤖"
        css_class = "bot"
        
    message_text = message
    correction_text = ""
    
    # Extract correction if present
    if not is_user and "[Correction]" in message:
        parts = message.split("[Correction]", 1)
        message_text = parts[0].strip()
        correction_text = parts[1].strip() if len(parts) > 1 else ""
    
    # Escape any HTML tags in the message content
    import html
    message_text = html.escape(message_text)
    correction_text = html.escape(correction_text)
    
    st.markdown(f"""
    <div class="chat-message {css_class}">
        <div class="avatar">{avatar}</div>
        <div class="message">
            {message_text}
            {f'<div class="correction"><strong>Correction:</strong> {correction_text}</div>' if correction_text else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_chat_interface():
    # Create a container for the chat messages
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            render_message(message['content'], message['role'] == 'user')
    
    # Chat input
    if st.session_state.session_active:
        user_input = st.chat_input("Type your message here...")
        if user_input:
            # Add user message to chat
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Get bot response
            with st.spinner("Thinking..."):
                response = st.session_state.bot.chain.predict(input=user_input)
                analyzed_response = st.session_state.bot.analyze_response(response)
            
            # Add bot response to chat
            st.session_state.messages.append({"role": "assistant", "content": analyzed_response})
            
            # Force the UI to refresh
            st.rerun()

def end_chat_session():
    if st.session_state.session_active:
        with st.spinner("Generating summary..."):
            # Generate summary
            summary = st.session_state.bot.generate_summary()
            st.session_state.session_summary = summary
            
            # End session in database
            end_session(st.session_state.bot.session_id)
            
            # Update session state
            st.session_state.session_active = False
        
        # Force the UI to refresh
        st.rerun()

# Main app
def main():
    # Initialize the app
    initialize_app()
    
    # Add background image
    st.markdown(add_bg_from_url("https://www.shutterstock.com/image-illustration/cloud-text-india-written-56-260nw-1712422855.jpg"), unsafe_allow_html=True)
    
    # App title with an emoji
    st.title("🌍 Language Learning Chatbot")
    
    # Setup flow
    if not st.session_state.session_active and st.session_state.session_summary is None:
        st.subheader("Welcome to your language learning assistant!")
        st.write("This chatbot will help you practice your language skills through conversation and provide feedback on your mistakes.")
        
        with st.form("setup_form"):
            st.subheader("Setup Your Learning Session")
            
            col1, col2 = st.columns(2)
            
            with col1:
                learning_language = st.text_input("What language do you want to learn?")
                native_language = st.text_input("What is your native language?")
                
            with col2:
                proficiency_level = st.selectbox(
                    "What is your current level?",
                    ["beginner", "intermediate", "advanced"]
                )
                
                scene = st.selectbox(
                    "Choose a conversation scenario",
                    [
                        "At a restaurant ordering food",
                        "Meeting someone new at a party",
                        "Shopping for clothes at a store",
                        "Asking for directions in a new city",
                        "Job interview practice"
                    ]
                )
            
            submitted = st.form_submit_button("Start Conversation")
            
            if submitted:
                if not learning_language or not native_language:
                    st.error("Please fill in all required fields")
                else:
                    # Set chatbot properties
                    st.session_state.bot.native_language = native_language
                    st.session_state.bot.learning_language = learning_language
                    st.session_state.bot.proficiency_level = proficiency_level
                    
                    # Create a session in the database
                    session_id = create_session(
                        st.session_state.user_id,
                        native_language,
                        learning_language,
                        proficiency_level
                    )
                    st.session_state.bot.session_id = session_id
                    
                    # Setup the conversation chain
                    with st.spinner("Setting up your conversation..."):
                        st.session_state.bot.setup_chain(scene)
                    
                        # Start the conversation with a message from the bot
                        response = st.session_state.bot.chain.predict(input="Let's start our conversation")
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Set session as active
                    st.session_state.session_active = True
                    
                    # Force the UI to refresh
                    st.rerun()
    
    # Active chat session
    elif st.session_state.session_active:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.subheader("Let's practice your language skills!")
        with col2:
            if st.button("End Conversation"):
                end_chat_session()
        
        # Display chat interface
        display_chat_interface()
    
    # Display summary
    elif st.session_state.session_summary is not None:
        st.subheader("Session Summary")
        st.markdown(st.session_state.session_summary)
        
        # Start new session button
        if st.button("Start a New Conversation"):
            # Reset session state
            st.session_state.bot = LanguageLearningBot(OPENAI_API_KEY)
            st.session_state.messages = []
            st.session_state.session_active = False
            st.session_state.session_summary = None
            st.session_state.user_id = str(uuid.uuid4())
            
            # Force the UI to refresh
            st.rerun()
    
    # Footer with improved styling
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px; margin-top: 20px;'>
        <hr>
        <p>🤖 Powered by OpenAI and LangChain | Made with ❤️ for language learners</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()