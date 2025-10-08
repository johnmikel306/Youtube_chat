#!/usr/bin/env python
"""Quick test to verify .env file is loading correctly"""

from dotenv import load_dotenv
load_dotenv()

from config.settings import get_api_key

api_key = get_api_key()

if api_key:
    print("✅ SUCCESS: API key loaded from .env file")
    print(f"   Key starts with: {api_key[:20]}...")
    print(f"   Key length: {len(api_key)} characters")
else:
    print("❌ ERROR: API key not found")
    print("   Make sure GROQ_API_KEY is set in your .env file")

