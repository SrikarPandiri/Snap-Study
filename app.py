import json
import asyncio

import streamlit as st

from google import genai
from google.genai import types

from telegram import Bot

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    TRANSLATION_PROMPT,
    SUMMARY_PROMPT,
    FLASHCARD_PROMPT,
    QUIZ_PROMPT,
    STUDY_MODE_PROMPT,
    TELEGRAM_SUMMARY_PROMPT,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Snap & Study",
    page_icon="📸",
    layout="centered",
)


# =========================================================
# GEMINI CLIENT
# =========================================================

@st.cache_resource
def get_gemini_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )


gemini_client = get_gemini_client()


# =========================================================
# TELEGRAM CONFIGURATION
# =========================================================

TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]


def send_telegram(chat_id, text):
    """
    Send a text message to a Telegram chat.
    """

    bot = Bot(
        token=TELEGRAM_BOT_TOKEN
    )

    asyncio.run(
        bot.send_message(
            chat_id=chat_id,
            text=text
        )
    )


# =========================================================
# SESSION STATE
# =========================================================

if "name" not in st.session_state:
    st.session_state.name = None

if "telegram_chat_id" not in st.session_state:
    st.session_state.telegram_chat_id = None

if "chat" not in st.session_state:
    st.session_state.chat = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "onboarded" not in st.session_state:
    st.session_state.onboarded = False


# =========================================================
# CREATE GEMINI CHAT
# =========================================================

def create_chat():
    """
    Create a new persistent Gemini conversation.
    """

    return gemini_client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )
    )


# =========================================================
# ONBOARDING
# =========================================================

if not st.session_state.onboarded:

    st.title("📸 Snap & Study")

    st.subheader(
        "Your AI study & translation buddy"
    )

    st.write(
        "Snap a photo, upload study material, or paste text "
        "and start learning."
    )

    # -----------------------------------------------------
    # NAME
    # -----------------------------------------------------

    name = st.text_input(
        "What should I call you?",
        placeholder="Enter your name"
    )

    # -----------------------------------------------------
    # TELEGRAM CHAT ID
    # -----------------------------------------------------

    telegram_chat_id = st.text_input(
        "Telegram Chat ID",
        placeholder="Enter your Telegram Chat ID"
    )

    st.caption(
        "Your Telegram Chat ID is required to receive "
        "study summaries on Telegram."
    )

    # -----------------------------------------------------
    # START LEARNING
    # -----------------------------------------------------

    if st.button(
        "Start Learning 🚀",
        use_container_width=True
    ):

        # Validate name
        if not name.strip():

            st.warning(
                "Please enter your name."
            )

            st.stop()

        # Validate Telegram Chat ID
        if not telegram_chat_id.strip():

            st.warning(
                "Please enter your Telegram Chat ID."
            )

            st.stop()

        # Save name
        st.session_state.name = name.strip()

        # Save Telegram Chat ID
        st.session_state.telegram_chat_id = (
            telegram_chat_id.strip()
        )

        # Create Gemini conversation
        st.session_state.chat = create_chat()

        # Create welcome message
        welcome_message = (
            WELCOME_MESSAGE_TEMPLATE.format(
                name=st.session_state.name
            )
        )

        # Save welcome message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": welcome_message,
            }
        )

        # Mark onboarding as complete
        st.session_state.onboarded = True

        # Reload application
        st.rerun()


# =========================================================
# MAIN APPLICATION
# =========================================================

st.title("📸 Snap & Study")

st.caption(
    "Snap → Extract → Translate → Understand → Study → Chat"
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📚 Study Tools")

    st.write(
        f"Welcome, **{st.session_state.name}**!"
    )

    st.divider()

    st.write("You can ask me to:")

    st.markdown(
        """
        - 📷 Read text from an image
        - 🌍 Translate text
        - 🧠 Explain concepts
        - 📝 Summarize notes
        - 🗂️ Create key points
        - 🃏 Create flashcards
        - ❓ Create quizzes
        - 🎓 Prepare for exams
        """
    )

    st.divider()

    # =====================================================
    # CLEAR CONVERSATION
    # =====================================================

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        # Clear displayed messages
        st.session_state.messages = []

        # Create a fresh Gemini conversation
        st.session_state.chat = create_chat()

        # Create new welcome message
        welcome_message = (
            WELCOME_MESSAGE_TEMPLATE.format(
                name=st.session_state.name
            )
        )

        # Add welcome message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": welcome_message,
            }
        )

        st.rerun()

    # =====================================================
    # TELEGRAM SUMMARY
    # =====================================================

    st.divider()

    st.subheader("📲 Telegram")

    st.caption(
        "Send a concise study summary of this conversation "
        "to your Telegram."
    )

    if st.button(
        "📲 Send Study Summary",
        use_container_width=True
    ):

        # Get current Gemini chat
        chat = st.session_state.chat

        # Check Gemini chat
        if chat is None:

            st.error(
                "Chat session is not initialized. "
                "Please refresh the page."
            )

            st.stop()

        # Check Telegram Chat ID
        if not st.session_state.telegram_chat_id:

            st.warning(
                "Telegram Chat ID is missing."
            )

            st.stop()

        # Create and send summary
        with st.spinner(
            "Creating your study summary..."
        ):

            try:

                # Ask Gemini to create summary
                summary_response = chat.send_message(
                    message=TELEGRAM_SUMMARY_PROMPT
                )

                telegram_summary = (
                    summary_response.text
                )

                # Send summary to Telegram
                send_telegram(
                    st.session_state.telegram_chat_id,
                    telegram_summary
                )

                st.success(
                    "Study summary sent to Telegram! 📲"
                )

            except Exception as e:

                st.error(
                    f"Could not send the Telegram summary: {e}"
                )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask anything about your study material...",
    accept_file=True,
    file_type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
)


# =========================================================
# HANDLE USER INPUT
# =========================================================

if user_input:

    # -----------------------------------------------------
    # GET TEXT
    # -----------------------------------------------------

    text = user_input.text

    # -----------------------------------------------------
    # GET IMAGE
    # -----------------------------------------------------

    uploaded_file = None

    if user_input.files:

        uploaded_file = user_input.files[0]

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        if text:

            st.markdown(text)

        if uploaded_file:

            st.image(
                uploaded_file,
                caption="Uploaded study material",
                use_container_width=True
            )

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    display_message = text

    if uploaded_file:

        if display_message:

            display_message += (
                "\n\n📷 Uploaded an image"
            )

        else:

            display_message = (
                "📷 Uploaded an image"
            )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": display_message,
        }
    )

    # -----------------------------------------------------
    # BUILD GEMINI CONTENT
    # -----------------------------------------------------

    contents = []

    # Add text
    if text:

        contents.append(text)

    # Add image
    if uploaded_file:

        image_bytes = uploaded_file.getvalue()

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=uploaded_file.type
        )

        contents.append(image_part)

    # -----------------------------------------------------
    # SEND CONTENT TO GEMINI
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                # Get current Gemini chat
                chat = st.session_state.chat

                # Safety check
                if chat is None:

                    st.error(
                        "Chat session is not initialized. "
                        "Please refresh the page."
                    )

                    st.stop()

                # Send message/image to Gemini
                response = chat.send_message(
                    message=contents
                )

                # Get AI response
                assistant_response = response.text

                # Display AI response
                st.markdown(
                    assistant_response
                )

            except Exception as e:

                assistant_response = (
                    "Sorry, something went wrong while "
                    "processing your request. Please try again."
                )

                st.error(
                    str(e)
                )

    # -----------------------------------------------------
    # SAVE ASSISTANT RESPONSE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response,
        }
    )