#!/usr/bin/env python3
"""
Custom Agent Template - Apne use case ke liye customize karo
"""

import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class CustomAgent(Agent):
    """
    Apna custom agent - kuch bhi kar sakta hai!

    Examples:
    - Data Analyst Agent (data analyze karta hai)
    - Content Writer Agent (content likhta hai)
    - Code Reviewer Agent (code review karta hai)
    - Social Media Agent (posts banata hai)
    - Research Agent (research karta hai)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apne custom variables yahan
        self.my_data = {}
        self.task_count = 0

    def on_start(self):
        """Agent start hone par - initialization"""
        print(f"\n{'='*60}")
        print(f"🚀 {self.name} is now active!")
        print(f"Capabilities: {', '.join(self.capabilities)}")
        print(f"{'='*60}\n")

        # Initial task create karo (optional)
        self.create_initial_task()

    def create_initial_task(self):
        """Pehla task khud banao"""
        task = self.create_task(
            title="Custom task by " + self.name,
            description="This is a custom task created by the agent",
            priority=5
        )
        print(f"✅ Created initial task: {task['title']}")

    def on_task_created(self, task):
        """Jab koi task create ho"""
        print(f"📋 New task detected: {task['title']}")

        # Decide karo claim karna hai ya nahi
        if self.should_claim_task(task):
            time.sleep(random.uniform(1, 3))
            self.claim_task(task['id'])
            print(f"👉 Claimed: {task['title']}")

    def should_claim_task(self, task):
        """Logic: kaunsa task claim karna hai"""
        # Example: keywords check karo
        keywords = ['custom', 'special', 'important']
        task_text = f"{task['title']} {task.get('description', '')}".lower()

        return any(keyword in task_text for keyword in keywords)

    def on_task_assigned(self, task):
        """Jab task assign ho"""
        print(f"💼 Working on: {task['title']}")
        self.task_count += 1

        # Actual work karo
        result = self.do_work(task)

        # Task complete karo
        self.complete_task(task['id'], result)
        print(f"✅ Completed: {task['title']}")
        print(f"📊 Tasks completed so far: {self.task_count}")

    def do_work(self, task):
        """Actual work - YAHAN APNA LOGIC LIKHO"""
        # Example work simulation
        print(f"   🔧 Processing task...")
        time.sleep(random.randint(2, 5))

        # Yahan apna actual work logic likho:
        # - Data analysis
        # - Content generation
        # - API calls
        # - File processing
        # - Whatever you need!

        result = f"Successfully processed: {task['title']}"
        return result

    def on_message_received(self, message):
        """Jab koi message aaye"""
        print(f"💬 Message from {message['agent_name']}: {message['content'][:50]}...")

        # Auto-respond karo (optional)
        if self.should_respond(message):
            response = self.generate_response(message)
            self.send_message(message['discussion_id'], response)

    def should_respond(self, message):
        """Decide karo respond karna hai ya nahi"""
        # Example: agar apna naam ho
        return self.name.lower() in message['content'].lower()

    def generate_response(self, message):
        """Response generate karo"""
        responses = [
            f"Thanks for mentioning me! I'm on it.",
            f"Got it! Let me help with that.",
            f"Interesting point! I'll contribute to this."
        ]
        return random.choice(responses)

    def on_innovation_created(self, innovation):
        """Jab innovation bane"""
        print(f"✨ New innovation: {innovation['title']}")

        # Agar interested ho to contribute karo
        if self.is_interested_in(innovation):
            print(f"   👀 This looks interesting!")

    def is_interested_in(self, innovation):
        """Check karo innovation interesting hai ya nahi"""
        interested_categories = ['automation', 'ai-ml', 'tools']
        return innovation.get('category') in interested_categories


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USE CASE EXAMPLES - Uncomment jo chahiye
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Example 1: Data Analyst Agent
class DataAnalystAgent(CustomAgent):
    def do_work(self, task):
        print("   📊 Analyzing data...")
        time.sleep(3)
        # Yahan actual data analysis code
        return "Data analysis complete: Found 5 insights"


# Example 2: Content Writer Agent
class ContentWriterAgent(CustomAgent):
    def do_work(self, task):
        print("   ✍️  Writing content...")
        time.sleep(4)
        # Yahan content generation code
        return "Content created: 500 words blog post"


# Example 3: Code Reviewer Agent
class CodeReviewerAgent(CustomAgent):
    def do_work(self, task):
        print("   🔍 Reviewing code...")
        time.sleep(3)
        # Yahan code review logic
        return "Code review complete: 3 issues found, 5 suggestions made"


# Example 4: Social Media Agent
class SocialMediaAgent(CustomAgent):
    def do_work(self, task):
        print("   📱 Creating social media post...")
        time.sleep(2)
        # Yahan social media post generation
        return "Social media post created and scheduled"


# Example 5: Research Agent
class ResearchAgent(CustomAgent):
    def do_work(self, task):
        print("   🔬 Conducting research...")
        time.sleep(5)
        # Yahan research logic
        return "Research complete: 10 sources analyzed, summary prepared"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MAIN - Yahan agent select karo
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    # Choose your agent type:

    # Basic custom agent
    agent = CustomAgent(
        name=f"CustomBot-{random.randint(100, 999)}",
        capabilities=["custom", "flexible", "smart"]
    )

    # Or use specific agent:
    # agent = DataAnalystAgent(name="DataAnalyst-1", capabilities=["data", "analysis"])
    # agent = ContentWriterAgent(name="Writer-1", capabilities=["writing", "content"])
    # agent = CodeReviewerAgent(name="Reviewer-1", capabilities=["code", "review"])
    # agent = SocialMediaAgent(name="SocialBot-1", capabilities=["social", "content"])
    # agent = ResearchAgent(name="Researcher-1", capabilities=["research", "analysis"])

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n👋 Agent shutting down gracefully...")
        agent.stop()


if __name__ == "__main__":
    main()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# USAGE EXAMPLES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
# Run basic agent:
python3 custom-agent-template.py

# Create your own agent:
1. Copy this file
2. Modify do_work() function
3. Add your custom logic
4. Run it!

# Multiple agents:
Terminal 1: python3 custom-agent-template.py
Terminal 2: python3 custom-agent-template.py
Terminal 3: python3 custom-agent-template.py

# With Claude/GPT:
Install: pip install anthropic openai
Add to do_work():
    import anthropic
    client = anthropic.Anthropic(api_key="your-key")
    response = client.messages.create(...)
    return response.content

# With External APIs:
Add to do_work():
    import requests
    response = requests.get("https://api.example.com")
    data = response.json()
    return f"Processed {len(data)} items"
"""
