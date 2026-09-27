# Stealth AI Overlay 👻🤖

A sleek, semi-transparent desktop AI assistant built with Python and Tkinter, powered by the **Google Gemini API**. It features **Windows Anti-Screen-Capture Protection** (making the app invisible to screen sharing/recording software like OBS, Discord, or Zoom) and **Voice Recognition** for hands-free interactions.

---

## ✨ Features

- 🔒 **Screen Capture Protection**: Uses native Windows API (`SetWindowDisplayAffinity`) to keep the window hidden from screenshots, screen recorders, and screen-sharing tools.
- 🤖 **Gemini AI Integration**: Uses the `gemini-3.1-flash-lite` model for fast and accurate assistant responses.
- 🎤 **Voice Command Support**: Speech recognition integrated with background threading so the UI remains smooth and responsive.
- 📐 **Dynamic Resizing**: Automatically calculates and resizes the window height depending on the length of the AI's response.
- 🎨 **Minimalist Semi-Transparent Overlay**: High-contrast, transparent black background designed to blend seamlessly into your desktop.

---

## 📁 Repository Structure

```text
├── main.py          # Core GUI application, audio handling, and window protection logic
├── gemini.py        # Gemini API client wrapper & response handler
├── mic-finder.py    # Helper utility to identify available microphone device indices
├── .env             # Environment file storing secret keys (Create one for yourself)
└── README.md        # Project documentation
```

---

## 🛠️ Prerequisites

- **Operating System**: Windows OS (Required for the `SetWindowDisplayAffinity` Win32 API function).
- **Python**: Python 3.9 or higher.
- **API Key**: A Google Gemini API key (from [Google AI Studio](https://aistudio.google.com/)).

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/GWSuryaYT/Hidden-Overlay.git
cd Hidden Overlay
```

### 2. Install Dependencies
Install all required libraries via `pip`:

```bash
pip install google-genai python-dotenv SpeechRecognition PyAudio
```
*(Note: If `PyAudio` installation fails on Windows, try `pip install pipwin` followed by `pipwin install pyaudio`)*

### 3. Environment Configuration
Create a `.env` file in the root directory and add your Gemini API key:

```env
GEMINI_KEY=your_actual_gemini_api_key_here
```

### 4. Configure Your Microphone
Run the microphone finder script to see all input devices and their respective indices:

```bash
python mic-finder.py
```

Look for your microphone in the printed list and copy its index number. Then open `main.py`, find `mic_index` inside the `speech_thread_worker` function, and set it to your device index:

```python
# main.py
def speech_thread_worker():
    mic_index = 2  # Replace '2' with your microphone index
```

---

## 🚀 Usage

Run the main script to launch the overlay:

```bash
python main.py
```

### Interacting with the Assistant:
- **Text Queries**: Type your prompt into the bottom text entry box and click **Send**.
- **Voice Queries**: Click **Mic**. The app will adjust for ambient noise, listen for your voice, transcribe the input into the entry box, and display it for review.
- **Anti-Capture**: Uncomment the line `# root.after(150, apply_protection)` in `main.py` if you want screen capture protection active automatically upon startup.

---

## ⚠️ Disclaimer

This tool utilizes Windows Native API calls (`user32.dll`) to exclude the window handle from display captures (`WDA_EXCLUDEFROMCAPTURE`). This is designed for privacy and utility purposes. Ensure you comply with all relevant platform guidelines when using screen capture modifications.