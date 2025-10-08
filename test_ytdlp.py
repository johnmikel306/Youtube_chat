#!/usr/bin/env python
"""Test yt-dlp YouTube loader"""

from src.youtube_loader import YouTubeLoader

# Test with a popular video
test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

print(f"Testing yt-dlp loader with: {test_url}\n")

try:
    loader = YouTubeLoader()
    print("✅ Loader initialized")
    
    print("📥 Fetching transcript...")
    docs = loader.load(test_url)
    
    print(f"✅ SUCCESS! Loaded {len(docs)} document chunks")
    print(f"\nFirst chunk preview:")
    print("-" * 60)
    print(docs[0].page_content[:300] + "...")
    print("-" * 60)
    
except Exception as e:
    print(f"❌ ERROR: {e}")

