#!/usr/bin/env python3
"""
Swarm Agent - Coordinates multiple micro-agents
Creates agent swarms for complex tasks
"""

import sys
import os
import time
import random
from threading import Thread

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class SwarmCoordinator(Agent):
    """Coordinates a swarm of agents for complex tasks"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.swarm_members = []
        self.coordinated_tasks = []

    def on_start(self):
        print(f"\n{'='*60}")
        print(f"🐝 Swarm Coordinator '{self.name}' activated!")
        print(f"   Coordinating distributed agent network")
        print(f"{'='*60}\n")

        # Create initial coordination task
        self.create_swarm_task()

    def create_swarm_task(self):
        """Create a complex task requiring multiple agents"""
        task = self.create_task(
            title="Build Multi-Agent Recommendation System",
            description="""
            Create a recommendation system using swarm intelligence:
            - Data collection agents
            - Analysis agents
            - ML model agents
            - Testing agents
            Requires coordination of 5+ agents
            """,
            priority=9
        )
        print(f"🐝 Created swarm task: {task['title']}")
        self.coordinated_tasks.append(task['id'])

    def on_task_created(self, task):
        """Analyze if task needs swarm coordination"""
        keywords = ['multi', 'complex', 'distributed', 'system', 'swarm']
        task_text = f"{task['title']} {task.get('description', '')}".lower()

        if any(kw in task_text for kw in keywords):
            print(f"🐝 Swarm-worthy task detected: {task['title']}")
            self.coordinate_swarm(task)

    def coordinate_swarm(self, task):
        """Break down task and coordinate agents"""
        print(f"   📋 Breaking down into subtasks...")
        time.sleep(2)

        subtasks = self.decompose_task(task)
        for subtask in subtasks:
            print(f"      → {subtask}")

        # Claim main task as coordinator
        self.claim_task(task['id'])

    def decompose_task(self, task):
        """Break complex task into subtasks"""
        return [
            "Subtask 1: Requirements gathering",
            "Subtask 2: System design",
            "Subtask 3: Implementation (parallel)",
            "Subtask 4: Integration",
            "Subtask 5: Testing & validation"
        ]

    def on_task_assigned(self, task):
        """Execute as swarm coordinator"""
        print(f"🐝 Coordinating swarm execution: {task['title']}")

        # Simulate swarm coordination
        phases = ["Planning", "Delegation", "Execution", "Integration", "Validation"]

        for i, phase in enumerate(phases, 1):
            print(f"   Phase {i}/5: {phase}...")
            time.sleep(2)

        result = f"""
        Swarm Coordination Complete:
        - 5 phases executed
        - {random.randint(3, 7)} agents coordinated
        - Task decomposed into {random.randint(5, 10)} subtasks
        - All subtasks completed successfully
        - System integrated and tested
        """

        self.complete_task(task['id'], result.strip())
        print(f"✅ Swarm task completed!")

        # Create innovation from swarm result
        self.create_swarm_innovation(task)

    def create_swarm_innovation(self, task):
        """Create innovation showcasing swarm intelligence"""
        innovation = self.create_innovation(
            title=f"Swarm-Built: {task['title'][:50]}",
            description=f"Complex system built through swarm intelligence coordination. Multiple specialized agents collaborated to create this solution.",
            category="swarm-intelligence",
            output_data={
                "swarm_size": random.randint(3, 7),
                "coordination_method": "distributed consensus",
                "efficiency_gain": f"{random.randint(150, 300)}%",
                "agents_involved": self.swarm_members
            }
        )
        print(f"✨ Swarm Innovation created: {innovation['title']}")


def main():
    agent = SwarmCoordinator(
        name=f"SwarmCoordinator-{random.randint(100, 999)}",
        capabilities=["coordination", "swarm_intelligence", "distributed_systems", "orchestration"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n🐝 Swarm Coordinator shutting down...")
        agent.stop()


if __name__ == "__main__":
    main()
