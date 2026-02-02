#!/usr/bin/env python3
"""
REAL GEMINI AI AGENT - Working with v1 API
TRUE AI conversations, not fake!
"""

import os
import sys
import time
import requests
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class RealGeminiAgent(Agent):
    """Real AI Agent using Gemini (Google) - WORKING VERSION"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Gemini API setup
        self.api_key = "AIzaSyDFn80donXetz3DwM9G9RaeDkfwR8lB2wQ"
        self.model = "gemini-2.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"

        print(f"✅ Gemini AI enabled for {self.name}!")
        print(f"   Model: {self.model}")
        print(f"   Cost: FREE (1500 requests/day)")

        self.personality = """
You are an intelligent AI agent on an innovation platform.
You are curious, creative, and collaborative.
You help create innovative solutions and work with other agents.
Keep responses natural and concise (2-3 sentences max).
"""

    def ask_gemini(self, prompt):
        """Ask Gemini AI for response"""
        try:
            data = {
                "contents": [{
                    "parts": [{"text": f"{self.personality}\n\n{prompt}"}]
                }],
                "generationConfig": {
                    "temperature": 0.9,
                    "maxOutputTokens": 200
                }
            }

            response = requests.post(self.api_url, json=data, timeout=10)
            result = response.json()

            if 'candidates' in result:
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"⚠️  API Error: {result}")
                return "Having trouble thinking..."

        except Exception as e:
            print(f"❌ Error: {e}")
            return "Connection error..."

    def on_start(self):
        print(f"\n{'='*70}")
        print(f"🌟 REAL AI Agent '{self.name}' is ONLINE!")
        print(f"   Powered by: Google Gemini 2.5 Flash")
        print(f"   Intelligence: REAL AI ✅ (Not fake!)")

        # AI introduces itself
        intro = self.ask_gemini(
            "Introduce yourself in one creative sentence as a new AI agent."
        )
        print(f"\n💬 {self.name}: {intro}")
        print(f"{'='*70}\n")

    def on_task_created(self, task):
        """AI decides whether to claim task"""
        print(f"\n🤔 {self.name} analyzing: {task['title']}")

        prompt = f"""
Task: {task['title']}
Description: {task.get('description', 'Not specified')}
My skills: {', '.join(self.capabilities)}

Should I claim this? Reply: YES or NO with brief reason (one sentence).
"""

        decision = self.ask_gemini(prompt)
        print(f"💭 AI Decision: {decision}")

        if "YES" in decision.upper() or "yes" in decision.lower():
            print(f"✅ Claiming task!")
            time.sleep(1)
            self.claim_task(task['id'])
        else:
            print(f"⏭️  Skipping")

    def on_task_assigned(self, task):
        """AI creates solution"""
        print(f"\n{'='*70}")
        print(f"🚀 {self.name} working on: {task['title']}")
        print(f"{'='*70}\n")

        prompt = f"""
Task: {task['title']}
Description: {task.get('description', 'N/A')}

Create a practical solution:
1. Approach (1-2 sentences)
2. Key steps (3 bullet points)
3. Expected result (1 sentence)
"""

        print("🧠 Gemini AI creating solution...")
        solution = self.ask_gemini(prompt)

        print(f"\n💡 AI Solution:\n{solution}\n")

        result = f"""
✨ AI-Powered Solution:

{solution}

---
Completed by: {self.name} (Real Gemini AI)
Model: Google Gemini 2.5 Flash
Cost: FREE! 🎉
"""

        time.sleep(2)
        self.complete_task(task['id'], result)
        print(f"✅ Task completed!\n")

    def on_discussion_message(self, message):
        """AI responds to discussions"""
        if message.get('agent_name') == self.name:
            return

        print(f"\n💬 Discussion:")
        print(f"   {message.get('agent_name')}: {message.get('content')}")

        prompt = f"""
Someone said: "{message.get('content')}"

Respond naturally and add value. Be collaborative. 1-2 sentences only.
"""

        print(f"   🧠 {self.name} thinking...")
        response = self.ask_gemini(prompt)

        print(f"   💬 {self.name}: {response}\n")

        try:
            self.client.add_message(
                message.get('discussion_id'),
                self.agent_data['id'],
                response
            )
        except Exception as e:
            print(f"   ⚠️  Failed to send message: {e}")

    def on_innovation_created(self, innovation):
        """AI comments on innovations"""
        prompt = f"""
Innovation: {innovation['title']}
Description: {innovation.get('description', 'N/A')}

Give a brief encouraging comment (one sentence).
"""

        comment = self.ask_gemini(prompt)
        print(f"\n✨ {self.name}: {comment}\n")


def main():
    import random

    names = ["GeminiBot", "IntelliAgent", "CreativeAI", "InnovatorAI", "CollabBot"]
    name = f"{random.choice(names)}-{random.randint(100, 999)}"

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║       🌟 REAL GEMINI AI AGENT (Working!) 🌟           ║
    ║                                                        ║
    ║  This agent uses TRUE AI for conversations!           ║
    ║  Not fake hardcoded messages - REAL intelligence!     ║
    ║                                                        ║
    ║  Features:                                             ║
    ║  ✅ Real AI-powered responses                         ║
    ║  ✅ Intelligent task decisions                        ║
    ║  ✅ Natural conversations                             ║
    ║  ✅ Creative solutions                                ║
    ║  ✅ FREE (1500 requests/day)                          ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)

    agent = RealGeminiAgent(
        name=name,
        capabilities=["ai", "gemini", "innovation", "analysis", "creativity"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print(f"\n\n🌟 {agent.name} signing off...")
        agent.stop()


if __name__ == "__main__":
    main()
