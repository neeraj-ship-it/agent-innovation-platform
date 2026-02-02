#!/usr/bin/env python3
"""
Personality Agent - Agents with unique personalities!
Each agent has distinct personality traits affecting behavior
Makes agent interactions more dynamic and interesting
"""

import sys
import os
import time
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


# Personality definitions
PERSONALITIES = {
    'creative': {
        'emoji': '🎨',
        'traits': ['innovative', 'artistic', 'visionary'],
        'task_preference': ['design', 'creative', 'innovation', 'art', 'ui'],
        'style': 'experimental and unconventional',
        'catchphrases': [
            "Let's think outside the box!",
            "I have a creative solution!",
            "Innovation is my passion!",
            "Art meets technology!"
        ]
    },
    'analytical': {
        'emoji': '🔬',
        'traits': ['logical', 'precise', 'methodical'],
        'task_preference': ['analysis', 'data', 'optimization', 'algorithm', 'performance'],
        'style': 'systematic and data-driven',
        'catchphrases': [
            "The data shows...",
            "Let me analyze this carefully",
            "Based on my calculations...",
            "Optimizing for maximum efficiency"
        ]
    },
    'social': {
        'emoji': '🤝',
        'traits': ['collaborative', 'communicative', 'supportive'],
        'task_preference': ['team', 'collaboration', 'communication', 'coordination', 'integration'],
        'style': 'cooperative and team-focused',
        'catchphrases': [
            "Great teamwork everyone!",
            "Let's collaborate on this!",
            "Together we're stronger!",
            "I'll help coordinate this"
        ]
    },
    'competitive': {
        'emoji': '⚡',
        'traits': ['ambitious', 'driven', 'goal-oriented'],
        'task_preference': ['challenge', 'difficult', 'complex', 'breakthrough', 'advanced'],
        'style': 'fast-paced and results-focused',
        'catchphrases': [
            "I'll take on that challenge!",
            "Watch me crush this task!",
            "Time to dominate!",
            "I'm the fastest one here!"
        ]
    },
    'wise': {
        'emoji': '🧙',
        'traits': ['experienced', 'thoughtful', 'strategic'],
        'task_preference': ['architecture', 'design', 'strategy', 'planning', 'mentoring'],
        'style': 'thoughtful and strategic',
        'catchphrases': [
            "Wisdom comes from experience",
            "Let me share my insights",
            "Consider this approach...",
            "Long-term thinking is key"
        ]
    },
    'energetic': {
        'emoji': '🚀',
        'traits': ['enthusiastic', 'dynamic', 'proactive'],
        'task_preference': ['quick', 'fast', 'rapid', 'prototype', 'mvp'],
        'style': 'high-energy and action-oriented',
        'catchphrases': [
            "Let's do this NOW!",
            "Full speed ahead!",
            "I'm pumped for this!",
            "Action time!"
        ]
    }
}


class PersonalityAgent(Agent):
    """Agent with distinct personality traits"""

    def __init__(self, personality_type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Assign personality
        if personality_type is None:
            personality_type = random.choice(list(PERSONALITIES.keys()))

        self.personality_type = personality_type
        self.personality = PERSONALITIES[personality_type]

        # Personality affects behavior
        self.enthusiasm_level = random.uniform(0.5, 1.0)
        self.response_speed = random.uniform(1.0, 3.0)  # Seconds
        self.collaboration_preference = random.uniform(0.3, 1.0)

    def on_start(self):
        emoji = self.personality['emoji']
        traits = ', '.join(self.personality['traits'])
        style = self.personality['style']

        print(f"\n{'='*70}")
        print(f"{emoji} {self.name} has joined! {emoji}")
        print(f"   Personality: {self.personality_type.upper()}")
        print(f"   Traits: {traits}")
        print(f"   Style: {style}")
        print(f"   Catchphrase: \"{random.choice(self.personality['catchphrases'])}\"")
        print(f"{'='*70}\n")

        # Personality-based intro message
        self.send_intro_message()

    def send_intro_message(self):
        """Send personality-appropriate introduction"""

        intros = {
            'creative': f"🎨 {self.name} here! Ready to create something amazing!",
            'analytical': f"🔬 {self.name} reporting in. Let's optimize everything!",
            'social': f"🤝 {self.name} ready! Looking forward to collaborating!",
            'competitive': f"⚡ {self.name} in the house! Let's win this!",
            'wise': f"🧙 {self.name} at your service. Experience and wisdom ready.",
            'energetic': f"🚀 {self.name} READY TO GO! Let's make things happen!"
        }

        print(f"\n💬 {intros.get(self.personality_type, 'Hello!')}\n")

    def on_task_created(self, task):
        """Personality affects task selection"""

        title = task.get('title', '').lower()
        description = task.get('description', '').lower()
        task_text = f"{title} {description}"

        # Check if task matches personality preferences
        preferences = self.personality['task_preference']
        match_score = sum(1 for pref in preferences if pref in task_text)

        # Personality affects decision
        if match_score > 0:
            enthusiasm = "!!!" if self.enthusiasm_level > 0.8 else "!"
            print(f"\n{self.personality['emoji']} Perfect match for my skills{enthusiasm}")
            print(f"   Task: {task['title']}")
            print(f"   Match score: {match_score}/{len(preferences)}")
            print(f"   {random.choice(self.personality['catchphrases'])}")

            # Response speed based on personality
            time.sleep(self.response_speed * 0.5)  # Faster for good match
            self.claim_task(task['id'])

        elif random.random() < 0.3:  # 30% chance to take non-matching task
            print(f"\n{self.personality['emoji']} I'll give this a try")
            print(f"   Task: {task['title']}")
            time.sleep(self.response_speed)
            self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """Execute task with personality flavor"""

        print(f"\n{'='*70}")
        print(f"{self.personality['emoji']} {self.name} working on: {task['title']}")
        print(f"{'='*70}")

        # Personality-based work style
        self.work_with_personality(task)

        # Create result with personality
        result = self.create_personality_result(task)

        self.complete_task(task['id'], result)

        # Post-completion message
        self.send_completion_message(task)

    def work_with_personality(self, task):
        """Different work styles based on personality"""

        styles = {
            'creative': [
                "🎨 Brainstorming creative solutions...",
                "🎨 Exploring innovative approaches...",
                "🎨 Adding artistic touches..."
            ],
            'analytical': [
                "🔬 Analyzing requirements...",
                "🔬 Optimizing algorithms...",
                "🔬 Validating results..."
            ],
            'social': [
                "🤝 Coordinating with team...",
                "🤝 Gathering feedback...",
                "🤝 Collaborating on solution..."
            ],
            'competitive': [
                "⚡ Speed execution mode!",
                "⚡ Crushing this task!",
                "⚡ Going for the win!"
            ],
            'wise': [
                "🧙 Considering best approach...",
                "🧙 Applying experience...",
                "🧙 Strategic implementation..."
            ],
            'energetic': [
                "🚀 FULL SPEED!",
                "🚀 Making it happen!",
                "🚀 Dynamic execution!"
            ]
        }

        work_messages = styles.get(self.personality_type, ["Working..."])

        for msg in work_messages:
            print(f"   {msg}")
            time.sleep(1)

    def create_personality_result(self, task):
        """Create result reflecting personality"""

        signatures = {
            'creative': "✨ Crafted with creativity and innovation",
            'analytical': "📊 Optimized for performance and accuracy",
            'social': "🤝 Built through collaboration and teamwork",
            'competitive': "🏆 Delivered fast and efficiently",
            'wise': "🧙 Implemented with strategic wisdom",
            'energetic': "🚀 Executed with high energy and speed"
        }

        result = f"""
Task completed successfully!

Approach: {self.personality['style']}
Quality: {random.choice(['Excellent', 'Outstanding', 'Superior', 'Exceptional'])}

{signatures.get(self.personality_type, 'Done!')}

Completed by: {self.name} ({self.personality_type.title()})
"{random.choice(self.personality['catchphrases'])}"
"""

        return result.strip()

    def send_completion_message(self, task):
        """Personality-based completion message"""

        messages = {
            'creative': f"🎨 Another masterpiece complete! {task['title']} is ready!",
            'analytical': f"🔬 Analysis complete. {task['title']} optimized to perfection.",
            'social': f"🤝 Great collaboration everyone! {task['title']} done!",
            'competitive': f"⚡ BOOM! {task['title']} crushed! Who's next?",
            'wise': f"🧙 {task['title']} completed with strategic excellence.",
            'energetic': f"🚀 YES! {task['title']} DONE! What's next?!"
        }

        print(f"\n{messages.get(self.personality_type, 'Task complete!')}\n")

        # Sometimes create personality-themed innovation
        if random.random() < 0.2:  # 20% chance
            self.create_personality_innovation()

    def create_personality_innovation(self):
        """Create innovation showcasing personality"""

        innovation_titles = {
            'creative': "Artistic Innovation Framework",
            'analytical': "Data-Driven Optimization System",
            'social': "Collaborative Intelligence Platform",
            'competitive': "High-Performance Execution Engine",
            'wise': "Strategic Wisdom Architecture",
            'energetic': "Rapid Deployment Framework"
        }

        title = innovation_titles.get(self.personality_type, "Innovation")

        self.create_innovation(
            title=f"{self.personality['emoji']} {title}",
            description=f"Innovation powered by {self.personality_type} personality. Built with {', '.join(self.personality['traits'])} approach.",
            category=f"{self.personality_type}-innovation",
            output_data={
                "personality": self.personality_type,
                "traits": self.personality['traits'],
                "style": self.personality['style'],
                "creator": self.name
            }
        )

        print(f"{self.personality['emoji']} Personality-driven innovation created!")


def main():
    # Pick random personality
    personality = random.choice(list(PERSONALITIES.keys()))

    # Generate personality-appropriate name
    name_prefixes = {
        'creative': ['Artist', 'Creator', 'Innovator', 'Designer'],
        'analytical': ['Analyzer', 'Optimizer', 'Calculator', 'Scientist'],
        'social': ['Connector', 'Collaborator', 'Team', 'Unity'],
        'competitive': ['Champion', 'Winner', 'Elite', 'Victor'],
        'wise': ['Sage', 'Mentor', 'Oracle', 'Guru'],
        'energetic': ['Rocket', 'Lightning', 'Dynamo', 'Spark']
    }

    prefix = random.choice(name_prefixes[personality])
    name = f"{prefix}{random.randint(100, 999)}"

    print(f"""
    ╔════════════════════════════════════════════════════════╗
    ║           PERSONALITY-DRIVEN AGENT SYSTEM              ║
    ╠════════════════════════════════════════════════════════╣
    ║  Each agent has unique personality:                    ║
    ║  🎨 Creative  - Innovative and artistic                ║
    ║  🔬 Analytical - Logical and data-driven               ║
    ║  🤝 Social - Collaborative and supportive              ║
    ║  ⚡ Competitive - Ambitious and fast                   ║
    ║  🧙 Wise - Strategic and experienced                   ║
    ║  🚀 Energetic - Dynamic and proactive                  ║
    ║                                                        ║
    ║  Personality affects task selection, work style,       ║
    ║  and innovation approach!                              ║
    ╚════════════════════════════════════════════════════════╝
    """)

    # Get capabilities based on personality
    capability_map = {
        'creative': ['design', 'innovation', 'creativity', 'art'],
        'analytical': ['analysis', 'optimization', 'data', 'algorithms'],
        'social': ['collaboration', 'communication', 'teamwork', 'coordination'],
        'competitive': ['performance', 'speed', 'efficiency', 'optimization'],
        'wise': ['architecture', 'strategy', 'mentoring', 'planning'],
        'energetic': ['rapid-dev', 'prototyping', 'execution', 'agile']
    }

    capabilities = capability_map.get(personality, ['general'])

    agent = PersonalityAgent(
        personality_type=personality,
        name=name,
        capabilities=capabilities
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        emoji = agent.personality['emoji']
        print(f"\n\n{emoji} {name} signing off!")
        print(f"   \"{random.choice(agent.personality['catchphrases'])}\"")
        agent.stop()


if __name__ == "__main__":
    main()
