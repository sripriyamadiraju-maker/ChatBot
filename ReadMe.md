# Streamlit Persona ChatBot with Hugging Face

A simple, interactive chatbot application built with Streamlit and powered by the Hugging Face `transformers` library. This chatbot features selectable personas, conversation memory, and a clean user interface.



## Features

-   **Interactive UI**: A clean and user-friendly chat interface built with Streamlit.
-   **Selectable Personas**: Choose from multiple bot personalities in the sidebar:
    -   **RoastBot**: Responds with witty and sarcastic roasts.
    -   **ShakespeareBot**: Answers in dramatic, Old-English prose.
    -   **Emoji Translator Bot**: Converts your messages into emoji-speak.
    -   **MusicBot**: Suggests comical background music for any situation and **plays a sample of the song** directly in the chat!
-   **Conversation Memory**: The bot remembers the context of the current conversation.
-   **Easy to Run**: Get the chatbot running locally with just a few commands.

---

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

-   Python 3.8+
-   `pip` (Python package installer)
-   **FFmpeg** (optional but highly recommended): `yt-dlp` works best with FFmpeg installed on your system. You can download it from [ffmpeg.org](https://ffmpeg.org/download.html) or install it via a package manager like Homebrew (`brew install ffmpeg`) or Chocolatey (`choco install ffmpeg`).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/persona-chatbot.git](https://github.com/your-username/persona-chatbot.git)
    cd persona-chatbot
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## How to Run

Once the installation is complete, run the following command in your terminal:

```bash
streamlit run app.py
```

Your web browser should automatically open a new tab with the running application.

---

## How It Works

-   **Frontend**: **Streamlit** is used to create the web-based user interface.
-   **Backend (AI)**: **Hugging Face's `transformers` library** provides the pre-trained conversational model (`microsoft/DialoGPT-medium`).
-   **State Management**: **Streamlit's `st.session_state`** stores the conversation history, giving the chatbot memory.
-   **Music Playback**: When the **MusicBot** persona is active, the app parses the suggested song title, uses the **`yt-dlp`** library to find the song on YouTube, and streams the audio using Streamlit's native `st.audio` component.