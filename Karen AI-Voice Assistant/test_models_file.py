import google.generativeai as genai
import os

if os.path.exists("gemini_api_key.txt"):
    with open("gemini_api_key.txt", "r") as f:
        key = f.read().strip()
        genai.configure(api_key=key)

test_models = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.0-pro",
    "gemini-2.0-flash-exp"
]

with open("model_results.txt", "w", encoding='utf-8') as f:
    f.write("--- START PROBE ---\n")
    for model_name in test_models:
        f.write(f"Testing: {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            f.write("SUCCESS ✅\n")
        except Exception as e:
            f.write(f"FAILED ❌ ({e})\n")
    f.write("--- END PROBE ---\n")
