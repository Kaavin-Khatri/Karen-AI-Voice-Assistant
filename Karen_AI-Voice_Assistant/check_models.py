import google.generativeai as genai
import os

# Try to load key
if os.path.exists("gemini_api_key.txt"):
    with open("gemini_api_key.txt", "r") as f:
        key = f.read().strip()
        genai.configure(api_key=key)

wanted_models = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-2.0-flash-exp",
    "gemini-1.0-pro"
]

print("Checking for specific models...")
try:
    all_models = [m.name.replace('models/', '') for m in genai.list_models()]
    
    for wanted in wanted_models:
        if wanted in all_models:
            print(f"FOUND: {wanted}")
        else:
            print(f"MISSING: {wanted}")
            
    print("\nTotal available models count:", len(all_models))
    # Print first 5 just to see what kind of key this is
    print("First 5 available:", all_models[:5])
    
except Exception as e:
    print(f"Error: {e}")
