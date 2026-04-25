import google.generativeai as genai
import os

# Try to load key
if os.path.exists("gemini_api_key.txt"):
    with open("gemini_api_key.txt", "r") as f:
        key = f.read().strip()
        genai.configure(api_key=key)

print("--- START MODEL LIST ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Print just the name, strip 'models/' prefix if present
            name = m.name.replace('models/', '')
            print(name)
except Exception as e:
    print(f"Error: {e}")
print("--- END MODEL LIST ---")
