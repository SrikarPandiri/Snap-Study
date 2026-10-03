# 📸 Snap & Study

> AI-powered study and translation assistant that turns photos, notes, and questions into understandable learning material.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

Snap & Study is an AI-powered study and translation assistant that helps students turn photos, notes, and questions into understandable learning material. Users can upload an image or paste study material, extract and translate text, get simplified explanations and summaries, generate flashcards and quizzes, and send study summaries to Telegram.

## 🚀 Live Demo

👉 **https://snapstudyai.streamlit.app/**

## 📸 Screenshots

### Home

![Snap & Study Home](screenshots/home.png)

### Image Analysis

![Image Analysis](screenshots/image-analysis.png)

### AI Study Assistant

![Study Chat](screenshots/study-chat.png)

### Telegram Summary

![Telegram Summary](screenshots/telegram-summary.png)

## ✨ Features

- 📷 Extract and understand text from images
- 🌍 Translate text
- 🧠 Explain difficult concepts
- 📝 Summarize study material
- 📌 Generate key points
- 🃏 Create flashcards
- ❓ Generate quizzes
- 🎓 Exam preparation
- 💬 Chat with study material
- 📲 Send study summaries to Telegram

## 🛠️ Tech Stack

- **Python**: core language
- **Streamlit**: web interface and deployment
- **Google Gemini API**: image understanding, translation, explanation, summarization, flashcards, and quizzes
- **Telegram Bot API**: delivering study summaries to Telegram

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ├── Text Input
 ├── Image Upload
 └── Study Tools
 │
 ▼
Google Gemini API
 │
 ├── Image Understanding
 ├── Translation
 ├── Explanation
 ├── Summarization
 ├── Flashcards
 └── Quiz Generation
 │
 ▼
Telegram Bot API
 │
 ▼
Study Summary
```

## 📂 Project Structure

```text
Snap-Study/
├── app.py              # Streamlit app and UI logic
├── prompts.py          # Prompt templates for each study tool
├── requirements.txt    # Python dependencies
├── README.md
├── LICENSE
├── .gitignore
├── screenshots/        # Images used in this README
└── .streamlit/
    └── secrets.toml    # Local secrets (never committed)
```

## ⚙️ Local Setup

### Prerequisites

- Python 3.10 or newer
- A [Google Gemini API key](https://aistudio.google.com/app/apikey)
- A Telegram bot token from [@BotFather](https://t.me/BotFather) (only needed for the Telegram feature)

### 1. Clone the repository

```bash
git clone https://github.com/SrikarPandiri/Snap-Study.git
cd Snap-Study
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure secrets

Create the file `.streamlit/secrets.toml` and add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

> ⚠️ **Never commit this file to GitHub.** It is already excluded through `.gitignore`.

### 6. Run the application

```bash
streamlit run app.py
```

The application will open at:

```text
http://localhost:8501
```

## 📲 Using the Telegram Feature

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the bot token into your secrets.
2. Send any message to your new bot so it can reach you.
3. Find your numeric **Chat ID** (for example, with a bot like @userinfobot).
4. Enter the Chat ID in the app, then send a study summary to Telegram.

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

Live application: https://snapstudyai.streamlit.app/

To deploy your own copy:

1. Fork this repository.
2. Create a new app on [Streamlit Community Cloud](https://streamlit.io/cloud) and point it to `app.py`.
3. In **App settings → Secrets**, add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
```

## 🔐 Security

API keys and bot tokens are stored using Streamlit secrets and are not included in the repository. If a key is ever exposed, revoke it immediately and generate a new one.

## ⚠️ Limitations

- AI responses depend on the availability of the Gemini API.
- Image quality can affect text extraction accuracy.
- Very large study materials may require processing in smaller sections.
- Telegram summaries require a valid Telegram Chat ID.
- API usage may be subject to provider limits and temporary availability.

### Troubleshooting: `503 UNAVAILABLE`

If you see a `503 UNAVAILABLE` error, the Gemini model is temporarily overloaded on Google's side. This is not a problem with the app or your API key. Wait a few moments and try again, or retry with a shorter input.

## 🔮 Future Improvements

- 📚 PDF and document processing
- 🗂️ Saved study sessions
- 📊 Learning progress dashboard
- 🔐 User authentication
- 🧠 Personalized learning paths
- 🎯 Adaptive quizzes
- 📈 Performance tracking
- 🌐 More translation languages
- 📱 Improved mobile experience

## 📌 Project Purpose

Snap & Study is designed to help students understand and revise learning material through AI-powered image understanding, translation, explanation, summarization, flashcards, quizzes, and conversational study assistance.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Srikar Pandiri**

GitHub: [@SrikarPandiri](https://github.com/SrikarPandiri)
