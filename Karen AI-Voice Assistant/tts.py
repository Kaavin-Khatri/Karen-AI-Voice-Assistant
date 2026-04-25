import asyncio
import os
import sys

# Try importing edge-tts and pygame
try:
    import edge_tts
    import pygame
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("EdgeTTS/Pygame not found. Falling back to pyttsx3.")

# Import pyttsx3 as fallback
import pyttsx3

# Voice Selection
VOICE = "en-US-AriaNeural"
OUTPUT_FILE = "speech.mp3"

async def generate_speech(text):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)

def play_audio():
    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
    
    # Cleanup
    try:
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    except:
        pass

def speak_fallback(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 180)
        engine.setProperty("volume", 0.9)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Fallback TTS Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        
        if EDGE_TTS_AVAILABLE:
            try:
                asyncio.run(generate_speech(text))
                play_audio()
            except Exception as e:
                print(f"EdgeTTS failed: {e}. Using fallback.")
                speak_fallback(text)
        else:
            speak_fallback(text)
