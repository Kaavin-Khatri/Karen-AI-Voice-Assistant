import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import random
import pywhatkit
import pyjokes
import cv2
from requests import get
import pyautogui
import Myalarm
import threading
import sys
import time
# import google.generativeai as genai # REMOVED: Deprecated
from google import genai
from google.genai import types
import json
import shutil
try:
    from sd_microphone import SoundDeviceMicrophone
except ImportError:
    print("sd_microphone.py not found or failed to import.")
    SoundDeviceMicrophone = None

# Optional dependencies - fail gracefully if not installed
try:
    import psutil
except ImportError:
    psutil = None

try:
    import speedtest
except ImportError:
    speedtest = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    from gnews import GNews
except ImportError:
    GNews = None

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        PdfReader = None

# GenAI Config
genai_client = None

# Try execution folder first
KEY_FILE = "gemini_api_key.txt"

def load_key_from_file():
    if os.path.exists(KEY_FILE):
        try:
            with open(KEY_FILE, "r") as f:
                key = f.read().strip()
                if key and "PASTE_YOUR_GEMINI_API_KEY_HERE" not in key:
                    return key
        except Exception as e:
            print(f"Error reading key file: {e}")
    return None

def configure_genai(api_key=None):
    global genai_client
    
    # If no key passed, try loading from file
    if not api_key:
        api_key = load_key_from_file()
        
    if api_key:
        try:
            genai_client = genai.Client(api_key=api_key)
            print("GenAI Configured Successfully (New SDK)")
        except Exception as e:
            print(f"GenAI Config Error: {e}")

def ask_genai(query):
    if not genai_client:
        return "I am not connected to my brain (API Key missing)."
    
    # List of common models to try first
    # PRIORITY: High Quota / Low Latency models first
    models_to_try = [
        'gemini-2.0-flash-lite',     # Often has separate quota
        'gemini-2.0-flash',          # Standard
        'gemini-2.5-flash',          # Newer Stable
        'gemini-flash-latest',       # Fallback to latest
        'gemini-2.0-flash-001',      # Specific version
    ]
    
    last_error = ""
    
    for model_name in models_to_try:
        try:
            response = genai_client.models.generate_content(
                model=model_name,
                contents=query + " (Answer concisely as a voice assistant named Karen)"
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            last_error = error_msg
            print(f"Model {model_name} failed: {error_msg}")
            continue

    # If we get here, absolutely nothing worked
    return f"I couldn't find any working AI model. Last error: {last_error[:100]}..."


# # For Audio - Initialize globally but manage carefully
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 0.9)
    # engine.setProperty('voice', voices[1].id)
except Exception as e:
    print(f"Engine init failed: {e}")
    engine = None

# Global explicitly for module-level access
last_spoken = ""

# Global explicitly for module-level access
last_spoken = ""

import queue
try:
    import pythoncom
except ImportError:
    pythoncom = None

import subprocess

# --- Direct TTS Optimization with Caching ---
import asyncio
import edge_tts
import pygame
import hashlib
import os

# Initialize mixer once
try:
    pygame.mixer.init()
except:
    pass

VOICE = "en-US-AriaNeural"
CACHE_DIR = "tts_cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

async def _generate_and_play(text):
    try:
        # Create a hash of the text + voice to ensure uniqueness
        text_hash = hashlib.md5(f"{text}_{VOICE}".encode()).hexdigest()
        filename = os.path.join(CACHE_DIR, f"{text_hash}.mp3")
        
        # Check cache
        if not os.path.exists(filename):
             # Generate if not exists
             communicate = edge_tts.Communicate(text, VOICE)
             await communicate.save(filename)
        
        # Play
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        # Do not unload/remove, keep for cache
        # pygame.mixer.music.unload() 
        
    except Exception as e:
        print(f"TTS Error: {e}")

def _run_async_tts(text):
    try:
        asyncio.run(_generate_and_play(text))
    except Exception as e:
        print(f"Async TTS Wrapper Error: {e}")

def speak(audio):
    global last_spoken
    
    # meaningful audio only
    if not audio:
        return
        
    last_spoken = audio
    print(f"Karen: {audio}")
    
    # Sanitize text
    import re
    clean_audio = re.sub(r'[\-\*#_]+', '', audio)
    clean_audio = re.sub(r'\s+', ' ', clean_audio).strip()
    
    # Stop previous if playing
    if pygame.mixer.get_init():
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except:
            pass
            
    # Run in thread
    threading.Thread(target=_run_async_tts, args=(clean_audio,), daemon=True).start()

def stop_speaking():
    if pygame.mixer.get_init():
        try:
            pygame.mixer.music.stop()
        except:
            pass

def wait_until_done():
    # Wait for pygame to finish
    if pygame.mixer.get_init():
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


# To Wish
def wishMe():
    hour = int(datetime.datetime.now().hour)
    
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")
    speak("Hi Sir. I am Karen. Your Virtual Assistant. How may I help you")
    


# For Taking Command
def takeCommand():
    #It Takes Microphone input from the user and returns string output

    r = sr.Recognizer()
    with SoundDeviceMicrophone() as source:
        print("Listening...")
        # Adjust for background noise to prevent premature cutoffs
        r.adjust_for_ambient_noise(source, duration=1.0)
        r.pause_threshold = 3.0 # Wait 3 seconds of silence before processing
        r.energy_threshold = 300 # Lower threshold to pick up quieter voice
        r.dynamic_energy_threshold = True 
        try:
            # Listening for up to 30 seconds or until silence
            audio = r.listen(source, phrase_time_limit=30, timeout=10)
        except:
            return "None"

    try:
        #print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query


camera_open = False
cap = None
latest_frame = None

def camera_loop():
    global cap, camera_open, latest_frame
    import cv2
    while camera_open:
        if cap:
            ret, img = cap.read()
            if ret:
                # Fix inversion
                img = cv2.flip(img, 1)  # mirror horizontally
                
                # Convert to RGB for Streamlit (OpenCV is BGR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                latest_frame = img
                # Show in separate window for performance/stability
                cv2.imshow('Karen Camera', cv2.cvtColor(img, cv2.COLOR_RGB2BGR)) # Convert back to BGR for OpenCV
            else:
                 pass
        
        # maintain UI responsiveness
        if cv2.waitKey(1) & 0xFF == 27: # Esc to close
            camera_open = False
            break
            
        time.sleep(0.03) # ~30 FPS

    if cap:
        cap.release()
    cv2.destroyAllWindows()



# --- New Feature Helper Functions ---
def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = battery.power_plugged
        status = "plugged in" if plugged else "running on battery"
        return f"Battery is at {percent}% and {status}."
    return "Battery status unavailable."

def check_internet_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        down = st.download() / 10**6
        up = st.upload() / 10**6
        return f"Download speed is {down:.2f} Mbps and upload speed is {up:.2f} Mbps."
    except Exception as e:
        return f"Could not check speed: {e}"

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    return f"Screenshot saved as {filename}"

def organize_downloads():
    # Target Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(downloads_path):
        return "Downloads folder not found."
    
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
        "Installers": [".exe", ".msi"],
        "Archives": [".zip", ".rar", ".7z"]
    }
    
    moved_count = 0
    for filename in os.listdir(downloads_path):
        file_path = os.path.join(downloads_path, filename)
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            for folder, extensions in file_types.items():
                if ext in extensions:
                    target_folder = os.path.join(downloads_path, folder)
                    try:
                        os.makedirs(target_folder, exist_ok=True)
                        shutil.move(file_path, os.path.join(target_folder, filename))
                        moved_count += 1
                    except Exception as e:
                        print(f"Error moving {filename}: {e}")
                    break
    return f"Organized {moved_count} files in Downloads."

def get_news():
    try:
        google_news = GNews(max_results=5, period='1d')
        json_resp = google_news.get_news('Technology')
        news_list = []
        for entry in json_resp:
            title = entry.get('title', 'No title')
            news_list.append(title)
        
        if not news_list:
            return "I couldn't find any news right now."
            
        return "Here are the top tech headlines: " + ". ".join(news_list)
    except Exception as e:
        return f"Error getting news: {e}"

def get_weather(city="Mumbai"):
    try:
        # wttr.in returns a simple text representation
        # format=3 gives "Condition, Temp"
        url = f"https://wttr.in/{city}?format=3"
        response = get(url)
        if response.status_code == 200:
            return f"The weather in {city} is {response.text.strip()}"
        else:
            return "I couldn't get the weather data."
    except Exception as e:
        return f"Weather error: {e}"

def download_video(url):
    try:
        # Download to user's Videos folder
        save_path = os.path.join(os.path.expanduser("~"), "Videos")
        
        ydl_opts = {
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'video')
            filename = ydl.prepare_filename(info)
            
        return f"Downloaded '{title}' to your Videos folder."
    except Exception as e:
        # Fallback to just opening it if download fails (e.g. strict age limit)
        webbrowser.open(url)
        return f"I couldn't download it directly ({str(e)[:50]}...), so I opened it for you."

# Simple To-Do JSON
TODO_FILE = "todo_list.json"
def manage_todo(action, item=None):
    tasks = []
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
        except:
            tasks = []
            
    if action == "add" and item:
        tasks.append(item)
        with open(TODO_FILE, "w") as f:
            json.dump(tasks, f)
        return f"Added {item} to your list."
    
    elif action == "list":
        if not tasks:
            return "Your to-do list is empty."
        return "You have: " + ", ".join(tasks)
        
    elif action == "clear":
        if os.path.exists(TODO_FILE):
            os.remove(TODO_FILE)
            return "Cleared your to-do list."
        return "List is already empty."
        
    return "Unknown todo action."

def analyze_camera_frame(question="What do you see?"):
    global latest_frame, genai_client
    if not genai_client:
        return "I need my AI brain (Gemini) connected to see."
        
    if latest_frame is None:
        return "I can't see anything. Is the camera open?"
        
    try:
        # Convert numpy array (latest_frame is RGB from camera_loop) to PIL Image
        pil_img = Image.fromarray(latest_frame)
        
        models_to_try = ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-2.0-flash-lite']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                 response = genai_client.models.generate_content(
                     model=model_name,
                     contents=[question + " (Answer briefly)", pil_img]
                 )
                 return response.text
            except Exception as e:
                 last_error = f"{model_name} failed: {e}"
                 print(last_error)
                 continue
                 
        return f"Vision error (Used all models): {last_error}"
             
    except Exception as e:
        return f"Vision error: {e}"

def analyze_screen(question="What is on my screen?"):
    global genai_client
    if not genai_client:
        return "I need my AI brain to see your screen."
        
    try:
        # Take screenshot
        temp_file = "temp_screen_analysis.png"
        pyautogui.screenshot(temp_file)
        
        # Load image
        pil_img = Image.open(temp_file)
        
        models_to_try = ['gemini-2.0-flash', 'gemini-2.5-flash', 'gemini-2.0-flash-lite']
        
        last_error = ""
        for model_name in models_to_try:
            try:
                 response = genai_client.models.generate_content(
                     model=model_name,
                     contents=[question + " (Answer briefly about the screen content)", pil_img]
                 )
                 # cleanup
                 if os.path.exists(temp_file):
                     os.remove(temp_file)
                 return response.text
            except Exception as e:
                 last_error = f"{model_name} failed: {e}"
                 print(last_error)
                 continue
                 
        if os.path.exists(temp_file):
            os.remove(temp_file)
        return f"Screen vision error (Used all models): {last_error}"
             
    except Exception as e:
        return f"Screen error: {e}"

def ask_documents(query):
    global genai_client
    if not genai_client:
        return "I need my AI brain to read documents."
        
    data_folder = "karen_data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        return f"I created a '{data_folder}' folder. Put your files there."
        
    context = ""
    file_count = 0
    
    # Read files
    try:
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                
                content = ""
                if ext == ".txt" or ext == ".md" or ext == ".py":
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                elif ext == ".pdf":
                    try:
                        reader = PdfReader(file_path)
                        for page in reader.pages:
                            content += page.extract_text() + "\n"
                    except:
                        pass
                        
                if content:
                    context += f"\n--- File: {filename} ---\n{content[:10000]}" # Limit per file
                    file_count += 1
    except Exception as e:
        return f"Error reading files: {e}"
        
    if file_count == 0:
        return f"The '{data_folder}' folder is empty."
        
    # Send to AI
    prompt = f"Answer this question based on the provided documents:\n\nQuestion: {query}\n\nDocuments Context:\n{context[:50000]}" # Total limit
    return ask_genai(prompt)


def process_query(query):
    """
    Process the command and return False if the system should stop/exit.
    Returns True to continue.
    """
    global camera_open, cap
    import wikipedia
    import webbrowser
    import os
    import pyautogui
    import pywhatkit
    
    query = query.lower()
    
    try:
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            wikipedia.auto_suggest=False
            query = query.replace('wikipedia', "")
            print(f"Query: {query}")
            try:
                results = wikipedia.summary(query, sentences=3, auto_suggest=False)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print(f"Wiki error: {e}")
                speak("Could not find results on Wikipedia")
    
        elif 'open youtube' in query:
            print("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            speak("opening youtube")

        elif 'open google' in query:
            print("Opening Google")
            webbrowser.open("https://www.google.com")
            speak("opening Google")
        
        elif 'open new tab' in query:
            webbrowser.open_new_tab("https://www.google.com")
            speak("your new tab sir")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")
            speak("opening instagram")

        elif 'open notepad' in query:
            nPath = "C:\\Windows\\system32\\notepad.exe"
            if os.path.exists(nPath):
                os.startfile(nPath)
                speak("opening notepad")
            else:
                speak("Notepad not found at verified path")

        elif 'close notepad' in query:
            speak("okay sir, closing your notepad")
            os.system("taskkill /f /im notepad.exe")

        elif 'open cmd' in query:
            os.system("start cmd")
            speak("opening command prompt")

        elif 'open microsoft' in query:
             try:
                 os.system("start msedge")
                 speak("opening Microsoft edge")
             except:
                 speak("Could not find Microsoft Edge")

        elif 'close microsoft' in query:
            speak("okay sir, closing Microsoft edge")
            os.system("taskkill /f /im msedge.exe")

        elif 'play' in query:
            song = query.replace('play', '')
            speak('playing ' + song + ' from youtube')
            try:
                threading.Thread(target=pywhatkit.playonyt, args=(song,), daemon=True).start()
            except Exception as e:
                print(f"Error playing video: {e}")
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

        elif 'download this video' in query or 'save this video' in query:
             # This assumes user provides URL in a specific way or we check clipboard? 
             # For simpler usage via voice, we can ask for the link.
             # BUT simpler: "download video [URL]" or just use GUI input.
             # Voice-only URL is hard. Let's try clipboard or ask user to paste.
             try:
                 import pyperclip
                 url = pyperclip.paste()
                 if "youtube.com" in url or "youtu.be" in url:
                     speak(f"Downloading video from clipboard link...")
                     speak(download_video(url))
                 else:
                     speak("Please copy a YouTube link first.")
             except ImportError:
                 speak("I need the pyperclip library to read your clipboard.")

        elif 'news' in query or 'headlines' in query:
             speak("Fetching the latest tech news.")
             speak(get_news())

        elif 'weather' in query:
             # user might say "weather in London"
             city = "Mumbai" # default
             if "in" in query:
                 city = query.split("in")[-1].strip()
             speak(f"Checking weather for {city}...")
             speak(get_weather(city))

        elif 'search' in query:
            search = query.replace('search', '')
            speak('searching ' + search + ' from google')
            webbrowser.open(f"https://www.google.com/search?q={search}")

        elif 'shut down the system' in query:
            os.system("shutdown /s /t 5")

        elif 'restart the system' in query:
            os.system("shutdown /r /s 5")

        elif 'sleep the system' in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        # --- New Features ---
        elif 'battery' in query or 'power' in query:
             speak(get_battery_status())

        elif 'internet speed' in query or 'speed test' in query:
             speak("Checking internet speed. This may take a moment.")
             speak(check_internet_speed())

        elif 'screenshot' in query:
             speak(take_screenshot())

        elif 'organize downloads' in query or 'clean downloads' in query:
             speak(organize_downloads())

        # Vision AI
        elif 'what do you see' in query or 'describe this' in query:
             speak("Let me take a look.")
             speak(analyze_camera_frame())

        elif 'read this' in query or 'read text' in query:
            speak("Reading text from camera.")
            speak(analyze_camera_frame("Read the text in this image deeply."))

        elif 'look at my screen' in query or 'read my screen' in query or 'what is on my screen' in query:
            speak("Looking at your screen...")
            speak(analyze_screen())
            
        elif 'fix this error' in query or 'analyze error' in query:
            speak("Checking the error on your screen.")
            speak(analyze_screen("Identify the error message on screen and suggest a fix."))

        # Spotify / Media Control
        elif 'spotify play' in query or 'play music' in query or 'pause music' in query or 'stop music' in query:
             pyautogui.press("playpause")
             speak("Toggled music playback")
             
        elif 'next song' in query or 'skip song' in query:
             pyautogui.press("nexttrack")
             speak("Skipping song")
             
        elif 'previous song' in query:
             pyautogui.press("prevtrack")
             speak("Playing previous song")

        elif 'previous song' in query:
             pyautogui.press("prevtrack")
             speak("Playing previous song")
        
        # RAG / Documents
        elif 'read my documents' in query or 'search documents' in query or 'search my notes' in query:
             q = query.replace('read my documents', '').replace('search documents', '').replace('search my notes', '').strip()
             if not q:
                 speak("What should I search for in your documents?")
             else:
                 speak(f"Searching {q} in your data folder...")
                 speak(ask_documents(q))

        # To-Do / Productivity
        elif 'add to my todo' in query or 'add to todo' in query:
             task = query.replace('add to my todo', '').replace('add to todo', '').strip()
             if task:
                 speak(manage_todo("add", task))
             else:
                 speak("What should I add?")

        elif 'remind me to' in query:
             task = query.replace('remind me to', '').strip()
             if task:
                 speak(manage_todo("add", task))
                 speak(f"I've added {task} to your list.")
             else:
                 speak("Remind you to do what?")

        elif 'what is on my list' in query or 'read my todo' in query or 'my todo list' in query:
             speak(manage_todo("list"))
        
        elif 'clear my todo' in query:
             speak(manage_todo("clear"))


        elif 'volume up' in query:
            pyautogui.press("volumeup")

        elif 'volume down' in query:
            pyautogui.press("volumedown")
            
        elif 'mute' in query or 'volume mute' in query:
            pyautogui.press("volumemute")

        elif 'open camera' in query and not camera_open:
            import cv2
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not cap.isOpened():
                cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

            if not cap.isOpened():
                speak("Sorry, I can't access the camera.")
            else:
                speak("Camera opened")
                camera_open = True
                threading.Thread(target=camera_loop, daemon=True).start()

        elif 'close camera' in query and camera_open:
            speak("Closing camera")
            camera_open = False

        elif 'hello' in query or 'hi' in query.split() or 'hey' in query.split():
            speak("Hello! I am ready to help you. What can I do for you?")

        elif 'who built you' in query:
            speak("I was built by a developer on 27 7 2022.")

        elif 'thank' in query:
            speak("It's a pleasure! You are always welcome.")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak (f"The time is {strTime}")

        elif 'joke' in query:
            speak((pyjokes.get_joke()))


        elif 'who are you' in query:
            speak("I am Karen. Your Virtual Assistant as a friend.")


        elif 'how was your day' in query:
            speak("It's been great! I hope your day was great too")

        elif 'what country are you from' in query:
            speak("I am from India, but I live in the cloud")

        elif 'your favourite country' in query:
            speak("Picking a favorite is impossible. Each country has its own unique beauty like Iceland's black sand beach of vestrahorn")

        elif 'can i ask you a question' in query:
            speak("I'd love to hear your question")

        elif 'ok karen' in query:
            speak("I'm here! What's next?")

        elif 'ok' in query:
            speak("I'm listening. How can I help?")

        elif 'ip address' in query:
            ip = get('https://api.ipify.org').text
            print(f"your IP Address is {ip}")
            speak(f"your IP Address is {ip}")

        elif 'kill yourself' in query:
            speak("Thanks for your time. Have a Good day Sir. byeee.")
            return False
        
        else:
            # Fallback to GenAI
            if genai_client:
                # speak("Thinking...") # User requested to remove this
                answer = ask_genai(query)
                speak(answer)
            else:
                # speak("I didn't understand that command and I am not connected to the internet brain.")
                 pass # Be silent if no command matched and no AI configured? Or just say it.
                 # Better to say it so user knows it was heard but not understood.
                 speak("I didn't understand that command.")
            
    except Exception as j:
        print(f"Error processing query: {j}")
        # continue -> return True
    
    return True


if __name__ == "__main__": 
    wishMe()
    
    while True:

        query = takeCommand().lower()
        if query == "none":
            continue

        should_continue = process_query(query)
        if not should_continue:
            break