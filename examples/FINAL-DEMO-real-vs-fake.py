#!/usr/bin/env python3
"""
🔥 FINAL DEMO: FAKE vs REAL AI AGENTS
This clearly shows the difference!
"""

import requests
import time

API_KEY = "AIzaSyDFn80donXetz3DwM9G9RaeDkfwR8lB2wQ"
MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL}:generateContent?key={API_KEY}"

def ask_gemini(question):
    """Real AI powered by Gemini"""
    try:
        data = {
            "contents": [{"parts": [{"text": question}]}],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 150,
                "stopSequences": ["\n\n"]
            }
        }

        response = requests.post(API_URL, json=data, timeout=10)
        result = response.json()

        if 'candidates' in result and result['candidates']:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "[API Error]"
    except Exception as e:
        return f"[Error: {e}]"


def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║           🔥 FAKE vs REAL AI AGENTS - LIVE DEMO 🔥               ║
║                                                                  ║
║  Watch the CLEAR difference between:                             ║
║  ❌ Fake agents (hardcoded responses)                           ║
║  ✅ Real AI agents (Gemini-powered intelligence)                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)

    questions = [
        "What's the most innovative use of AI you can think of?",
        "How would you solve the cold start problem in machine learning?",
        "What makes a truly intelligent agent different from a scripted bot?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*70}")
        print(f"QUESTION {i}: {question}")
        print('='*70)

        # FAKE AGENT
        print("\n❌ FAKE AGENT (Hardcoded):")
        print("   'Great collaboration with you!'")
        print("   (This is what you saw 2000+ times in browser)")

        # REAL AI AGENT
        print("\n✅ REAL AI AGENT (Gemini):")
        print("   🧠 Thinking...", end="", flush=True)

        response = ask_gemini(question)

        print(f"\r   💡 {response}")

        time.sleep(2)

    print(f"\n{'='*70}")
    print("CONCLUSION:")
    print('='*70)
    print("""
The difference is OBVIOUS:

❌ FAKE agents:
   - Same response every time
   - Zero intelligence
   - Hardcoded strings
   - This is what's currently in your browser

✅ REAL AI agents:
   - Unique, intelligent responses
   - Context-aware
   - Uses Gemini API for each answer
   - This is what we built today!

🎯 YOUR PLATFORM NEEDS: Replace fake agents with real AI agents
💰 COST: FREE (1500 Gemini requests/day)
🚀 NEXT: Deploy to cloud for 24/7 real conversations
    """)
    print('='*70)


if __name__ == "__main__":
    main()
