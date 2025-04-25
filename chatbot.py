import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import pyttsx3
import speech_recognition as sr
from PIL import Image, ImageTk, ImageSequence
from datetime import datetime
import time
import os
import json
import requests
import wikipedia
import threading

# -------------------- API KEYS --------------------
GEMINI_API_KEY = "AIzaSyAYXBHmFuvsOzFDMw_FR3Kl-r0mrNNUc70"
OPENWEATHER_API_KEY = "995bf5575b93308e2484367e4a9e6f16"

# -------------------- Initialize Speech Engine --------------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)

# -------------------- Global Variables --------------------
dark_mode = True
chat_history = []
weather_cache = {}
frame_index = 0
frames = []

# -------------------- Gemini API --------------------
def get_gemini_reply(question):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": question}]}]}

        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if response.status_code == 200 and "candidates" in data:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return "🤖 No valid response from Gemini."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return "🤖 Error connecting to Gemini server."

# -------------------- Weather API --------------------
def get_weather(city):
    if city in weather_cache and (time.time() - weather_cache[city]['timestamp'] < 600):
        return weather_cache[city]['data']

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = (
                f"🌦️ {data['weather'][0]['description'].capitalize()} | "
                f"🌡️ {data['main']['temp']}°C | "
                f"💨 {data['wind']['speed']} m/s"
            )
            weather_cache[city] = {'data': weather, 'timestamp': time.time()}
            return weather
        else:
            return "🌥️ Couldn't fetch weather data."
    except Exception as e:
        print(f"Weather API Error: {e}")
        return "❌ Weather service unavailable."

# -------------------- Wikipedia Search --------------------
def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        return "🔍 No results found on Wikipedia."

# -------------------- Voice Output in Thread --------------------
def speak(reply):
    """Plays the bot's response using a separate thread."""
    def run():
        engine.say(reply)
        engine.runAndWait()

    threading.Thread(target=run).start()

# -------------------- Chat Functionality --------------------
def send_message():
    user_input = entry.get().strip()
    if not user_input:
        return

    timestamp = datetime.now().strftime("%H:%M:%S")
    chat_history.append(f"[{timestamp}] You: {user_input}")
    chat_window.insert(tk.END, f"[{timestamp}] You: {user_input}\n", "user")

    chat_window.insert(tk.END, f"[{timestamp}] VRA: Typing...\n", "bot")
    chat_window.see(tk.END)
    root.update_idletasks()
    time.sleep(0.5)

    # Handle commands
    if user_input.lower().startswith("weather"):
        city = user_input.split(" ", 1)[-1]
        reply = get_weather(city)
    elif user_input.lower().startswith("wiki"):
        query = user_input.split(" ", 1)[-1]
        reply = search_wikipedia(query)
    else:
        reply = get_gemini_reply(user_input)

    chat_history.append(f"[{timestamp}] VRA: {reply}")
    chat_window.insert(tk.END, f"[{timestamp}] VRA: {reply}\n", "bot")
    
    # Simultaneous voice output
    speak(reply)

    entry.delete(0, tk.END)
    chat_window.see(tk.END)

# -------------------- Voice Input --------------------
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_window.insert(tk.END, "🎤 Listening...\n", "bot")
        root.update_idletasks()
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            entry.insert(0, text)
        except sr.UnknownValueError:
            chat_window.insert(tk.END, "🤖 Couldn't understand you.\n", "bot")
        except sr.RequestError:
            chat_window.insert(tk.END, "❌ Speech service error.\n", "bot")

# -------------------- Save Chat --------------------
def save_chat():
    with open("chat_history.json", "w") as file:
        json.dump(chat_history, file)
    messagebox.showinfo("Saved", "Chat saved successfully!")

# -------------------- Theme Toggle --------------------
def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    colors = {
        "bg": "#2E2E2E" if dark_mode else "#F0F0F0",
        "fg": "#00FF00" if dark_mode else "#000000",
        "entry_bg": "#1C2526" if dark_mode else "#FFFFFF",
        "btn_bg": "#00FF00" if dark_mode else "#0057D9",
        "btn_fg": "#000000" if dark_mode else "#FFFFFF"
    }

    root.configure(bg=colors["bg"])
    chat_window.configure(bg=colors["bg"], fg=colors["fg"])
    entry.configure(bg=colors["entry_bg"], fg=colors["fg"])

    for btn in [send_btn, voice_btn, save_btn, theme_btn]:
        btn.configure(bg=colors["btn_bg"], fg=colors["btn_fg"])

# -------------------- Robot GIF Animation --------------------
def animate_gif():
    global frame_index
    frame_index = (frame_index + 1) % len(frames)
    image_label.configure(image=frames[frame_index])
    root.after(100, animate_gif)

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("Virtual Robot Assistant (VRA) - Stylish Version with GIF")
root.geometry("1100x900")
root.configure(bg="#2E2E2E")

# Load Robot GIF
gif = Image.open("robot.gif")
frames = [ImageTk.PhotoImage(frame.resize((200, 200))) for frame in ImageSequence.Iterator(gif)]

# Display Robot GIF
image_label = tk.Label(root, bg="#2E2E2E")
image_label.pack(pady=10)
animate_gif()

# Chat Window
chat_window = tk.Text(root, height=20, width=100, bg="#1C2526", fg="#00FF00", font=("Courier", 14), bd=2, relief="solid")
chat_window.pack(pady=10)

# Input Box & Buttons
frame = tk.Frame(root, bg="#2E2E2E")
frame.pack(pady=10)

entry = tk.Entry(frame, width=70, bg="#1C2526", fg="#00FF00", font=("Courier", 12), bd=2, relief="solid")
entry.grid(row=0, column=0, padx=5)

send_btn = tk.Button(frame, text="Send", command=send_message, bg="#00FF00", fg="#000000", font=("Helvetica", 10, "bold"))
send_btn.grid(row=0, column=1, padx=5)

voice_btn = tk.Button(frame, text="🎤 Voice", command=voice_input, bg="#00FF00", fg="#000000")
voice_btn.grid(row=0, column=2, padx=5)

save_btn = tk.Button(frame, text="💾 Save", command=save_chat, bg="#00FF00", fg="#000000")
save_btn.grid(row=0, column=3, padx=5)

theme_btn = tk.Button(frame, text="🌙 Theme", command=toggle_theme, bg="#00FF00", fg="#000000")
theme_btn.grid(row=0, column=4, padx=5)

root.mainloop()