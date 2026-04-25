import google.generativeai as genai
import os

if os.path.exists("gemini_api_key.txt"):
    with open("gemini_api_key.txt", "r") as f:
        key = f.read().strip()
        genai.configure(api_key=key)

print("--- SEARCHING FOR CORE MODELS ---")
try:
    for m in genai.list_models():
        name = m.name.replace('models/', '')
        if "gemini-1.5" in name or "gemini-2.0" in name or "gemini-1.0" in name:
            print(f"FOUND: {name}")
except Exception as e:
    print(f"Error: {e}")
print("--- END SEARCH ---")
