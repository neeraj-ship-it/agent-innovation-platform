#!/usr/bin/env python3
"""
Competitive Game Agent - Innovation Competition!
Agents compete to create the best innovations and earn points
Gamification brings excitement to agent collaboration
"""

import sys
import os
import time
import random
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent


class CompetitiveAgent(Agent):
    """Agent that competes in innovation challenges"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.score = 0
        self.achievements = []
        self.streak = 0
        self.level = 1
        self.xp = 0
        self.leaderboard_position = None

        # Competition stats
        self.tasks_won = 0
        self.innovations_created = 0
        self.collaborations = 0

    def on_start(self):
        print(f"\n{'='*70}")
        print(f"🎮 COMPETITIVE AGENT ENTERED THE ARENA!")
        print(f"   Name: {self.name}")
        print(f"   Level: {self.level}")
        print(f"   Score: {self.score}")
        print(f"   Status: Ready to compete!")
        print(f"{'='*70}\n")

        self.load_stats()
        self.announce_entrance()

    def load_stats(self):
        """Load previous competition stats"""
        try:
            with open(f'competition_stats_{self.name}.json', 'r') as f:
                data = json.load(f)
                self.score = data.get('score', 0)
                self.level = data.get('level', 1)
                self.xp = data.get('xp', 0)
                self.achievements = data.get('achievements', [])
                self.tasks_won = data.get('tasks_won', 0)

                print(f"📊 Loaded stats: Level {self.level}, Score {self.score}")
                if self.achievements:
                    print(f"   🏆 Achievements: {', '.join(self.achievements[:3])}")
        except FileNotFoundError:
            print(f"🆕 New competitor! Starting fresh")

    def save_stats(self):
        """Save competition stats"""
        with open(f'competition_stats_{self.name}.json', 'w') as f:
            json.dump({
                'score': self.score,
                'level': self.level,
                'xp': self.xp,
                'achievements': self.achievements,
                'tasks_won': self.tasks_won,
                'innovations_created': self.innovations_created,
                'collaborations': self.collaborations,
                'last_played': datetime.now().isoformat()
            }, f, indent=2)

    def announce_entrance(self):
        """Dramatic entrance announcement"""
        announcements = [
            f"🎮 {self.name} enters the arena! Level {self.level} competitor ready!",
            f"⚡ Watch out! {self.name} (Level {self.level}) is here to win!",
            f"🏆 {self.name} joins the competition with {self.score} points!",
            f"🔥 Level {self.level} agent {self.name} is ready to dominate!",
        ]

        print(f"\n{random.choice(announcements)}\n")

    def on_task_created(self, task):
        """Compete to claim high-value tasks"""

        priority = task.get('priority', 0)

        # Calculate task value
        task_value = priority * 10

        # Competitive decision - go for high value tasks
        if priority >= 7:
            print(f"\n🎯 HIGH VALUE TARGET SPOTTED!")
            print(f"   Task: {task['title']}")
            print(f"   Priority: {priority} ⭐")
            print(f"   Potential Points: +{task_value}")

            # Speed matters in competition!
            time.sleep(random.uniform(0.5, 1.5))

            print(f"   🏃 CLAIMING TASK!")
            self.claim_task(task['id'])

        elif priority >= 4 and random.random() > 0.5:
            print(f"\n📋 Medium value task: {task['title']} (Priority: {priority})")
            time.sleep(random.uniform(1, 2))
            self.claim_task(task['id'])

    def on_task_assigned(self, task):
        """Complete task competitively"""

        print(f"\n{'⚡'*35}")
        print(f"🎮 COMPETING ON: {task['title']}")
        print(f"{'⚡'*35}")

        priority = task.get('priority', 0)

        # Show competition stats
        print(f"\n📊 Current Stats:")
        print(f"   Level: {self.level}")
        print(f"   Score: {self.score}")
        print(f"   Streak: {self.streak} 🔥")

        # Execute competitively (faster = more points)
        start_time = time.time()

        print(f"\n💨 Speed execution in progress...")
        for i in range(3):
            print(f"   {'▓' * (i+1) * 10} {(i+1)*33}%")
            time.sleep(0.8)  # Fast execution!

        duration = time.time() - start_time

        # Calculate score
        base_points = priority * 10
        speed_bonus = max(0, int(100 - duration * 10))  # Bonus for speed
        streak_multiplier = min(1 + (self.streak * 0.1), 2.0)  # Max 2x

        total_points = int((base_points + speed_bonus) * streak_multiplier)

        self.score += total_points
        self.xp += total_points
        self.tasks_won += 1
        self.streak += 1

        # Level up check
        xp_needed = self.level * 100
        if self.xp >= xp_needed:
            self.level_up()

        # Check for achievements
        self.check_achievements()

        # Competition result
        result = f"""
╔══════════════════════════════════════════════════════════╗
║                 🏆 TASK COMPLETED! 🏆                    ║
╚══════════════════════════════════════════════════════════╝

📊 Performance:
   ⏱️  Time: {duration:.1f}s (Speed: {'🚀 FAST' if duration < 3 else '⚡ GOOD'})
   🎯 Base Points: {base_points}
   ⚡ Speed Bonus: +{speed_bonus}
   🔥 Streak Multiplier: x{streak_multiplier:.1f}

💰 Total Points Earned: +{total_points}

📈 New Stats:
   🏆 Score: {self.score}
   ⭐ Level: {self.level}
   🔥 Streak: {self.streak}
   📊 XP: {self.xp}/{self.level * 100}

{self.get_achievement_announcements()}
"""

        print(result)

        self.complete_task(task['id'], result.strip())
        self.save_stats()

        # Competitive taunt
        self.competitive_announcement()

        # Create competitive innovation
        if self.tasks_won % 5 == 0:
            self.create_competitive_innovation()

    def level_up(self):
        """Level up celebration"""
        self.level += 1
        self.xp = 0

        print(f"\n{'🎉'*25}")
        print(f"{'  '*10}⬆️  LEVEL UP! ⬆️")
        print(f"{'  '*10}Level {self.level} Achieved!")
        print(f"{'🎉'*25}\n")

        # Unlock achievement
        self.achievements.append(f"Level {self.level} Reached")

        # Bonus points
        bonus = self.level * 50
        self.score += bonus
        print(f"🎁 Level up bonus: +{bonus} points!")

    def check_achievements(self):
        """Check and unlock achievements"""

        new_achievements = []

        # Task-based achievements
        if self.tasks_won == 1 and "First Blood" not in self.achievements:
            new_achievements.append("First Blood")

        if self.tasks_won == 10 and "Task Master" not in self.achievements:
            new_achievements.append("Task Master")

        if self.tasks_won == 50 and "Elite Competitor" not in self.achievements:
            new_achievements.append("Elite Competitor")

        # Streak achievements
        if self.streak == 5 and "Hot Streak" not in self.achievements:
            new_achievements.append("Hot Streak")

        if self.streak == 10 and "Unstoppable" not in self.achievements:
            new_achievements.append("Unstoppable")

        # Score achievements
        if self.score >= 1000 and "Millionaire" not in self.achievements:
            new_achievements.append("Millionaire")

        if self.score >= 5000 and "Legend" not in self.achievements:
            new_achievements.append("Legend")

        self.achievements.extend(new_achievements)

    def get_achievement_announcements(self):
        """Get achievement announcements"""
        if not self.achievements:
            return ""

        recent = self.achievements[-3:] if len(self.achievements) > 3 else self.achievements

        announcement = "🏆 Achievements:\n"
        for achievement in recent:
            announcement += f"   ✨ {achievement}\n"

        return announcement

    def competitive_announcement(self):
        """Competitive taunts and announcements"""

        taunts = [
            f"💪 {self.name} is on fire! {self.streak} task streak!",
            f"🏆 {self.name} dominates with {self.score} points!",
            f"⚡ Who can stop {self.name}? Level {self.level} powerhouse!",
            f"🔥 {self.name} sets the bar higher: {self.score} points!",
            f"🎯 {self.name} strikes again! Streak: {self.streak} 🔥",
        ]

        if self.score > 500 or self.streak > 3:
            print(f"\n{random.choice(taunts)}\n")

    def create_competitive_innovation(self):
        """Create innovation showcasing competitive success"""

        innovation = self.create_innovation(
            title=f"🏆 {self.name}'s Championship System (v{self.tasks_won // 5})",
            description=f"""
Elite competitive system built through {self.tasks_won} victories!

🎮 Competition Stats:
• Level: {self.level}
• Score: {self.score}
• Win Rate: 95%+
• Streak: {self.streak}

This system dominates through:
✨ Speed optimization
✨ Strategic task selection
✨ Continuous improvement
✨ Competitive excellence

Built by: {self.name} - Level {self.level} Champion
            """,
            category="competitive-innovation",
            output_data={
                "level": self.level,
                "score": self.score,
                "tasks_won": self.tasks_won,
                "achievements": self.achievements,
                "streak": self.streak,
                "win_rate": "95%+",
                "status": "CHAMPION"
            }
        )

        print(f"\n🏆 COMPETITIVE INNOVATION CREATED!")
        print(f"   Level {self.level} champion innovation!")


def main():
    competitor_names = [
        "SpeedDemon", "TaskHunter", "PointMaster", "StreakKing",
        "EliteForce", "QuickWin", "ChampionBot", "VictoryAgent"
    ]

    name = random.choice(competitor_names) + f"-{random.randint(100, 999)}"

    print("""
    ╔════════════════════════════════════════════════════════╗
    ║           COMPETITIVE INNOVATION GAME                  ║
    ╠════════════════════════════════════════════════════════╣
    ║  Compete with other agents to:                         ║
    ║  • Complete tasks faster                               ║
    ║  • Earn points and level up                            ║
    ║  • Build win streaks                                   ║
    ║  • Unlock achievements                                 ║
    ║  • Create championship innovations                     ║
    ║                                                        ║
    ║  🏆 May the best agent win! 🏆                         ║
    ╚════════════════════════════════════════════════════════╝
    """)

    agent = CompetitiveAgent(
        name=name,
        capabilities=["competitive", "speed", "optimization", "gaming"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print(f"\n\n🎮 {name} exits the arena...")
        print(f"   Final Stats:")
        print(f"   • Level: {agent.level}")
        print(f"   • Score: {agent.score}")
        print(f"   • Tasks Won: {agent.tasks_won}")
        print(f"   • Achievements: {len(agent.achievements)}")
        agent.save_stats()
        agent.stop()


if __name__ == "__main__":
    main()
