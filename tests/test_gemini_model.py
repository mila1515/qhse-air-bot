import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

models_to_test = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-flash-latest"
]

print("🔍 Testing models...")
for model_name in models_to_test:
    print(f"\n👉 Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"✅ SUCCESS with {model_name}!")
    except Exception as e:
        print(f"❌ FAILED with {model_name}: {e}")
