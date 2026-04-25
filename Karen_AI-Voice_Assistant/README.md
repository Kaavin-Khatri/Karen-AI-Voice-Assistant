# Karen AI: Your Advanced Virtual Assistant 🤖✨

Karen is a cutting-edge, personal AI voice assistant featuring a stunning, futuristic glassmorphic GUI. Built with **Python** and **Streamlit**, it integrates the power of **Google Gemini** for conversational intelligence and vision-based reasoning, providing a seamless and high-end user experience.

---

## 🌟 Visual Excellence
Karen features a "Sci-Fi HUD" inspired interface with:
- **Glassmorphism Design**: Frosted glass effects and subtle micro-animations.
- **Dynamic Reactor Core**: A glowing, pulsing visual indicator for the assistant's state.
- **Responsive Chat Bubbles**: Modern, intuitive conversation flow.
- **Dark Tech Theme**: A premium radial gradient background with grid overlays.

---

## 🚀 Key Features

### 🎙️ Intelligent Voice Interaction
- **Advanced Speech Recognition**: Accurately interprets voice commands using Google's speech-to-text.
- **High-Quality TTS**: Natural-sounding voice output powered by `edge-tts` with high-performance caching for instant responses.
- **Live Chat Mode**: Continuous listening mode for a hands-free experience.

### 🧠 AI & Vision Capabilities
- **Powered by Gemini**: Uses the latest Gemini 2.0 Flash models for smart, concise, and context-aware responses.
- **Vision AI (Camera)**: Can "see" through your webcam, describing surroundings or reading text from physical objects.
- **Screen Analysis**: Captures and analyzes your screen to identify errors, explain content, or read documents.
- **RAG (Document Analysis)**: "Search my documents" feature to answer questions based on your local files (PDF, TXT, MD, PY).

### 🛠️ Productivity & System Automation
- **Downloads Organizer**: Automatically sorts your `Downloads` folder into Images, Documents, Installers, and Archives.
- **To-Do Management**: Voice-controlled task list (add, list, clear).
- **System Control**: Launch/Close applications (Notepad, CMD, Edge), and manage system power (Shutdown, Sleep, Restart).
- **Media & Volume Control**: Integrated with Spotify and system media keys for volume and playback management.

### 🌐 Web & Utilities
- **YouTube Integration**: Search, play, and even download videos directly.
- **Tech News & Weather**: Stay updated with the latest tech headlines and local weather reports.
- **System Diagnostics**: Check internet speed and battery status with a single voice command.

---

## 📂 Project Modules & Functions

| Module | Functionality |
| :--- | :--- |
| `karen.py` | The heart of the assistant. Handles command processing, AI integration, and feature logic. |
| `streamlit_app.py` | The main GUI entry point. Provides the futuristic web interface and real-time UI updates. |
| `tts.py` | Custom Text-to-Speech engine utilizing `edge-tts` for high-fidelity audio. |
| `Myalarm.py` | Dedicated module for managing alarms and timers. |
| `sd_microphone.py` | Optimizes sound device input for better recognition accuracy. |
| `requirements.txt` | List of all Python dependencies required to run the project. |

---

## 🛠️ Installation Guide

### 1. Prerequisites
- Python 3.9 or higher
- A Google Gemini API Key ([Get it here](https://aistudio.google.com/))

### 2. Clone the Repository
```bash
git clone https://github.com/Kaavin-Khatri/Karen-AI-Voice-Assistant.git
cd Karen-AI-Voice-Assistant
```

### 3. Install Dependencies
```bash
pip install -r "Karen AI-Voice Assistant/requirements.txt"
```

### 4. Configuration
Create a file named `gemini_api_key.txt` in this folder and paste your Gemini API key there.

---

## 🎮 How to Run

Launch the Streamlit app from this directory:

```bash
streamlit run streamlit_app.py
```

Once launched, you can interact with Karen via the **chat input** or by clicking the **🎤 Speak** button.

---

## 📜 Voice Commands Examples
- *"Hey Karen, what do you see?"* (Opens camera and describes surroundings)
- *"Organize my downloads"* (Cleans up your Downloads folder)
- *"What is on my screen?"* (Analyzes current screen content)
- *"Play some lo-fi music"* (Plays music on YouTube)
- *"Add 'Buy groceries' to my to-do list"*
- *"Check my internet speed"*

---

## 🤝 Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to open a Pull Request.

## 📄 License
This project is licensed under the MIT License.
