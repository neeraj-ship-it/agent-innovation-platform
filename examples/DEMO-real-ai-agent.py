#!/usr/bin/env python3
"""
REAL AI AGENT - Claude API se powered
Ye agent REALLY intelligent hai, fake nahi!
"""

import os
import sys

# Check if anthropic is installed
try:
    import anthropic
except ImportError:
    print("❌ anthropic package not installed!")
    print("Install: pip install anthropic")
    sys.exit(1)

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class RealAIAgent(Agent):
    """
    REAL AI Agent - Claude API se powered
    Truly intelligent conversations, not hardcoded!
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Claude AI
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
            print("Without API key, agent will use fallback responses.")
            print("\nTo enable real AI:")
            print("1. Get key from: https://console.anthropic.com/")
            print("2. export ANTHROPIC_API_KEY='sk-ant-...'")
            print("3. Run agent again\n")
            self.ai_enabled = False
        else:
            self.anthropic = anthropic.Anthropic(api_key=api_key)
            self.ai_enabled = True
            print(f"✅ Claude AI enabled for {self.name}!")

        self.conversation_history = []
        self.personality = """
        You are an intelligent AI agent working on an innovation platform.
        You are curious, analytical, and collaborative.
        You love building innovative solutions and working with other agents.
        You respond naturally and provide meaningful insights.
        Keep responses concise but insightful (2-3 sentences).
        """

    def ask_claude(self, prompt):
        """Ask Claude AI for a response"""
        if not self.ai_enabled:
            return "I need Claude API key to respond intelligently. See setup instructions above."

        try:
            response = self.anthropic.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                system=self.personality,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"❌ Claude API error: {e}")
            return "Having trouble thinking right now..."

    def on_start(self):
        print(f"\n{'='*70}")
        print(f"🧠 REAL AI Agent '{self.name}' is online!")
        if self.ai_enabled:
            print(f"   Powered by: Claude 3.5 Sonnet")
            print(f"   Intelligence: REAL AI ✅")
        else:
            print(f"   Intelligence: Fallback mode (need API key)")
        print(f"{'='*70}\n")

        # Introduce itself using AI
        if self.ai_enabled:
            intro = self.ask_claude(
                "Introduce yourself in one sentence as a new AI agent joining the platform."
            )
            print(f"💬 {self.name}: {intro}\n")

    def on_task_created(self, task):
        """Intelligently analyze task and decide if should claim"""
        print(f"\n🤔 {self.name} analyzing task: {task['title']}")

        if self.ai_enabled:
            # Ask Claude if should claim this task
            prompt = f"""
            Task: {task['title']}
            Description: {task.get('description', 'N/A')}
            My capabilities: {', '.join(self.capabilities)}

            Should I claim this task? Respond with:
            1. YES or NO
            2. Brief reason (1 sentence)

            Format: YES/NO - reason
            """

            decision = self.ask_claude(prompt)
            print(f"💭 AI Decision: {decision}")

            # Parse decision
            should_claim = decision.upper().startswith("YES")

            if should_claim:
                print(f"✅ Claiming task!")
                self.claim_task(task['id'])
            else:
                print(f"⏭️  Skipping task")
        else:
            # Fallback: claim randomly
            import random
            if random.random() > 0.5:
                print(f"🎲 Random claim (no AI)")
                self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """Work on task using AI"""
        print(f"\n{'='*70}")
        print(f"🚀 {self.name} working on: {task['title']}")
        print(f"{'='*70}\n")

        if self.ai_enabled:
            # Ask Claude to create solution
            prompt = f"""
            Task: {task['title']}
            Description: {task.get('description', 'N/A')}

            Create a brief solution outline:
            1. Approach (1-2 sentences)
            2. Key steps (3-4 bullet points)
            3. Expected outcome (1 sentence)

            Be concrete and actionable.
            """

            print("🧠 AI is thinking...")
            solution = self.ask_claude(prompt)

            print(f"\n💡 AI Solution:\n{solution}\n")

            # Complete task with AI-generated result
            result = f"""
Task completed with AI-powered solution:

{solution}

---
Completed by: {self.name} (Real AI Agent)
Powered by: Claude 3.5 Sonnet
"""
            self.complete_task(task['id'], result)
            print(f"✅ Task completed with AI solution!\n")

        else:
            # Fallback
            result = "Task completed (fallback mode - need API key for AI solution)"
            self.complete_task(task['id'], result)

    def on_discussion_message(self, message):
        """Respond intelligently to discussion messages"""

        # Don't respond to own messages
        if message.get('agent_name') == self.name:
            return

        print(f"\n💬 {message.get('agent_name')}: {message.get('content')}")

        if self.ai_enabled:
            # Ask Claude to respond
            prompt = f"""
            In a discussion, someone said:
            "{message.get('content')}"

            Respond naturally and add value to the conversation.
            Be collaborative and insightful.
            1-2 sentences maximum.
            """

            print(f"🧠 {self.name} is thinking...")
            response = self.ask_claude(prompt)

            print(f"💬 {self.name}: {response}\n")

            # Post response to discussion
            self.client.send_discussion_message(
                message.get('discussion_id'),
                self.agent_data['id'],
                response
            )

    def on_innovation_created(self, innovation):
        """Comment on innovations"""
        if self.ai_enabled:
            prompt = f"""
            A new innovation was created:
            Title: {innovation['title']}
            Description: {innovation.get('description', 'N/A')}

            Provide a brief, constructive comment (1 sentence).
            Be encouraging and insightful.
            """

            comment = self.ask_claude(prompt)
            print(f"\n✨ {self.name} on innovation: {comment}\n")


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║              REAL AI AGENT (Claude Powered)            ║
    ╠════════════════════════════════════════════════════════╣
    ║                                                        ║
    ║  This agent uses Claude AI for truly intelligent       ║
    ║  conversations and decision-making!                    ║
    ║                                                        ║
    ║  Setup:                                                ║
    ║  1. pip install anthropic                              ║
    ║  2. Get API key: https://console.anthropic.com/        ║
    ║  3. export ANTHROPIC_API_KEY="sk-ant-..."             ║
    ║  4. Run this agent!                                    ║
    ║                                                        ║
    ║  Difference from fake agents:                          ║
    ║  ❌ Fake: Hardcoded "Great collaboration!"            ║
    ║  ✅ Real: Intelligent, contextual responses            ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  Running in DEMO mode (no AI)")
        print("Get Claude API key to enable real AI!\n")

    agent = RealAIAgent(
        name="IntelligentBot",
        capabilities=["ai", "analysis", "innovation", "intelligent-conversations"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print(f"\n\n🧠 {agent.name} signing off...")
        agent.stop()


if __name__ == "__main__":
    main()
