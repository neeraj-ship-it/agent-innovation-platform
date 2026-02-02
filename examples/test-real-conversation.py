#!/usr/bin/env python3
"""
Test script to demonstrate REAL AI conversations using Gemini
This will show the difference between fake and real AI
"""

import os
import sys
import time
import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent

API_KEY = "AIzaSyDFn80donXetz3DwM9G9RaeDkfwR8lB2wQ"
MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

def ask_gemini_ai(prompt):
    """Direct Gemini API call to show REAL AI response"""
    try:
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 150
            }
        }

        response = requests.post(API_URL, json=data, timeout=10)
        result = response.json()

        if 'candidates' in result:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"API Error: {result}"
    except Exception as e:
        return f"Error: {e}"


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║          🔥 REAL AI vs FAKE AI DEMO 🔥                 ║
    ║                                                        ║
    ║  Watch the difference between:                         ║
    ║  ❌ FAKE: "Great collaboration with you!"             ║
    ║  ✅ REAL: Intelligent Gemini AI responses              ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Test questions
    questions = [
        "What's the most innovative use of AI in healthcare right now?",
        "How would you design a scalable recommendation system?",
        "What's your approach to solving the cold start problem in ML?"
    ]

    print("\n" + "="*70)
    print("❌ FAKE AGENT RESPONSES (Hardcoded)")
    print("="*70)
    for q in questions:
        print(f"\nQ: {q}")
        print(f"A: Great collaboration with you!")  # This is what fake agents say

    print("\n\n" + "="*70)
    print("✅ REAL GEMINI AI RESPONSES (Intelligent)")
    print("="*70)

    for q in questions:
        print(f"\n\nQ: {q}")
        print(f"\n🧠 Gemini AI thinking...")
        response = ask_gemini_ai(q)
        print(f"\n💡 REAL AI Answer:")
        print(f"   {response}")
        time.sleep(1)

    print("\n\n" + "="*70)
    print("DIFFERENCE IS CLEAR! 🎯")
    print("="*70)
    print("\n✅ Real AI agents use Gemini to generate intelligent, contextual responses")
    print("❌ Fake agents just repeat hardcoded messages")
    print("\nThis is what your platform needs - REAL AI conversations!")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()
