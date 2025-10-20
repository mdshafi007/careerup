"""
Direct Google Generative AI SDK test (no LangChain).
This will test if your API key works at all.
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("DIRECT GEMINI API TEST (No LangChain)")
print("=" * 60)
print(f"API Key: {GEMINI_API_KEY[:20]}...{GEMINI_API_KEY[-10:]}")
print()

# Configure the SDK
genai.configure(api_key=GEMINI_API_KEY)

# List available models
print("Fetching available models...")
try:
    models = genai.list_models()
    print("\n✅ Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"   - {model.name}")
    print()
except Exception as e:
    print(f"❌ Error listing models: {e}\n")

# Test models
models_to_test = [
    "gemini-pro",
    "gemini-1.5-pro",
    "gemini-1.5-flash",
]

print("Testing models with direct SDK...\n")

for model_name in models_to_test:
    print(f"Testing: {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say hello")
        print(f"✅ SUCCESS")
        print(f"   Response: {response.text[:50]}")
        print()
    except Exception as e:
        print(f"❌ FAILED")
        print(f"   Error: {str(e)[:150]}")
        print()

print("=" * 60)
