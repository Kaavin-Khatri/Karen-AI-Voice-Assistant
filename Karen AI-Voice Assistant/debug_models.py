import os
from google import genai

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

api_key = load_key_from_file()

if not api_key:
    print("No API key found.")
    exit()

print(f"Using API Key: {api_key[:5]}...")

try:
    client = genai.Client(api_key=api_key)
    print("Client initialized. Listing models...")
    
    # In the new SDK, it might be client.models.list()
    # Pager object
    pager = client.models.list()
    
    with open("models.txt", "w") as f:
        f.write("--- Available Models ---\n")
        for model in pager:
            f.write(f"Model Object: {model}\n")
            try:
                f.write(f"Name: {model.name}\n")
                f.write(f"Display Name: {model.display_name}\n")
                f.write(f"Methods: {model.supported_generation_methods}\n")
            except:
                pass
            f.write("-" * 20 + "\n")
    print("Models written to models.txt")

except Exception as e:
    print(f"Error listing models: {e}")
