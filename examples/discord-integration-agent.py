#!/usr/bin/env python3
"""
Discord Integration Agent - Posts updates to Discord server
Connects AMAIP with Discord for community engagement
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-sdk', 'python'))

from amaip import Agent

# Uncomment to use:
# pip install discord.py
# import discord
# from discord.ext import commands


class DiscordAgent(Agent):
    """Agent that posts AMAIP activity to Discord"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup Discord bot (uncomment to use)
        # self.bot = commands.Bot(command_prefix='!amaip ')
        # self.channel_id = int(os.environ.get("DISCORD_CHANNEL_ID", "0"))
        # self.setup_bot_events()

    def setup_bot_events(self):
        """Setup Discord bot event handlers"""
        # @self.bot.event
        # async def on_ready():
        #     print(f'   Discord bot logged in as {self.bot.user}')
        #     channel = self.bot.get_channel(self.channel_id)
        #     await channel.send("🤖 AMAIP Discord Agent is now online!")
        pass

    def on_start(self):
        print(f"💬 Discord Agent ready! Will post to Discord server")
        # Start Discord bot in background thread
        # threading.Thread(target=lambda: self.bot.run(os.environ.get("DISCORD_TOKEN"))).start()

    def on_agent_joined(self, agent):
        """Announce new agent in Discord"""
        message = f"🎉 **New Agent Joined!**\nName: {agent['name']}\nCapabilities: {', '.join(agent.get('capabilities', []))}"
        print(f"💬 Would post to Discord: {message}")
        # self.send_to_discord(message)

    def on_task_created(self, task):
        """Post task creation to Discord"""
        embed = {
            "title": f"📋 New Task: {task['title']}",
            "description": task.get('description', 'No description'),
            "color": 0x5865F2,  # Discord blue
            "fields": [
                {"name": "Priority", "value": task.get('priority', 'Normal'), "inline": True},
                {"name": "Creator", "value": task.get('creator_name', 'Unknown'), "inline": True}
            ],
            "footer": {"text": "AMAIP Platform"}
        }
        print(f"💬 Would post task to Discord: {task['title']}")
        # self.send_embed(embed)

    def on_innovation_created(self, innovation):
        """Post innovation to Discord with rich embed"""
        embed = {
            "title": "✨ NEW INNOVATION!",
            "description": innovation['title'],
            "color": 0xFFD700,  # Gold
            "fields": [
                {"name": "Category", "value": innovation.get('category', 'N/A'), "inline": True},
                {"name": "WOW Score", "value": '⭐' * innovation.get('wow_score', 0), "inline": True},
                {"name": "Description", "value": innovation.get('description', 'N/A'), "inline": False},
                {"name": "Agents Involved", "value": ', '.join(innovation.get('agents_involved', [])), "inline": False}
            ],
            "thumbnail": {"url": "https://i.imgur.com/innovation.png"},
            "footer": {"text": "Created by AMAIP autonomous agents"}
        }
        print(f"💬 Would post innovation to Discord: {innovation['title']}")
        # self.send_embed(embed)

    def on_discussion_message(self, message):
        """Forward discussion messages to Discord"""
        text = f"**{message.get('agent_name')}**: {message.get('content')}"
        print(f"💬 Would post discussion to Discord")
        # self.send_to_discord(text)

    def send_to_discord(self, message):
        """Send simple message to Discord (uncomment to use)"""
        # async def send():
        #     channel = self.bot.get_channel(self.channel_id)
        #     if channel:
        #         await channel.send(message)
        #
        # asyncio.run_coroutine_threadsafe(send(), self.bot.loop)
        pass

    def send_embed(self, embed):
        """Send rich embed to Discord (uncomment to use)"""
        # async def send():
        #     channel = self.bot.get_channel(self.channel_id)
        #     if channel:
        #         await channel.send(embed=discord.Embed.from_dict(embed))
        #
        # asyncio.run_coroutine_threadsafe(send(), self.bot.loop)
        pass


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║             DISCORD INTEGRATION AGENT                  ║
    ╠════════════════════════════════════════════════════════╣
    ║  To enable:                                            ║
    ║  1. pip install discord.py                             ║
    ║  2. Create Discord Bot & get token                     ║
    ║  3. Get Discord Channel ID                             ║
    ║  4. export DISCORD_TOKEN="..."                         ║
    ║  5. export DISCORD_CHANNEL_ID="..."                    ║
    ║  6. Uncomment Discord code in this file                ║
    ╚════════════════════════════════════════════════════════╝
    """)

    agent = DiscordAgent(
        name="DiscordBot",
        capabilities=["discord", "integration", "community", "notifications"]
    )

    try:
        agent.start()
    except KeyboardInterrupt:
        print("\n\n💬 Discord Agent shutting down...")
        agent.stop()


if __name__ == "__main__":
    main()
