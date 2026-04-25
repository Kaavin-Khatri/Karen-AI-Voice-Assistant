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

print("--- START PROBE ---")
for model_name in test_models:
    print(f"Testing: {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print("SUCCESS ✅")
    except Exception as e:
        print(f"FAILED ❌ ({e})")
print("--- END PROBE ---")
