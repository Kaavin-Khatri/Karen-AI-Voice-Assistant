import google.generativeai as genai
import os

if os.path.exists("gemini_api_key.txt"):
    with open("gemini_api_key.txt", "r") as f:
        key = f.read().strip()
        genai.configure(api_key=key)

print("Saving models to file...")
with open("all_models_full.txt", "w", encoding="utf-8") as f:
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                f.write(f"{m.name}\n")
                count += 1
        f.write(f"Total count: {count}\n")
    except Exception as e:
        f.write(f"Error listing models: {e}\n")
print("Done.")
