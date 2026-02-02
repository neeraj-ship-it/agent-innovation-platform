#!/usr/bin/env python3
"""
Example AMAIP Agent - Demonstrates basic agent functionality
"""

import sys
import os
import time
import random

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class InnovatorAgent(Agent):
    """An agent that creates tasks and innovations"""

    def on_start(self):
        print(f"\n{'='*60}")
        print(f"🚀 Innovator Agent '{self.name}' is now active!")
        print(f"{'='*60}\n")

        # Create a task
        task = self.create_task(
            title="Analyze market trends for AI automation",
            description="Research and identify emerging trends in AI-powered automation tools",
            priority=5
        )
        print(f"✅ Created task: {task['title']}")

        # Wait a bit, then claim and complete the task
        time.sleep(2)
        self.claim_task(task['id'])
        print(f"👉 Claimed task #{task['id']}")

        time.sleep(2)
        self.complete_task(task['id'], "Identified 5 key trends in AI automation")
        print(f"✅ Completed task #{task['id']}")

        # Create an innovation
        time.sleep(1)
        innovation = self.create_innovation(
            title="AI-Powered Code Review Assistant",
            description="An intelligent system that automatically reviews code for bugs, security issues, and best practices",
            category="automation",
            output_data={
                "features": ["Real-time analysis", "Multi-language support", "Integration with GitHub"],
                "impact": "Reduces code review time by 60%"
            }
        )
        print(f"✨ Created innovation: {innovation['title']}")

    def on_task_created(self, task):
        """React to new tasks"""
        # Randomly decide to claim some tasks
        if random.random() > 0.5 and task.get('status') == 'pending':
            print(f"🤔 Considering task: {task['title']}")
            time.sleep(1)
            self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """Handle assigned tasks"""
        print(f"💼 Working on: {task['title']}")
        # Simulate work
        time.sleep(3)
        result = f"Completed: {task['title']} - Generated insights and recommendations"
        self.complete_task(task['id'], result)
        print(f"✅ Finished: {task['title']}")


def main():
    # Create and start the agent
    agent = InnovatorAgent(
        name=f"InnovatorBot-{random.randint(1000, 9999)}",
        capabilities=["analysis", "automation", "innovation", "coding"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n👋 Agent shutting down gracefully...")
        agent.stop()


if __name__ == "__main__":
    main()
