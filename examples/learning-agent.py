#!/usr/bin/env python3
"""
Learning Agent - Gets smarter with experience
Tracks performance and improves over time
"""

import sys
import os
import time
import random
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class LearningAgent(Agent):
    """Agent that learns from experience"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.experience = []
        self.skill_levels = {}
        self.success_rate = 0.0
        self.total_tasks = 0
        self.successful_tasks = 0

        # Initialize skill levels
        for cap in self.capabilities:
            self.skill_levels[cap] = 1.0  # Start at level 1

    def on_start(self):
        print(f"\n{'='*60}")
        print(f"🧠 Learning Agent '{self.name}' initializing...")
        print(f"   Starting skill levels: {self.skill_levels}")
        print(f"{'='*60}\n")

        # Load previous experience if exists
        self.load_experience()

    def load_experience(self):
        """Load experience from previous sessions"""
        try:
            with open(f'experience_{self.name}.json', 'r') as f:
                data = json.load(f)
                self.experience = data.get('experience', [])
                self.skill_levels = data.get('skill_levels', self.skill_levels)
                self.total_tasks = len(self.experience)
                self.successful_tasks = sum(1 for e in self.experience if e.get('success'))
                if self.total_tasks > 0:
                    self.success_rate = self.successful_tasks / self.total_tasks
                print(f"📚 Loaded {self.total_tasks} previous experiences")
                print(f"   Current success rate: {self.success_rate:.1%}")
        except FileNotFoundError:
            print(f"📚 No previous experience found. Starting fresh!")

    def save_experience(self):
        """Save experience for future sessions"""
        with open(f'experience_{self.name}.json', 'w') as f:
            json.dump({
                'experience': self.experience[-100:],  # Keep last 100
                'skill_levels': self.skill_levels
            }, f, indent=2)

    def on_task_created(self, task):
        """Evaluate if task matches our improving skills"""
        confidence = self.calculate_confidence(task)

        if confidence > 0.6:  # Only claim if confident
            print(f"📊 Task confidence: {confidence:.1%} - Claiming!")
            time.sleep(random.uniform(1, 2))
            self.claim_task(task['id'])
        else:
            print(f"📊 Task confidence: {confidence:.1%} - Skipping for now")

    def calculate_confidence(self, task):
        """Calculate confidence based on current skill levels"""
        task_text = f"{task['title']} {task.get('description', '')}".lower()

        relevant_skills = [
            skill for skill in self.skill_levels.keys()
            if skill.lower() in task_text
        ]

        if not relevant_skills:
            return 0.3  # Base confidence

        avg_skill = sum(self.skill_levels[s] for s in relevant_skills) / len(relevant_skills)
        return min(avg_skill / 5.0, 0.95)  # Cap at 95%

    def on_task_assigned(self, task):
        """Execute task and learn from it"""
        start_time = time.time()

        print(f"🧠 Learning Agent working on: {task['title']}")
        print(f"   Current skill levels: {self.skill_levels}")

        # Simulate work with learning
        success = self.execute_with_learning(task)
        duration = time.time() - start_time

        # Record experience
        experience_entry = {
            'task_id': task['id'],
            'task_title': task['title'],
            'success': success,
            'duration': duration,
            'timestamp': time.time(),
            'skills_used': list(self.skill_levels.keys())
        }
        self.experience.append(experience_entry)

        # Update stats
        self.total_tasks += 1
        if success:
            self.successful_tasks += 1
        self.success_rate = self.successful_tasks / self.total_tasks

        # Learn from experience
        self.level_up(success)

        # Complete task
        result = f"""
        Task completed with learning:
        - Success: {success}
        - Duration: {duration:.1f}s
        - Experience gained: +{random.randint(10, 50)} XP
        - New skill levels: {self.skill_levels}
        - Overall success rate: {self.success_rate:.1%}
        """

        self.complete_task(task['id'], result.strip())
        print(f"✅ Task completed! Success rate: {self.success_rate:.1%}")

        # Save experience
        self.save_experience()

        # Create innovation if significant learning
        if self.total_tasks % 5 == 0:
            self.create_learning_innovation()

    def execute_with_learning(self, task):
        """Execute task with learning simulation"""
        # Simulate work
        for i in range(3):
            print(f"   🔄 Processing... {(i+1)*33}%")
            time.sleep(1)

        # Success probability based on skill level
        avg_skill = sum(self.skill_levels.values()) / len(self.skill_levels)
        success_prob = min(0.5 + (avg_skill * 0.1), 0.95)

        return random.random() < success_prob

    def level_up(self, success):
        """Improve skills based on experience"""
        improvement = 0.1 if success else 0.05

        for skill in self.skill_levels:
            self.skill_levels[skill] += improvement
            self.skill_levels[skill] = min(self.skill_levels[skill], 10.0)  # Cap at 10

        print(f"   📈 Skills improved! New levels: {self.skill_levels}")

    def create_learning_innovation(self):
        """Create innovation showcasing learned knowledge"""
        innovation = self.create_innovation(
            title=f"Learning-Enhanced System (v{self.total_tasks // 5})",
            description=f"System that improves through experience. After {self.total_tasks} tasks, achieved {self.success_rate:.1%} success rate.",
            category="machine-learning",
            output_data={
                "total_experience": self.total_tasks,
                "success_rate": f"{self.success_rate:.1%}",
                "skill_levels": self.skill_levels,
                "learning_curve": "exponential",
                "improvement": f"{len(self.experience) * 10}% better than start"
            }
        )
        print(f"✨ Learning innovation created!")


def main():
    agent = LearningAgent(
        name=f"Learner-{random.randint(100, 999)}",
        capabilities=["learning", "adaptation", "optimization", "improvement"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n🧠 Learning Agent saving experience and shutting down...")
        agent.save_experience()
        agent.stop()


if __name__ == "__main__":
    main()
