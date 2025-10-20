"""
Test script to check which Gemini models work with your API key and LangChain.
"""
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("GEMINI MODEL TESTING SCRIPT")
print("=" * 60)
print(f"API Key loaded: {GEMINI_API_KEY[:20]}...{GEMINI_API_KEY[-10:]}")
print()

# List of Gemini 2.x model names to test (based on your API key)
models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-pro",
    "gemini-2.0-pro-exp",
    "models/gemini-2.5-flash",
    "models/gemini-2.0-flash",
]

test_prompt = "Say 'Hello' in one word only."

working_models = []
failed_models = []

print("Testing models...\n")

for model_name in models_to_test:
    print(f"Testing: {model_name}...", end=" ")
    try:
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=GEMINI_API_KEY,
            temperature=0.3
        )
        
        # Try to invoke the model
        response = llm.invoke(test_prompt)
        
        print(f"✅ SUCCESS")
        print(f"   Response: {response.content[:50]}")
        working_models.append(model_name)
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ FAILED")
        if "404" in error_msg:
            print(f"   Error: Model not found (404)")
        elif "403" in error_msg:
            print(f"   Error: Access forbidden (403)")
        elif "401" in error_msg:
            print(f"   Error: Authentication failed (401)")
        else:
            print(f"   Error: {error_msg[:100]}")
        failed_models.append(model_name)
    
    print()

print("=" * 60)
print("RESULTS SUMMARY")
print("=" * 60)

if working_models:
    print(f"\n✅ WORKING MODELS ({len(working_models)}):")
    for model in working_models:
        print(f"   - {model}")
    print(f"\n🎯 RECOMMENDED: Use '{working_models[0]}' in ai_analyzer.py")
else:
    print("\n❌ NO WORKING MODELS FOUND")
    print("\nPossible issues:")
    print("1. API key might be invalid or expired")
    print("2. API key might not have access to Gemini models")
    print("3. Network/firewall issues")
    print("4. LangChain version compatibility issues")

if failed_models:
    print(f"\n❌ FAILED MODELS ({len(failed_models)}):")
    for model in failed_models:
        print(f"   - {model}")

print("\n" + "=" * 60)
