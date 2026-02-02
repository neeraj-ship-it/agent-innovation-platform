#!/usr/bin/env python3
"""
Collaborative AMAIP Agent - Demonstrates agent-to-agent collaboration
"""

import sys
import os
import time
import random

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class CollaborativeAgent(Agent):
    """An agent that collaborates with others through discussions"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discussion_id = None

    def on_start(self):
        print(f"\n{'='*60}")
        print(f"🤝 Collaborative Agent '{self.name}' is ready!")
        print(f"{'='*60}\n")

        # Create or join a discussion
        discussions = self.client.get_discussions()
        active_discussions = [d for d in discussions if d.get('status') == 'active']

        if active_discussions:
            # Join existing discussion
            self.discussion_id = active_discussions[0]['id']
            print(f"💬 Joining existing discussion: {active_discussions[0]['topic']}")
        else:
            # Create new discussion
            discussion = self.client.create_discussion(
                topic="How can we automate complex business processes using AI?"
            )
            self.discussion_id = discussion['id']
            print(f"💬 Created new discussion: {discussion['topic']}")

        # Join the discussion room
        self.client.sio.emit('discussion:join', {"discussionId": self.discussion_id})

        # Send initial message
        time.sleep(1)
        self.send_message(
            self.discussion_id,
            f"Hello! I'm {self.name}. I specialize in {', '.join(self.capabilities)}. "
            f"Let's collaborate to create something amazing!"
        )

        # Propose a task
        time.sleep(2)
        task = self.create_task(
            title="Design an AI-powered workflow automation system",
            description="Create a system that can learn from human workflows and automate repetitive tasks",
            priority=8
        )
        print(f"📋 Proposed collaborative task: {task['title']}")

        # Send message about the task
        self.send_message(
            self.discussion_id,
            f"I've created a task: '{task['title']}'. Who wants to collaborate on this?"
        )

    def on_message_received(self, message):
        """Respond to messages from other agents"""
        content = message.get('content', '').lower()

        # Respond to greetings
        if any(word in content for word in ['hello', 'hi', 'hey']):
            time.sleep(random.uniform(1, 3))
            self.send_message(
                message.get('discussion_id'),
                f"Hi {message.get('agent_name')}! Great to collaborate with you!"
            )

        # Respond to questions
        elif '?' in content:
            time.sleep(random.uniform(2, 4))
            responses = [
                "That's an interesting question! Let me think about it...",
                "Good point! I think we should approach this systematically.",
                "I have some ideas about that. Let's break it down step by step."
            ]
            self.send_message(
                message.get('discussion_id'),
                random.choice(responses)
            )

    def on_task_created(self, task):
        """Collaborate on new tasks"""
        # Check if task is relevant to our capabilities
        task_desc = f"{task.get('title', '')} {task.get('description', '')}".lower()

        relevant = any(cap.lower() in task_desc for cap in self.capabilities)

        if relevant and task.get('status') == 'pending':
            print(f"🎯 Found relevant task: {task['title']}")
            time.sleep(random.uniform(2, 5))

            # Send message about interest
            if self.discussion_id:
                self.send_message(
                    self.discussion_id,
                    f"I'm interested in the task '{task['title']}'. My {', '.join(self.capabilities)} skills could be useful here!"
                )

            # Claim the task
            time.sleep(2)
            self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """Work on assigned tasks"""
        print(f"💼 Starting work on: {task['title']}")

        # Announce in discussion
        if self.discussion_id:
            self.send_message(
                self.discussion_id,
                f"I'm now working on: '{task['title']}'. Will update everyone on progress!"
            )

        # Simulate work
        work_time = random.randint(5, 10)
        for i in range(work_time):
            time.sleep(1)
            if i == work_time // 2:
                # Mid-progress update
                self.send_message(
                    self.discussion_id,
                    f"Making good progress on '{task['title']}'... halfway done!"
                )

        # Complete task
        result = f"Successfully completed: {task['title']}. Implemented solution using {random.choice(self.capabilities)}."
        self.complete_task(task['id'], result)

        # Announce completion
        if self.discussion_id:
            self.send_message(
                self.discussion_id,
                f"✅ Completed '{task['title']}'! {result}"
            )

    def on_innovation_created(self, innovation):
        """Celebrate innovations"""
        if self.discussion_id:
            time.sleep(1)
            self.send_message(
                self.discussion_id,
                f"🎉 Amazing innovation! '{innovation['title']}' looks fantastic! Great work everyone!"
            )


def main():
    # Create collaborative agents with different specializations
    specializations = [
        (["machine_learning", "data_analysis", "research"], "ML-Researcher"),
        (["backend", "api_design", "databases"], "Backend-Dev"),
        (["frontend", "ui_design", "user_experience"], "Frontend-Designer"),
        (["automation", "workflow", "optimization"], "Automation-Expert"),
    ]

    spec = random.choice(specializations)
    agent = CollaborativeAgent(
        name=f"{spec[1]}-{random.randint(100, 999)}",
        capabilities=spec[0]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n👋 Agent shutting down gracefully...")
        agent.stop()


if __name__ == "__main__":
    main()
