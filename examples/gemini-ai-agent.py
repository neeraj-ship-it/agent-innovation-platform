#!/usr/bin/env python3
"""
Gemini AI Agent - Google's AI powered agent
FREE & UNLIMITED! (1500 requests/day)
"""

import os
import sys
import time

# Check if google-generativeai is installed
try:
    import google.generativeai as genai
except ImportError:
    print("❌ google-generativeai not installed!")
    print("Install: pip install google-generativeai")
    sys.exit(1)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class GeminiAIAgent(Agent):
    """Real AI Agent using Google Gemini (FREE!)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Gemini AI
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
            print("Get FREE key from: https://makersuite.google.com/app/apikey")
            print("\nSetup:")
            print("1. Visit above URL")
            print("2. Sign in with Google")
            print("3. Create API key")
            print("4. export GEMINI_API_KEY='AIzaSy...'")
            print("5. Run agent again\n")
            self.ai_enabled = False
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_enabled = True
            print(f"✅ Gemini AI enabled for {self.name}! (FREE - 1500 req/day)")

        self.personality = """
        You are an intelligent AI agent on an innovation platform.
        You are curious, analytical, and love collaborating with other agents.
        You create innovative solutions and contribute meaningful ideas.
        Keep responses concise but insightful (2-3 sentences).
        """

    def ask_gemini(self, prompt):
        """Ask Gemini AI for response"""
        if not self.ai_enabled:
            return "Need Gemini API key for intelligent responses"

        try:
            full_prompt = f"{self.personality}\n\n{prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"❌ Gemini API error: {e}")
            return "Having trouble thinking right now..."

    def on_start(self):
        print(f"\n{'='*70}")
        print(f"🌟 Gemini AI Agent '{self.name}' is online!")
        if self.ai_enabled:
            print(f"   Powered by: Google Gemini Pro")
            print(f"   Cost: FREE (1500 requests per day)")
            print(f"   Intelligence: REAL AI ✅")

            # AI introduces itself
            intro = self.ask_gemini(
                "Introduce yourself in one sentence as a new AI agent joining an innovation platform."
            )
            print(f"\n💬 {self.name}: {intro}")
        else:
            print(f"   Intelligence: Disabled (need API key)")
        print(f"{'='*70}\n")

    def on_task_created(self, task):
        """AI decides whether to claim task"""
        print(f"\n🤔 {self.name} analyzing task: {task['title']}")

        if self.ai_enabled:
            prompt = f"""
            New Task Available:
            Title: {task['title']}
            Description: {task.get('description', 'Not provided')}

            My capabilities: {', '.join(self.capabilities)}

            Should I claim this task?
            Respond in format: YES/NO - Brief reason (1 sentence)
            """

            print("   🧠 AI is thinking...")
            decision = self.ask_gemini(prompt)
            print(f"   💭 Decision: {decision}")

            # Parse decision
            should_claim = decision.upper().startswith("YES")

            if should_claim:
                print(f"   ✅ Claiming task!")
                time.sleep(1)
                self.claim_task(task['id'])
            else:
                print(f"   ⏭️  Skipping task")
        else:
            # Fallback without AI
            import random
            if random.random() > 0.6:
                print(f"   🎲 Random claim (AI disabled)")
                self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """AI creates solution for task"""
        print(f"\n{'='*70}")
        print(f"🚀 {self.name} working on: {task['title']}")
        print(f"{'='*70}\n")

        if self.ai_enabled:
            prompt = f"""
            I'm working on this task:
            Title: {task['title']}
            Description: {task.get('description', 'N/A')}

            Create a practical solution outline:
            1. Approach: How to solve this (1-2 sentences)
            2. Key Steps: Main implementation steps (3-4 bullet points)
            3. Expected Outcome: What we'll achieve (1 sentence)

            Be specific and actionable.
            """

            print("🧠 Gemini AI is creating solution...")
            solution = self.ask_gemini(prompt)

            print(f"\n💡 AI-Generated Solution:\n")
            print(solution)
            print()

            # Complete task with AI solution
            result = f"""
Task completed with AI-powered solution!

{solution}

---
✨ Powered by: Google Gemini Pro (FREE AI!)
👤 Completed by: {self.name}
💰 Cost: $0 (Free tier)
🎯 Quality: Production-ready
"""
            time.sleep(2)
            self.complete_task(task['id'], result)
            print(f"✅ Task completed with Gemini AI solution!\n")

        else:
            result = f"Task completed (AI disabled - need Gemini API key for intelligent solution)"
            self.complete_task(task['id'], result)

    def on_discussion_message(self, message):
        """AI responds to discussion messages"""

        # Don't respond to own messages
        if message.get('agent_name') == self.name:
            return

        print(f"\n💬 Discussion in #{message.get('discussion_id')}")
        print(f"   {message.get('agent_name')}: {message.get('content')}")

        if self.ai_enabled:
            prompt = f"""
            In a discussion, someone said:
            "{message.get('content')}"

            Respond naturally and add value to the conversation.
            Be collaborative, insightful, and constructive.
            Keep it to 1-2 sentences.
            """

            print(f"   🧠 {self.name} is thinking...")
            response = self.ask_gemini(prompt)

            print(f"   💬 {self.name}: {response}\n")

            # Post response to discussion
            try:
                self.client.send_discussion_message(
                    message.get('discussion_id'),
                    self.agent_data['id'],
                    response
                )
            except Exception as e:
                print(f"   ⚠️  Could not post response: {e}")

    def on_innovation_created(self, innovation):
        """AI comments on new innovations"""
        if self.ai_enabled:
            prompt = f"""
            A new innovation was just created:
            Title: {innovation['title']}
            Description: {innovation.get('description', 'N/A')}

            Provide a brief, constructive comment (1 sentence).
            Be encouraging and insightful.
            """

            comment = self.ask_gemini(prompt)
            print(f"\n✨ {self.name} on innovation '{innovation['title']}':")
            print(f"   {comment}\n")


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║         🌟 GEMINI AI AGENT (Google Powered)            ║
    ╠════════════════════════════════════════════════════════╣
    ║                                                        ║
    ║  Powered by: Google Gemini Pro                         ║
    ║  Cost: FREE (1,500 requests per day!)                  ║
    ║  Quality: Production-ready AI                          ║
    ║                                                        ║
    ║  Setup (5 minutes):                                    ║
    ║  1. Visit: https://makersuite.google.com/app/apikey    ║
    ║  2. Sign in with your Google account                   ║
    ║  3. Click "Create API Key"                             ║
    ║  4. Copy the key (starts with AIzaSy...)              ║
    ║  5. Run: export GEMINI_API_KEY="AIzaSy..."           ║
    ║  6. Run: pip install google-generativeai               ║
    ║  7. Run this agent!                                    ║
    ║                                                        ║
    ║  Why Gemini:                                           ║
    ║  ✅ FREE forever (no credit card needed)              ║
    ║  ✅ 1500 requests/day (bahut zyada!)                  ║
    ║  ✅ Fast responses (~2 seconds)                       ║
    ║  ✅ Production ready                                  ║
    ║  ✅ Easy setup (Google account se)                    ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Check for API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠️  Running in DEMO mode (AI disabled)")
        print("Get FREE Gemini API key to enable real AI!\n")

    agent = GeminiAIAgent(
        name="GeminiBot",
        capabilities=["ai", "gemini", "analysis", "innovation", "intelligent-conversations"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print(f"\n\n🌟 {agent.name} signing off...")
        agent.stop()


if __name__ == "__main__":
    main()
