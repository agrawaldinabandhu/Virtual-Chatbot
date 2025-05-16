# 🤖 Virtual Robot Assistant (VRA)

A voice and text-based intelligent assistant with a stylish GUI, capable of chatting, answering general questions via Google Gemini API, fetching live weather info, and retrieving Wikipedia summaries — all in real-time using a dynamic robot-themed interface.

---

## 🧠 Features

- 🎙️ Voice Recognition (via microphone)
- 💬 Chat-based interaction with Gemini AI
- 🌤️ Real-time Weather Info (OpenWeather API)
- 📚 Wikipedia Search
- 🗃️ Save chat history to file
- 🌗 Light/Dark Theme toggle
- 🖼️ Animated Robot GIF in UI

---

## 📦 Tech Stack

- **Python** 3.x
- **Tkinter** – GUI
- **SpeechRecognition** – Voice input
- **pyttsx3** – Text-to-speech
- **Wikipedia** – Knowledge base
- **Requests** – API communication
- **PIL (Pillow)** – GIF animation

---

## 🔧 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/virtual-robot-assistant.git
   cd virtual-robot-assistant

2. Install Required Libraries (cmd or bash)
  * pip install -r requirements.txt
/ If requirements.txt is not available, manually install:
  * pip install pyttsx3 SpeechRecognition wikipedia requests pillow

3. Add Required Files
 * Place a robot GIF named robot.gif in the root folder (for animated assistant).
 * Ensure you have a working microphone for voice input.

4. Add Your API Keys
 * Open the .py file and replace with:
     GEMINI_API_KEY = "your-gemini-api-key"
     OPENWEATHER_API_KEY = "your-openweather-api-key"

5. Running the Assistant
    * python your_script_name.py
   
7. Usage
 *Type or speak your queries (click 🎤 Voice)
 *Ask for weather:

8. Saving the chat:
   *Click the 💾 Save button to store the chat history in a chat_history.json file.

# A Screenshot of the Interface:
![Screenshot (1)](https://github.com/user-attachments/assets/71709032-0099-461d-ba21-0fd5f07069fa)

# License
This project is open-source and free to use for educational purposes.

